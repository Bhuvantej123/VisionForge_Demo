"""
rag/vectorstore.py — Dev 1
Store and retrieve embedding vectors using ChromaDB (persistent local client).
"""

import os
from pathlib import Path
from typing import List

import chromadb
from chromadb import Collection
from dotenv import load_dotenv

load_dotenv()

# Resolve chroma_db relative to the project root (parent of this file's parent)
# This ensures the path is correct regardless of the working directory.
_CHROMA_PATH = str(Path(__file__).parent.parent / "chroma_db")


def _get_client() -> chromadb.PersistentClient:
    """Return a persistent ChromaDB client stored at <project_root>/chroma_db."""
    return chromadb.PersistentClient(path=_CHROMA_PATH)


def store_embeddings(
    chunks: List[str],
    embeddings: List[List[float]],
    sources: List[str],
    collection_name: str | None = None,
) -> None:
    """
    Persist text chunks and their embeddings into ChromaDB.

    Args:
        chunks: List of text strings (the original chunk content).
        embeddings: List of embedding vectors — one per chunk.
        sources: List of source filenames — one per chunk (e.g. "guide.pdf").
        collection_name: ChromaDB collection name. Defaults to COLLECTION_NAME from .env.

    Returns:
        None
    """
    collection_name = collection_name or os.getenv("COLLECTION_NAME", "rag_demo")
    client = _get_client()
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    # Build unique IDs: source + chunk index (handles re-ingestion of same file cleanly)
    ids = [f"{sources[i]}::chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": sources[i]} for i in range(len(sources))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"[vectorstore] Stored {len(chunks)} chunks in collection '{collection_name}'.")


def get_collection(collection_name: str | None = None) -> Collection:
    """
    Retrieve an existing ChromaDB collection.

    Args:
        collection_name: Name of the ChromaDB collection. Defaults to COLLECTION_NAME from .env.

    Returns:
        A ChromaDB Collection object.

    Raises:
        Exception: If the collection does not exist.
    """
    collection_name = collection_name or os.getenv("COLLECTION_NAME", "rag_demo")
    client = _get_client()
    return client.get_collection(name=collection_name)
