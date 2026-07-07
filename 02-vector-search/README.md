# Module 02 — Vector Search

**Notebooks:** [vector_search.ipynb](vector_search.ipynb) · [vector_search_persistant.ipynb](vector_search_persistant.ipynb) · [vector_search_pgvector.ipynb](vector_search_pgvector.ipynb)

**Homework:** [02-homework/](02-homework/) → see [02-homework/README.md](02-homework/README.md)

---

## What this module is about

This module introduces **dense vector search** as an alternative to keyword search. Instead of matching words, you convert text into numerical vectors (embeddings) where semantically similar sentences are geometrically close. Searching becomes a nearest-neighbor problem in vector space.

The pipeline from Module 01 is reused, but the `search()` step is replaced with a vector-based lookup — everything else (prompt, LLM, RAG loop) stays the same.

---

## Topics covered

### 1. Embeddings with `sentence-transformers`

The `all-MiniLM-L6-v2` model converts text into 384-dimensional float vectors. Sentences with similar meaning produce vectors that point in similar directions.

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

v = model.encode("Can I still join the course?")
v.shape  # (384,)
```

The model returns **L2-normalized** vectors, which means each vector has length 1. This is important because it turns cosine similarity into a simple dot product.

### 2. Cosine Similarity via Dot Product

For two normalized vectors `a` and `b`:

```
cosine_similarity(a, b) = a · b
```

Because both vectors are unit length, the dot product gives the cosine directly — no division needed.

```python
v1 = model.encode("Can I join after the start date?")
dv = model.encode("Yes, you can still register...")

similarity = v1.dot(dv)  # e.g. 0.3233
```

A score near 1.0 means very similar; near 0 means unrelated; negative means opposite meaning.

### 3. Batch Encoding All Documents

Encoding 1 350 documents one by one is slow. `sentence-transformers` accepts batches:

```python
import numpy as np
from tqdm.auto import tqdm

vectors = []
for i in tqdm(range(0, len(texts), 50)):
    batch = texts[i:i + 50]
    vectors.extend(model.encode(batch))

X = np.array(vectors)  # shape: (1350, 384)
```

### 4. Vectorized Search with NumPy

Once all documents are in a matrix `X`, finding the closest document to a query vector `v` is a single matrix multiply:

```python
scores = X.dot(v)          # shape: (1350,) — one score per doc
top5 = np.argsort(scores)[-5:][::-1]
```

This is fast because NumPy runs the dot product in optimized BLAS routines. No loops needed.

### 5. Vector Search with `minsearch.VectorSearch`

`minsearch` also provides an in-memory vector index with keyword filtering support:

```python
from minsearch import VectorSearch

vindex = VectorSearch(keyword_fields=['course'])
vindex.fit(X, documents)

results = vindex.search(
    query_vector,
    num_results=5,
    filter_dict={'course': 'llm-zoomcamp'}
)
```

This combines approximate nearest-neighbor search with hard filters — useful when you want semantic similarity but only within a specific subset of documents.

### 6. Persistent Vector Index with `sqlitesearch` (`vector_search_persistant.ipynb`)

`sqlitesearch.VectorSearchIndex` stores the vectors on disk in a SQLite file, so the index survives notebook restarts:

```python
from sqlitesearch import VectorSearchIndex

vs_index = VectorSearchIndex(
    keyword_fields=['course'],
    mode='ivf',        # Inverted File Index — approximate, fast
    db_path='faq_vectors2.db'
)
vs_index.fit(vectors, documents)
```

Supported index modes: `ivf` (fast approximate), `hnsw` (high quality approximate), `lsh` (locality-sensitive hashing).

### 7. Vector Search with pgvector (`vector_search_pgvector.ipynb`)

An alternative persistent backend using **PostgreSQL + pgvector extension**. Documents and embeddings are stored in a `vector` column, and search is done via SQL operators:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);

CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

SELECT * FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

The `<=>` operator is cosine distance. pgvector's HNSW index makes this fast even with millions of rows.

### 8. `RAGVector` — Plugging Vectors into the RAG Pipeline

`RAGVector` extends `RAGBase` from Module 01, overriding only the `search()` method:

```python
class RAGVector(RAGBase):

    def __init__(self, embedder, **kwargs):
        super().__init__(**kwargs)
        self.embedder = embedder

    def search(self, query, num_results=5):
        query_vector = self.embedder.encode(query)
        filter_dict = {'course': self.course}
        return self.index.search(query_vector, num_results=num_results, filter_dict=filter_dict)
```

Everything else — `build_context`, `build_prompt`, `llm`, `rag` — is inherited unchanged. This is the power of the class hierarchy: swapping the retrieval backend requires changing exactly one method.

---

## Keyword Search vs Vector Search

| | Keyword (`minsearch`) | Vector (`sentence-transformers`) |
|---|---|---|
| Matching | Exact word overlap + TF-IDF weighting | Semantic meaning (even if words differ) |
| Speed | Very fast | Slower (encoding cost) |
| Handles synonyms | No | Yes |
| Handles typos | Partially | Yes (to a degree) |
| Needs embeddings | No | Yes |

Example: the query `"I just found out about the program, can I still enroll?"` matches documents about joining even though the word "enroll" doesn't appear in them — vector search finds the semantic match.

---

## Stack

| Component | Tool |
|-----------|------|
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`, 384-dim) |
| In-memory vector search | `numpy` dot product + `minsearch.VectorSearch` |
| Persistent vector index | `sqlitesearch` (IVF/HNSW/LSH) |
| PostgreSQL vector search | `pgvector` extension + HNSW index |
| LLM | Groq API — `llama-3.1-8b-instant` |
| Notebook | JupyterLab (Dockerized) |
| Package manager | `uv` |

---

## Running locally

```bash
# Module 02 — vector search notebooks
docker compose up module-02 --build

# Module 02 — homework (pgvector + ONNX embedder)
docker compose up pgvector module-02-homework --build
```

| Notebook | URL |
|----------|-----|
| `module-02` | [http://localhost:8890](http://localhost:8890) |
| `module-02-homework` | [http://localhost:8891](http://localhost:8891) |