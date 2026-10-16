from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import research_node, analyst_node, compliance_auditor_node

def should_continue(state: AgentState) -> str:
    """
    Conditional edge logic:
    - If Compliance Auditor approved the report -> terminate at END.
    - If Auditor requested changes AND revision_count < 3 -> loop back to analyst_node.
    - If maximum safety revisions reached -> terminate at END with warning.
    """
    status = state.get("compliance_status", "PENDING")
    revisions = state.get("revision_count", 0)
    
    if status == "APPROVED":
        return END
    
    if revisions >= 3:
        # Loop safety guard
        return END
        
    return "analyst_node"

def build_financial_agent_graph():
    """
    Constructs and compiles the cyclic LangGraph multi-agent workflow.
    """
    workflow = StateGraph(AgentState)
    
    # 1. Add Nodes
    workflow.add_node("research_node", research_node)
    workflow.add_node("analyst_node", analyst_node)
    workflow.add_node("compliance_auditor_node", compliance_auditor_node)
    
    # 2. Add Linear & Conditional Edges
    workflow.add_edge(START, "research_node")
    workflow.add_edge("research_node", "analyst_node")
    workflow.add_edge("analyst_node", "compliance_auditor_node")
    
    workflow.add_conditional_edges(
        "compliance_auditor_node",
        should_continue,
        {
            "analyst_node": "analyst_node",
            END: END
        }
    )
    
    # 3. Compile Graph
    app = workflow.compile()
    return app

# Singleton compiled app
agent_app = build_financial_agent_graph()

