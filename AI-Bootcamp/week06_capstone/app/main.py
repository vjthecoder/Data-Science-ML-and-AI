"""FastAPI backend for the AI Career Coach.

Run:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY="sk-ant-..."
    uvicorn main:app --reload

Endpoints:
    GET  /health
    POST /analyze-resume        {resume_text}
    POST /skill-gap             {resume_text, job_description}
    POST /interview-questions   {role, n}
    POST /learning-path         {target_role, current_skills}
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent import (
    analyze_resume,
    detect_skill_gap,
    generate_interview_questions,
    generate_learning_path,
)

app = FastAPI(title="AI Career Coach", version="1.0.0")


class ResumeRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, max_length=20000)


class SkillGapRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, max_length=20000)
    job_description: str = Field(..., min_length=1, max_length=20000)


class InterviewRequest(BaseModel):
    role: str = Field(..., min_length=1, max_length=200)
    n: int = Field(8, ge=1, le=25)


class LearningPathRequest(BaseModel):
    target_role: str = Field(..., min_length=1, max_length=200)
    current_skills: list[str] = Field(default_factory=list)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze-resume")
def analyze(req: ResumeRequest):
    return {"analysis": analyze_resume(req.resume_text)}


@app.post("/skill-gap")
def skillgap(req: SkillGapRequest):
    return detect_skill_gap(req.resume_text, req.job_description)


@app.post("/interview-questions")
def interview(req: InterviewRequest):
    return {"questions": generate_interview_questions(req.role, req.n)}


@app.post("/learning-path")
def learning_path(req: LearningPathRequest):
    return {"path": generate_learning_path(req.target_role, req.current_skills)}
