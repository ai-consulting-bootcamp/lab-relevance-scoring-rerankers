# Lab Proof: First match ≠ right match
Relevance scoring and rerankers for Trustworthy AI & the EU AI Act

## 1. What I built
A small RAG pipeline over two sources, with a baseline and a reranked path, metadata filtering, and a manual evaluation.

| Part | Choice |
|---|---|
| Sources | `podcast.txt` (deep dive on the 2019 Ethics Guidelines for Trustworthy AI) and `eu_ai_act.pdf` (Regulation (EU) 2024/1689, 144 pages) |
| Chunking | `RecursiveCharacterTextSplitter`, 1000 characters, 150 overlap |
| Metadata | `source` (podcast / eu_ai_act), `section` (recitals p.1–43 / articles p.44–123 / annexes p.124–144 / trustworthy_ai_guidelines), `page`, `article` (number), `title` |
| Article detection | regex `^Ar\s?ticle\s+(\d+)\s*$` on whole lines; text collected per article, then chunked (every chunk keeps its article metadata) |
| Result | 794 chunks: articles 407, recitals 308, annexes 60, podcast 19 |
| Vector store | Chroma + OpenAI `text-embedding-3-small` |
| Reranker | Cohere `rerank-v3.5`: top 20 from vector search → reranked → top 5 |
| Filtering | Chroma `filter={"source": ...}` / `{"section": ...}` |
| Generation | `gpt-4o-mini`, temperature 0, answer ONLY from numbered sources, cite [n], honest exit "The retrieved sources do not answer this." |

```python
def rerank_search(query, k_initial=20, top_n=5):
    candidates = vectorstore.similarity_search(query, k=k_initial)
    reranked = reranker.compress_documents(candidates, query)
    return [(d, d.metadata["relevance_score"]) for d in reranked[:top_n]]

def filtered_rerank(query, where, k_initial=20, top_n=5):
    candidates = vectorstore.similarity_search(query, k=k_initial, filter=where)
    reranked = reranker.compress_documents(candidates, query)
    return [(d, d.metadata["relevance_score"]) for d in reranked[:top_n]]
```

Test questions with an answer key (written before running):

| # | Question | Expected source |
|---|---|---|
| Q1 | Which AI practices are prohibited? | EU AI Act, Article 5 |
| Q2 | What does human in the loop mean? | Podcast (HITL / HOTL / HIC) |
| Q3 | Must a chatbot tell users that it is an AI? | EU AI Act, Article 50 |
| Q4 | When do the rules of the AI Act start to apply? | EU AI Act, Article 113 |

## 2. Query
Main trace: **Q4 "When do the rules of the AI Act start to apply?"**, the case where the first match was not the right match.

## 3. Retrieved evidence
**Retrieval: baseline vs. reranked (top 5)**

