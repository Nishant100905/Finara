"""
LLM-based intent router for the Enterprise RAG + Financial Coach.

Possible intents:
- RAG
- FINANCIAL
- HYBRID

IMPORTANT: this router **defaults to RAG** for any ambiguous or
document-related query. The reason is that misclassifying a
document-grounded question (e.g., "What are the Total Liabilities of
Apex Retail Solutions Pvt. Ltd. FY2024?") as FINANCIAL causes the
graph to skip the entire retrieval pipeline and answer from general
model knowledge — which is the exact bug this fix targets.
"""

from __future__ import annotations

import json
import logging
import re
from enum import Enum

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.graph.state import GraphState
from app.llm import llm

logger = logging.getLogger(__name__)


from app.core.constants import Intent


# ==========================================================
# Heuristic signals — RAG by default
# ==========================================================

# These phrases almost always mean "look at the uploaded document."
_RAG_KEYWORDS = (
    "pdf",
    "document",
    "documents",
    "uploaded",
    "upload",
    "this file",
    "this report",
    "according to",
    "as per",
    "based on the",
    "in the",
    "from the",
    "page",
    "annual report",
    "balance sheet",
    "income statement",
    "cash flow statement",
    "statement of",
    "notes to",
    "schedule",
    "appendix",
    "exhibit",
    "section",
    "chapter",
    "clause",
    "paragraph",
    "row",
    "column",
    "table",
    "figure",
    "chart",
    "disclosure",
    "audit",
    "auditor",
    "financial statements",
    "total assets",
    "total liabilities",
    "total equity",
    "shareholders",
    "shareholder",
    "revenue",
    "expenses",
    "net profit",
    "net loss",
    "ebitda",
    "gross margin",
    "operating margin",
    "pat",
    "pbt",
    "eps",
    "dividend",
    "shares",
    "fy2024",
    "fy2023",
    "fy2022",
    "fy2021",
    "fy2020",
    "q1",
    "q2",
    "q3",
    "q4",
    "year ended",
    "year-end",
    "as on",
    "as at",
)

# Strong financial-action verbs that warrant the FINANCIAL branch.
_FINANCIAL_ACTION_KEYWORDS = (
    "buy ",
    "sell ",
    "invest in ",
    "calculate emi",
    "compute emi",
    "monthly sip",
    "start a sip",
    "i should invest",
    "should i invest",
    "recommend a stock",
    "recommend a fund",
    "create a portfolio",
    "build a portfolio",
    "rebalance",
    "what is the price of",
    "current price",
    "stock price",
    "share price",
    "market cap",
    "convert ",
)

# Common suffixes for company / legal-entity names. The presence of any
# of these in the query is a strong RAG signal.
_COMPANY_SUFFIX_RE = re.compile(
    r"\b(pvt\.?\s*ltd\.?|private\s+limited|limited|ltd\.?|inc\.?|incorporated|"
    r"corp\.?|corporation|llc|l\.l\.c\.?|plc|gmbh|s\.a\.|s\.p\.a\.|"
    r"co\.?\s*ltd\.?|holdings|group|enterprises|industries)\b",
    re.IGNORECASE,
)

# Currency / monetary markers.
_CURRENCY_RE = re.compile(
    r"(₹|\$|€|£|rs\.?|inr|usd|eur|gbp|crore|cr\.?|lakh|lac)\b",
    re.IGNORECASE,
)


def _looks_like_document_query(query: str) -> bool:
    """Return True if the query has any strong RAG signal."""
    q = query.lower()
    if any(kw in q for kw in _RAG_KEYWORDS):
        return True
    if _COMPANY_SUFFIX_RE.search(query):
        return True
    if _CURRENCY_RE.search(query):
        return True
    # A year range like "FY2024" or "2023-24" is a very strong RAG signal.
    if re.search(r"\b(?:fy|f\.y\.?)?\s*20\d{2}(?:\s*[-–]\s*\d{2,4})?\b", q):
        return True
    return False


def _looks_like_financial_action(query: str) -> bool:
    """Return True only when the user is clearly asking for a financial action."""
    q = query.lower()
    return any(kw in q for kw in _FINANCIAL_ACTION_KEYWORDS)


# ==========================================================
# LLM-based classification (used only as a fallback)
# ==========================================================

class IntentResult(BaseModel):
    intent: Intent = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str = Field(...)


