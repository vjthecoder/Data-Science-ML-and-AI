# Week 6 Interview Questions: Final Project, Deployment & GitHub Packaging

## System Design
1. Walk through the architecture of the AI Career Coach end to end.
2. Why split deterministic logic (skill extraction) from LLM calls (advice)? What does each buy?
3. How does RAG ground the coach's output, and why does that matter?
4. How would you scale this app from one user to 10,000 concurrent users?
5. Where would you add caching, and what would you cache?

## API & Backend
6. Why validate requests with Pydantic? What happens without it?
7. How do you handle timeouts and errors on outbound LLM calls in a web API?
8. uvicorn vs gunicorn-with-uvicorn-workers — when would you use each?
9. How would you add rate limiting and authentication to the FastAPI service?
10. Why expose a `/health` endpoint, and how do platforms use it?

## Deployment & MLOps/LLMOps
11. Walk through containerizing and deploying this app. Why pass secrets at runtime?
12. Compare Cloud Run, Render, Railway, and ECS Fargate for this workload.
13. What goes in CI for an LLM app (lint, tests, notebook compile, evals)?
14. How would you monitor a deployed LLM app (latency, cost, error rate, faithfulness)?
15. How do you manage and rotate the `ANTHROPIC_API_KEY` securely in production?

## Cost & Reliability
16. List five levers to control LLM cost in this app.
17. How would you make the app degrade gracefully if the LLM provider is down?
18. What's your strategy for prompt/version management as the product evolves?
19. How would you A/B test a new prompt or a new model before rolling it out?

## Security & Privacy
20. Resumes contain PII. How do you handle storage, logging, and retention responsibly?
21. How do you defend against prompt injection in user-supplied resumes/job descriptions?
22. Why should secrets never appear in the Docker image or committed code?

## GitHub Packaging & Career
23. What makes a GitHub project "portfolio quality" to a hiring manager?
24. Why do conventional commits, a CI badge, and a clear README matter to reviewers?
25. How would you write the README so a recruiter understands the project in 60 seconds?

## Scenario
26. A user says the coach gave generic, ungrounded advice. Diagnose across parsing, RAG,
    prompting, and model layers.
27. Your cloud bill spiked overnight. How do you find and fix the cause in an LLM app?
28. You need to add a "cover letter generator" feature. Walk through the changes across
    `agent.py`, `main.py`, `streamlit_app.py`, tests, and deployment.