| Query | Baseline (vector) | Reranked (Cohere) |
|---|---|---|
| Q1 | Art.5 (0.664), Art.4 *AI literacy* (0.586), recitals p.9, p.8, p.12 | Art.5 (**0.948**), recitals p.9, p.12, p.9, p.8 |
| Q2 | podcast 0.287, 0.168, recitals p.21 0.145, podcast 0.134, 0.122 | podcast **0.776, 0.725**, 0.454, 0.094, recitals p.21 **0.038** |
| Q3 | podcast, podcast, recitals p.34, **Art.50 (#4)**, podcast | podcast, podcast, podcast, recitals p.8, podcast: **Art.50 gone** |
| Q4 | Art.5, Art.106, Art.50, Art.111, Art.103 | Art.110, Art.105, Art.111, Art.106: **no Art.113** |

**Q4 diagnosis**
- Art. 113 exists in the store as one chunk and contains the answer: *"This Regulation shall enter into force on the twentieth day following that of its publication… It shall apply from 2 August 2026. However: (a) Chapters I and II shall apply from 2 February 2025; (b) … from 2 August 2025; (c) Article 6(1) … from 2 August 2027."*
- Rank of Art. 113 for Q4 (articles only): **not in the top 200** of 407 article chunks.
- Direct cosine similarity: Art. 113 **0.392** vs. top hit Art. 5 **0.573**.
- Winners instead: Art. 105, 106, 103 (amendments whose chunks are mostly citations and page footers) and Art. 111 (transition rules that *mention* dates and Art. 113).

**Fix attempts (measured)**

| Fix | Q4: Art. 113 rank | Q3: Art. 50 rank |
|---|---|---|
| v1 raw store, filtered | not in top 200 | rank 2 (0.286) |
| + metadata filter + rerank | not in candidates | #5 (0.116), deepfake paragraph, not §1 |
| Reworded query ("enter into force and apply") | not found | – |
| v2 store: 407 footer lines and signature block removed, article title added to every chunk | **not in top 200** | **rank 8 (0.240), worse** |

## 4. Final output (Q4)
**Baseline** (sources: Art.111, Art.5, Art.111, Art.50, Art.5):
> The rules of the AI Act start to apply to operators of high-risk AI systems that have been placed on the market or put into service before 2 August 2026, only if those systems undergo significant changes in their designs after that date. Additionally, providers of general-purpose AI models that have been placed on the market before 2 August 2025 must comply with the obligations of the Regulation by 2 August 2027 [1].

**Reranked** (sources: Art.111, Art.110, Art.111, Art.108, recitals p.6):
> … same as above … Furthermore, AI systems which are components of large-scale IT systems established by certain legal acts and placed on the market before 2 August 2027 must be brought into compliance by 31 December 2030 [1][3].

**Correct answer (Art. 113):** entry into force 20 days after publication; general application from **2 August 2026**; prohibitions (Chapters I–II) from 2 February 2025; GPAI and governance rules from 2 August 2025; Art. 6(1) from 2 August 2027.

**Trace:** every sentence is backed by Art. 111, so the answer is *faithful to its sources*. But Art. 111 regulates transition for systems **already on the market**; it does not answer when the Act applies. The model never used the honest exit.

## 5. Manual evaluation (Step 7, v2 store, no filter)
| Q | Baseline answer | Reranked answer |
|---|---|---|
| Q1 | ⚠️ 7 of 8 Art. 5 practices, all cited; **misses real-time remote biometric identification** | ⚠️ 7 of 8, all cited; **misses social scoring** |
| Q2 | ✅ Correct, from the podcast (approve every action, tightest control, automation bias) | ✅ Correct, same content; one small addition ("human oversight is integral") |
| Q3 | ⚠️ "Yes", but cites only the **podcast** (non-binding 2019 guidelines), not Art. 50 | ⚠️ Same: correct conclusion, wrong authority |
| Q4 | ❌ Plausible, cited, wrong (Art. 111 transition rules) | ❌ Same, with even more confident detail |

Summary: reranking clearly improved **retrieval** for Q1 and Q2 (higher scores, noise removed, clear gap between relevant and irrelevant chunks), but did not change the **answer quality**: 1 correct, 2 partially correct, 1 wrong in both pipelines.

## 6. Failure or limitation: where the system gives a plausible but unsupported answer
1. **Stage 1 decides everything.** Q4's answer chunk was never retrieved (not in top 200). A reranker can only re-sort what vector search found; filtering and cleaning did not bring it back. The LLM then built a precise-sounding answer with real dates and correct citations to the wrong article. **Faithful ≠ true.**
2. **Vocabulary mismatch.** Art. 113 is mostly dates and chapter numbers; "shall apply" appears in dozens of articles. Embeddings capture topics, not dates, and keyword search (BM25, tested separately) did not find it either.
3. **Reranking can hurt.** For Q3 the reranker preferred the podcast and recitals (plain-language explanations) over Art. 50 (the binding rule). It judges "does this answer the question?", not "is this the legally authoritative source?". The answer was right in substance, but a client would get a "must" backed by non-binding guidance.
4. **Top-5 limits completeness.** Art. 5 has 8 prohibitions; each pipeline missed a different one because that chunk was not in its 5 sources.
5. **Measured, not assumed:** cleaning the chunks sounded like the obvious fix, but it did not help Q4 and made Q3 worse (rank 2 → 8). It did help Q1 (four Art. 5 chunks in the baseline instead of three).
6. PDF extraction differs between `pypdf` versions (794 vs. 822 chunks, broken spacing like "Ar ticle" on one machine), which changes chunking and results.

## 7. Next improvements (not built)
- **Query rewriting**: let an LLM rewrite the question into the document's legal vocabulary ("entry into force", "shall apply from") before searching.
- **Source routing**: legal "must" questions → EU AI Act articles only; concept questions → podcast/recitals.
- **Larger top-n or completeness check** for list questions like Q1.
- **Grounding check**: if no retrieved chunk directly answers the question (e.g. low rerank score), force the honest exit instead of an answer.