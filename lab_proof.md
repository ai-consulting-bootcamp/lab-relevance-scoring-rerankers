# Lab Proof: First match ≠ right match

## 1. What I built
A RAG pipeline over two sources: a podcast on the EU *Ethics Guidelines for Trustworthy AI* and the EU AI Act PDF. Both sources go into one Pinecone index with source, page, section and article metadata. Results are reranked by an LLM (top 10 vector candidates, each scored 0-1 by `gpt-4o-mini`, combined as `0.3 * similarity + 0.7 * llm_score`, top 5 kept). An LCEL chain answers only from the retrieved chunks and cites each one as `[source, page | chunk_id]`.
Code: [relevance_scoring_rerankers.ipynb](relevance_scoring_rerankers.ipynb) (Steps 6–7).

## 2. Query
"What fines apply for using a prohibited AI practice?"

## 3. Retrieved evidence
Reranked top 5 (`answer(query, retrieve_fn=reranked_search)`):

| Rank | Source | Page / chunk_id | Score | Snippet |
|---|---|---|---|---|
| 1 | EU AI Act (Reg. 2024/1689), Art. 99 | p.115 / `regulation-665` | 0.884 | "3. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7 % of its total worldwide annual turnover…" |
| 2 | EU AI Act (Reg. 2024/1689), Art. 100 | p.117 / `regulation-673` | 0.883 | "2. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 1 500 000." |
| 3 | EU AI Act (Reg. 2024/1689), Art. 100–101 | p.117 / `regulation-675` | 0.875 | "6. Funds collected by imposition of fines in this Article shall contribute to the general budget of the Union…" |
| 4 | EU AI Act (Reg. 2024/1689), Art. 80–81 | p.108 / `regulation-635` | 0.872 | "…the provider shall be subject to fines in accordance with Article 99." |
| 5 | EU AI Act (Reg. 2024/1689), Art. 80 | p.108 / `regulation-634` | 0.664 | "…the provider shall be subject to fines in accordance with Article 99." |

## 4. Final answer
> Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 35,000,000 or, if the offender is an undertaking, up to 7% of its total worldwide annual turnover for the preceding financial year, whichever is higher [EU AI Act (Reg. 2024/1689), p.115 | regulation-665].

## 5. Trace
| Claim in the answer | Chunk | Exact text in the chunk |
|---|---|---|
| Fines of up to EUR 35,000,000 for breaching the Article 5 prohibitions | `regulation-665`, p.115 (Article 99(3)) | "Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 35 000 000" |
| Or up to 7% of total worldwide annual turnover for undertakings, whichever is higher | `regulation-665`, p.115 (Article 99(3)) | "or, if the offender is an undertaking, up to 7 % of its total worldwide annual turnover for the preceding financial year, whichever is higher" |

Every claim comes from the single cited chunk, and nothing in the answer is unsupported.

## 6. Baseline vs reranked
- **What changed:** with baseline search, the top result for this query was `regulation-342` (Article 4 "AI literacy" plus the start of Article 5). It mentions prohibited practices but says nothing about fines: *first match ≠ right match*. The correct chunk `regulation-665` was only at rank 3. The reranker moved it to rank 1.
- **The answer did not change.** The LLM reads all 5 chunks, so it found the EUR 35M / 7% rule in both cases. Across the 5 test queries, reranking changed the order every time but changed the answer only once (Q1, which listed 3 prohibited practices instead of 1).
- **Cost:** baseline uses 1 LLM call and about 1.7 s per query. Reranked uses 11 LLM calls (10 relevance scores + 1 answer) and about 7.8 s per query.
- **Worth it?** Not at this setup (k=5 into the prompt). It adds about 4.5x the latency and 11x the calls for a better rank-1 that the generator didn't need. It would be worth it with a large candidate pool and a small final context, where rank really decides what the LLM sees, or with a cheaper reranker (cross-encoder, or one batched scoring call).

Full evaluation table for all 5 queries: Step 7 in the notebook.

## 7. Failure or limitation
1. **Incomplete answer that looks complete (this query):** `regulation-673` (Article 100: fines of up to EUR 1 500 000 for Union institutions, bodies and agencies) was retrieved at rank 2, but the answer leaves it out. A reader would think EUR 35M / 7% is the only fine regime. Citations show where the answer came from, but not what it skipped.
2. **Wrong citation:** for "human-in-the-loop vs human-on-the-loop", the reranked answer is correct but cites `podcast-7`. That chunk only defines human-in-the-loop. The human-on-the-loop definition is in `podcast-8`. The model cites by chunk label, and nothing checks that the cited chunk actually contains the claim.
3. **Retrieval OK, generation fails:** for "What are the seven requirements for trustworthy AI?", both methods retrieved `regulation-50` (recital 27, which lists all seven), and the reranker put it at #1. The model still answered "I don't know based on the sources", because the Act calls them "principles", not "requirements". The podcast covers them across chunks 7–14, so no single chunk holds the whole list.
4. **Metadata mislabelling:** `regulation-342` begins with Article 4 but is tagged `article: 5`, because the chunker assigns the *last* heading in a chunk. Filtering on `article = 5` therefore returns Article 4 text too.

---

## Appendix: reflections from Steps 1–5

**Missing metadata (Step 1):** the original chunks had no field for the EU AI Act section or the article number. `source_type`, `source_name`, `chunk_id` and `page` aren't enough to filter for "Article 5" or "only recitals". A page number helps locate text, but it isn't a structured `article` or `section` value. I added `section` (`"recital"`, `"article"`, `"annex"`) and `article` (e.g. `5`).

**Podcast traceability (Step 1):** podcast chunks have a `chunk_id` but no page or other human-readable position. Timestamps (`start_time` / `end_time`), or paragraph or line numbers, would let a reviewer find the passage in the original transcript.

**Baseline observation (Step 2):** the clearest *first match ≠ right match* cases were "What AI practices are prohibited under the EU AI Act?" and "What fines apply for using a prohibited AI practice?". In both, the top result was the Article 4 AI literacy chunk (scores 0.698 and 0.633), while more relevant chunks ranked lower.

**Metadata filtering (Step 5):** the Article 5 search filters on both source and article number:

```python
filter={"source_type": {"$eq": "regulation"}, "article": {"$eq": 5}}
```

The index had to be rebuilt because Pinecone stores metadata with each vector at upload time. Changing `chunk_with_metadata` only updates the local chunks. Re-uploading stores the new fields so Pinecone can filter on them.
