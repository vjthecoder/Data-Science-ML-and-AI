"""AI Career Coach agent.

Orchestrates the capstone features by calling Claude with RAG-grounded context:
  - resume analysis
  - skill gap detection
  - interview question generation
  - learning path generation

Each function degrades gracefully to an offline stub when ANTHROPIC_API_KEY is unset, so the
app and tests run without a key.

Dependencies: anthropic
Environment: ANTHROPIC_API_KEY (never hardcode)
"""

from __future__ import annotations

import json
import os

from rag import build_context
from resume_parser import extract_skills, skill_gap

MODEL = os.environ.get("COACH_MODEL", "claude-opus-4-8")


def _llm(system: str, user: str, max_tokens: int = 1024) -> str:
    """Call Claude; fall back to a clearly-marked stub when no API key is configured."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return f"[offline stub — set ANTHROPIC_API_KEY for real output]\nSYSTEM: {system[:80]}...\nUSER: {user[:120]}..."
    import anthropic

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user}],
    )
    return next((b.text for b in resp.content if b.type == "text"), "")


def analyze_resume(resume_text: str) -> str:
    """Summarize strengths, weaknesses, and suggested improvements."""
    context = build_context("resume best practices for AI engineering roles")
    system = (
        "You are an expert technical career coach. Analyze the resume and give concise, "
        "actionable feedback: 3 strengths, 3 weaknesses, 3 concrete improvements. "
        "Ground advice in the provided context."
    )
    user = f"Context:\n{context}\n\nResume:\n{resume_text[:6000]}"
    return _llm(system, user)


def detect_skill_gap(resume_text: str, job_description: str) -> dict:
    """Return a structured skill-gap analysis (deterministic) plus an LLM narrative."""
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    gap = skill_gap(resume_skills, job_skills)

    system = (
        "You are a career coach. Given a skill-gap analysis, write a short paragraph advising "
        "the candidate on what to prioritize learning and how to position existing skills."
    )
    user = f"Skill gap (JSON): {json.dumps(gap)}\n\nWrite the advice."
    gap["advice"] = _llm(system, user, max_tokens=400)
    return gap


def generate_interview_questions(role: str, n: int = 8) -> str:
    """Generate role-specific interview questions grounded in KB context."""
    context = build_context(f"interview expectations for {role}")
    system = (
        "You are a senior interviewer. Generate role-specific interview questions covering "
        "technical, system-design, and behavioral areas. Number them."
    )
    user = f"Context:\n{context}\n\nRole: {role}\nGenerate {n} questions."
    return _llm(system, user)


def generate_learning_path(target_role: str, current_skills: list[str]) -> str:
    """Produce a personalized, prioritized learning roadmap."""
    context = build_context(f"skills required for {target_role}")
    system = (
        "You are a learning-path designer. Produce a prioritized, time-boxed roadmap "
        "(weeks 1-8) to reach the target role, building on the candidate's current skills. "
        "Recommend concrete projects."
    )
    user = (
        f"Context:\n{context}\n\nTarget role: {target_role}\n"
        f"Current skills: {', '.join(current_skills) or 'none listed'}"
    )
    return _llm(system, user, max_tokens=1200)


# A simple tool-routing "agent" entry point used by the API/UI.
def coach(action: str, **kwargs):
    actions = {
        "analyze_resume": lambda: analyze_resume(kwargs["resume_text"]),
        "skill_gap": lambda: detect_skill_gap(kwargs["resume_text"], kwargs["job_description"]),
        "interview_questions": lambda: generate_interview_questions(
            kwargs["role"], kwargs.get("n", 8)
        ),
        "learning_path": lambda: generate_learning_path(
            kwargs["target_role"], kwargs.get("current_skills", [])
        ),
    }
    if action not in actions:
        raise ValueError(f"unknown action: {action}")
    return actions[action]()


if __name__ == "__main__":
    print(coach("interview_questions", role="AI Engineer", n=3))
