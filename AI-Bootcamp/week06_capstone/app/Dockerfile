# AI Career Coach — container image (runs the FastAPI backend by default)
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Do NOT bake secrets into the image — pass ANTHROPIC_API_KEY at runtime:
#   docker run -e ANTHROPIC_API_KEY=sk-ant-... -p 8000:8000 ai-career-coach
EXPOSE 8000

# Healthcheck hits the FastAPI /health endpoint
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

# Default: FastAPI. To run the Streamlit UI instead, override the command:
#   docker run -p 8501:8501 ai-career-coach streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
