# Module 02 — Homework (pgvector)

**Notebook:** [02-homework.ipynb](02-homework.ipynb)

## Progress

**Infrastructure**
- [x] Spun up a PostgreSQL + pgvector container (`pgvector/pgvector:pg17`) via Docker Compose
- [x] Connected with `psycopg` v3 (`autocommit=True` to avoid aborted-transaction errors across notebook cells)
- [x] Enabled `CREATE EXTENSION IF NOT EXISTS vector` and created a `documents` table with a `vector` column
- [x] Built HNSW index with `vector_cosine_ops` for approximate nearest-neighbor search
- [x] Replaced `sentence-transformers` with a lightweight ONNX-based `Embedder` (no PyTorch dependency) — `onnxruntime` + `tokenizers` + mean pooling + L2 normalisation
- [x] Downloaded `Xenova/all-MiniLM-L6-v2` ONNX model files via `embed/download.py`

**Q1 — Embedding a query**
- [x] Embedded `"How does approximate nearest neighbor search work?"` → 384-dim unit vector; `v[0] = -0.0206`

**Q2 — Cosine similarity**
- [x] Fetched lesson `07-sqlitesearch-vector.md` from GitHub via `gitsource.GithubRepositoryDataReader` (pinned commit `8c1834d`)
- [x] Embedded document content and computed cosine similarity with Q1 query → **0.3611**

**Q3 — Chunking and search by hand**
- [x] Fetched all `02-vector-search/lessons/` markdown files (9 docs)
- [x] Chunked with `gitsource.chunk_documents(size=2000, step=1000)` → 40 overlapping chunks
- [x] Text format per chunk: `f"{doc['start']} {doc['content']} {doc['filename']}"`
- [x] Batch-embedded all 40 chunks; searched with `X.dot(query_vector)` + `np.argsort`
- [x] Top score improved to **0.6312** (vs 0.3611 on full doc) — chunking concentrates meaning, improving retrieval

**Q4 — Vector search with minsearch**
- [x] Fetched entire repo markdown (all paths containing `/`), chunked → ~600 chunks across 12 batches
- [x] Built `minsearch.VectorSearch` index fitted on chunk embeddings
- [x] Queried `"What metric do we use to evaluate a search engine?"` → top result: `04-evaluation/lessons/05-search-metrics.md` (Hit Rate & MRR lesson)

## Stack

| Component | Tool |
|-----------|------|
| Embeddings | `onnxruntime` + `tokenizers` (ONNX export of `all-MiniLM-L6-v2`) |
| Vector database | PostgreSQL + `pgvector` extension |
| DB driver | `psycopg` v3 |
| Data source | `gitsource` (GitHub repo reader, pinned commit) |
| Notebook | JupyterLab (Dockerized, `uv`-managed venv) |

## Running locally

```bash
docker compose up pgvector module-02-homework --build
```

Open [http://localhost:8891](http://localhost:8891).

> **Note:** packages must be added via `uv add` in the Dockerfile and the image rebuilt — `uv pip install --system` is not visible to the `uv run jupyter` kernel.
>
> On first use, run inside the notebook to download the ONNX model:
> ```python
> from embed.download import download
> download("Xenova/all-MiniLM-L6-v2")
> ```