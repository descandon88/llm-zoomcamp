# Module 03 — Homework (Kestra Orchestration)

**Notebook/Flows path:** [03-orchestration/03-homework/](.)

---

## Importing Flows into Kestra

To import a flow YAML file into Kestra via the API:

```bash
curl -X POST -u ${KESTRA_USERNAME}:${KESTRA_PASSWORD} \
  http://localhost:8080/api/v1/flows/import \
  -F fileUpload=@flows/4_simple_agent.yaml
```

Replace `flows/4_simple_agent.yaml` with the path to any flow file you want to import.

---

## Question 1 — Context Engineering

**Prompt used:** *"Create a Kestra flow that loads NYC taxi data from CSV to BigQuery"*

The same prompt was submitted to ChatGPT and to Kestra's AI Copilot to compare the quality of the generated flows.

### Answer

> **AI Copilot has access to current Kestra plugin documentation**

AI Copilot is backed by RAG — it retrieves up-to-date plugin schemas and examples before generating the YAML. ChatGPT only has its training data, so it may use outdated or hallucinated plugin names/properties.

---

### AI Copilot result — [01-ai-copilot-result.yaml](01-ai-copilot-result.yaml)

```yaml
id: magpie_131966
namespace: company.team

tasks:
  - id: load_nyc_taxi_data
    type: io.kestra.plugin.gcp.bigquery.LoadFromGcs
    from:
      - gs://kestra-samples/nyc-taxi-data/yellow_tripdata_2023-01.csv
    destinationTable: kestra_project.nyc_taxi_dataset.yellow_tripdata
    format: CSV
    autodetect: true
    csvOptions:
      allowJaggedRows: true
      encoding: UTF-8
      fieldDelimiter: ","
  - id: load_success
    type: io.kestra.plugin.core.log.Log
    message: "NYC taxi data loaded to BigQuery table '{{ outputs.load_nyc_taxi_data.destinationTable }}' successfully!"
```

Compact, uses the correct `LoadFromGcs` plugin with real property names, and references the output in a log message.

---

### ChatGPT result — [01-chatgpt-result.yaml](01-chatgpt-result.yaml)

```yaml
id: nyc_taxi_csv_to_bigquery
namespace: company.team

variables:
  projectId: your-gcp-project
  dataset: ny_taxi
  table: yellow_tripdata_2024_01
  location: US
  csvUrl: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2024-01.csv.gz

tasks:
  - id: download_csv
    type: io.kestra.plugin.core.http.Download
    uri: "{{ vars.csvUrl }}"

  - id: create_dataset
    type: io.kestra.plugin.gcp.bigquery.Query
    projectId: "{{ vars.projectId }}"
    serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
    sql: |
      CREATE SCHEMA IF NOT EXISTS `{{ vars.projectId }}.{{ vars.dataset }}`
      OPTIONS(location="{{ vars.location }}");

  - id: load_csv
    type: io.kestra.plugin.gcp.bigquery.LoadFromGcs
    projectId: "{{ vars.projectId }}"
    serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
    from:
      - "{{ outputs.download_csv.uri }}"
    destinationTable: "{{ vars.projectId }}.{{ vars.dataset }}.{{ vars.table }}"
    format: CSV
    csvOptions:
      skipLeadingRows: 1
      autodetect: true
      fieldDelimiter: ","
      allowQuotedNewLines: true
      quote: "\""
    writeDisposition: WRITE_TRUNCATE
```

More verbose and adds extra steps (download + create dataset), but plugin property names may not match the current Kestra version exactly.

---

## Question 2 — RAG vs No RAG

**Task:** Run `1_chat_without_rag.yaml` and `2_chat_with_rag.yaml` in the Kestra UI and compare the responses about Kestra 1.1 features.

### Answer

> **Vague, generic, or fabricated — the model guesses from training data**

---

### Without RAG — `1_chat_without_rag.yaml`

The model invents plausible-sounding features (Worker Groups, API Key Auth, Local Dev Server) that were **not** introduced in Kestra 1.1. The response is confident but inaccurate — classic hallucination from stale training data.

> *"Did you notice that this response seems to be: Incorrect? Vague/generic? Listing features that haven't been added in exactly this version but rather a long time ago?"*

---

### With RAG — `2_chat_with_rag.yaml`

The model retrieves the actual Kestra 1.1 release documentation before answering, producing accurate, grounded results:

1. **New Filters** — UI filters redesigned with save/reset and column customization
2. **No-Code Dashboard Editor** — build dashboards without YAML via a form-based UI
3. **Multi-Agent AI Systems** — AI agents can delegate to other AI agents as tools
4. **Fix with AI** — AI-powered suggestions when task runs fail
5. **Human Task** *(Enterprise)* — pause executions until a human manually approves

> *"Note that this response is detailed, accurate, and grounded in the actual release documentation."*

---

## Key takeaway

| | Without RAG | With RAG |
|---|---|---|
| Source | Model training data (stale) | Retrieved release docs (current) |
| Accuracy | Hallucinated / generic | Grounded and accurate |
| Kestra version awareness | None | Exact version match |

Context matters. The same LLM gives completely different quality answers depending on whether it has access to real documentation at query time.

