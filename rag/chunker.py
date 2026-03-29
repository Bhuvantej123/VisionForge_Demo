"""
rag/chunker.py — Dev 1
Split raw text into overlapping chunks using LangChain.
"""

import os
from typing import List

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> List[str]:
    """
    Split a raw text string into overlapping chunks.

    Args:
        text: The raw text to split.
        chunk_size: Max chars per chunk. Defaults to CHUNK_SIZE from .env (500).
        chunk_overlap: Chars of overlap between chunks. Defaults to CHUNK_OVERLAP from .env (50).

    Returns:
        A list of text chunk strings.
    """
    chunk_size = chunk_size or int(os.getenv("CHUNK_SIZE", 500))
    chunk_overlap = chunk_overlap or int(os.getenv("CHUNK_OVERLAP", 50))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)
