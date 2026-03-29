# VisionForge RAG Demo

A **Retrieval-Augmented Generation (RAG)** system for domain-specific document Q&A.  
Upload PDF or text files, ask natural-language questions, and receive **cited, accurate answers** grounded in your documents — powered by **Google Gemini** and **ChromaDB**.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Embeddings | Google Gemini `gemini-embedding-001` |
| LLM | Google Gemini `gemini-1.5-flash` |
| Vector Store | ChromaDB (local, persistent) |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |
| PDF Parsing | PyMuPDF |
| UI | Streamlit |

---

## Project Structure

```
VisionForge_Demo/
├── rag/                  # RAG core (loader, chunker, embedder, vectorstore, retriever)
├── core/pipeline.py      # get_answer() — retrieves + prompts + calls LLM
├── ui/app.py             # Streamlit UI
├── utils/logger.py       # JSONL query logger
├── prompts/              # Prompt template
├── data/sample_docs/     # Demo documents (PDF / txt)
├── logs/                 # Auto-created — query_log.jsonl written here
├── chroma_db/            # Auto-created — persistent vector store
├── main.py               # CLI ingestion entry point
├── requirements.txt
├── .env                  # Local secrets (never commit)
└── .env.example          # Safe-to-commit template
```

---

## Setup

### 1. Prerequisites
- Python 3.11+
- A [Google AI Studio](https://aistudio.google.com/) API key (free tier)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example env file and fill in your key:

```bash
copy .env.example .env
```

Edit `.env`:
```
GEMINI_API_KEY=your_key_here
COLLECTION_NAME=rag_demo
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=5
```

---

## Usage

### Ingest documents (CLI)

Ingest a single file:
```bash
python main.py --file data/sample_docs/my_document.pdf
```

Ingest all files in `data/sample_docs/`:
```bash
python main.py --all
```

### Run the Streamlit UI

```bash
streamlit run ui/app.py
```

Then open [http://localhost:8501](http://localhost:8501).

1. Upload PDF or `.txt` files in the **sidebar**
2. Type your question in the **chat input**
3. Get a **cited answer** with source passages

---

## Run Tests

```bash
python -m pytest tests/test_rag.py -v
```

All Gemini and ChromaDB calls are mocked — no API key needed for tests.

---

## Logs

Every query and answer is appended to `logs/query_log.jsonl`:

```json
{"time": "2026-03-29 11:00:00", "query": "What is ...?", "answer": "According to ...", "sources": ["doc.pdf"], "response_time_ms": 1240}
```

---

## Notes

- The `chroma_db/` and `logs/` directories are created automatically on first run.
- Free-tier Gemini embedding: 100 requests/minute. The embedder auto-throttles at ~92 req/min.
- Re-ingesting the same file will add duplicate chunks; clear `chroma_db/` to reset.