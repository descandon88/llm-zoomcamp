FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

# Install CPU-only torch first (~200 MB vs ~2 GB for the CUDA default build)
RUN uv pip install --system --no-cache torch --index-url https://download.pytorch.org/whl/cpu

# Export remaining deps from lock file and install, skipping torch (already installed)
RUN uv export --frozen --no-dev --no-hashes -o /tmp/requirements.txt && \
    grep -v "^torch" /tmp/requirements.txt > /tmp/requirements_filtered.txt && \
    uv pip install --system --no-cache -r /tmp/requirements_filtered.txt

RUN uv pip install --system --no-cache sqlitesearch

# Module 01 homework dependencies
RUN uv pip install --system --no-cache gitsource
RUN uv pip install --system --no-cache toyaikit

COPY . .

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]
