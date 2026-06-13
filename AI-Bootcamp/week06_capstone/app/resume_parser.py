"""Resume parsing utilities for the AI Career Coach.

Extracts raw text from PDF/TXT resumes and pulls a rough skill list using a keyword
dictionary (fast, offline). The LLM-based analysis lives in agent.py.

Dependencies: pypdf (for PDF support).
"""

from __future__ import annotations

import re

# A small, extensible skill dictionary. In production, load from a maintained taxonomy.
KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "c++", "go", "rust",
    "pandas", "numpy", "scikit-learn", "pytorch", "tensorflow", "xgboost",
    "machine learning", "deep learning", "nlp", "computer vision",
    "rag", "llm", "langchain", "llamaindex", "prompt engineering",
    "aws", "gcp", "azure", "docker", "kubernetes", "fastapi", "flask", "streamlit",
    "git", "ci/cd", "airflow", "spark", "tableau", "power bi", "excel",
    "communication", "leadership", "project management",
]


def extract_text(path: str) -> str:
    """Extract raw text from a PDF or plain-text resume."""
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_skills(text: str, skills: list[str] | None = None) -> list[str]:
    """Return the subset of known skills mentioned in the text (case-insensitive)."""
    skills = skills or KNOWN_SKILLS
    low = text.lower()
    found = []
    for skill in skills:
        # word-boundary match so "go" doesn't match "google"
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, low):
            found.append(skill)
    return sorted(set(found))


def skill_gap(resume_skills: list[str], required_skills: list[str]) -> dict:
    """Compare resume skills against a job's required skills."""
    have = {s.lower() for s in resume_skills}
    need = {s.lower() for s in required_skills}
    return {
        "matched": sorted(have & need),
        "missing": sorted(need - have),
        "extra": sorted(have - need),
        "coverage": round(len(have & need) / len(need), 2) if need else 1.0,
    }


if __name__ == "__main__":
    sample = "Experienced in Python, Pandas, and AWS. Built ML models with scikit-learn."
    found = extract_skills(sample)
    print("Skills found:", found)
    print("Gap vs job:", skill_gap(found, ["python", "pytorch", "docker", "aws"]))
