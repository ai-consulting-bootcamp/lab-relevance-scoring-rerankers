# Lab Proof: First Match ≠ Right Match

## Goal

In this experiment, I compared standard retrieval with retrieval followed by reranking. I wanted to see whether reranking made the retrieved evidence more relevant to the question and helped keep the answer grounded in the sources.

## Sources and Preparation

- Source 1: “Trust and AI Systems,” a podcast transcript from the Software Engineering Institute at Carnegie Mellon University (10 pages).
- Source 2: The official text of the European Union Artificial Intelligence Act, Regulation (EU) 2024/1689 (144 pages).
- Number of chunks created: 803.
- Chunking: Each chunk contained up to 1,000 characters, with 150 characters of overlap.
- Metadata: Source type, section, and page number.
- Embedding model: `text-embedding-3-small` (1,536 dimensions).
- Vector database: Pinecone, using cosine similarity.
- Reranker model: `cross-encoder/ms-marco-MiniLM-L6-v2`.
- Answer-generation model: `gpt-4o-mini`, with temperature set to zero.

## Test Query

> What evidence and safeguards help a user assess whether a high-risk AI system is trustworthy?

## Workflow

1. I loaded both documents, split them into 803 chunks, and added the source type and page number to each chunk.
2. I generated embeddings for the chunks and stored them in Pinecone.
3. I ran a standard search for the query and recorded the top five results. I also repeated the search with a filter for each source type.
4. I sent the top ten results from the standard search to the reranker and kept the five highest-ranked results.
5. I gave the top five results from each method to the language model using the same prompt, then compared the answers for relevance and source support.

## Evidence: Initial Retrieval

1. Source: EU AI Act; page 18; Pinecone score: 0.6790  
   Relevant text: “...appropriate to qualify as high-risk AI systems intended to be used by a judicial authority...”

2. Source: EU AI Act; page 60; Pinecone score: 0.6569  
   Relevant text: “...the expected lifetime of the high-risk AI system and any necessary maintenance...”

3. Source: Podcast transcript; page 2; Pinecone score: 0.6457  
   Relevant text: “It is never a situation where we are going to be or should be building systems that are one hundred percent trusted.”

4. Source: EU AI Act; page 61; Pinecone score: 0.6442  
   Relevant text: “The levels of accuracy and the relevant accuracy metrics of high-risk AI systems shall be declared...”

5. Source: EU AI Act; page 22; Pinecone score: 0.6395  
   Relevant text: “Technical robustness is a key requirement for high-risk AI systems.”

## Evidence: After Reranking

1. Rank: 1; source: EU AI Act; page 17; reranker score: 3.8567  
   Relevant text: “...where such AI systems are not sufficiently transparent, explainable and documented.”

2. Rank: 2; source: Podcast transcript; page 2; reranker score: 3.1242  
   Relevant text: “Then, by giving them that information, they can then determine if there is risk...”

3. Rank: 3; source: EU AI Act; page 19; reranker score: 2.8831  
   Relevant text: “In identifying the reasonably foreseeable misuse of high-risk AI systems...”

4. Rank: 4; source: EU AI Act; page 61; reranker score: 2.6735  
   Relevant text: “The levels of accuracy and the relevant accuracy metrics... shall be declared...”

5. Rank: 5; source: EU AI Act; page 22; reranker score: 2.5800  
   Relevant text: “Technical robustness is a key requirement for high-risk AI systems.”

## Comparison

| Result | Before reranking | After reranking |
|---|---:|---:|
| EU AI Act, page 18: classification of judicial AI systems | 1 | Outside the top five |
| EU AI Act, page 60: technical documentation and the beginning of Article 14 | 2 | Outside the top five |
| Podcast, page 2 | 3 | 2 |
| EU AI Act, page 61: accuracy and resilience | 4 | 4 |
| EU AI Act, page 22: technical robustness | 5 | 5 |
| EU AI Act, page 17: transparency and documentation | Between 6 and 10 | 1 |
| EU AI Act, page 19: foreseeable misuse | Between 6 and 10 | 3 |

