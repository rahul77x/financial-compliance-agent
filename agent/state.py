from typing import Annotated, Dict, Any, List, Optional
from typing_extensions import TypedDict
import operator

class AgentState(TypedDict):
    """
    State definition for the Autonomous Financial & Compliance Intelligence Agent.
    Maintains memory across cyclic graph nodes and human-in-the-loop review.
    """
    user_query: str
    extracted_data: Dict[str, Any]
    web_research: List[str]
    draft_report: str
    compliance_status: str  # "APPROVED" | "CHANGES_REQUESTED" | "PENDING"
    compliance_feedback: List[str]
    revision_count: int
    human_approved: Optional[bool]
    messages: Annotated[List[Dict[str, str]], operator.add]

