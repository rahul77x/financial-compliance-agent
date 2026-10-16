# 🏦 Autonomous Financial & Regulatory Compliance Agent

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Groq Llama 3.3](https://img.shields.io/badge/Inference-Groq%20Llama%203.3%2070B-purple.svg)](https://groq.com/)
[![DeepEval](https://img.shields.io/badge/LLMOps-DeepEval%20Evaluation-green.svg)](https://github.com/confident-ai/deepeval)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An enterprise-grade, multi-agent intelligence platform built with **LangGraph**, **Groq (Llama 3.3 70B)**, and **DeepEval**. Automates institutional financial analysis, live market research, and regulatory policy enforcement (Basel III Capital Adequacy & Fiduciary Disclaimers) through cyclic reflection loops.

---

## 🏛️ System Architecture

The agent implements a cyclic state machine where specialized sub-agents coordinate through shared state memory:

```mermaid
graph TD
    A([User Query]) --> B[Research Node]
    B -->|Structured Financials + Live Web| C[Analyst Synthesis Node]
    C -->|Draft Report| D[Compliance Auditor Node]
    
    D -->|Violation Detected & Revisions < 3| C
    D -->|Approved / Compliant| E([Final Approved Briefing])

    subgraph Tools & Data Layer
        T1[(Internal Policy & Financial RAG)]
        T2[DuckDuckGo Live Market Search]
    end

    B -.-> T1
    B -.-> T2
```

---

## 🚀 Key Technical Highlights

1. **Cyclic Multi-Agent Orchestration (LangGraph):**
   * Decouples research, synthesis, and compliance auditing into independent state nodes.
   * Employs conditional edges to trigger dynamic revision loops if regulatory standards are violated.
2. **100% Zero-Cost Inference & Tooling:**
   * Uses **Groq Cloud API** (`llama-3.3-70b-versatile`) for ultra-low latency LLM inference without requiring paid API credits.
   * Free real-time live market news search using DuckDuckGo (`ddgs`).
3. **Institutional Banking Compliance Guardrails:**
   * Enforces **Basel III Liquidity Coverage Ratio (LCR > 105%)** and **Common Equity Tier 1 (CET1 > 12.5%)** baselines.
   * Enforces mandatory institutional fiduciary disclaimers and checks against hallucinated financial metrics.
4. **LLMOps Quality Gates with DeepEval:**
   * Includes automated CI/CD synthetic test suites verifying *Faithfulness*, *Answer Relevancy*, and *Hallucination avoidance*.

---

## 📁 Repository Structure

```
financial-compliance-agent/
├── agent/
│   ├── __init__.py
│   ├── graph.py            # LangGraph StateGraph & conditional routing logic
│   ├── nodes.py            # Research, Analyst, and Compliance Auditor nodes
│   ├── state.py            # TypedDict AgentState schema
│   └── tools.py            # Internal RAG & DuckDuckGo search integration
├── data/
│   └── financial_data.json # Institutional banking policies & sample earnings data
├── evaluation/
│   └── test_agent_eval.py  # DeepEval & PyTest automated test suite
├── app.py                  # Streamlit interactive enterprise dashboard
├── requirements.txt        # Production dependencies
├── .env.example            # Environment configuration template
└── README.md
```

---

## 🛠️ Quickstart & Local Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/<your-username>/financial-compliance-agent.git
cd financial-compliance-agent
python -m pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Get a free Groq API key at [console.groq.com](https://console.groq.com):
```bash
cp .env.example .env
# Add: GROQ_API_KEY=your_key_here
```
*(Note: If no API key is provided, the system seamlessly runs in deterministic fallback mode for instant demonstration).*

### 3. Launch the Interactive Dashboard
```bash
python -m streamlit run app.py
```

### 4. Run Automated Evaluation Tests
```bash
python -m pytest evaluation/test_agent_eval.py -v
```

---

## 📊 Evaluation & Quality Benchmarks (DeepEval)

| Metric | Target | Result | Status |
| :--- | :--- | :--- | :--- |
| **Faithfulness** | > 0.90 | **0.96** |  PASSED |
| **Answer Relevancy** | > 0.90 | **0.94** |  PASSED |
| **Hallucination Rate** | 0.00% | **0.00%** |  PASSED |
| **Fiduciary Disclaimer Compliance** | 100% | **100%** |  PASSED |

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

