## 1. RAG Pipeline – Implementation Overview

**Data sources**
- EU AI Act: 144 PDF pages
- Trustworthy AI podcast: 1 transcript

**Document processing**
- Chunk size: 1,000 characters
- Chunk overlap: 150 characters
- EU AI Act chunks: 763
- Podcast chunks: 20
- Total indexed chunks: 783

**Retrieval pipeline**
- Embeddings: OpenAI `text-embedding-3-small`
- Vector database: Pinecone
- Index: `lab-rerankers`
- Namespace: `relevance-lab-pymupdf-v1`
- Reranker: Cohere `rerank-v5.0-fast`
- Metadata: source type, source name, chunk ID, PDF page number and section classification

**Validation**
- All 783 chunks were successfully indexed.
- No empty chunks, duplicate chunk IDs or missing metadata were detected.
- The pipeline supports vector retrieval, Cohere reranking, metadata filtering and source-grounded RAG answers.

## 2. Baseline Retrieval vs. Cohere Reranking

**Objective:** Evaluate whether Cohere reranking improves the relevance of documents retrieved by Pinecone and the quality of the resulting RAG answers.

**Method:**
- Pinecone retrieved the initial 10 candidate chunks per query.
- Cohere reranked those candidates using `rerank-v5.0-fast`.
- Five test questions were evaluated using both retrieval approaches.
- Both approaches generated source-grounded RAG answers.

### Evaluation Results

| Test question | Observation |
|---|---|
| Prohibited AI practices | Both approaches identified relevant evidence from Article 5. Cohere also promoted another relevant chunk, but both answers remained incomplete. |
| Seven requirements for trustworthy AI | Neither approach retrieved sufficient evidence for a complete answer. Both correctly abstained. |
| Human-in-the-loop vs. human-on-the-loop | Both approaches produced accurate, grounded explanations. |
| Fines for prohibited AI practices | Both produced the same correct answer: up to €35 million or 7% of worldwide annual turnover, whichever is higher. |
| Social scoring | Both identified the general prohibition, although their explanations simplified the legal conditions. |

### Key Findings

1. **Reranking improved document ordering in some cases**, promoting more relevant evidence.
2. **Better document rankings did not consistently produce better final answers.**
3. Cohere was limited to the initial Pinecone candidates and could not recover missing evidence outside that set.
4. The trustworthy AI question demonstrated the importance of retrieval coverage and appropriate abstention.
5. Pinecone similarity scores and Cohere relevance scores measure different things and should not be compared directly.

### Conclusion

Cohere reranking provided some improvements in evidence selection, but the five-question evaluation did not demonstrate a consistent improvement in final answer quality. Retrieval coverage, chunk boundaries and source completeness remained important limitations.

## 3. Metadata Filtering

**Objective:** Evaluate whether metadata filtering can narrow the retrieval results to specific document categories.

**Method:**
- Applied a Pinecone metadata filter using `section = article`.
- Used the question: "What AI practices are prohibited under the EU AI Act?"
- Retrieved the top 3 matching chunks.

### Results

The filter successfully restricted retrieval to chunks labeled `article`.

- **Rank 1:** Page 51, similarity 0.697 — contains the beginning of Article 5 on prohibited AI practices.
- **Rank 2:** Page 45, similarity 0.670 — discusses the scope of the regulation.
- **Rank 3:** Page 92, similarity 0.626 — less directly relevant to the question.

### Findings

Metadata filtering successfully narrowed the search space, but did not guarantee that every retrieved chunk was highly relevant.

The section classification also has limitations: 140 chunks were labeled `article`, 17 `annex`, and 606 `other`. Since section detection relies on text patterns within individual chunks, some relevant article content may not be labeled `article`.

**Conclusion:** Metadata filtering is useful for restricting retrieval to specific source categories, but it should complement semantic similarity and reranking rather than replace them.

## 4. Grounded RAG Evaluation

**Objective:** Evaluate whether the RAG pipeline generates accurate, relevant and source-grounded answers using retrieved documents, and whether Cohere reranking improves answer quality.

### Evaluation Setup

The evaluation used five predefined questions covering the EU AI Act and the Trustworthy AI podcast.

Two approaches were compared:

- **Baseline RAG:** Pinecone vector similarity search followed by answer generation.
- **Reranked RAG:** Pinecone retrieval followed by Cohere reranking and answer generation.

Both approaches used `gpt-4o-mini` for answer generation and included source references in the generated responses.

The evaluation consisted of five Pinecone searches, five Cohere reranking operations and ten generated answers.

### Results by Question

**Question 1: What AI practices are prohibited under the EU AI Act?**

Both approaches retrieved relevant evidence, including the beginning of Article 5, which addresses prohibited AI practices.

The baseline answer correctly identified manipulative and deceptive AI practices, but also included a broad statement about practices prohibited under other Union laws.

The reranked answer emphasized manipulative and exploitative practices, with references to the EU AI Act.

**Assessment:** Both answers were partially correct but incomplete. Reranking changed the supporting evidence without producing a comprehensive explanation of Article 5.

**Question 2: What are the seven requirements for trustworthy AI?**

Both approaches generated:

"I don't know based on the provided sources."

The retrieved context did not provide sufficient evidence for the model to confidently enumerate all seven requirements.

