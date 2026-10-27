# Lab Proof: Relevance Scoring and Reranking

## Learning Goal

Demonstrate how embedding-based retrieval and a reranker select evidence for a question about Trustworthy AI and high-risk AI systems, while keeping the retrieved evidence inspectable.

## Workflow and Configuration

1. Loaded `podcast.txt` and `eu_ai_act.pdf` into LangChain `Document` objects.
2. Split the EU AI Act at exact section-heading lines, then used LangChain's `RecursiveCharacterTextSplitter` with:
   - `chunk_size=1500` characters
   - `chunk_overlap=250` characters
3. Created **609 chunks**: 596 from the EU AI Act and 13 from the podcast transcript. Each chunk retained source metadata; EU AI Act chunks also retained PDF page and section metadata.
4. Used OpenAI `text-embedding-3-small` to create 1536-dimensional embeddings.
5. Stored the vectors in Pinecone index `rag2-relevance-rerankers`, using cosine similarity. This experiment queried the `section-aware-v1` namespace, which contains the 609 section-aware chunks.
6. Retrieved 12 candidates with Pinecone, then reranked those candidates with Cohere `rerank-v5.0-pro`, returning the top five.

## Query

> What does trustworthy AI require, and what requirements does the EU AI Act impose on high-risk AI systems?

## Retrieval and Reranking Evidence

Pinecone's initial top-12 results were all from `eu_ai_act`. Examples:

| Initial rank | Pinecone similarity | Evidence locator |
|---:|---:|---|
| 1 | 0.6735 | EU AI Act PDF, p. 43, preamble |
| 3 | 0.6641 | EU AI Act PDF, p. 55, Article 8 |
| 8 | 0.6585 | EU AI Act PDF, p. 61, Article 15 |
| 9 | 0.6476 | EU AI Act PDF, p. 8, Recital 27 |

Cohere reranked the retrieved candidates as follows:

| Reranked position | Cohere relevance score | Evidence locator |
|---:|---:|---|
| 1 | 0.7061 | EU AI Act PDF, p. 18, Recital 64 |
| 2 | 0.6979 | EU AI Act PDF, p. 61, Article 15 |
| 3 | 0.6885 | EU AI Act PDF, p. 61, Article 15 |
| 4 | 0.6230 | EU AI Act PDF, p. 8, Recital 27 |
| 5 | 0.6197 | EU AI Act PDF, p. 21, preamble |

The reranker moved Article 15 evidence from initial ranks 8 and 10 into positions 2 and 3. It also placed the passage about the 2019 Trustworthy AI guidelines at position 4.

## Final Output

The EU AI Act's Recital 27 recalls seven ethical principles from the 2019 Trustworthy AI guidelines: human agency and oversight; technical robustness and safety; privacy and data governance; transparency; diversity, non-discrimination and fairness; societal and environmental well-being; and accountability. The recital describes these principles as non-binding.

For high-risk AI systems, Recital 64 explains that mandatory requirements should take account of the system's intended purpose and context of use, as well as the provider's risk-management system. Article 15 provides specific requirements for accuracy, robustness and cybersecurity throughout the system lifecycle. It also addresses accuracy metrics, resilience to faults, backup or fail-safe measures, feedback loops, and cybersecurity threats such as data poisoning and adversarial examples.

This is a summary of the evidence retrieved in this experiment, not an exhaustive list of all EU AI Act obligations.

## Limitation

The initial top-12 retrieval contained no podcast chunks. The reranker only reorders the candidates it receives, so it could not add podcast evidence. This run therefore supports its answer from the EU AI Act alone; it does not establish what the podcast says.

The scores indicate model-assessed relevance. They do not establish factual correctness or legal authority, so the retrieved text and its locator still require human inspection.

## Step 7: Manual Evaluation

I compared two RAG runs using the same query and the same generation model (`gpt-4o-mini`):

- **Baseline:** the top five candidates from Pinecone similarity search.
- **Reranked:** the top five candidates after Cohere reranking of the initial retrieval results.

### Query

> What does trustworthy AI require, and what requirements does the EU AI Act impose on high-risk AI systems?

### Results

The baseline answer covered the Act’s general purpose, mandatory requirements, intended purpose and context of use, and risk management. Its evidence was comparatively broad and did not clearly enumerate the trustworthy AI principles or the specific Article 15 requirements.

The Cohere-reranked answer included the seven trustworthy AI principles from Recital 27 and more specific Article 15 evidence on accuracy, robustness, cybersecurity, feedback loops, and resilience. This made the answer more detailed for the query.

### Grounding review

The reranked answer also showed a grounding limitation. It described a two-person verification requirement without clearly limiting it to the specific context described by the cited source. It also attached an irrelevant citation to the claim about accuracy and performance metrics. The cited evidence should be checked at claim level, especially for legal scope.

### Conclusion

For this query, Cohere reranking surfaced evidence that supported a more detailed answer than the Pinecone-only top five. However, reranking did not guarantee correct interpretation or citation. The result still required manual verification against the source text and its scope.

