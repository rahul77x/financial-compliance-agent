import json
import os
import warnings
from typing import List, Dict, Any

warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "financial_data.json")

def load_data() -> Dict[str, Any]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"banking_policies": [], "mock_earnings_reports": []}

def search_banking_policies(query: str) -> List[Dict[str, Any]]:
    """
    Search institutional regulatory compliance policies (e.g. AML, Basel III LCR, Fiduciary rules).
    """
    data = load_data()
    policies = data.get("banking_policies", [])
    query_lower = query.lower()
    
    matched = []
    for pol in policies:
        combined_text = (pol["title"] + " " + pol["category"] + " " + " ".join(pol["rules"])).lower()
        # Simple dense/keyword matching
        if any(term in combined_text for term in query_lower.split()):
            matched.append(pol)
            
    return matched if matched else policies[:1]

def get_company_financials(ticker: str) -> Dict[str, Any]:
    """
    Retrieve structured financial earnings data for a specific banking ticker (e.g., AIBG, BOI).
    """
    data = load_data()
    reports = data.get("mock_earnings_reports", [])
    ticker_clean = ticker.strip().upper()
    
    for report in reports:
        if report["ticker"] == ticker_clean or ticker_clean in report["company_name"].upper():
            return report
            
    # Default fallback if ticker not in mock dataset
    return {
        "ticker": ticker_clean,
        "status": "not_found",
        "message": f"Ticker {ticker_clean} not in local database. Web search should be utilized."
    }

def search_live_market_news(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Execute real-time live market and regulatory news search using DuckDuckGo (Free, zero-cost).
    """
    results = []
    try:
        with DDGS() as ddgs:
            ddg_results = list(ddgs.text(query, max_results=max_results))
            for r in ddg_results:
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })
    except Exception as e:
        results.append({
            "title": "Search Service Notice",
            "snippet": f"Web search encountered a fallback: {str(e)}",
            "url": ""
        })
    return results
