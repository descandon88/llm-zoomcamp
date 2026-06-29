FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install CPU-only torch first (~200 MB vs ~2 GB for the CUDA default build)
RUN uv pip install --system --no-cache torch --index-url https://download.pytorch.org/whl/cpu

# Common dependencies across all modules
RUN uv pip install --system --no-cache \
    jupyter \
    requests \
    openai \
    python-dotenv \
    minsearch \
    sentence-transformers \
    sqlitesearch \
    gitsource \
    "psycopg[binary]" \
    tqdm

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]