SYSTEM_PROMPT = """
You are an intent classification model.

Classify the user's request into exactly one category.

RAG
Use when the question is about:
- Uploaded PDFs
- Documents
- Reports
- Enterprise knowledge
- Technical documentation
- Research papers
- Company documents
- Financial figures appearing in an uploaded document

FINANCIAL
Use ONLY when the user is asking for a real-time financial action
or computation that requires external tools, e.g.:
- "buy 100 shares of Apple"
- "calculate EMI for a 20L loan at 9% for 5 years"
- "what is the current price of Reliance"
- "rebalance my portfolio to 60/40"

HYBRID
Use when BOTH are required AND no uploaded document is involved.

IMPORTANT:
If the user is asking about specific numbers, company names, fiscal
years, balance-sheet items, audit figures, or any content that could
plausibly be in an uploaded document, classify as RAG — even if the
words sound financial.

Examples:

Question:
Analyze this annual report and tell me if I should invest.
Intent:
RAG

Question:
What is CRAG?
Intent:
RAG

Question:
What are the Total Liabilities of Apex Retail Solutions Pvt. Ltd. FY2024?
Intent:
RAG

Question:
Calculate EMI for a 20L loan at 9% for 5 years.
Intent:
FINANCIAL

Question:
Compare Apple and Microsoft stock.
Intent:
FINANCIAL

Return ONLY valid JSON.

Example:

{
    "intent":"RAG",
    "confidence":0.95,
    "reason":"The question is about figures in an uploaded document."
}
"""


def classify_intent(query: str) -> IntentResult:
    """
    Classify a user query into RAG, FINANCIAL or HYBRID.

    Order of operations:
    1. If the query has any strong document/company/currency/year signal → RAG.
    2. If the query has a clear financial-action signal → FINANCIAL.
    3. Otherwise, ask the LLM — but **default to RAG** on parse failure
       or low confidence.
    """

    # -------------------------------------------------
    # 1. Heuristic: strong RAG signals
    # -------------------------------------------------

    if _looks_like_document_query(query):
        logger.info(
            "[intent] Heuristic RAG match for query: %s",
            query,
        )
        return IntentResult(
            intent=Intent.RAG,
            confidence=0.95,
            reason="Query contains document / company / currency / year signal.",
        )

    # -------------------------------------------------
    # 2. Heuristic: clear financial action
    # -------------------------------------------------

    if _looks_like_financial_action(query):
        logger.info(
            "[intent] Heuristic FINANCIAL match for query: %s",
            query,
        )
        return IntentResult(
            intent=Intent.FINANCIAL,
            confidence=0.90,
            reason="Query contains a clear financial-action verb.",
        )

    # -------------------------------------------------
    # 3. LLM fallback — default to RAG on any error
    # -------------------------------------------------

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content

        if isinstance(content, list):
            content = "".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )

        content = str(content).strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(content)
        result = IntentResult(**data)

        # If the LLM says FINANCIAL but confidence is low, fall back to RAG.
        if (
            result.intent == Intent.FINANCIAL
            and result.confidence < 0.85
        ):
            logger.info(
                "[intent] Downgrading low-confidence FINANCIAL (%.2f) to RAG.",
                result.confidence,
            )
            return IntentResult(
                intent=Intent.RAG,
                confidence=result.confidence,
                reason="Low-confidence FINANCIAL fallback to RAG.",
            )

        logger.info(
            "[intent] LLM classified=%s confidence=%.2f reason=%s",
            result.intent.value,
            result.confidence,
            result.reason,
        )

        return result

    except Exception:
        logger.exception("Intent parsing failed; defaulting to RAG.")

        return IntentResult(
            intent=Intent.RAG,
            confidence=0.0,
            reason="Fallback classification (default to RAG).",
        )


def intent_router(state: GraphState):
    """
    LangGraph node.
    """

    document_ids = state.get("document_ids")
    if document_ids:
        logger.info("[intent] document_ids provided (%s), enforcing RAG intent", document_ids)
        result = IntentResult(
            intent=Intent.RAG,
            confidence=1.0,
            reason="Explicit document_ids provided by caller.",
        )
    else:
        result = classify_intent(state["query"])

    state["metadata"] = state.get("metadata") or {}
    state["metadata"]["intent"] = result.intent.value
    state["metadata"]["intent_confidence"] = result.confidence
    state["metadata"]["intent_reason"] = result.reason

    logger.info(
        "[intent] classified=%s confidence=%.2f",
        result.intent.value,
        result.confidence,
    )

    return state


def route_intent(state: GraphState) -> str:
    """
    Decide which branch of the graph should execute.

    The RAG branch is always preferred unless the intent is
    unambiguously FINANCIAL.
    """

    metadata = state.get("metadata") or {}
    intent = metadata.get("intent", "RAG")

    if intent == Intent.FINANCIAL.value:
        return "financial"

    # HYBRID also goes through the RAG pipeline first — if the
    # retrieved context answers the question, we never need the
    # financial tools. The graph builder short-circuits to END after
    # the RAG pipeline so we never end up at the hybrid_agent unless
    # the orchestrator explicitly routes there.
    return "rag"
