# Lab Proof: First match ≠ right match

## 1. What I built
I built a retrieval-augmented question-answering pipeline over podcast and EU AI Act chunks, with baseline vector search, LLM relevance reranking, source metadata filtering, and citations. The implementation and recorded results are in [relevance_scoring_rerankers.ipynb](./relevance_scoring_rerankers.ipynb).

## 2. Query
"What are the seven requirements for trustworthy AI?"

## 3. Retrieved evidence
| Rank | Source | Page / chunk_id | Score | Snippet |
|---|---|---|---:|---|
| Baseline 1 | Trustworthy AI podcast | `podcast-2` | 0.674 similarity | “...how do we make AI worthy of trust? And our mission for this deep dive is to figure out how to...” |
| Reranked 1 | EU AI Act (Reg. 2024/1689) | p. 8 | 0.883 combined reranking score | “(27) While the risk-based approach is the basis for a proportionate and effective set of binding rules...” |

The notebook’s top-10 baseline results also show this EU AI Act passage at rank 4 with a similarity score of 0.611. Scores are not directly comparable across methods: the baseline score is vector similarity, while the reranked score combines vector similarity and the LLM relevance score.

## 4. Final answer
The seven principles for trustworthy AI include human agency and oversight; technical robustness and safety; privacy and data governance; transparency; diversity, non-discrimination and fairness; societal and environmental well-being; and accountability [EU AI Act (Reg. 2024/1689), p.8.0].

## 5. Trace
The answer’s list of seven principles is attributed to the EU AI Act chunk retrieved from page 8. The notebook’s reranked results place that chunk first for this query; its baseline comparison says “I don't know based on the sources.”

## 6. Baseline vs reranked
For this query, baseline retrieval’s top result was podcast chunk `podcast-2` (similarity 0.674), and the baseline answer was “I don't know based on the sources.” Reranking promoted the relevant EU AI Act passage (page 8, combined score 0.883), enabling the cited answer. The notebook’s evaluation marks the baseline answer incorrect and the reranked answer correct and grounded.

Across the notebook’s five-query cost measurement, reranking averaged 10.16 seconds versus 2.36 seconds for baseline—about 4.3× slower, with 10 extra LLM calls and approximately 2,710 extra tokens per query. The measured extra cost was about $0.00041 per query ($0.41 per 1,000 queries). That tradeoff can be worthwhile for research or compliance work where recovering a grounded answer matters, but the added latency may be too high for interactive chat.

## 7. Failure or limitation
Reranking cannot recover evidence that is missing from the initial candidate set, and the LLM judge may still mis-rank or prefer superficially related text. It also adds latency and LLM calls. The notebook demonstrates that limitation: for “What fines apply for using a prohibited AI practice?”, both baseline and reranked answers said “I don't know based on the sources.”
