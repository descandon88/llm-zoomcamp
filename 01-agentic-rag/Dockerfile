FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

# Install CPU-only torch first (~200 MB vs ~2 GB for the CUDA default build)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Export remaining deps from lock file and install, skipping torch (already installed)
RUN uv export --frozen --no-dev --no-hashes -o /tmp/requirements.txt && \
    grep -v "^torch" /tmp/requirements.txt > /tmp/requirements_filtered.txt && \
    pip install --no-cache-dir -r /tmp/requirements_filtered.txt

COPY . .

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]
