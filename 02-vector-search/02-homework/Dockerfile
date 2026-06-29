FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

RUN uv init --no-workspace
RUN uv add onnxruntime tokenizers numpy tqdm minsearch gitsource
RUN uv add --dev huggingface-hub jupyter
RUN uv pip install --system --no-cache \
    openai \
    python-dotenv \
    "psycopg[binary]" \
    gitsource \
    tqdm


EXPOSE 8888

CMD ["uv", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]