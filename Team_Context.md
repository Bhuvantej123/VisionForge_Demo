# TEAM CONTEXT — RAG Demo Hackathon

## What We Are Building
A Retrieval Augmented Generation (RAG) system for domain-specific 
document Q&A. Users upload PDFs or text files, ask natural language 
questions, and get cited answers grounded in the documents.

## Hackathon Deadline
April 12th — recorded video demo, 3-5 minutes long

## Tech Stack
- Python 3.11
- ChromaDB (vector store — runs locally, no setup needed)
- OpenAI text-embedding-3-small (embeddings)
- GPT-4o-mini (LLM for answer generation)
- Streamlit (UI)
- LangChain (chunking only — no heavy agent usage)
- PyMuPDF (PDF parsing)
- python-dotenv (environment variables)

---

## Folder Structure & Ownership

rag-demo/
├── rag/                 → Dev 1 owns this (RAG core)
├── core/                → Dev 1 owns this (pipeline + get_answer)
├── ui/                  → Dev 2 owns this (Streamlit UI)
├── utils/               → Dev 3 owns this (logger)
├── prompts/             → Dev 3 owns this (prompt template)
├── data/sample_docs/    → Dev 3 owns this (demo PDFs)
├── main.py              → Dev 1 owns this
├── requirements.txt     → Dev 1 owns this
├── .env                 → Dev 1 owns this (never commit)
├── .env.example         → Dev 1 owns this (safe to commit)
├── .gitignore           → Dev 1 owns this
└── README.md            → Dev 3 owns this

---

## Team Roles

### Dev 1 (RAG Core + Integration Lead)
Owns: rag/, core/, main.py, all config files
Builds:
- rag/loader.py       → PDF/text to raw text
- rag/chunker.py      → raw text to chunks
- rag/embedder.py     → chunks to vectors
- rag/vectorstore.py  → store and persist vectors in ChromaDB
- rag/retriever.py    → query to top-k relevant chunks
- core/pipeline.py    → get_answer() function, prompt builder, LLM call
- main.py             → entry point, ties everything together
Do NOT touch: ui/, utils/

### Dev 2 (UI)
Owns: ui/app.py
Builds:
- File upload interface (PDF/text)
- Chat input for user queries
- Answer display with formatting
- Source citations display
- Uses get_answer() from core/pipeline.py as a black box
Do NOT touch: rag/, core/

### Dev 3 (Logger + Prompt + Docs)
Owns: utils/logger.py, prompts/prompt_template.txt, data/, README.md
Builds:
- utils/logger.py           → logs every query/answer to jsonl file
- prompts/prompt_template.txt → prompt wording and iteration
- data/sample_docs/         → curate 5-10 good domain-specific demo PDFs
- README.md                 → setup and run instructions
Do NOT touch: rag/, core/, ui/

---

## Agreed Interfaces — LOCKED ON DAY 1, DO NOT CHANGE

### retrieve()
File:    rag/retriever.py
Input:   query (str), top_k (int) = 5
Output:  list of dicts
Example output:
[
  {
    "text": "Ibuprofen is a nonsteroidal anti-inflammatory drug...",
    "source": "medical_guide.pdf",
    "score": 0.92
  },
  {
    "text": "Recommended adult dosage is 200-400mg every 4-6 hours...",
    "source": "medical_guide.pdf",
    "score": 0.87
  }
]

### get_answer()
File:    core/pipeline.py
Input:   query (str)
Output:  dict
Example output:
{
  "answer": "According to medical_guide.pdf, ibuprofen dosage is...",
  "sources": [
    {"text": "chunk text here...", "source": "medical_guide.pdf", "score": 0.92}
  ],
  "query": "What is the dosage for ibuprofen?"
}

### log_query()
File:    utils/logger.py
Input:   query (str), answer (str), sources (list of dicts), 
         response_time_ms (int)
Output:  None — writes to logs/query_log.jsonl
Example log entry:
{
  "time": "2024-04-01 10:32:01",
  "query": "What is the dosage for ibuprofen?",
  "answer": "According to medical_guide.pdf...",
  "sources": ["medical_guide.pdf"],
  "response_time_ms": 1240
}

---

## Stub Implementations
These are fake implementations so everyone can start on Day 1
without waiting for each other.

### retrieve() stub — Dev 2 and Dev 3 use this until Dev 1 finishes
```python
def retrieve(query: str, top_k: int = 5) -> list[dict]:
    return [
        {
            "text": "This is a sample chunk from the document...",
            "source": "sample.pdf",
            "score": 0.92
        },
        {
            "text": "Another relevant passage from the document...",
            "source": "sample.pdf",
            "score": 0.87
        }
    ]
```

### get_answer() stub — Dev 2 uses this until Dev 1 finishes
```python
def get_answer(query: str) -> dict:
    return {
        "answer": "This is a placeholder answer for UI testing purposes.",
        "sources": [
            {"text": "Sample chunk text...", "source": "test.pdf", "score": 0.91}
        ],
        "query": query
    }
```

---

## Environment Variables (.env)
OPENAI_API_KEY=your_key_here
COLLECTION_NAME=rag_demo
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=5

---

## Git Workflow

### Branch names
dev1/rag-core        → Dev 1
dev2/ui              → Dev 2
dev3/pipeline        → Dev 3

### Day 1 setup
# Dev 1 does this first
git checkout -b dev1/rag-core
# write all stubs immediately
git add .
git commit -m "feat: add all stub functions"
git push origin dev1/rag-core

# Dev 2 and Dev 3 branch off Dev 1's branch
git checkout -b dev2/ui origin/dev1/rag-core
git checkout -b dev3/pipeline origin/dev1/rag-core

### Rules
- Never push directly to main
- Never edit files outside your owned folder
- Commit often with clear messages
- Dev 1 reviews and merges everything into main at the end

---

## Completed Files
(Dev 1 updates this section as files are finished
so other agents have the real code to reference)

### rag/loader.py
[paste completed code here when done]

### rag/chunker.py
[paste completed code here when done]

### rag/embedder.py
[paste completed code here when done]

### rag/vectorstore.py
[paste completed code here when done]

### rag/retriever.py
[paste completed code here when done]

### core/pipeline.py
[paste completed code here when done]

---

## How To Use This Document
1. Paste this ENTIRE file at the start of every AI agent session
2. Then add your role at the bottom like this:

"I am Dev [X]. I own [folder].
Help me build [specific file] next.
Treat [other modules] as black boxes that already work."

3. As Dev 1 completes files, paste the real code
   into the Completed Files section above
   so your agent has the actual implementation to reference.