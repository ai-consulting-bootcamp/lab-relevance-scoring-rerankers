# Lab Proof: First match ≠ right match

## 1. What I built

I built a retrieval-augmented generation pipeline over the Trustworthy AI podcast transcript and the EU AI Act. The pipeline uses OpenAI embeddings, Pinecone similarity search, source/section/article metadata filtering, a local Cross-Encoder reranker, and an LCEL answer chain that cites the retrieved evidence.

Implementation: [relevance_scoring_rerankers.ipynb](./relevance_scoring_rerankers.ipynb)

## 2. Query

> What fines apply for using a prohibited AI practice?

## 3. Retrieved evidence

The final comparison used the following top results:

| Method / rank | Source | Page / chunk | Score | Snippet or relevance |
|---|---|---|---:|---|
| Baseline #1 | EU AI Act | p.51 | 0.633 | Article 4, “AI literacy” — a weak match for a question about fines |
| Baseline #3 | EU AI Act | p.115 | 0.613 | Penalties section containing the Article 99 fine provisions |
| Reranked #1 | EU AI Act | p.115 | 4.259 | Penalties section containing the Article 99 fine provisions |
| Reranked #2 | EU AI Act | p.117 | 4.098 | Further penalty and infringement details |

## 4. Final answer

Non-compliance with the prohibition of the AI practices referred to in Article 5 is subject to administrative fines of up to **EUR 35,000,000** or, if the offender is an undertaking, up to **7% of its total worldwide annual turnover** for the preceding financial year, whichever is higher [EU AI Act (Reg. 2024/1689), p.115].

## 5. Trace

The fine amount and the 7% turnover alternative come from the Article 99 penalties text on page 115 of the EU AI Act. In the baseline retrieval, that evidence was only ranked third. The Cross-Encoder moved the page 115 result to rank one, making the evidence supporting the answer easier to find.

The baseline rank-one result came from page 51 and discussed Article 4, AI literacy. It was semantically related to the EU AI Act but did not answer the question about fines. This is the clearest example of “first match ≠ right match.”

## 6. Baseline vs. reranked

For this query, reranking changed the evidence order but not the final answer. The baseline answer and the reranked answer both returned the same EUR 35 million / 7% result.

In the saved run:

- Baseline answer time: approximately 2.03 seconds
- Reranked answer time: approximately 1.90 seconds
- The reranker used a local Cross-Encoder and did not require an additional LLM scoring call.

For this query, reranking was useful because it moved the relevant penalty chunk from rank three to rank one. The timing comparison is only one run, so it should not be treated as a reliable performance benchmark.

## 7. Failure or limitation

The initial Article 5 metadata filter returned no results because the regular-expression word boundary was incorrectly encoded in the notebook JSON. I corrected the regex, and local chunking now identifies six Article 5 chunks. 

The baseline system can also return a plausible but weakly relevant chunk, such as Article 4 for the fines query. The RAG answer may still be correct because the relevant chunk appears lower in the retrieved context, but this is why retrieved evidence must be inspected and reranked.

## Stop and think reflections

### 1. What metadata was missing initially?

The original metadata identified the source and chunk, but not the document structure inside the source. Useful fields for the EU AI Act were source section, article, recital, and paragraph. Without those fields, filtering for “Article 5” or “only recitals” was not possible. Adding the fields required rebuilding the Pinecone index because existing vectors retain their original metadata.

### 2. How can a reviewer find a podcast chunk?

The podcast has no page numbers. A reviewer can use the chunk ID, such as podcast-8, together with the stored text excerpt and search for that excerpt in data/podcast.txt. Character offsets, timestamps, speaker names, or transcript sections would provide stronger traceability, but the current chunk ID and text still identify the source passage.
