from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import agent_node, tool_node, final_answer_node

def should_continue(state: AgentState) -> str:
    if state.get("iteration", 0) >= 5:
        return "end"
    if state.get("tool_result"):
        return "final"
    if state.get("tool_to_call"):
        return "tool"
    return "agent"

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tool", tool_node)
    graph.add_node("final", final_answer_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tool": "tool", "final": "final", "agent": "agent", "end": END})
    graph.add_edge("tool", "agent")
    graph.add_edge("final", END)
    return graph.compile()
