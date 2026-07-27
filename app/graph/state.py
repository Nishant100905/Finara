"""
LangGraph State Definition

This file defines the shared state passed between all nodes
in the Enterprise RAG pipeline.

The state is designed to support the deterministic RAG-first
routing pipeline:

    User Question
        ↓
    Embed
        ↓
    Retrieve
        ↓
    Rerank
        ↓
    Relevance Check ─── above threshold ──► Answer from RAG (END)
        │                                       (uses document context only)
        │ below threshold
        ↓
    Tavily Search
        ↓
    Web Relevance Check ── useful results ──► Answer from Web (END)
        │                                     (with source URLs)
        │ no useful results
        ↓
    Answer from LLM (END)
        (general model knowledge)

The state is a TypedDict (total=False) so every key is optional —
nodes only set what they produce.
"""

from typing import Annotated, Any

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class GraphState(TypedDict, total=False):
    """
    Shared LangGraph state.
    """

    # =====================================================
    # User Information
    # =====================================================

    user_id: str
    thread_id: str

    # =====================================================
    # Document Selection (scopes retrieval)
    # =====================================================

    # Optional list of document_ids the user wants to query against.
    # When empty/None, retrieval uses only the user_id filter.
    document_ids: list[str]

    # =====================================================
    # User Query
    # =====================================================

    query: str
    sanitized_query: str

    # =====================================================
    # Conversation History
    # =====================================================

    messages: Annotated[list[Any], add_messages]

    # =====================================================
    # HyDE (preserved for backward compatibility; not used in
    # the deterministic RAG-first pipeline to avoid an extra
    # LLM call before the retriever has anything to score).
    # =====================================================

    hypothetical_documents: list[str]

    # =====================================================
    # Embeddings
    # =====================================================

    query_embedding: list[float]

    # =====================================================
    # Retrieval
    # =====================================================

    dense_results: list[dict]
    sparse_results: list[dict]
    merged_results: list[dict]
    reranked_results: list[dict]

    # =====================================================
    # Relevance Check
    # =====================================================

    # The single most relevant chunk's score after reranking.
    # Used to decide RAG vs. web search.
    best_relevance_score: float

    # RAG → True if local chunks were good enough to answer.
    # Tavily → True if the web search was used.
    rag_decision: str          # "FOUND" | "NOT_FOUND"
    tavily_decision: str       # "FOUND" | "NOT_FOUND"
    final_routing: str         # "RAG" | "TAVILY" | "LLM"

    # Backward-compatible flags consumed by older nodes.
    use_web_search: bool
    rag_used: bool
    tavily_invoked: bool

    # =====================================================
    # Tavily
    # =====================================================

    web_results: list[dict]

    # =====================================================
    # Spotlight Context
    # =====================================================

    context: str
    context_preview: str

    # =====================================================
    # LLM Output
    # =====================================================

    answer: str
    sources: list[Any]

    # =====================================================
    # Self-RAG (preserved; no longer used in the deterministic
    # pipeline but kept so the key exists in state.)
    # =====================================================

    reflection_score: float
    retry_count: int

    # =====================================================
    # Cache
    # =====================================================

    embedding_cache_hit: bool
    answer_cache_hit: bool

    # =====================================================
    # Metadata
    # =====================================================

    metadata: dict[str, Any]

    # =====================================================
    # Errors
    # =====================================================

    error: str | None

    # =====================================================
    # Financial Agent (preserved for the financial branch)
    # =====================================================

    selected_tool: str
    tool_input: dict[str, Any]
    tool_output: Any

    # =====================================================
    # Financial Profile
    # =====================================================

    monthly_income: float
    monthly_expenses: float
    monthly_savings: float

    risk_profile: str
    investment_horizon: str

    financial_goal: str

    portfolio: dict[str, float]

    watchlist: list[str]

    preferred_currency: str

    # =====================================================
    # Market Data
    # =====================================================

    stock_symbol: str
    stock_data: dict[str, Any]
    portfolio_analysis: dict[str, Any]

    # =====================================================
    # Orchestration
    # =====================================================

    execution_plan: list[str]
    current_agent: str
    completed_agents: list[str]
