"""
main.py — Dev 1
Entry point for document ingestion.
  Full pipeline: load → chunk → embed → store in ChromaDB.
  Run with: python main.py --file path/to/doc.pdf
            python main.py --all    (ingests everything in data/sample_docs/)
"""

import argparse
from pathlib import Path

from dotenv import load_dotenv

from rag.loader import load_document
from rag.chunker import chunk_text
from rag.embedder import embed_chunks
from rag.vectorstore import store_embeddings

load_dotenv()

SAMPLE_DOCS_DIR = Path(__file__).parent / "data" / "sample_docs"
SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


def ingest_document(file_path: str, source_name: str | None = None) -> None:
    """
    Full ingestion pipeline for a single file: load → chunk → embed → store.

    Args:
        file_path: Path to the PDF or text file to ingest.
        source_name: Label to attach to all chunks (defaults to the filename).
    """
    path = Path(file_path)
    source_name = source_name or path.name

    print(f"[ingest] Loading '{source_name}'...")
    text = load_document(str(path))
    print(f"[ingest] Extracted {len(text):,} characters.")

    print("[ingest] Chunking...")
    chunks = chunk_text(text)
    print(f"[ingest] Created {len(chunks)} chunks.")

    print("[ingest] Embedding...")
    embeddings = embed_chunks(chunks)
    print(f"[ingest] Got {len(embeddings)} embeddings.")

    print("[ingest] Storing in ChromaDB...")
    sources = [source_name] * len(chunks)
    store_embeddings(chunks, embeddings, sources)
    print(f"[ingest] [OK] '{source_name}' ingested successfully.\n")



def _ingest_all() -> None:
    """Ingest every supported file found in data/sample_docs/."""
    files = [
        f for f in SAMPLE_DOCS_DIR.iterdir()
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    if not files:
        print(f"[main] No supported files found in {SAMPLE_DOCS_DIR}")
        return
    for f in files:
        ingest_document(str(f))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="RAG Demo — document ingestion tool"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        metavar="PATH",
        help="Path to a single PDF or .txt file to ingest.",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help=f"Ingest all supported files in {SAMPLE_DOCS_DIR}.",
    )

    args = parser.parse_args()

    if args.all:
        _ingest_all()
    else:
        ingest_document(args.file)
