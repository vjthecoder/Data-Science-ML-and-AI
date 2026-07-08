# Deploying to Railway

Railway deploys from a GitHub repo (Nixpacks) or a Dockerfile with minimal config.

## Steps (Docker)
1. Push the repo to GitHub.
2. Railway → **New Project → Deploy from GitHub repo**.
3. In the service settings, set the **Root Directory** to
   `AI-Bootcamp/week06_capstone/app` (Railway detects the `Dockerfile`).
4. Add a **Variable** `ANTHROPIC_API_KEY` (Railway encrypts it).
5. Railway assigns a port via `$PORT` — the FastAPI start respects it if you set the start
   command:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
   (For Streamlit: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`)
6. Generate a public domain in the service's **Settings → Networking**.

## Notes
- Bind to `$PORT` — Railway sets it; hardcoding a port will fail health checks.
- Store `ANTHROPIC_API_KEY` as a Railway variable; never commit it.
- Railway's free tier has usage limits; upgrade for always-on services.

## Best practices
- Use the Dockerfile for reproducible builds.
- Set a healthcheck path (`/health`) in service settings.
- Use separate services for the API and the Streamlit UI if you deploy both.
