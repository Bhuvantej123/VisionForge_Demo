"""
rag/embedder.py — Dev 1
Convert text chunks into embedding vectors using Google Gemini API.
Model: models/gemini-embedding-001
Free tier limit: 100 requests/minute — this module throttles automatically.
"""

import os
import re
import time
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_EMBED_MODEL = "models/gemini-embedding-001"
_DELAY_SECONDS = 0.65       # 0.65s per call ≈ 92 req/min (free tier max: 100)
_MAX_RETRIES = 3


def _configure():
    """Configure the Gemini client (idempotent)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. "
            "Create a .env file with GEMINI_API_KEY=your_key (copy from .env.example)."
        )
    genai.configure(api_key=api_key)


def _embed_one(text: str, task_type: str = "retrieval_document") -> List[float]:
    """
    Embed a single string with retry logic for rate-limit errors.

    Args:
        text: The text to embed.
        task_type: Gemini task type hint.
                   Use "retrieval_document" for ingested chunks,
                   "retrieval_query" for user queries.
    """
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            result = genai.embed_content(
                model=_EMBED_MODEL,
                content=text,
                task_type=task_type,
            )
            return result["embedding"]
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower() or "rate" in err.lower():
                retry_after = 60  # default: wait 60s
                try:
                    match = re.search(r"seconds:\s*(\d+)", err)
                    if match:
                        retry_after = int(match.group(1)) + 2
                except Exception:
                    pass
                if attempt < _MAX_RETRIES:
                    print(f"[embed] Rate limit hit. Waiting {retry_after}s before retry {attempt}/{_MAX_RETRIES}...")
                    time.sleep(retry_after)
                else:
                    raise
            else:
                raise


def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Generate embedding vectors for a list of text chunks.
    Throttled to ~92 requests/minute to respect the Gemini free-tier limit.

    Args:
        chunks: List of text strings to embed.

    Returns:
        List of embedding vectors (same order as input).
    """
    if not chunks:
        return []

    _configure()
    embeddings = []
    total = len(chunks)
    estimated_mins = round((total * _DELAY_SECONDS) / 60, 1)
    print(f"[embed] Embedding {total} chunks (~{estimated_mins} min at free-tier rate)...")

    for i, chunk in enumerate(chunks, start=1):
        embeddings.append(_embed_one(chunk, task_type="retrieval_document"))
        time.sleep(_DELAY_SECONDS)   # throttle to stay under 100 req/min
        if i % 20 == 0 or i == total:
            print(f"[embed] {i}/{total} chunks embedded...")

    return embeddings


def embed_query(query: str) -> List[float]:
    """
    Embed a single query string.

    Args:
        query: The user's question.

    Returns:
        A single embedding vector.
    """
    _configure()
    return _embed_one(query, task_type="retrieval_query")
