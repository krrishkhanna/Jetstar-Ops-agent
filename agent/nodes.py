import re
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .state import AgentState
from .tools import tools, get_flight_status, get_rebooking_options, get_passenger_credits

SYSTEM_PROMPT = """You are a Jetstar Airways assistant.
Use tools to answer flight status, rebooking, and travel credit queries.
Never guess — always retrieve accurate information from tools."""

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

def agent_node(state: AgentState) -> dict:
    """The brain — reads the query, decides which tool to call."""
    llm = get_llm()
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=state["query"])]
    if state.get("tool_result"):
        messages.append(AIMessage(content=f"Tool returned: {state['tool_result']}"))
    response = llm.invoke(messages)
    tool_to_call = ""
    if response.tool_calls:
        tool_to_call = response.tool_calls[0]["name"]
    return {
        "messages": [{"role": "assistant", "content": str(response.content)}],
        "tool_to_call": tool_to_call,
        "iteration": state.get("iteration", 0) + 1,
    }

def tool_node(state: AgentState) -> dict:
    """The hands — executes the tool the agent chose."""
    tool_name = state["tool_to_call"]
    query = state["query"]
    result = "Could not execute tool."
    if tool_name == "get_flight_status":
        match = re.search(r'JQ\d{3,4}', query.upper().replace(" ", ""))
        flight = match.group() if match else "JQ101"
        result = get_flight_status.invoke({"flight_number": flight})
    elif tool_name == "get_rebooking_options":
        match = re.search(r'JQ\d{3,4}', query.upper().replace(" ", ""))
        flight = match.group() if match else "JQ303"
        result = get_rebooking_options.invoke({"flight_number": flight})
    elif tool_name == "get_passenger_credits":
        match = re.search(r'JS\d{3}', query.upper())
        pid = match.group() if match else "JS001"
        result = get_passenger_credits.invoke({"passenger_id": pid})
    return {"tool_result": result, "messages": [{"role": "tool", "content": result}]}

def final_answer_node(state: AgentState) -> dict:
    """The voice — formats tool result into a clean passenger response."""
    plain_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content="You are a friendly Jetstar customer service assistant. Format the retrieved information into a clear, helpful, concise response for the passenger."),
        HumanMessage(content=f"Passenger asked: {state['query']}\nInformation retrieved: {state['tool_result']}\n\nWrite a helpful response."),
    ]
    response = plain_llm.invoke(messages)
    return {"final_answer": response.content, "messages": [{"role": "assistant", "content": response.content}]}
