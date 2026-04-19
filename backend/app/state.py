from typing import Annotated, TypedDict
import operator

class AgentState(TypedDict):
    drug_name: str
    # Each agent will append their findings to this list
    research_notes: Annotated[list, operator.add]
    # score range 0-100
    impact_score: int