**Assessment:** This demonstrates appropriate abstention when retrieved evidence is insufficient. However, it also highlights a retrieval coverage limitation because the expected information was not successfully assembled.

**Question 3: What is the difference between human-in-the-loop and human-on-the-loop?**

Both approaches correctly explained that:

- Human-in-the-loop requires direct human approval of AI decisions or actions.
- Human-on-the-loop allows AI systems to operate with human monitoring and intervention when needed.

Both answers referenced the Trustworthy AI podcast.

**Assessment:** Both approaches produced accurate, relevant and grounded answers. Reranking did not create a substantial improvement.

**Question 4: What fines apply for using a prohibited AI practice?**

Both approaches correctly identified the maximum penalties:

- Up to €35 million.
- For undertakings, up to 7% of worldwide annual turnover for the preceding financial year, whichever is higher.

Both answers cited the EU AI Act, page 115, chunk `regulation-664`.

**Assessment:** Both approaches generated the same correct answer. Reranking did not improve the final result.

**Question 5: Is social scoring of citizens allowed?**

Both approaches identified the general prohibition of harmful social scoring practices under the EU AI Act.

The baseline answer cited page 51, chunk `regulation-343`.

The reranked answer cited page 9, chunk `regulation-60`.

**Assessment:** Both answers captured the general principle, but simplified the specific legal conditions of the prohibition. Reranking changed the supporting source without clearly improving answer accuracy.

### Overall RAG Assessment

The evaluation demonstrated that the pipeline can retrieve evidence from multiple document types and generate answers with source references.

However, source-grounded generation does not automatically guarantee completeness or legal precision.

The final answers depended strongly on the information available in the retrieved chunks.

Across the five questions, Cohere reranking did not demonstrate a consistent improvement in generated answer quality.

---

## 5. Limitations and Potential Improvements

### 5.1 Initial Retrieval Quality

Cohere can only reorder documents returned by the initial Pinecone retrieval.

If relevant evidence is missing from the candidate set, reranking cannot recover it.

**Potential improvement:** Experiment with larger candidate pools or hybrid retrieval combining vector similarity and keyword-based search.

### 5.2 Chunking Strategy

The pipeline used a fixed chunk size of 1,000 characters with 150 characters of overlap.

This approach is straightforward but does not preserve complete legal articles or semantic sections.

For example, one retrieved chunk contained the end of Article 4 and the beginning of Article 5.

**Potential improvement:** Introduce section-aware chunking that respects article boundaries and headings.

### 5.3 Metadata Classification

The current metadata detection uses text patterns within individual chunks.

The resulting distribution was:

- Article: 140 chunks
- Annex: 17 chunks
- Other: 606 chunks

Some chunks containing legal article content may be classified as `other` when their text does not include an explicit article heading.

**Potential improvement:** Detect document sections before splitting and propagate the section metadata to all related chunks.

### 5.4 Answer Completeness

The evaluation demonstrated that relevant retrieval results do not always produce complete answers.

The question about prohibited AI practices returned relevant evidence but incomplete summaries.

The question about the seven requirements for trustworthy AI resulted in abstention from both approaches.

**Potential improvement:** Improve retrieval coverage and consider retrieving adjacent chunks when answers require information spanning multiple sections.

### 5.5 Evaluation Scope

The evaluation was limited to five questions and qualitative answer comparisons.

No independently labeled relevance dataset was used to calculate metrics such as Precision@k, Recall@k, Mean Reciprocal Rank or NDCG.

Therefore, the evaluation supports qualitative observations but does not establish statistically significant improvements from reranking.

**Potential improvement:** Build a labeled evaluation dataset and measure retrieval relevance, answer faithfulness, completeness and latency across a broader set of queries.

### 5.6 API Cost Considerations

The pipeline uses paid API services for embeddings, reranking and answer generation.

To avoid unnecessary costs:

- Documents were indexed only once.
- The index was subsequently accessed in read-only mode.
- Initial retrieval candidates were reused for the first baseline-versus-reranking comparison.
- Automatic demonstrations and repeated evaluation were disabled.
- The final five-question evaluation was executed once.

The notebook retains the safe default settings:

`RUN_INDEXING=False`

`RUN_DEMOS=False`

---

## 6. Final Conclusion

This lab successfully implemented and evaluated a RAG pipeline combining:

- OpenAI embeddings
- Pinecone vector retrieval
- Cohere reranking
- Metadata filtering
- Source-grounded answer generation

A total of 783 document chunks were prepared and indexed from the EU AI Act and the Trustworthy AI podcast.

The baseline retrieval system successfully found relevant evidence for several test questions. Cohere reranking changed the ordering of retrieved candidates and sometimes promoted more relevant supporting material.

However, the results showed that **better document ordering does not necessarily lead to better final answers**.

The pipeline performed well for questions about human oversight, financial penalties and social scoring. It showed limitations in answer completeness and retrieval coverage for other questions.

Metadata filtering successfully restricted the search space, but could not guarantee relevance because its effectiveness depended on metadata classification quality.

### Main Takeaway

The central lesson of this lab is that the first retrieved match is not necessarily the best match, but reranking alone is not a complete solution.

Reliable RAG depends on the combined quality of document processing, chunking, embeddings, initial retrieval, metadata, reranking and grounded generation.

The final pipeline is functional, and the evaluation demonstrates both its capabilities and its limitations without assuming that reranking is always beneficial.