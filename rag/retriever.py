"""
rag/retriever.py — Dev 1
Given a query, embed it and return the top-k most relevant chunks from ChromaDB.

LOCKED INTERFACE — do not change function signature.
Dev 2 and Dev 3 depend on this exact signature.
"""

import os
from typing import List

from dotenv import load_dotenv

from rag.embedder import embed_query
from rag.vectorstore import get_collection

load_dotenv()


def retrieve(query: str, top_k: int | None = None) -> List[dict]:
    """
    Retrieve the top-k most relevant document chunks for a given query.

    Args:
        query: The user's natural-language question.
        top_k: Number of top results to return. Defaults to TOP_K from .env (5).

    Returns:
        List of dicts, each with:
            - "text"   (str)   : The chunk text.
            - "source" (str)   : The source filename (e.g. "medical_guide.pdf").
            - "score"  (float) : Cosine similarity score (0–1, higher = more relevant).

    Example:
        [
            {"text": "Ibuprofen is...", "source": "medical_guide.pdf", "score": 0.92},
            {"text": "Dosage is...",    "source": "medical_guide.pdf", "score": 0.87},
        ]
    """
    top_k = top_k or int(os.getenv("TOP_K", 5))

    # Embed the query using the same model as ingestion
    query_vector = embed_query(query)

    # Query ChromaDB
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # ChromaDB returns lists-of-lists (one per query embedding)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # ChromaDB cosine space returns distances (0 = identical).
    # Convert to a similarity score: score = 1 - distance
    chunks = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        chunks.append(
            {
                "text": doc,
                "source": meta.get("source", "unknown"),
                "score": float(round(1.0 - float(dist), 4)),
            }
        )

    return chunks
