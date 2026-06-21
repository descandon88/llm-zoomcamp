# LLM Zoomcamp

Personal progress repository for the [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) course by DataTalks.Club.

---

## Module 01 — Agentic RAG

**Currently watching:** [1.13 — Function Calling](https://www.youtube.com/watch?v=CeEki_0mdGo&list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv&index=15)

### Progress

**RAG Pipeline** — [module_01.ipynb](01-agentic-rag/module_01.ipynb)
- [x] Fetched the DataTalks.Club FAQ dataset — 1 342 documents across multiple courses
- [x] Built a keyword search index with `minsearch` (boosting on `question` and `section` fields, filtering by course)
- [x] Wired up an LLM via Groq's OpenAI-compatible API (`llama-3.1-8b-instant`)
- [x] Engineered a prompt template separating `INSTRUCTIONS` from `USER_PROMPT_TEMPLATE`
- [x] Implemented helper functions: `search()`, `build_context()`, `build_prompt()`
- [x] Assembled the full RAG pipeline: `rag(question)` → search → prompt → LLM → answer
- [x] Refactored pipeline into `RAGBase` class (`rag_helper.py`)

**Agentic / Function Calling** — [agents.ipynb](01-agentic-rag/agents.ipynb)
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

## Running locally

```bash
docker compose up --build
```

Open [http://localhost:8888](http://localhost:8888).

> Dependencies are declared in [01-agentic-rag/pyproject.toml](01-agentic-rag/pyproject.toml).  
> Copy `.env.example` to `.env` and set `GROQ_API_KEY` before starting.
