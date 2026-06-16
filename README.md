# LLM Zoomcamp

Personal progress repository for the [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) course by DataTalks.Club.

---

## Module 01 — Agentic RAG

**Notebook:** [01-agentic-rag/module_01.ipynb](01-agentic-rag/module_01.ipynb)  
**Currently watching:** [1.8 — RAG Helper](https://www.youtube.com/watch?v=JxaC6Hrym6c&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv&index=10)

### Progress

- [x] Fetched the DataTalks.Club FAQ dataset — 1 342 documents across multiple courses
- [x] Built a keyword search index with `minsearch` (boosting on `question` and `section` fields, filtering by course)
- [x] Wired up an LLM via Groq's OpenAI-compatible API (`llama-3.1-8b-instant`)
- [x] Engineered a prompt template separating `INSTRUCTIONS` from `USER_PROMPT_TEMPLATE`
- [x] Implemented helper functions: `search()`, `build_context()`, `build_prompt()`
- [x] Assembled the full RAG pipeline: `rag(question)` → search → prompt → LLM → answer

### Stack

| Component | Tool |
|-----------|------|
| Search | `minsearch` (in-memory keyword index) |
| LLM | Groq API — `llama-3.1-8b-instant` |
| Notebook | JupyterLab (Dockerized) |
| Package manager | `uv` |

---

## Running locally

```bash
docker compose up --build
```

Open [http://localhost:8888](http://localhost:8888).

> Dependencies are declared in [01-agentic-rag/pyproject.toml](01-agentic-rag/pyproject.toml).  
> Copy `.env.example` to `.env` and set `GROQ_API_KEY` before starting.
