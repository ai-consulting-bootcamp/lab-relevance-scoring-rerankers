
EU AI Act chunks currently have source type, source name, chunk ID, and page number. They tell you where a passage came from, but not its legal structure.

The main missing fields are:
- section: Is the passage a recital, an article, or an annex?
- article: Which article does it belong to, such as Article 5?
- chapter: Which chapter contains it?


For the podcast - timestamps would be useful to see where the relevant passage came from.

# Lab Proof: First match ≠ right match

## 1. What I built
a rag-pipeline that uses metadata and 2 differnt sources to provide answers to questions regarding the eu ai act.

query → retrieve chunks (Pinecone) → (optional) rerank → format context → LLM → answer


## 2. Query
"'What AI practices are prohibited under the EU AI Act?'"

## 3. Retrieved evidence
| Rank | Source | Page / chunk_id | Score | Snippet |

=== Baseline | Query: What AI practices are prohibited under the EU AI Act?
#1  score=0.748  [regulation | p.51.0]  'Article 5\nProhibited AI practices\n1. The following AI practices shall be prohibited:\n(a) the placing on the market, the '
#2  score=0.698  [regulation | p.51.0]  'Article 4\nAI literacy\nProviders and deployers of AI systems shall take measures to ensure, to their best extent, a suffi'
#3  score=0.684  [regulation | p.12.0]  '(45) Practices that are prohibited by Union law, including data protection law, non-discrimination law, consumer \nprotec'
#4  score=0.684  [regulation | p.12.0]  '(45) Practices that are prohibited by Union law, including data protection law, non-discrimination law, consumer \nprotec'
#5  score=0.681  [regulation | p.9.0]  'intention to distort behaviour where the distortion results from factors external to the AI system which are outside \nth'

## 4. Final answer

The following AI practices are prohibited under the EU AI Act:

1. The placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person’s consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm [EU AI Act (Reg. 2024/1689), p.51, Article 5].

2. The placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation [EU AI Act (Reg. 2024/1689), p.51, Article 5].

## 5. Trace
=== Chunks behind this answer | Query: What AI practices are prohibited under the EU AI Act?
#1  score=0.748  [regulation | p.51.0]  'Article 5\nProhibited AI practices\n1. The following AI practices shall be prohibited:\n(a) the placing on the market, the '
#2  score=0.684  [regulation | p.12.0]  '(45) Practices that are prohibited by Union law, including data protection law, non-discrimination law, consumer \nprotec'
#3  score=0.682  [regulation | p.9.0]  'intention to distort behaviour where the distortion results from factors external to the AI system which are outside \nth'
#4  score=0.660  [regulation | p.3.0]  'operators involved in the AI value chain under this Regulation should apply without prejudice to national law, in \ncompl'
#5  score=0.660  [regulation | p.45.0]  '(b) prohibitions of certain AI practices;\n(c) specific requirements for high-risk AI systems and obligations for operato'


## 6. Baseline vs reranked
What changed? Was it worth the cost?

Q1 | Baseline | 3.9 s
What AI practices are prohibited under the EU AI Act?

ANSWER:
 The following AI practices are prohibited under the EU AI Act:

1. The placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person’s consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm [EU AI Act (Reg. 2024/1689), p.51, Article 5].

2. The placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation [EU AI Act (Reg. 2024/1689), p.51, Article 5].

=== Q1 Baseline: chunks used | Query: What AI practices are prohibited under the EU AI Act?
#1  score=0.748  [regulation | p.51.0]  'Article 5\nProhibited AI practices\n1. The following AI practices shall be prohibited:\n(a) the placing on the market, the '
#2  score=0.684  [regulation | p.12.0]  '(45) Practices that are prohibited by Union law, including data protection law, non-discrimination law, consumer \nprotec'
#3  score=0.682  [regulation | p.9.0]  'intention to distort behaviour where the distortion results from factors external to the AI system which are outside \nth'
#4  score=0.660  [regulation | p.3.0]  'operators involved in the AI value chain under this Regulation should apply without prejudice to national law, in \ncompl'
#5  score=0.660  [regulation | p.45.0]  '(b) prohibitions of certain AI practices;\n(c) specific requirements for high-risk AI systems and obligations for operato'

====================================================================================================
Q1 | Reranked | 10.1 s
What AI practices are prohibited under the EU AI Act?

ANSWER:
 The following AI practices are prohibited under the EU AI Act:

1. The placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person’s consciousness or purposefully manipulative or deceptive techniques, with the objective, or the effect of materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision, thereby causing them to take a decision that they would not have otherwise taken in a manner that causes or is reasonably likely to cause that person, another person or group of persons significant harm [EU AI Act (Reg. 2024/1689), p.51, Article 5].

2. The placing on the market, the putting into service or the use of an AI system that exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation [EU AI Act (Reg. 2024/1689), p.51, Article 5].

=== Q1 Reranked: chunks used | Query: What AI practices are prohibited under the EU AI Act?
#1  score=0.924  [regulation | p.51.0]  'Article 5\nProhibited AI practices\n1. The following AI practices shall be prohibited:\n(a) the placing on the market, the '
#2  score=0.890  [regulation | p.8.0]  'manipulative, exploitative and social control practices. Such practices are particularly harmful and abusive and \nshould'
#3  score=0.555  [regulation | p.12.0]  '(45) Practices that are prohibited by Union law, including data protection law, non-discrimination law, consumer \nprotec'
#4  score=0.554  [regulation | p.9.0]  'intention to distort behaviour where the distortion results from factors external to the AI system which are outside \nth'
#5  score=0.548  [regulation | p.45.0]  '(b) prohibitions of certain AI practices;\n(c) specific requirements for high-risk AI systems and obligations for operato'


reranked is slightly better. essntailly the same answer, but the Baseline version misses a critical chunk (page 8, chunk nr 2 in he reranked version)

## 7. Failure or limitation
Where could this system give a plausible but unsupported answer?

A strong limitation to discuss is incomplete retrieval. Your answer lists two prohibited practices, but the evidence shown for Article 5 is only a snippet, and the retrieved set may not contain every relevant provision. So the answer could sound complete while actually omitting other prohibited practices. Reranking can improve which chunks appear first, but it cannot guarantee that all relevant evidence was retrieved or that the final answer is fully supported.