---

## Model Configuration

**Gemini model used:** `gemini-3.1-flash-lite`

---

## Question 3 — Token Usage (Short Summary)

**Task:** Run `4_simple_agent.yaml` with `summary_length = short` (leave other inputs as defaults).

**Question:** What is the approximate output token count usage logged by the `log_token_usage` task?

### Answer

> **Short summary uses ~55 output tokens (60-100 range)**

**Token Usage Summary (short):**
```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 55
- Total tokens: 337

English Brevity Agent:
- Input tokens: 70
- Output tokens: 38
- Total tokens: 108
```

The multilingual agent output for a short summary is approximately **60-100 tokens**.

## Question 4 — Token Usage (Long Summary)

**Task:** Run `4_simple_agent.yaml` again with `summary_length = long`.

**Question:** Compare the multilingual agent output token count to Question 3. Roughly how many times more output tokens does the long summary use?

### Answer

> **Long summary uses ~2.9x more output tokens than short (2-5x range)**

**Token Usage Summary (long):**
```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 160
- Total tokens: 442

English Brevity Agent:
- Input tokens: 175
- Output tokens: 35
- Total tokens: 210
```

**Comparison to Question 3:**
- Short summary (Q3): 55 output tokens
- Long summary (Q4): 160 output tokens
- Ratio: 160 ÷ 55 = **~2.9x more tokens**

The long summary uses approximately **2-5x more output tokens** than the short summary, demonstrating how prompt length and output length constraints directly impact token usage and costs.

---

## Key Takeaway (Questions 3 & 4)

| | Short Summary | Long Summary |
|---|---|---|
| Multilingual agent output tokens | 55 | 160 |
| Ratio | 1x (baseline) | ~2.9x |
| Cost implication | Lower | Higher |

**Token usage scales with output constraints.** When you increase summary length requirements, output tokens grow significantly. This is crucial for cost planning when running agentic workflows at scale — longer outputs directly translate to higher API costs and latency.


---

## Question 5 — Impact of Output Constraints (3 Sentences)

**Task:** 
1. Open `4_simple_agent.yaml` in the Kestra flow editor
2. Find the `english_brevity` task and change its prompt from asking for **exactly 1 sentence** to **exactly 3 sentences**
3. Save the flow and run it with `summary_length = long`

**Question:** Compare the `english_brevity` output token count to the original 1-sentence version (also with `summary_length = long`). How do they compare?

### Answer

> **3 sentences uses ~2x more tokens than 1 sentence, despite similar total compression ratios**

**Token Usage Comparison (summary_length = long):**

**Original (1 sentence):**
```
English Brevity Agent:
- Input tokens: 175
- Output tokens: 35
- Total tokens: 210
```

**Modified (3 sentences):**
```
English Brevity Agent:
- Input tokens: 178
- Output tokens: 76
- Total tokens: 254
```

**Analysis:**
- 1 sentence: 35 output tokens
- 3 sentences: 76 output tokens
- Increase: 76 ÷ 35 = **~2.17x more tokens**
- Token increase: ~20% overhead (178 vs 175 input tokens)

The 3-sentence constraint produces **approximately 2x more output tokens** than the 1-sentence constraint. The output length requirement (not input length) is the primary driver of token usage — forcing the model to generate longer outputs dramatically increases costs.

---

## Question 6 — Best Practices for Production Workflows

**Question:** Based on what you learned in this module, for production workflows requiring deterministic, repeatable results with strict compliance requirements (e.g., financial reporting, workflows in highly regulated industries), which approach is most appropriate?

### Answer

> **Use traditional task-based workflows for predictability and auditability**

**Reasoning:**

For compliance-heavy, deterministic workflows:

1. **Predictability** — Traditional task-based workflows have explicit, deterministic logic. Each task produces the same output given the same input. AI-assisted or agentic flows introduce non-determinism (LLM outputs vary), which is problematic for regulated environments.

2. **Auditability** — Task-based workflows have clear audit trails: explicit task definitions, inputs, outputs, and execution logs. Compliance audits require traceability.

3. **Reproducibility** — Financial reporting and regulatory workflows must be reproducible. AI flows depend on model versions, temperature settings, and randomness — making reproducibility challenging.

4. **When AI is appropriate** — Use AI agents for:
   - Exploratory/flexible workflows (content generation, summarization, creative tasks)
   - Where non-determinism is acceptable
   - Non-critical, non-regulated processes

**Key Insight:** Kestra's strength is letting you choose the right tool — AI-assisted flows for innovation, traditional tasks for compliance. Know your requirements first.

---

## Module Summary

| Question | Focus | Key Learning |
|----------|-------|--------------|
| Q1 | AI Copilot vs ChatGPT | RAG enables accurate, up-to-date generation |
| Q2 | RAG impact on accuracy | Context access transforms hallucination into grounded answers |
| Q3-Q5 | Token usage scaling | Output constraints directly drive costs; 2-3x increases are typical |
| Q6 | Production readiness | Choose determinism for compliance, flexibility for innovation |

**Overall:** Token usage scales with output requirements, and workflow choice depends on compliance/auditability needs vs innovation/flexibility goals.
