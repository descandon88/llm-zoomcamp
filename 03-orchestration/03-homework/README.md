# Module 03 — Homework (Kestra Orchestration)

**Notebook/Flows path:** [03-orchestration/03-homework/](.)

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