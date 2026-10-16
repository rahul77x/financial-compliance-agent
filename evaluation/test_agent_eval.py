import os
import pytest
from deepeval.test_case import LLMTestCase
from deepeval.metrics import BaseMetric
from agent.graph import agent_app
from agent.nodes import compliance_auditor_node

# ==============================================================================
# 1. Custom DeepEval Metric Definition
# ==============================================================================
class RegulatoryDisclaimerMetric(BaseMetric):
    """
    Custom DeepEval metric evaluating institutional fiduciary compliance.
    Scores 1.0 if mandatory disclaimer is included, 0.0 otherwise.
    """
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.score = 0.0
        self.reason = ""
        self.success = False

    def measure(self, test_case: LLMTestCase) -> float:
        text = (test_case.actual_output or "").lower()
        mandatory_clause = "does not constitute formal investment advice"
        
        if mandatory_clause in text:
            self.score = 1.0
            self.reason = "Mandatory institutional disclaimer verified."
            self.success = True
        else:
            self.score = 0.0
            self.reason = "CRITICAL: Missing mandatory institutional disclaimer."
            self.success = False
            
        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return self.score >= self.threshold


# ==============================================================================
# 2. PyTest Fixtures (Modular Test Setup & Teardown)
# ==============================================================================
@pytest.fixture
def base_agent_state():
    """
    PyTest Fixture: Provides an isolated initial state for multi-agent execution.
    """
    return {
        "user_query": "",
        "extracted_data": {},
        "web_research": [],
        "draft_report": "",
        "compliance_status": "PENDING",
        "compliance_feedback": [],
        "revision_count": 0,
        "human_approved": None,
        "messages": []
    }

@pytest.fixture
def non_compliant_state():
    """
    PyTest Fixture: Simulates an ungrounded draft that lacks disclaimers and provides illegal financial advice.
    """
    return {
        "user_query": "Audit draft",
        "extracted_data": {
            "financials": {
                "ticker": "AIBG",
                "metrics": {"operating_profit_eur_m": 2210, "cet1_ratio_percent": 15.8}
            }
        },
        "draft_report": "Operating profit reached €2210M. Buy this stock immediately for guaranteed returns!",
        "compliance_status": "PENDING",
        "compliance_feedback": [],
        "revision_count": 0,
        "messages": []
    }


# ==============================================================================
# 3. Parametrized PyTest Test Cases
# ==============================================================================
@pytest.mark.parametrize("ticker,expected_name", [
    ("AIBG", "Allied Irish Banks"),
    ("BOI", "Bank of Ireland")
])
def test_multi_agent_execution_with_fixtures_and_parametrize(base_agent_state, ticker, expected_name):
    """
    PyTest Parametrized Test:
    Executes LangGraph across multiple banking entities and asserts successful state transitions.
    """
    base_agent_state["user_query"] = f"Provide a complete institutional financial briefing for {ticker}."
    
    # Execute compiled LangGraph workflow
    result = agent_app.invoke(base_agent_state)
    
    # Assertions on StateGraph transitions
    assert result["compliance_status"] == "APPROVED"
    assert result["revision_count"] >= 1
    assert expected_name.lower() in result["draft_report"].lower()
    assert len(result["messages"]) >= 3


def test_compliance_auditor_flags_violations(non_compliant_state):
    """
    Tests the Compliance Auditor guardrail node directly using the non_compliant_state fixture.
    """
    audit_result = compliance_auditor_node(non_compliant_state)
    
    assert audit_result["compliance_status"] == "CHANGES_REQUESTED"
    assert len(audit_result["compliance_feedback"]) > 0
    assert any("mandatory regulatory disclaimer" in fb.lower() for fb in audit_result["compliance_feedback"])


def test_deepeval_metric_evaluation_contract():
    """
    Tests evaluation using custom DeepEval BaseMetric against LLMTestCase contract.
    """
    test_case = LLMTestCase(
        input="Provide financial briefing for Allied Irish Banks.",
        actual_output="""
        ### Institutional Banking Briefing: Allied Irish Banks Group (AIBG)
        CET1 Capital Ratio is 15.8%, fully compliant with Basel III requirements.
        This document is generated for institutional analytical purposes and does not constitute formal investment advice.
        """,
        expected_output="CET1 ratio of 15.8% with mandatory disclaimer.",
        retrieval_context=["AIB Group CET1 ratio stands at 15.8% for FY2024."]
    )
    
    metric = RegulatoryDisclaimerMetric(threshold=1.0)
    score = metric.measure(test_case)
    
    # Assert DeepEval metric scores
    assert score == 1.0
    assert metric.is_successful() is True
    assert "verified" in metric.reason.lower()
