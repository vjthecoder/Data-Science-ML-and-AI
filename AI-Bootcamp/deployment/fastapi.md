# Deploying the FastAPI Backend

The capstone backend (`week06_capstone/app/main.py`) is a standard ASGI app served by uvicorn.

## Local / VM
```bash
cd AI-Bootcamp/week06_capstone/app
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn main:app --host 0.0.0.0 --port 8000
# Swagger UI at /docs, health at /health
```

## Production process management
- Run multiple workers behind the built-in server: `uvicorn main:app --workers 4` (CPU-bound)
  or use **gunicorn** with uvicorn workers:
  ```bash
  pip install gunicorn
  gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000
  ```
- Put a reverse proxy (nginx/Caddy) or a platform load balancer in front for TLS.
- Use a process manager (systemd, supervisor) or a container orchestrator for restarts.

## Containerized (recommended)
The provided `Dockerfile` runs `uvicorn main:app` by default — see `docker.md`. Deploy that
image to Render, Railway, Cloud Run, or ECS (see the respective guides).

## Production checklist
- [ ] Validate request bodies with Pydantic (already done via `BaseModel` + `Field`)
- [ ] Add structured logging and request IDs
- [ ] Add rate limiting (e.g. slowapi) and timeouts on outbound LLM calls
- [ ] Configure CORS if a browser frontend calls the API directly
- [ ] Secrets via environment / secret manager — never in code
- [ ] Health endpoint wired to the platform's healthcheck (`/health`)
