"""
ui/app.py — Dev 2
Professional Streamlit UI — Minimalist, corporate styling without emojis.
Uses get_answer() from core/pipeline.py as a black box.
"""

import os
import sys
import tempfile
import time
from pathlib import Path

import streamlit as st

# Ensure project root is on sys.path
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.pipeline import get_answer
from main import ingest_document


# ─── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="VisionForge RAG",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Professional CSS ─────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    /* ---------- Fonts and Core ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ---------- Sidebar (Corporate Dark) ---------- */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #94a3b8 !important;
        font-size: 0.9rem;
    }

    /* ---------- Main Area ---------- */
    .stApp {
        background-color: #020617;
    }
    
    h1 {
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* ---------- Chat Message Styling ---------- */
    .user-msg {
        background-color: #2563eb;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.95rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .bot-msg {
        background-color: #1e293b;
        color: #e2e8f0;
        border-radius: 8px;
        border: 1px solid #334155;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        max-width: 90%;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ---------- Source Citations ---------- */
    .source-container {
        margin-top: 0.5rem;
        margin-left: 1.5rem;
        padding-left: 1rem;
        border-left: 1px solid #334155;
    }
    
    .source-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 6px 0;
        color: #64748b;
        font-size: 0.85rem;
    }
    
    .source-tag {
        background-color: #0f172a;
        color: #3b82f6;
        border: 1px solid #1e3a8a;
        border-radius: 4px;
        padding: 2px 8px;
        font-weight: 500;
        font-family: monospace;
    }

    .match-score {
        margin-left: auto;
        font-weight: 600;
    }

    /* ---------- Buttons and Inputs ---------- */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.75rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ─── Session state ─────────────────────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = []


# ─── Sidebar ──────────────────────────────────────────────────────────────────

def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### VisionForge RAG")
        st.markdown("Enterprise Document Intelligence")
        st.divider()

        st.markdown("**Document Management**")
        uploaded = st.file_uploader(
            "Upload PDF or TXT sources",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        _handle_uploads(uploaded or [])

        if st.session_state.ingested_files:
            st.markdown("---")
            st.markdown("**Active Knowledge Base**")
            for fname in st.session_state.ingested_files:
                st.caption(f"FILE: {fname}")

        st.divider()
        st.markdown("**System Usage**")
        st.caption("1. Upload documentation")
        st.caption("2. Query the knowledge base")
        st.caption("3. Review cited references")
        
        st.divider()
        if st.button("Clear Session Data", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


def _handle_uploads(files) -> None:
    for uploaded_file in files:
        if uploaded_file.name in st.session_state.ingested_files:
            continue

        with st.spinner(f"Processing {uploaded_file.name}..."):
            try:
                suffix = Path(uploaded_file.name).suffix
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=suffix
                ) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                ingest_document(tmp_path, source_name=uploaded_file.name)
                st.session_state.ingested_files.append(uploaded_file.name)
                st.toast(f"Source Added: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Ingestion Error: {uploaded_file.name} - {e}")
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass


# ─── Main Interface ──────────────────────────────────────────────────────────

def render_header() -> None:
    st.markdown("<h1>VisionForge RAG</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Analyze document repositories with grounded, cited responses powered by Gemini.</div>", 
        unsafe_allow_html=True
    )


def render_chat_history() -> None:
    for item in st.session_state.chat_history:
        # User message
        st.markdown(
            f'<div class="user-msg">{item["query"]}</div>',
            unsafe_allow_html=True,
        )
        # Assistant message
        st.markdown(
            f'<div class="bot-msg">{item["result"]["answer"]}</div>',
            unsafe_allow_html=True,
        )
        _render_sources(item["result"]["sources"])


def _render_sources(sources: list) -> None:
    if not sources:
        return
    with st.expander("Reference Passages", expanded=False):
        for src in sources:
            score_pct = int(src.get("score", 0) * 100)
            score_color = "#10b981" if score_pct >= 80 else "#f59e0b" if score_pct >= 60 else "#ef4444"
            st.markdown(
                f"""
                <div class="source-item">
                    <span class="source-tag">{src.get('source', 'unknown')}</span>
                    <span style="flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap">
                        {src.get('text', '')[:120]}...
                    </span>
                    <span class="match-score" style="color:{score_color}">{score_pct}% match</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def main() -> None:
    render_sidebar()
    render_header()
    st.divider()

    if not st.session_state.ingested_files:
        st.info("System Ready. Please initialize the knowledge base by uploading documents in the sidebar.")

    render_chat_history()

    query = st.chat_input("Enter query...")
    if query:
        if not st.session_state.ingested_files:
            st.warning("Knowledge base uninitialized. Please upload documents.")
            return

        with st.spinner("Analyzing..."):
            try:
                result = get_answer(query)
            except Exception as e:
                st.error(f"Analysis Error: {e}")
                return

        st.session_state.chat_history.append({"query": query, "result": result})
        st.rerun()


if __name__ == "__main__":
    main()
