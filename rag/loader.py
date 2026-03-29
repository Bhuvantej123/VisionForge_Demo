"""
rag/loader.py — Dev 1
Load PDF or plain-text files and return raw extracted text.
"""

import fitz  # PyMuPDF
from pathlib import Path


def load_document(file_path: str) -> str:
    """
    Load a PDF or plain-text file and return its full text content.

    Args:
        file_path: Path to a .pdf or .txt file.

    Returns:
        A single string with all text from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not .pdf or .txt.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _load_pdf(path)
    elif suffix == ".txt":
        return _load_txt(path)
    else:
        raise ValueError(
            f"Unsupported file type: '{suffix}'. Only .pdf and .txt are supported."
        )


def _load_pdf(path: Path) -> str:
    """Extract text from every page of a PDF using PyMuPDF."""
    doc = fitz.open(str(path))
    pages_text = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            pages_text.append(text)
    doc.close()
    return "\n".join(pages_text)


def _load_txt(path: Path) -> str:
    """Read a plain-text file."""
    return path.read_text(encoding="utf-8")
