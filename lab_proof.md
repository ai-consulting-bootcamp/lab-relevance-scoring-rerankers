# Lab Proof: Relevance Scoring and Rerankers

## Workflow

Loaded `podcast.txt` and `eu_ai_act.pdf`, extracted their text, and split it into overlapping chunks with source metadata (`source_type`, `source_file`, section/page, and `chunk_index`). Encoded the chunks and query with `sentence-transformers/all-MiniLM-L6-v2`, then ranked chunks by cosine similarity. Compared source-filtered results, scored the baseline candidates with `gpt-4o-mini`, and reranked the same query's top 10 embedding candidates with `cross-encoder/ms-marco-MiniLM-L-6-v2`. The pipeline returned the passages, metadata, similarity scores, and reranker scores for inspection.

## Query

> What does human oversight mean in trustworthy AI?

## Retrieved Evidence

- **EU AI Act, page 8, chunk 1** (`source_type: eu_ai_act`): Describes human agency and oversight as AI serving people, respecting human dignity and personal autonomy, and being appropriately controlled and overseen by humans.
- **EU AI Act, page 60, chunk 1** (`source_type: eu_ai_act`): Article 14 says high-risk AI systems should be designed to be effectively overseen by natural persons, with oversight aiming to prevent or minimize risks to health, safety, or fundamental rights.
- **Podcast transcript, chunk 8** (`source_type: podcast`): Explains human-in-the-loop, human-on-the-loop, and human-in-command oversight. It warns that automation bias can make human review ineffective unless people have the capacity to override the system.

## Final Output

Human oversight means that AI remains a tool under meaningful human control: people must be able to oversee it, and those assigned oversight should be able to understand its limits and intervene. For high-risk systems, the cited EU AI Act passage describes oversight as a way to prevent or minimize risks to health, safety, and fundamental rights. (EU AI Act, pages 8 and 60; podcast transcript, chunk 8.)

## Baseline vs. Reranked Evaluation

The baseline similarity search returned EU AI Act chunks in this order: page 60, chunk 3 (0.709); page 60, chunk 1 (0.706); and page 21, chunk 3 (0.687). The cross-encoder reranked the top 10 candidates and returned page 8, chunk 0 (6.508); page 8, chunk 1 (5.839); and page 60, chunk 1 (4.467). The reranker promoted the broad definition of human agency and oversight, while the baseline emphasized practical oversight measures such as monitoring and automation-bias awareness. These score scales differ, so the comparison is based on the retrieved passages and their ordering, not the numerical scores.

## Failure or Limitation

Some passages are split across chunks: page 8, chunk 0 ends with “human agency and oversight means that,” and chunk 1 continues the definition. A single chunk can therefore be incomplete when inspected alone. Also, the cross-encoder only reranks the top 10 candidates supplied by embedding retrieval; relevant evidence outside that candidate set cannot be promoted. Retrieval and reranking scores are ranking signals, not verification that a final answer is correct, so the cited source text still needs to be inspected.
