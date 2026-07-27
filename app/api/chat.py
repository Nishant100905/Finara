"""
Chat API Router
Enterprise RAG System
"""

import asyncio
import json
import logging
import re
from typing import AsyncIterator, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, protected_route
from app.cache.answer_cache import cache_answer, get_cached_answer
from app.graph.builder import rag_graph
from app.security.input_security import secure_input
from app.security.output_security import validate_output

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    thread_id: Optional[str] = None
    document_ids: Optional[list[str]] = None
    selected_document: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    source: str
    cache_hit: bool = False
    thread_id: Optional[str] = None
    final_routing: Optional[str] = None       # "RAG" | "TAVILY" | "LLM"
    rag_decision: Optional[str] = None        # "FOUND" | "NOT_FOUND"
    tavily_decision: Optional[str] = None     # "FOUND" | "NOT_FOUND"
    tavily_invoked: Optional[bool] = None
    rag_used: Optional[bool] = None
    sources: Optional[list] = None


# ==========================================================
# Chat Endpoint
# ==========================================================

@router.post("", response_model=ChatResponse, summary="Enterprise RAG Chat")
async def chat(
    request: ChatRequest,
    user=Depends(protected_route),
    db: Session = Depends(get_db),
):
    """
    Enterprise RAG Chat Endpoint.

    Every request is routed through the deterministic RAG-first
    graph in ``app.graph.builder``. The graph logs the full
    decision pipeline (embedding, retrieval, rerank, relevance
    check, Tavily, final routing) so the operator can verify
    that uploaded documents are always consulted first.
    """
    try:
        # --------------------------------------------------
        # Input Security
        # --------------------------------------------------
        security_result = secure_input(request.message)
        sanitized_query = security_result["sanitized"]

        # --------------------------------------------------
        # Answer Cache
        # --------------------------------------------------
        try:
            cached = get_cached_answer(sanitized_query)
        except Exception as e:
            logger.warning("Answer cache lookup raised, falling back to LLM: %s", e)
            cached = None

        if cached:
            logger.info("Answer Cache HIT")
            return ChatResponse(
                answer=cached,
                source="answer_cache",
                cache_hit=True,
                thread_id=request.thread_id,
                final_routing="CACHE",
            )

        logger.info("Answer Cache MISS")

        # --------------------------------------------------
        # LangGraph Input
        # --------------------------------------------------
        thread_id = request.thread_id or f"user_{user['id']}"

        doc_ids = list(request.document_ids or [])
        if request.selected_document and request.selected_document not in doc_ids:
            doc_ids.append(request.selected_document)

        graph_input = {
            "query": sanitized_query,
            "sanitized_query": sanitized_query,
            "user_id": user["id"],
            "thread_id": thread_id,
            "document_ids": doc_ids,
        }

        config = {"configurable": {"thread_id": thread_id}}

        logger.info("=" * 80)
        logger.info("Invoking LangGraph (RAG-first deterministic pipeline)")
        logger.info("Thread ID  : %s", thread_id)
        logger.info("User ID    : %s", user["id"])
        logger.info("Doc IDs    : %s", doc_ids)
        logger.info("=" * 80)

        # --------------------------------------------------
        # Execute Graph
        # --------------------------------------------------
        try:
            result = await rag_graph.ainvoke(graph_input, config=config)
        except Exception:
            logger.exception("LangGraph execution failed!")
            raise

        logger.info("LangGraph completed successfully for user %s", user.get("id", "unknown"))

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LangGraph returned no response.",
            )

        answer = (
            result.get("answer")
            or result.get("response")
            or result.get("final_answer")
        )
        if answer is None:
            logger.error("Graph returned no answer field. Keys: %s",
                         list(result.keys()) if result else None)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Answer generation failed.",
            )

        # --------------------------------------------------
        # Normalize Output
        # --------------------------------------------------
        if isinstance(answer, list):
            parts = []
            for block in answer:
                if isinstance(block, dict):
                    parts.append(block.get("text", ""))
                else:
                    parts.append(str(block))
            answer = "\n".join(parts)
        elif not isinstance(answer, str):
            answer = str(answer)
        answer = answer.strip()
        if not answer:
            answer = "I'm sorry, I couldn't generate an answer based on the provided information."

        # --------------------------------------------------
        # Final routing summary (also visible in the UI via
        # the ChatResponse fields).
        # --------------------------------------------------
        metadata = result.get("metadata") or {}
        final_routing = (
            result.get("final_routing")
            or metadata.get("final_routing")
            or "LLM"
        )
        rag_decision = result.get("rag_decision") or metadata.get("rag_decision") or "NOT_FOUND"
        tavily_decision = result.get("tavily_decision") or metadata.get("tavily_decision")
        tavily_invoked = bool(result.get("tavily_invoked") or metadata.get("tavily_invoked"))
        rag_used = bool(result.get("rag_used") or metadata.get("rag_used"))
        sources = result.get("sources") or []

        reranked_chunks = len(result.get("reranked_results") or result.get("dense_results") or [])
        sim_scores = metadata.get("similarity_scores") or []
        tavily_count = len(result.get("web_results") or [])

        final_route_label = "PDF" if final_routing == "RAG" else ("Tavily" if final_routing == "TAVILY" else "LLM")

        logger.info("=" * 80)
        logger.info("========== RAG ROUTING DEBUG SUMMARY ==========")
        logger.info("User Query       : %s", request.message)
        logger.info("Retrieved Chunks : %d", reranked_chunks)
        logger.info("Similarity Scores: %s", sim_scores)
        logger.info("RAG Decision     : %s", rag_decision)
        logger.info("Invoking Tavily  : %s", "YES" if tavily_invoked else "NO")
        logger.info("Tavily Results   : %d", tavily_count)
        logger.info("Final Route      : %s", final_route_label)
        logger.info("===============================================")
        logger.info("=" * 80)

        # --------------------------------------------------
        # Output Security
        # --------------------------------------------------
        validated_answer = validate_output(answer)

        # --------------------------------------------------
        # Cache Answer
        # --------------------------------------------------
        try:
            cache_answer(sanitized_query, validated_answer)
            logger.info("Answer cached successfully.")
        except Exception as e:
            logger.warning("Answer cache write failed: %s", e)

        return ChatResponse(
            answer=validated_answer,
            source="rag_pipeline",
            cache_hit=False,
            thread_id=thread_id,
            final_routing=final_routing,
            rag_decision=rag_decision,
            tavily_decision=tavily_decision,
            tavily_invoked=tavily_invoked,
            rag_used=rag_used,
            sources=sources,
        )

    except HTTPException:
        raise
    except Exception:
        logger.exception("Chat endpoint failed.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


# ==========================================================
# Streaming Chat Endpoint (SSE) — preserved format
# ==========================================================

_STREAM_CHUNK_PATTERN = r"(\s+)"


def _sse_format(payload: str) -> str:
    return f"data: {payload}\n\n"


def _split_stream_tokens(text: str) -> list[str]:
    return re.split(_STREAM_CHUNK_PATTERN, text)


async def _run_graph(
    request: ChatRequest,
    user: dict,
) -> tuple[str, dict]:
    """
    Run the RAG-first graph and return (validated_answer, metadata).
    """
    security_result = secure_input(request.message)
    sanitized_query = security_result["sanitized"]

    try:
        cached = get_cached_answer(sanitized_query)
    except Exception as e:
        logger.warning("Answer cache lookup raised (stream): %s", e)
        cached = None

    if cached:
        logger.info("Answer Cache HIT (stream)")
        return cached, {"cache_hit": True, "final_routing": "CACHE"}

    logger.info("Answer Cache MISS (stream)")

    thread_id = request.thread_id or f"user_{user['id']}"
    doc_ids = list(request.document_ids or [])
    if request.selected_document and request.selected_document not in doc_ids:
        doc_ids.append(request.selected_document)

    graph_input = {
        "query": sanitized_query,
        "sanitized_query": sanitized_query,
        "user_id": user["id"],
        "thread_id": thread_id,
        "document_ids": doc_ids,
    }
    config = {"configurable": {"thread_id": thread_id}}

    logger.info("=" * 80)
    logger.info("Invoking LangGraph (stream)")
    logger.info("Thread ID: %s", thread_id)
    logger.info("=" * 80)

    result = await rag_graph.ainvoke(graph_input, config=config)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LangGraph returned no response.",
        )

    answer = (
        result.get("answer")
        or result.get("response")
        or result.get("final_answer")
    )
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Answer generation failed.",
        )

    if isinstance(answer, list):
        parts = []
        for block in answer:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            else:
                parts.append(str(block))
        answer = "\n".join(parts)
    elif not isinstance(answer, str):
        answer = str(answer)
    answer = answer.strip()
    if not answer:
        answer = "I'm sorry, I couldn't generate an answer based on the provided information."

    metadata = result.get("metadata") or {}
    final_routing = (
        result.get("final_routing")
        or metadata.get("final_routing")
        or "LLM"
    )

    rag_decision = result.get("rag_decision") or metadata.get("rag_decision") or "NOT_FOUND"
    tavily_invoked = bool(result.get("tavily_invoked") or metadata.get("tavily_invoked"))
    reranked_chunks = len(result.get("reranked_results") or result.get("dense_results") or [])
    sim_scores = metadata.get("similarity_scores") or []
    tavily_count = len(result.get("web_results") or [])
    final_route_label = "PDF" if final_routing == "RAG" else ("Tavily" if final_routing == "TAVILY" else "LLM")

    logger.info("=" * 80)
    logger.info("========== RAG ROUTING DEBUG SUMMARY (STREAM) ==========")
    logger.info("User Query       : %s", request.message)
    logger.info("Retrieved Chunks : %d", reranked_chunks)
    logger.info("Similarity Scores: %s", sim_scores)
    logger.info("RAG Decision     : %s", rag_decision)
    logger.info("Invoking Tavily  : %s", "YES" if tavily_invoked else "NO")
    logger.info("Tavily Results   : %d", tavily_count)
    logger.info("Final Route      : %s", final_route_label)
    logger.info("========================================================")
    logger.info("=" * 80)

    log_meta = {
        "cache_hit": False,
        "final_routing": final_routing,
        "rag_decision": rag_decision,
        "tavily_decision": result.get("tavily_decision") or metadata.get("tavily_decision"),
        "tavily_invoked": tavily_invoked,
        "rag_used": bool(result.get("rag_used") or metadata.get("rag_used")),
        "sources": result.get("sources") or [],
    }

    validated_answer = validate_output(answer)

    try:
        cache_answer(sanitized_query, validated_answer)
    except Exception as e:
        logger.warning("Answer cache write failed (stream): %s", e)

    return validated_answer, log_meta


