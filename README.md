# LLM Zoomcamp

Personal progress repository for the [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) course by DataTalks.Club.

---

## Module 01 — Agentic RAG

**Notebooks:** [module_01.ipynb](01-agentic-rag/module_01.ipynb) · [agents.ipynb](01-agentic-rag/agents.ipynb)

### Progress

**RAG Pipeline**
- [x] Fetched the DataTalks.Club FAQ dataset — 1 342 documents across multiple courses
- [x] Built a keyword search index with `minsearch` (boosting on `question` and `section` fields, filtering by course)
- [x] Wired up an LLM via Groq's OpenAI-compatible API (`llama-3.1-8b-instant`)
- [x] Engineered a prompt template separating `INSTRUCTIONS` from `USER_PROMPT_TEMPLATE`
- [x] Implemented helper functions: `search()`, `build_context()`, `build_prompt()`
- [x] Assembled the full RAG pipeline: `rag(question)` → search → prompt → LLM → answer
- [x] Refactored pipeline into `RAGBase` class (`rag_helper.py`)

**Agentic / Function Calling**
- [x] Defined a `search` tool in the OpenAI function-calling schema
- [x] Called `chat.completions.create` with tools using `llama-3.3-70b-versatile` on Groq
- [x] Parsed tool call response: `call.function.name` and `call.function.arguments`
- [x] Built multi-turn conversation loop: user → tool call → tool result → final answer

### Stack

| Component | Tool |
|-----------|------|
| Search | `minsearch` (in-memory keyword index) |
| LLM | Groq API — `llama-3.3-70b-versatile` |
| Notebook | JupyterLab (Dockerized) |
| Package manager | `uv` |

---

## Module 02 — Vector Search

**Notebook:** [vector_search.ipynb](02-vector-search/vector_search.ipynb)

### Progress

- [x] Loaded the `all-MiniLM-L6-v2` sentence-transformers model
- [x] Encoded queries and documents into 384-dim embeddings
- [x] Computed similarity between query/document pairs via dot product
- [x] Reused `ingest.py` from Module 01 (cross-module import via shared Docker volume mount)
- [x] Batch-encoded all 1 350 FAQ documents into embeddings (with `tqdm` progress tracking)
- [x] Built a vectorized similarity search with `numpy` — embedding matrix `X`, scores via `X.dot(query_vector)`
- [x] Retrieved top-5 most relevant documents using `np.argsort`
- [x] Extended to persistent vector search with `sqlitesearch.VectorSearchIndex` (IVF mode, on-disk `.db` file)
- [x] Implemented `RAGVector(RAGBase)` — overrides `search()` to embed the query and use vector index; reuses prompt/LLM pipeline from Module 01

### Stack

| Component | Tool |
|-----------|------|
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Similarity search | `numpy` (vectorized dot product) |
| Persistent vector index | `sqlitesearch` (`VectorSearchIndex`, IVF/HNSW/LSH) |
| Notebook | JupyterLab (Dockerized) |

---

## Module 02 — Homework (pgvector)

→ See [02-vector-search/02-homework/README.md](02-vector-search/02-homework/README.md)

---

## Running locally

This repo uses one Docker Compose service per module. Before starting, create a `.env` file with:

```
GROQ_API_KEY=...
OPENAI_API_KEY=...
```

```bash
# Module 01
docker compose up module-01 --build

# Module 02 — vector search
docker compose up module-02 --build

# Module 02 — homework (pgvector)
docker compose up pgvector module-02-homework --build
```

| Service | URL |
|---------|-----|
| `general` | http://localhost:8888 |
| `module-01` | http://localhost:8889 |
| `module-02` | http://localhost:8890 |
| `module-02-homework` | http://localhost:8891 |
| `pgvector` (Postgres) | localhost:5432 |

> **Note:** `module-02-homework` uses a `uv`-managed virtualenv (`uv run jupyter`). Any new packages must be added via `uv add` in the Dockerfile and the image rebuilt — `uv pip install --system` won't be visible to the notebook kernel.
>
> On first use, run `from embed.download import download; download("Xenova/all-MiniLM-L6-v2")` inside the notebook to fetch the ONNX model files before importing `Embedder`.
