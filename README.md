# LLM Zoomcamp

Personal repository for my classes and progress through the [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) course by DataTalks.Club. Contains my notes, experiments, and homework solutions for each module.

---

## Module 01 — Agentic RAG

→ See [01-agentic-rag/README.md](01-agentic-rag/README.md)

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

→ See [02-vector-search/README.md](02-vector-search/README.md)

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

## Module 04 — RAG Evaluation

**Video:** [4.13 LLM as a Judge](https://www.youtube.com/watch?v=BEXVULgalDM&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv&index=42)

**Notebook:** [04-evaluation/01-data-gen.ipynb](04-evaluation/01-data-gen.ipynb)

Runs inside the `general` service (http://localhost:8888) — the whole repo is mounted at `/app`.

### Progress

- [x] Filtered FAQ dataset to `llm-zoomcamp` course documents
- [x] Generated evaluation questions using structured LLM output (`client.beta.chat.completions.parse()` with Pydantic models)
- [x] Adapted `evaluation_utils.py` to use Groq-compatible Chat Completions API (instead of OpenAI Responses API)
- [x] Configured structured output with Groq models that support `json_schema` (`openai/gpt-oss-20b`)
- [x] Wired cost tracking via `calc_price()` using `prompt_tokens` / `completion_tokens`
- [x] `RAGWithUsage(RAGBase)` — RAG pipeline with per-call usage tracking and cumulative cost reporting

### Stack

| Component | Tool |
|-----------|------|
| LLM (structured output) | Groq — `openai/gpt-oss-20b` |
| Structured output format | `client.beta.chat.completions.parse()` + Pydantic |
| RAG pipeline | `RAGWithUsage(RAGBase)` with usage tracking |
| Notebook | JupyterLab via `general` service |

---

## Module 03 — Workflow Orchestration with Kestra

**Video:** [Generate Workflows using AI](https://www.youtube.com/watch?v=OTiOdt17hZg&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv&index=31)

### Progress

- [x] Added Kestra (`v1.3.21`) and its backing PostgreSQL to `docker-compose.yml`
- [x] Configured Kestra AI Copilot with Gemini (`gemini-2.0-flash`)
- [x] Configured credentials as env vars (`KESTRA_USERNAME`, `KESTRA_PASSWORD`, `GEMINI_API_KEY`)
- [x] Mounted `03-orchestration/flows/` into the container; flows imported via Kestra API
- [x] Ran AI Copilot vs ChatGPT comparison (Q1) — Copilot uses RAG over plugin docs
- [x] Ran RAG vs no-RAG flows (`1_chat_without_rag.yaml` / `2_chat_with_rag.yaml`) — Q2
- [x] Ran `4_simple_agent.yaml` for token usage analysis — Q3 & Q4

→ See [03-orchestration/03-homework/README.md](03-orchestration/03-homework/README.md)

### Stack

| Component | Tool |
|-----------|------|
| Orchestrator | Kestra `v1.3.21` |
| Kestra backend | PostgreSQL 18 |
| AI workflow generation | Gemini 2.0 Flash (via AI Copilot) |
| Flow agents | `io.kestra.plugin.ai.agent.AIAgent` |

---

## Module 05 — Monitoring

**Video:** [5.4 Capturing Metrics](https://www.youtube.com/watch?v=JGh6-DqaueA&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv&index=48) (at 4:17)

**App:** [05-monitoring/app.py](05-monitoring/app.py)

→ See [module-05 in docker-compose.yml](docker-compose.yml)

Own Compose service (`module-05`), built from the root `Dockerfile` — Streamlit UI at http://localhost:8501.

### Progress

- [x] Built a Streamlit chat UI (`app.py`) wrapping the RAG assistant
- [x] Reused the `RAGBase` / `ingest.py` pattern from earlier modules for the FAQ index and Groq-backed LLM (`assistant.py`, `rag_helper.py`)
- [x] Added `streamlit` to the shared root image and exposed port `8501` (`Dockerfile`)
- [x] Added dedicated `module-05` Compose service — mounts `05-monitoring/` and auto-starts `streamlit run app.py` on container start

### Stack

| Component | Tool |
|-----------|------|
| UI | `streamlit` |
| RAG pipeline | `RAGBase` (`rag_helper.py`) |
| LLM | Groq API |

---

## Running locally

This repo uses one Docker Compose service per module. Before starting, create a `.env` file with:

```
GROQ_API_KEY=...
OPENAI_API_KEY=...
SECRET_GEMINI_API_KEY=...   # Base64-encoded
SECRET_TAVILY_API_KEY=...   # Base64-encoded
SECRET_OPENAI_API_KEY=...   # Base64-encoded
```

> `SECRET_*` values must be Base64-encoded. Encode with:
> ```powershell
> [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your-key-here"))
> ```

```bash
# Module 01
docker compose up module-01 --build

# Module 02 — vector search
docker compose up module-02 --build

# Module 02 — homework (pgvector)
docker compose up pgvector module-02-homework --build

# Module 03 — Kestra
docker compose up kestra_postgres kestra

# Module 05 — monitoring (Streamlit)
docker compose up module-05 --build
```

| Service | URL |
|---------|-----|
| `general` | http://localhost:8888 |
| `module-01` | http://localhost:8889 |
| `module-02` | http://localhost:8890 |
| `module-02-homework` | http://localhost:8891 |
| `module-05` | http://localhost:8501 |
| `pgvector` (Postgres) | localhost:5432 |
| `kestra` | http://localhost:8080 |

> **Note:** `module-02-homework` uses a `uv`-managed virtualenv (`uv run jupyter`). Any new packages must be added via `uv add` in the Dockerfile and the image rebuilt — `uv pip install --system` won't be visible to the notebook kernel.
>
> On first use, run `from embed.download import download; download("Xenova/all-MiniLM-L6-v2")` inside the notebook to fetch the ONNX model files before importing `Embedder`.
>
> `module-05` auto-starts Streamlit on container start (`command: streamlit run app.py ...` in `docker-compose.yml`) — no manual launch needed. Rebuild/restart it with `make chat` from `05-monitoring/` (or run the underlying command directly if `make` isn't installed):
> ```bash
> docker-compose -f ../docker-compose.yml up -d --build module-05
> ```
