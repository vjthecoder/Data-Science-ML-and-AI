"""Smoke tests for the AI Career Coach (run offline — no API key needed).

Run:
    cd app && python -m pytest test_app.py
"""

from resume_parser import extract_skills, skill_gap
from rag import KnowledgeBase, build_context
from agent import coach


def test_extract_skills():
    text = "Built ML models in Python with scikit-learn and deployed on AWS using Docker."
    skills = extract_skills(text)
    assert "python" in skills
    assert "aws" in skills
    assert "docker" in skills


def test_skill_gap():
    gap = skill_gap(["python", "aws"], ["python", "pytorch", "docker"])
    assert gap["matched"] == ["python"]
    assert "pytorch" in gap["missing"]
    assert 0 <= gap["coverage"] <= 1


def test_knowledge_base_retrieve():
    kb = KnowledgeBase()
    hits = kb.retrieve("how to become an AI engineer", k=2)
    assert len(hits) == 2
    assert all(isinstance(h, str) for h in hits)


def test_build_context():
    ctx = build_context("RAG skills")
    assert isinstance(ctx, str) and len(ctx) > 0


def test_coach_offline_stub():
    # Without ANTHROPIC_API_KEY, agent functions return a clearly-marked stub (no crash).
    out = coach("interview_questions", role="AI Engineer", n=3)
    assert isinstance(out, str) and len(out) > 0


def test_coach_unknown_action():
    import pytest

    with pytest.raises(ValueError):
        coach("nonexistent")
