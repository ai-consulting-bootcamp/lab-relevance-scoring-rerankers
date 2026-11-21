# Lab Proof: First match ≠ right match

## Workflow
`relevance_scoring_rerankers.ipynb`
1. Load 472 pre-chunked EU AI Act chunks (Article/Annex + page metadata) from my Project 2 chunk cache
2. Embed with `all-MiniLM-L6-v2`, store in ChromaDB (in-memory)
3. Baseline: vector search, top 20
4. Rerank: cross-encoder `ms-marco-MiniLM-L-6-v2`, keep top 5
5. Metadata filter: `where={"article": "Article 14"}`
6. RAG: `gpt-4o-mini`, answer only from context and cite the article. Switching retrievers is a 1-line change (`use_rerank`)

## Query
"What are the obligations of providers of high-risk AI systems?"
Correct source: **Article 16**

## Retrieved evidence

| Rank | Baseline | Reranked |
|---|---|---|
| 1 | Section 3 heading (labeled Art. 15) | **Art. 16, Obligations of providers** (score 9.4) |
| 2 | Art. 26, obligations of *deployers* | Art. 25, value chain (8.33) |
| 3 | Recital, page 24 | Art. 26, deployers (8.04) |

Article 16 was not in the baseline top 3. The reranker moved it to #1.

## Final output
**Without rerank:** answer cites [Article 26] and lists *deployer* obligations (use per instructions for use) as if they were provider obligations. Plausible, but unsupported for this question.

**With rerank:** answer lists Article 16 (a)–(l): Section 2 compliance, QMS (Art. 17), documentation (Art. 18), logs (Art. 19), conformity assessment, EU declaration (Art. 47), CE marking (Art. 48), registration (Art. 49), corrective actions (Art. 20), accessibility. Cited [ARTICLE 16]. Each point traces to the retrieved chunk.

## Evaluation (manual, 3 queries)

| Query | Correct | Baseline #1 | Reranked #1 |
|---|---|---|---|
| Provider obligations | Art. 16 | ✗ (heading) | ✓ |
| Human oversight | Art. 14 | ✓ | ✓ |
| Prohibited practices | Art. 5 | ✓ | ✓ |

Metadata filter "Article 14": 3/3 chunks correct.
Takeaway: the reranker helps most when the query's wording overlaps with several sections (provider vs deployer). When the baseline is already right, it keeps the right answer at #1.

## Failure / limitation
1. **Plausible but unsupported answer:** without reranking, the LLM answered confidently from the wrong article (deployer vs provider). Citing the source in the answer is what made the error visible.
2. **Metadata mislabel:** the chunker carries the previous article label onto the next section heading ("Section 3" heading tagged as Article 15). A filter on Article 15 would return the wrong chunk.
3. **Corpus gap:** podcast transcripts not included; corpus is EU AI Act only, so source-type filtering (podcast vs regulation) was not tested.
4. **Domain mismatch:** the cross-encoder is trained on web search (MS MARCO), not legal text; #2 and #3 reranked results are still only partly relevant.