Before reranking, the EU AI Act chunk from page 18 was ranked first. After reranking, the page 17 chunk moved from outside the top five to first place, and the page 19 chunk moved to third place.

In my assessment, reranking improved the results somewhat, but not completely. The first result from the standard search discussed why AI systems used to assist judicial authorities may be classified as high-risk. That did not directly answer how a user can assess whether a system is trustworthy. The reranker moved it out of the top five and brought forward chunks about transparency and documentation (page 17), foreseeable misuse (page 19), and the podcast’s point that people need information to assess risk (page 2).

Reranking also had costs. First, it removed the page 60 chunk, where Article 14 on human oversight begins. As a result, the reranked answer did not mention human oversight, even though it is a relevant safeguard. One possible reason is that most of the chunk concerns technical documentation and only the beginning of Article 14 appears in it.

Second, the new top result, from page 17, is still about a specific context involving law enforcement. Like the page 18 result, it may have ranked highly because it shares terms relevant to the query. The result does not establish that the statement is a general rule for every high-risk AI system.

## Final Answer for the Experiment

I included claims that are supported by the retrieved text I inspected.

### Legal information from the EU AI Act

- Article 15(3) says that the accuracy levels and relevant accuracy metrics of high-risk AI systems must be declared in the accompanying instructions for use. This describes what those instructions must state; it does not, by itself, prove that a particular system meets the declared metrics. (Page 61.)

- High-risk AI systems must be as resilient as possible to errors, faults, and inconsistencies, with technical and organisational measures taken to support that resilience. (Article 15(4), page 61; Recital 75, page 22.)

- Annex IV describes information to be included in the technical documentation, including the system’s expected lifetime, necessary maintenance and updates, and, where relevant, mechanisms for collecting and interpreting logs. This information appears in Annex IV, which is linked to Article 11(1). (Page 60.)

- A recital says that providers should consider reasonably foreseeable misuse of high-risk AI systems. Because this text is in the preamble, I present it as context rather than as a standalone requirement from an operative article. (Page 19.)

- Page 17 says that insufficient transparency, explainability, and documentation can be relevant to classifying certain AI systems used in a specific context as high-risk. This passage does not establish a general requirement for every high-risk AI system.

- Article 14 on human oversight begins on page 60, but the retrieved text I inspected showed only the beginning of that article. I therefore do not make a detailed claim about its requirements here.

### Podcast perspective

- The speakers say that when people receive appropriate information, they can assess whether risk exists and how much risk there may be. (Page 2.)

- The speakers say that AI systems should not be treated as one hundred percent trustworthy, because context and AI systems can change. This is the speakers’ perspective, not a legal requirement. (Page 2.)

## Limitation or Possible Failure

One limitation is that I tested only one query and did not define a human-labelled relevance set in advance. Therefore, my judgment that the results improved is a manual assessment, not a measured performance score.

The reranker also only reorders the ten initial candidates. If the relevant chunk is not among those ten candidates, the reranker cannot retrieve it. In addition, the reranker scores and Pinecone similarity scores use different scales and should not be compared directly. The reranker was not selected or evaluated specifically for legal texts, so it may rank passages with matching terms highly even when their legal context is narrow.

For example, the model’s answer after reranking said that high-risk AI systems must be transparent and documented to retain public trust, citing page 17. The retrieved passage did not support the “retain public trust” claim, and its context was specific rather than a general rule. Similarly, the answer before reranking attributed a bias-mitigation claim to page 61, but that claim was not visible in the printed excerpt. Both model answers also referred to “calibrated trust,” which was not visible in the excerpts I printed. I printed only the first 300–500 characters of each chunk, so I would need to inspect the full chunks to verify those claims.

## Security Check

I stored API keys in `.env` and loaded them with `load_dotenv`. I did not print keys in the code or notebook output. I configured Git to ignore `.env`.

- `git check-ignore .env`: .env
- `git ls-files | findstr .env`: nothing found in the python files and notebook


Before submitting, I will confirm that no API keys appear in files tracked by Git. I will also clear notebook output that exposes my local Windows path.