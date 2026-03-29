"""
utils/logger.py — Dev 3
Responsibility: Log every query/answer pair to a JSONL file.

LOCKED INTERFACE — do not change function signature.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List

# Resolve logs directory relative to the project root
_LOGS_DIR = Path(__file__).parent.parent / "logs"
_LOG_FILE = _LOGS_DIR / "query_log.jsonl"


def log_query(
    query: str,
    answer: str,
    sources: List[dict],
    response_time_ms: int,
) -> None:
    """
    Append a query/answer record to logs/query_log.jsonl.

    Args:
        query: The user's original question.
        answer: The LLM-generated answer string.
        sources: List of source dicts used (each has "text", "source", "score").
        response_time_ms: Time taken to generate the answer, in milliseconds.

    Returns:
        None — writes a single JSON line to logs/query_log.jsonl.

    Example log entry written:
        {
            "time": "2024-04-01 10:32:01",
            "query": "What is the dosage for ibuprofen?",
            "answer": "According to medical_guide.pdf...",
            "sources": ["medical_guide.pdf"],
            "response_time_ms": 1240
        }
    """
    # Ensure the logs directory exists
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Extract unique source filenames for the log entry
    source_names = list(dict.fromkeys(s.get("source", "unknown") for s in sources))

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "answer": answer,
        "sources": source_names,
        "response_time_ms": response_time_ms,
    }

    with open(_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
