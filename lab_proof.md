```markdown
# Lab Proof: First match ≠ right match

## 1. What I built
I built a small retrieval-and-rerank pipeline in [relevance_scoring_rerankers.ipynb](./relevance_scoring_rerankers.ipynb) that loads the EU AI Act PDF and the podcast transcript, chunks them with metadata, embeds the chunks in Pinecone, runs a baseline similarity search, and then reranks the candidate set before answering the user question with source citations.

## 2. Query
"What AI practices are prohibited under the EU AI Act?"

## 3. Retrieved evidence
| Rank | Source | Page / chunk_id | Score | Snippet |
|---|---|---|---|---|
| 1 | regulation | p.51 | 0.698 (baseline) / reranked to top result | "(c) the placing on the market, the putting into service or the use of AI systems for the evaluation or classification of natural persons ..." |
| 2 | regulation | p.9 | 0.588 (baseline) | "multiple data points related to their social behaviour in multiple contexts or known, inferred or predicted personal or behavioural data" |
| 3 | regulation | p.12 | 0.684 (baseline) | "Practices that are prohibited by Union law, including data protection law, non-discrimination law, consumer protection law, and competition law" |

The first baseline hit was a misleading lexical match on the word "prohibited" rather than the actual Article 5 clause; the reranked results pulled the system back toward the relevant Article 5 text about prohibited AI practices.

## 4. Final answer
The EU AI Act prohibits AI practices that materially distort human behaviour through subliminal or deceptive techniques, exploit the vulnerabilities of specific groups, and evaluate or classify natural persons through social scoring or similar profiling in a way that leads to unjustified or disproportionate treatment. Those are the key prohibited practices under Article 5 of the regulation [regulation, p.51], [regulation, p.9].

## 5. Trace
- The claim that the Act forbids social scoring and similar classification of people comes from the chunk describing the evaluation or classification of natural persons, which is explicitly about prohibited AI uses in the Act [regulation, p.51].
- The claim that the social-scoring concept involves personal and behavioural data is supported by the definition chunk describing multiple data points related to a person’s social behaviour and personal data [regulation, p.9].
- The broader idea that these are prohibited practices is consistent with the Act’s framing of prohibited practices under Union law and the relevant Article 5 structure [regulation, p.12].

## 6. Baseline vs reranked
The baseline vector search was vulnerable to a false positive: a high-similarity result mentioning "prohibited" and "AI law" appeared early, but it was not the actual prohibited-practices clause. The reranker corrected this by prioritising the Article 5 language tied to the evaluation/classification of natural persons and the social-scoring definition. This was worth the extra cost for a legal question because the retrieval error was material: the wrong chunk would have produced a plausible but incorrect answer. In a production system, that improvement matters more than the small extra latency or cost.

## 7. Failure or limitation
This system can still produce a plausible but unsupported answer when the retrieved context is semantically close but legally incomplete. For example, if the query is vague or the vector store misses the exact Article 5 section, the model may infer a general legal answer from nearby wording instead of the strict prohibited-practices language. A strong guardrail is to require a citation for every factual claim and, when the evidence is weak, return: "I don't know based on the sources." That prevents the pipeline from confidently answering from general legal knowledge alone.

