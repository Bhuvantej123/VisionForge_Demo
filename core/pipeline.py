"""
core/pipeline.py — Dev 1
Orchestrate: retrieve → build prompt → call Gemini LLM → return cited answer.

LOCKED INTERFACE — do not change get_answer() signature.
Dev 2 depends on this function as a black box.
"""

import os
import time
from pathlib import Path
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv

from rag.retriever import retrieve
from utils.logger import log_query

load_dotenv()

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "prompt_template.txt"
_LLM_MODEL = "gemini-2.5-flash"
_model: genai.GenerativeModel | None = None


def _get_model() -> genai.GenerativeModel:
    """Lazy-init shared Gemini GenerativeModel."""
    global _model
    if _model is None:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        _model = genai.GenerativeModel(_LLM_MODEL)
    return _model


# ─── Public Interface ────────────────────────────────────────────────────────

def get_answer(query: str) -> dict:
    """
    Given a user query, retrieve relevant chunks and generate a cited answer.

    Args:
        query: The user's natural-language question.

    Returns:
        {
            "answer":  str        — LLM-generated answer with source citations,
            "sources": list[dict] — chunks used: [{"text", "source", "score"}, ...],
            "query":   str        — the original query echoed back,
        }
    """
    start = time.monotonic()

    top_k = int(os.getenv("TOP_K", 5))
    chunks = retrieve(query, top_k=top_k)

    prompt = _build_prompt(query, chunks)
    answer = _call_llm(prompt)

    elapsed_ms = int((time.monotonic() - start) * 1000)
    print(f"[pipeline] get_answer completed in {elapsed_ms}ms")

    # Log every query/answer pair (Dev 3's logger)
    try:
        log_query(query=query, answer=answer, sources=chunks, response_time_ms=elapsed_ms)
    except Exception as log_err:
        print(f"[pipeline] Warning: logging failed — {log_err}")

    return {
        "answer": answer,
        "sources": chunks,
        "query": query,
    }


# ─── Internal Helpers ─────────────────────────────────────────────────────────

def _build_prompt(query: str, chunks: List[dict]) -> str:
    """
    Load the prompt template and fill in {context} and {query}.

    Context is a numbered list of chunk texts with their source filenames.
    """
    template = _PROMPT_PATH.read_text(encoding="utf-8")

    context_lines = []
    for i, chunk in enumerate(chunks, start=1):
        context_lines.append(
            f"[{i}] (source: {chunk['source']})\n{chunk['text']}"
        )
    context = "\n\n".join(context_lines)

    return template.format(context=context, query=query)


def _call_llm(prompt: str) -> str:
    """
    Send a prompt to Gemini 1.5 Flash and return the response text.
    """
    model = _get_model()
    response = model.generate_content(prompt)
    return response.text.strip()
