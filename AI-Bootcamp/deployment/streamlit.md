# Deploying the Streamlit UI (Streamlit Community Cloud)

Streamlit Community Cloud is the fastest free way to publish the AI Career Coach UI.

## Steps
1. Push the repo to GitHub (entry point `week06_capstone/app/streamlit_app.py`).
2. Go to https://share.streamlit.io → **New app**.
3. Select the repo/branch; set **Main file path** to
   `AI-Bootcamp/week06_capstone/app/streamlit_app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
   Map it into the environment at the top of the app:
   ```python
   import os, streamlit as st
   if "ANTHROPIC_API_KEY" in st.secrets:
       os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
   ```
5. Set the requirements file to `AI-Bootcamp/week06_capstone/app/requirements.txt`.
6. Deploy → you get a public `*.streamlit.app` URL.

## Notes
- The app runs in **offline stub mode** without a key — handy for a no-secret demo.
- Community Cloud sleeps on inactivity; for always-on, deploy the container (see `docker.md`)
  to Render/Railway/Cloud Run.
- Keep `requirements.txt` lean (omit `sentence-transformers`/`chromadb` unless using prod RAG).

## Best practices
- Never commit secrets; use the Secrets manager.
- Pin dependency versions; add a README with a screenshot and the live URL.