async def _stream_chat_events(
    request: ChatRequest,
    user: dict,
) -> AsyncIterator[str]:
    try:
        answer, meta = await _run_graph(request, user)

        # Metadata event — frontend's api.ts already understands this.
        yield _sse_format(
            json.dumps(
                {
                    "source": "answer_cache" if meta.get("cache_hit") else "rag_pipeline",
                    "cache_hit": meta.get("cache_hit", False),
                    "final_routing": meta.get("final_routing"),
                    "rag_decision": meta.get("rag_decision"),
                    "tavily_decision": meta.get("tavily_decision"),
                    "tavily_invoked": meta.get("tavily_invoked"),
                    "rag_used": meta.get("rag_used"),
                }
            )
        )

        for token in _split_stream_tokens(answer):
            if not token:
                continue
            yield _sse_format(json.dumps(token))
            await asyncio.sleep(0)

        yield _sse_format("[DONE]")

    except HTTPException as exc:
        logger.exception("Streaming chat failed (HTTPException).")
        yield _sse_format(json.dumps({"error": exc.detail}))
        yield _sse_format("[DONE]")

    except Exception as exc:
        logger.exception("Streaming chat failed.")
        yield _sse_format(json.dumps({"error": str(exc) or "Internal server error."}))
        yield _sse_format("[DONE]")


@router.post("/stream", summary="Enterprise RAG Chat (SSE stream)")
@router.post("/chat/stream", include_in_schema=False)
async def chat_stream(
    request: ChatRequest,
    user=Depends(protected_route),
    db: Session = Depends(get_db),
):
    return StreamingResponse(
        _stream_chat_events(request, user),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
