
from typing import TypedDict


class AgentState(TypedDict):
    messages: list
    research_results: list
    final_answer: str