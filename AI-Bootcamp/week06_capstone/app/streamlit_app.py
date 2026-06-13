"""Streamlit frontend for the AI Career Coach.

Run:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY="sk-ant-..."
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import os
import tempfile

import streamlit as st

from agent import (
    analyze_resume,
    detect_skill_gap,
    generate_interview_questions,
    generate_learning_path,
)
from resume_parser import extract_skills, extract_text

st.set_page_config(page_title="AI Career Coach", page_icon="🎯", layout="wide")
st.title("🎯 AI Career Coach")

if not os.environ.get("ANTHROPIC_API_KEY"):
    st.info("Running in offline stub mode. Set ANTHROPIC_API_KEY for real LLM output.")

# --- Resume input (shared across tabs) ---
with st.sidebar:
    st.header("Your Resume")
    uploaded = st.file_uploader("Upload resume (PDF or TXT)", type=["pdf", "txt"])
    resume_text = ""
    if uploaded:
        safe_name = os.path.basename(uploaded.name)
        tmp = os.path.join(tempfile.gettempdir(), safe_name)
        with open(tmp, "wb") as f:
            f.write(uploaded.read())
        resume_text = extract_text(tmp)
        st.success(f"Loaded {len(resume_text)} characters.")
    resume_text = st.text_area("…or paste resume text", value=resume_text, height=200)

tabs = st.tabs(["Resume Analysis", "Skill Gap", "Interview Questions", "Learning Path"])

with tabs[0]:
    st.subheader("Resume Analysis")
    if st.button("Analyze", key="analyze") and resume_text:
        with st.spinner("Analyzing…"):
            st.markdown(analyze_resume(resume_text))
    elif not resume_text:
        st.caption("Add your resume in the sidebar first.")

with tabs[1]:
    st.subheader("Skill Gap Detection")
    jd = st.text_area("Paste a target job description", height=180, key="jd")
    if st.button("Find gaps", key="gap") and resume_text and jd:
        with st.spinner("Comparing…"):
            result = detect_skill_gap(resume_text, jd)
        c1, c2, c3 = st.columns(3)
        c1.metric("Coverage", f"{int(result['coverage'] * 100)}%")
        c2.metric("Matched", len(result["matched"]))
        c3.metric("Missing", len(result["missing"]))
        st.write("**Missing skills:**", ", ".join(result["missing"]) or "none 🎉")
        st.markdown(result["advice"])

with tabs[2]:
    st.subheader("Interview Question Generator")
    role = st.text_input("Target role", value="AI Engineer", key="role")
    n = st.slider("How many questions", 3, 20, 8)
    if st.button("Generate questions", key="iq"):
        with st.spinner("Generating…"):
            st.markdown(generate_interview_questions(role, n))

with tabs[3]:
    st.subheader("Learning Path Generator")
    target = st.text_input("Target role", value="AI Engineer", key="target")
    if st.button("Build my roadmap", key="lp"):
        skills = extract_skills(resume_text) if resume_text else []
        with st.spinner("Designing your path…"):
            st.markdown(generate_learning_path(target, skills))
