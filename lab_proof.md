# Lab Proof: First match ≠ right match

## 1. What I built

I built a RAG pipeline using Pinecone vector search, metadata filtering,
cross-encoder reranking, and source citations.

Notebook: `relevance_scoring_rerankers.ipynb`

## 2. Query

"What AI practices are prohibited under the EU AI Act?"

## 3. Retrieved evidence

| Rank | Source | Page / chunk_id | Score | Snippet |
|---|---|---|---|---|
| 1 | EU AI Act | Article 5 / regulation chunk | Cross-encoder score | Article 5 lists prohibited AI practices. |
| 2 | EU AI Act | Article 5 / regulation chunk | Cross-encoder score | Prohibitions include manipulation, exploitation, and social scoring. |
| 3 | EU AI Act | Article 5 / regulation chunk | Cross-encoder score | Other prohibitions cover biometric categorisation and certain biometric identification uses. |

## 4. Final answer

Article 5 of the EU AI Act prohibits certain AI practices because they can
manipulate people, exploit vulnerabilities, or create unacceptable risks. The
prohibited practices include subliminal or manipulative techniques, exploiting
the vulnerabilities of specific groups, and social scoring. The Act also
prohibits several biometric uses, including some biometric categorisation,
emotion recognition in workplaces and schools, untargeted scraping of facial
images to build databases, and certain real-time remote biometric
identification uses in publicly accessible spaces. The legal text includes
limited exceptions for some of these categories.

Source: [EU AI Act, Article 5].

## 5. Trace

- Claim 1: The Act prohibits manipulative or subliminal AI techniques.  
  Supported by: `[EU AI Act, Article 5]`

- Claim 2: The Act prohibits exploiting the vulnerabilities of specific people
  or groups and prohibits social scoring in the circumstances described by the
  Act.  
  Supported by: `[EU AI Act, Article 5]`

- Claim 3: Article 5 also regulates or prohibits several biometric practices,
  including certain biometric categorisation, emotion recognition, facial
  image scraping, and real-time remote biometric identification.  
  Supported by: `[EU AI Act, Article 5]`

## 6. Baseline vs reranked

- Baseline top result: A semantically similar EU AI Act chunk about prohibited
  practices.
- Reranked top result: A chunk focused more directly on Article 5 and the list
  of prohibited practices.
- Did reranking change the answer? It mainly changed the order of the retrieved
  evidence; the central answer remained about Article 5.
- Did reranking improve the result? Yes, when the Article 5 chunk moved higher,
  because the answer was then grounded in the most directly relevant passage.
- Additional cost or time: The cross-encoder adds local inference time for the
  ten retrieved candidates, but it does not require one LLM API call per
  candidate. The exact timing depends on the machine and is printed by Step 7.

## 7. Failure or limitation

The system could produce a plausible but unsupported answer if the correct
information is not present in the retrieved chunks. It may also assign an
incorrect relevance score or fail to retrieve the best chunk. Metadata
filtering is only reliable for fields that were added before the documents
were uploaded; adding a new field requires rebuilding the Pinecone index.
