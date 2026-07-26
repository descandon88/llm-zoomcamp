# Homework 5 — Monitoring (OpenTelemetry tracing)
## Q1. 1. How many spans does the trace produce?

## Q2. Capturing metrics as span attributes

**Question:** How many input tokens do we see for the LLM call?

Evidence — the `llm` span, with `input_tokens`/`output_tokens` set via `span.set_attribute(...)`:

```json
{
    "name": "llm",
    "attributes": {
        "input_tokens": 1229,
        "output_tokens": 215
    },
    "start_time": "2026-07-25T22:47:47.784496Z",
    "end_time": "2026-07-25T22:47:48.852073Z"
}
```

**Answer: 1229 input tokens.**

---

## Q3. Span timing

**Question:** For a typical query, roughly how long does the LLM call take?

```
Total spans: 3
  search: 5.73 ms
  llm: 2729.37 ms
  rag: 2842.29 ms
```

**Answer:** Roughly **1.5–2.8 seconds** (varies run to run). The `llm` span dominates the trace — it's the network round-trip to Groq plus model inference — while `search` (in-memory keyword lookup via `minsearch`) takes only a few milliseconds. `rag` (the parent span) is essentially `search + llm` combined.

---

## Q4/Q5. Saving traces to SQLite

**Question:** Which span names appear in the `spans` table?

```powershell
docker exec llm-zoomcamp-hw5 python -c "import sqlite3; conn = sqlite3.connect('/app/traces.db'); [print(row) for row in conn.execute('SELECT * FROM spans')]"
```

```
('search', 1785021293793050377, 1785021293798781493, None, None, None)
('llm',    1785021293862077758, 1785021296591444468, 1229, 145, None)
('rag',    1785021293792976579, 1785021296635265911, None, None, None)
```

**Answer:** `search`, `llm`, `rag` — one row per span, persisted by the custom `SQLiteSpanExporter` instead of only printing to the console. Only the `llm` row has `input_tokens`/`output_tokens` populated, since that's the only span with those attributes set.

---

## Q6. Token stability

**Question:** How much do the input tokens vary across 4 runs of the same query?

```powershell
docker exec -e PYTHONPATH=/app llm-zoomcamp-hw5 python llm-zoomcamp-hw5/q6_tokenStability.py
```

```
(1229,)
(1229,)
(1229,)
(1229,)
(1229,)
(1229,)
(1229,)
(1229,)
(1229,)
```

**Answer:** They **don't vary at all** — every run produces exactly 1229 input tokens. Input tokens are fully deterministic here: the query string is hardcoded, `search()` uses `minsearch`'s keyword index (deterministic ranking for a given query), and the system `instructions` never change. Since the exact same prompt gets tokenized every time, `input_tokens` is identical run to run. (By contrast, `output_tokens` *does* vary between runs — e.g. 104, 131, 145, 166, 199, 215 seen across different executions — because the LLM's generation isn't deterministic even given identical input.)
