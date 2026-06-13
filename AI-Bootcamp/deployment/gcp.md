# Deploying to Google Cloud (Cloud Run)

Cloud Run is the easiest GCP path for the containerized AI Career Coach — serverless,
autoscaling (to zero), HTTPS out of the box.

## Steps
1. Build and push to Artifact Registry (or let Cloud Run build from source):
   ```bash
   gcloud artifacts repositories create coach --repository-format=docker --location=us-central1
   cd AI-Bootcamp/week06_capstone/app
   gcloud builds submit --tag us-central1-docker.pkg.dev/PROJECT/coach/ai-career-coach
   ```
2. Deploy, injecting the secret from Secret Manager:
   ```bash
   # Store the key once:
   echo -n "sk-ant-..." | gcloud secrets create ANTHROPIC_API_KEY --data-file=-

   gcloud run deploy ai-career-coach \
     --image us-central1-docker.pkg.dev/PROJECT/coach/ai-career-coach \
     --region us-central1 --port 8000 --allow-unauthenticated \
     --set-secrets ANTHROPIC_API_KEY=ANTHROPIC_API_KEY:latest
   ```
3. Cloud Run returns an HTTPS URL; `/health` and `/docs` are live.

## Streamlit UI on Cloud Run
Override the container command:
```bash
gcloud run deploy coach-ui --image ... --port 8501 \
  --command streamlit --args run,streamlit_app.py,--server.port,8501,--server.address,0.0.0.0 \
  --set-secrets ANTHROPIC_API_KEY=ANTHROPIC_API_KEY:latest
```

## Notes
- Cloud Run scales to zero — first request after idle has a cold start.
- Use **Secret Manager** for `ANTHROPIC_API_KEY`; never put it in the image or env literal.
- You can also call Claude via **Vertex AI** with provider-prefixed model IDs if you prefer
  GCP-native billing; this app defaults to the Anthropic API.
- Set min instances > 0 if you need to avoid cold starts.
