"""
LangGraph Builder

Constructs the Enterprise RAG workflow as a **deterministic**
RAG-first pipeline, exactly as specified:

    embed → retrieve → rerank → relevance_check
                                          │
                          ┌───────────────┴───────────────┐
                          │                               │
                  above threshold                   below threshold
                          │                               │
                  answer_from_rag (END)              tavily → spotlight
                                                              │
                                                       web_relevance_check
                                                              │
                                            ┌─────────────────┴────────────────┐
                                            │                                  │
                                      useful results                    no useful results
                                            │                                  │
                                    answer_from_web (END)              answer_from_llm (END)

The FINANCIAL branch is compiled into a separate graph
(``financial_graph``) and is invoked from the chat API only
when the user explicitly requests a financial action. RAG is
the default for every other query.

The graph is deterministic — every routing decision is based
on a numeric threshold or a structural check. No LLM is asked
to make a routing decision.
"""

from __future__ import annotations

import logging

from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from app.database.checkpoint import checkpointer
from app.graph.state import GraphState
from app.graph.rag_router import (
    entry_router,
    post_rag_router,
    relevance_router,
    web_relevance_router,
)

# Pipeline nodes
from app.graph.nodes.embed import embed_node
from app.graph.nodes.retrieve import retrieve_node
from app.graph.nodes.rrf import rrf_node
from app.graph.nodes.rerank import rerank_node
from app.graph.nodes.relevance_check import relevance_check_node
from app.graph.nodes.answer_from_rag import answer_from_rag_node
from app.graph.nodes.answer_from_web import answer_from_web_node
from app.graph.nodes.answer_from_llm import answer_from_llm_node
from app.graph.nodes.tavily import tavily_node
from app.graph.nodes.web_relevance import web_relevance_check_node
from app.graph.nodes.spotlight import spotlight_node

# Financial branch (preserved)
from app.graph.financial_agent import financial_agent, should_continue
from app.graph.tools import FINANCIAL_TOOLS

logger = logging.getLogger(__name__)


# ==========================================================
# RAG-first pipeline
# ==========================================================

rag_builder = StateGraph(GraphState)

rag_builder.add_node("embed", embed_node)
rag_builder.add_node("retrieve", retrieve_node)
rag_builder.add_node("rrf", rrf_node)
rag_builder.add_node("rerank", rerank_node)
rag_builder.add_node("spotlight", spotlight_node)
rag_builder.add_node("relevance_check", relevance_check_node)
rag_builder.add_node("answer_from_rag", answer_from_rag_node)
rag_builder.add_node("tavily", tavily_node)
rag_builder.add_node("spotlight_web", spotlight_node)
rag_builder.add_node("web_relevance_check", web_relevance_check_node)
rag_builder.add_node("answer_from_web", answer_from_web_node)
rag_builder.add_node("answer_from_llm", answer_from_llm_node)

# Entry → embed (deterministic)
rag_builder.set_entry_point("embed")

# Linear pipeline up to the relevance check
rag_builder.add_edge("embed", "retrieve")
rag_builder.add_edge("retrieve", "rrf")
rag_builder.add_edge("rrf", "rerank")
rag_builder.add_edge("rerank", "spotlight")
rag_builder.add_edge("spotlight", "relevance_check")

# After relevance check: RAG or Tavily
rag_builder.add_conditional_edges(
    "relevance_check",
    relevance_router,
    {
        "rag": "answer_from_rag",
        "tavily": "tavily",
    },
)

# After RAG answer: END if answered, Tavily if insufficient/refused
rag_builder.add_conditional_edges(
    "answer_from_rag",
    post_rag_router,
    {
        "end": END,
        "tavily": "tavily",
    },
)

# Tavily path: search → spotlight → web_relevance → answer or LLM
rag_builder.add_edge("tavily", "spotlight_web")
rag_builder.add_edge("spotlight_web", "web_relevance_check")

rag_builder.add_conditional_edges(
    "web_relevance_check",
    web_relevance_router,
    {
        "web": "answer_from_web",
        "llm": "answer_from_llm",
    },
)

rag_builder.add_edge("answer_from_web", END)
rag_builder.add_edge("answer_from_llm", END)

rag_graph = rag_builder.compile(checkpointer=checkpointer)
logger.info("RAG-first deterministic graph compiled.")


# ==========================================================
# Financial branch (preserved for the financial action route)
# ==========================================================

financial_builder = StateGraph(GraphState)
tool_node = ToolNode(FINANCIAL_TOOLS)

financial_builder.add_node("financial_agent", financial_agent)
financial_builder.add_node("financial_tools", tool_node)

financial_builder.set_entry_point("financial_agent")

financial_builder.add_conditional_edges(
    "financial_agent",
    should_continue,
    {
        "tools": "financial_tools",
        "end": END,
    },
)
financial_builder.add_edge("financial_tools", "financial_agent")

financial_graph = financial_builder.compile(checkpointer=checkpointer)
logger.info("Financial agent graph compiled.")


# ==========================================================
# Public factory
# ==========================================================

def build_graph():
    """
    Backward-compatible factory. Returns the RAG-first graph
    (which is what the chat API uses by default).
    """
    return rag_graph
