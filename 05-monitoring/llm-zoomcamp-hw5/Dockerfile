FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN uv pip install --system --no-cache \
    jupyter \
    requests \
    openai \
    python-dotenv \
    minsearch \
    gitsource \
    streamlit \
    pandas \
    pydantic \
    "psycopg[binary]" \
    tqdm \
    opentelemetry-api \
    opentelemetry-sdk

EXPOSE 8888
EXPOSE 8501

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]
