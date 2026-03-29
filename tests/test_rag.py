"""
tests/test_rag.py
Unit tests for Dev 1's RAG modules.
All Gemini and ChromaDB calls are mocked — no real API keys needed.
Run with: python -m pytest tests/test_rag.py -v
"""

import tempfile
import os
import unittest
from unittest.mock import MagicMock, patch


# ─── loader.py ───────────────────────────────────────────────────────────────

class TestLoader(unittest.TestCase):

    def test_load_txt(self):
        """load_document() should read a plain text file correctly."""
        from rag.loader import load_document

        content = "Hello RAG world.\nSecond line."
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w",
                                         delete=False, encoding="utf-8") as f:
            f.write(content)
            tmp_path = f.name
        try:
            result = load_document(tmp_path)
            self.assertEqual(result, content)
        finally:
            os.unlink(tmp_path)

    def test_load_file_not_found(self):
        """load_document() raises FileNotFoundError for missing files."""
        from rag.loader import load_document
        with self.assertRaises(FileNotFoundError):
            load_document("no/such/file.txt")

    def test_load_unsupported_extension(self):
        """load_document() raises ValueError for unsupported extensions."""
        from rag.loader import load_document
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            tmp_path = f.name
        try:
            with self.assertRaises(ValueError):
                load_document(tmp_path)
        finally:
            os.unlink(tmp_path)

    @patch("rag.loader.fitz.open")
    def test_load_pdf(self, mock_fitz_open):
        """load_document() should extract text from each PDF page."""
        from rag.loader import load_document

        mock_page = MagicMock()
        mock_page.get_text.return_value = "Page one text."
        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))
        mock_fitz_open.return_value = mock_doc

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            tmp_path = f.name
        try:
            result = load_document(tmp_path)
            self.assertIn("Page one text.", result)
        finally:
            os.unlink(tmp_path)


# ─── chunker.py ──────────────────────────────────────────────────────────────

class TestChunker(unittest.TestCase):

    def test_chunk_text_returns_list(self):
        """chunk_text() should return a non-empty list of strings."""
        from rag.chunker import chunk_text
        text = "word " * 300  # ~1500 chars → multiple chunks at size=500
        chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 1)

    def test_chunk_text_empty(self):
        """chunk_text() should return empty list or single chunk for empty text."""
        from rag.chunker import chunk_text
        result = chunk_text("", chunk_size=500, chunk_overlap=50)
        self.assertIsInstance(result, list)

    def test_chunk_text_short(self):
        """chunk_text() should return single chunk for short text."""
        from rag.chunker import chunk_text
        result = chunk_text("Short text.", chunk_size=500, chunk_overlap=50)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Short text.")


# ─── embedder.py (Gemini) ─────────────────────────────────────────────────────

class TestEmbedder(unittest.TestCase):

    @patch("rag.embedder.genai.embed_content")
    @patch("rag.embedder.genai.configure")
    def test_embed_chunks_shape(self, mock_configure, mock_embed):
        """embed_chunks() should return one vector per input chunk."""
        from rag.embedder import embed_chunks

        # embed_chunks calls _embed_one once per chunk → genai.embed_content called twice.
        # Each call returns a flat embedding vector (as the real API does).
        mock_embed.side_effect = [
            {"embedding": [0.1, 0.2]},
            {"embedding": [0.3, 0.4]},
        ]
        result = embed_chunks(["chunk one", "chunk two"])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [0.1, 0.2])
        self.assertEqual(result[1], [0.3, 0.4])
        self.assertEqual(mock_embed.call_count, 2)

    @patch("rag.embedder.genai.embed_content")
    @patch("rag.embedder.genai.configure")
    def test_embed_chunks_empty(self, mock_configure, mock_embed):
        """embed_chunks([]) should return [] without making any API calls."""
        from rag.embedder import embed_chunks
        result = embed_chunks([])
        self.assertEqual(result, [])
        mock_embed.assert_not_called()

    @patch("rag.embedder.genai.embed_content")
    @patch("rag.embedder.genai.configure")
    def test_embed_query(self, mock_configure, mock_embed):
        """embed_query() should return a single vector."""
        from rag.embedder import embed_query

        mock_embed.return_value = {"embedding": [0.5, 0.6, 0.7]}
        result = embed_query("what is dosage?")

        self.assertEqual(result, [0.5, 0.6, 0.7])
        # Must use retrieval_query task_type
        call_kwargs = mock_embed.call_args.kwargs
        self.assertEqual(call_kwargs.get("task_type"), "retrieval_query")


# ─── pipeline.py (Gemini) ─────────────────────────────────────────────────────

class TestPipeline(unittest.TestCase):

    @patch("core.pipeline._call_llm")
    @patch("core.pipeline.retrieve")
    def test_get_answer_structure(self, mock_retrieve, mock_call_llm):
        """get_answer() should return a dict with answer, sources, query keys."""
        from core.pipeline import get_answer

        mock_retrieve.return_value = [
            {"text": "Sample chunk.", "source": "doc.pdf", "score": 0.91}
        ]
        mock_call_llm.return_value = "The answer is 42."

        result = get_answer("What is the answer?")

        self.assertIn("answer", result)
        self.assertIn("sources", result)
        self.assertIn("query", result)
        self.assertEqual(result["query"], "What is the answer?")
        self.assertEqual(result["answer"], "The answer is 42.")
        self.assertEqual(len(result["sources"]), 1)

    @patch("core.pipeline._call_llm")
    @patch("core.pipeline.retrieve")
    def test_get_answer_sources_passthrough(self, mock_retrieve, mock_call_llm):
        """Sources in get_answer() output should be unchanged from retrieve()."""
        from core.pipeline import get_answer

        sources = [{"text": "x", "source": "a.pdf", "score": 0.9}]
        mock_retrieve.return_value = sources
        mock_call_llm.return_value = "answer"

        result = get_answer("query")
        self.assertEqual(result["sources"], sources)

    @patch("core.pipeline.genai")
    def test_call_llm_uses_gemini(self, mock_genai):
        """_call_llm() should call Gemini GenerativeModel.generate_content."""
        from core.pipeline import _call_llm
        import core.pipeline as pipeline_module

        mock_model = MagicMock()
        mock_model.generate_content.return_value = MagicMock(text="  gemini answer  ")
        pipeline_module._model = mock_model

        result = _call_llm("some prompt")
        self.assertEqual(result, "gemini answer")
        mock_model.generate_content.assert_called_once_with("some prompt")

        # Restore
        pipeline_module._model = None


if __name__ == "__main__":
    unittest.main()
