"""PDF Chatbot — Streamlit RAG application.

Run:
    pip install streamlit chromadb sentence-transformers pypdf anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."
    streamlit run app.py
"""

from __future__ import annotations

import os
import tempfile

import streamlit as st

from rag_core import answer, build_chunks, build_index

st.set_page_config(page_title="PDF Chatbot", page_icon="📄")
st.title("📄 Chat with your PDFs")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "collection" not in st.session_state:
    st.session_state.collection = None

# --------------------------------------------------------------------------- #
# Sidebar: upload + index
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.header("1. Upload PDFs")
    uploaded = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if st.button("Index documents", disabled=not uploaded):
        if not os.environ.get("ANTHROPIC_API_KEY"):
            st.warning("Set ANTHROPIC_API_KEY in your environment to enable answering.")
        with st.spinner("Extracting, chunking, embedding…"):
            paths = []
            for f in uploaded:
                # Sanitize: use only the basename, write to a temp dir
                safe_name = os.path.basename(f.name)
                tmp = os.path.join(tempfile.gettempdir(), safe_name)
                with open(tmp, "wb") as out:
                    out.write(f.read())
                paths.append(tmp)
            chunks = build_chunks(paths)
            st.session_state.collection = build_index(chunks)
        st.success(f"Indexed {len(chunks)} chunks from {len(paths)} file(s).")

    st.caption("Answers are grounded in your uploaded PDFs and cite source + page.")

# --------------------------------------------------------------------------- #
# Chat
# --------------------------------------------------------------------------- #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your PDFs…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.collection is None:
            reply = "Please upload and index PDFs first (sidebar)."
        else:
            with st.spinner("Thinking…"):
                result = answer(st.session_state.collection, prompt)
            cites = "  \n".join(f"- {c}" for c in result["citations"])
            reply = result["answer"] + (f"\n\n**Sources:**  \n{cites}" if cites else "")
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
