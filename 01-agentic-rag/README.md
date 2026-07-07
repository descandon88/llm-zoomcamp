# Module 01 — Agentic RAG

**Notebooks:** [module_01.ipynb](module_01.ipynb) · [agents.ipynb](agents.ipynb) · [persinsent_rag.ipynb](persinsent_rag.ipynb) · [sqlite-ingest.ipynb](sqlite-ingest.ipynb)

**Homework:** [01-homework/01-homework.ipynb](01-homework/01-homework.ipynb)

---

## What this module is about

This module covers the fundamentals of **Retrieval-Augmented Generation (RAG)** and extends the concept into **agentic / function-calling** pipelines. The core idea is that an LLM alone doesn't know the answers to course-specific questions, but if you retrieve relevant documents first and inject them into the prompt, the LLM can answer accurately.

The "agentic" part goes one step further: instead of always retrieving documents, you give the model a `search` tool and let it decide *when* and *what* to search for. The model calls the tool, gets results, and keeps looping until it has enough information to answer.

---

## Topics covered

### 1. The FAQ Dataset

The DataTalks.Club FAQ is fetched at runtime from their public API — 1 342 documents across multiple courses (llm-zoomcamp, data-engineering-zoomcamp, mlops-zoomcamp, etc.). Each document has `course`, `section`, `question`, and `answer` fields.

```python
import requests
docs_url = "https://datatalks.club/faq/json/courses.json"
```

The `ingest.py` module encapsulates the fetch logic (`load_faq_data`) and index creation (`build_index`).

### 2. Keyword Search with `minsearch`

`minsearch` is a lightweight in-memory search library. You define which fields to search (text) and which to filter (keyword), then call `index.fit(documents)`.

Key concepts:
- **`boost_dict`** — weights per field (e.g., `{'question': 3.0, 'section': 0.5}` — question matches rank higher)
- **`filter_dict`** — hard filters (e.g., `{'course': 'llm-zoomcamp'}` — only return results from this course)
- **`num_results`** — how many documents to retrieve

### 3. LLM via Groq (OpenAI-compatible API)

The Groq API is used with the OpenAI Python client by pointing `base_url` at `https://api.groq.com/openai/v1`. This means the same `chat.completions.create` call works for both OpenAI and Groq.

```python
openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
```

Models used: `llama-3.1-8b-instant` (fast, cheap) and `llama-3.3-70b-versatile` (better for function calling).

### 4. Prompt Engineering

The prompt is split into two parts:
- **`INSTRUCTIONS`** — system-level context telling the model its role and constraints
- **`USER_PROMPT_TEMPLATE`** — per-query template combining the user's question with the retrieved context

The `build_context()` function formats search results as `Section / Q: ... / A: ...` blocks so the model can read them clearly.

### 5. Full RAG Pipeline

```
user question
    → search(question)         # keyword search → top-5 docs
    → build_context(results)   # format docs into a readable block
    → build_prompt(q, context) # fill the prompt template
    → llm(prompt)              # call the model
    → answer
```

### 6. `RAGBase` Class (`rag_helper.py`)

The pipeline is refactored into a reusable class stored in `rag_helper.py` (shared across modules via Docker volume mount). Key methods:

| Method | What it does |
|--------|--------------|
| `search(query)` | Keyword search with boost/filter |
| `build_context(results)` | Format docs as text block |
| `build_prompt(query, results)` | Fill prompt template |
| `llm(prompt)` | Call the model |
| `rag(query)` | Run the full pipeline end-to-end |

### 7. Function Calling (Agentic Loop)

The model is given a `search` tool described in the OpenAI function-calling schema. Instead of always searching, the model decides whether it needs to search and with what query.

```python
search_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search the FAQ database...",
        "parameters": { ... }
    }
}
```

The loop works like this:

1. Send user message + tool definition to the model
2. If the model returns a tool call → parse `call.function.name` and `call.function.arguments`
3. Execute the tool and append the result to `messages`
4. Send the extended conversation back to the model
5. Repeat until the model returns a plain text answer (no tool calls)

This is the core **agentic loop** pattern. The model keeps calling tools until it decides it has enough information.

### 8. Persistent RAG with SQLite (`sqlite-ingest.ipynb`)

An alternative to in-memory search using SQLite to store and query documents across notebook restarts.

---

## Homework — Module 01

**Notebook:** [01-homework/01-homework.ipynb](01-homework/01-homework.ipynb)

The homework applies the module concepts to a different data source: the **lesson markdown files** from the LLM Zoomcamp GitHub repo, fetched via `gitsource.GithubRepositoryDataReader`.

| Question | Task | Answer |
|----------|------|--------|
| Q2 | Keyword search on lesson content → find which lesson answers "How does the agentic loop keep calling the model until it stops?" | `01-agentic-rag/lessons/14-agentic-loop.md` |
| Q3 | Build RAG with `RAGBase`, count tokens | prompt: 7 221 · completion: 381 · total: **7 602** |
| Q4 | Chunk documents (`size=2000, step=1000`), rebuild RAG → how much do tokens drop? | chunked total: **2 540** (~3× fewer tokens vs full-doc RAG) |
| Q5 | Search the chunked index for a different query | Top result: `01-agentic-rag/lessons/15-frameworks.md` |

**Key insight from Q4:** Chunking concentrates relevant text into smaller units, so the prompt context is tighter and token usage drops significantly — without sacrificing answer quality.

---

## Stack

| Component | Tool |
|-----------|------|
| Keyword search | `minsearch` (in-memory BM25-like index) |
| LLM | Groq API — `llama-3.1-8b-instant` / `llama-3.3-70b-versatile` |
| Function calling | OpenAI tool-use format (works on Groq) |
| Data source | DataTalks.Club FAQ API + `gitsource` (homework) |
| Notebook | JupyterLab (Dockerized) |
| Package manager | `uv` |

---

## Running locally

```bash
docker compose up module-01 --build
```

Open [http://localhost:8889](http://localhost:8889).

The container mounts `rag_helper.py` and `ingest.py` at `/app` so changes to those files are reflected immediately without rebuilding.