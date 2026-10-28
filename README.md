# First match does not mean right match

This lab compares baseline vector retrieval, LLM relevance scoring, and a MiniLM cross-encoder over a Trustworthy AI podcast transcript and the supplied EU AI Act PDF.

The reviewer entry point is [lab_proof.md](lab_proof.md). It is an AI-assisted draft pending the author's review. The manual correctness assessments are explicitly pending rather than represented as completed work.

## Experiment files

| File | Contents |
|---|---|
| `relevance_scoring_rerankers.ipynb` | Source preparation, embeddings, Pinecone, both rerankers, metadata filters, LCEL RAG, and evaluation |
| `artifacts/experiment.json` | Full candidate pools, score components, answers, cited evidence, failure case, and timings |
| `artifacts/chunks.json` | All chunks with structural metadata and stable IDs |
| `artifacts/sources.json` | Source file sizes and SHA-256 hashes |
| `artifacts/comparison.csv` | Ranking changes, overlap, and timing observations |
| `manual_evaluation.csv` | Author assessment fields for all five queries and all three methods |
| `review_notes.md` | Analysis of observed grounding failures and trace checks |
| `data/` | Unmodified copies of the two supplied corpus files |
| `requirements.txt` | Direct dependencies |
| `requirements-lock.txt` | Exact dependency versions from the executed environment |

## Reproducibility

The experiment uses Python 3.12. Credentials are read from `.env`; `.env.example` contains only empty variable names. The notebook uses `text-embedding-3-small`, `gpt-4o-mini`, and `cross-encoder/ms-marco-MiniLM-L6-v2`. OpenAI provides embeddings, relevance scores, and generated answers. Pinecone stores source text and vectors; the cross-encoder runs locally. The first run downloads its model weights.

The dependency installation command is `python -m pip install -r requirements-lock.txt`. The notebook executes from the repository root with the selected Python environment. Source documents are in `data/`. Saved notebook outputs and artifacts preserve the observed run without additional API calls.

Stable IDs and corpus-specific namespaces prevent duplicate vectors. A basic namespace lacks structural metadata, while an enriched namespace supports article and section filters. The rebuild demonstration does not delete an existing index. The local `.cache/` contains embeddings and scoring responses and is excluded from version control.

## Interpretation

All rerankers operate on the same ten baseline candidates per query and retain five. Changes in rank, overlap, and latency are directly measured. Correctness, relevance, and semantic support require the author's manual assessment; valid citation IDs alone do not establish support. The PDF is a fixed 2024 source snapshot, not a current legal advisory service.

## Deliverable status

The executed notebook covers source loading, embeddings for all chunks, cosine retrieval, LLM scoring, a dedicated cross-encoder, source and article filters, LCEL RAG, and five-query comparisons. The draft proof includes one supported answer, exact evidence, a claim trace, comparison results, and observed failures. Manual correctness and grounding ratings and the author's final proof revision remain pending.
