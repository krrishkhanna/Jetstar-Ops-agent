from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    query: str
    messages: Annotated[List[dict], operator.add]
    tool_to_call: str
    tool_result: str
    final_answer: str
    iteration: int
