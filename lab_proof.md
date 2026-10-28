# Lab Proof: First match does not mean right match

## 1. What I built

A RAG pipeline over the supplied EU AI Act PDF and Trustworthy AI podcast compares baseline cosine retrieval, LLM relevance scoring, and a local MiniLM cross-encoder. The same ten candidates are used by both rerankers, and each method supplies five chunks to the same citation-based generation chain.

Implementation: [executed notebook](relevance_scoring_rerankers.ipynb). Full records: [experiment.json](artifacts/experiment.json). Readable results: [answers and evidence](artifacts/answers_and_evidence.md).

The corpus is a fixed snapshot: 144 PDF pages and the supplied transcript. Metadata captures source type, one-based PDF page, article/recital/annex, stable chunk ID, and exact podcast character offsets. The source hashes are in [sources.json](artifacts/sources.json).

## 2. Query

> What is the difference between human-in-the-loop and human-on-the-loop?

## 3. Retrieved evidence

The following is the baseline context actually supplied to the answer model. Scores are cosine similarities, not probabilities. Baseline is selected for this proof because both HITL and HOTL claims cite the passage containing their definitions. The cross-encoder answer is retained in the comparison, including its incorrect citation choice.

| Rank | Source | Page / chunk ID | Score | Snippet |
|---|---|---|---|---|
| 1 | Trustworthy AI podcast | chars 6775:7774 / `podcast-0008` | 0.5313 | human in command. It's a gradient of control. Let's break that down. Human in the loop. That's the tightest control. The AI makes a suggestion, but a human has to click approve for every single action. But let me play doubles advocate here. If you have an AI processing 10,000 loan applications an hour, is human in the loop even real? That's a huge risk. Or is the human just a rubber stamp because |
| 2 | Trustworthy AI podcast | chars 5927:6924 / `podcast-0007` | 0.3824 | crime data is biased, which it almost always is, you're violating fairness by targeting specific neighborhoods over and over. So it's a direct clash. Exactly. Does the potential for safety outweigh the certainty of surveillance and bias? The guidelines don't give a yes or no. They say this tension must be acknowledged, debated, and reasoned out. It can't just pretend the trade-off doesn't exist. T |
| 3 | EU AI Act (Reg. 2024/1689) | p.21 / `regulation-0168` | 0.3780 | (73) High-risk AI systems should be designed and developed in such a way that natural persons can oversee their functioning, ensure that they are used as intended and that their impacts are addressed over the system’s lifecycle. To that end, appropriate human oversight measures should be identified by the provider of the system before its placing on the market or putting into service. In partic |
| 4 | EU AI Act (Reg. 2024/1689) | p.21 / `regulation-0169` | 0.3749 | AI systems include mechanisms to guide and inform a natural person to whom human oversight has been assigned to make informed decisions if, when and how to intervene in order to avoid negative consequences or risks, or stop the system if it does not perform as intended. Considering the significant consequences for persons in the case of an incorrect match by certain biometric identification sys |
| 5 | EU AI Act (Reg. 2024/1689) | p.60 / `regulation-0445` | 0.3554 | Article 14 Human oversight 1. High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use. 2. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge when a high-risk AI sys |

Exact retrieved chunks:

### podcast-0008 (chars 6775:7774)

> human in command. It's a gradient of control. Let's break that down. Human in the loop. That's the tightest control. The AI makes a suggestion, but a human has to click approve for every single action. But let me play doubles advocate here. If you have an AI processing 10,000 loan applications an hour, is human in the loop even real? That's a huge risk. Or is the human just a rubber stamp because they can't possibly review that fast? It's called automation bias. The human just trust the machine too much or gets fatigued and just clicks. Yes, yes, yes. The guidelines warn about this. Just having a human sitting there isn't enough. They need to have the actual capacity to override the system. OK, so then you have human on the loop where the human monitors and just steps in if things look weird and human in command where the human decides when the system runs and when it dies, which brings up the stop button. Oh, yes, the big red button. The requirement explicitly mentions the capability

### podcast-0007 (chars 5927:6924)

> crime data is biased, which it almost always is, you're violating fairness by targeting specific neighborhoods over and over. So it's a direct clash. Exactly. Does the potential for safety outweigh the certainty of surveillance and bias? The guidelines don't give a yes or no. They say this tension must be acknowledged, debated, and reasoned out. It can't just pretend the trade-off doesn't exist. That moves us perfectly into the how theory is great, but engineers need requirements. They need specs. And chapter two of the source lists seven of them. This is really the meat of the document. This is the bridge between be ethical and right code. OK, requirement one is human agency and oversight. This goes back to autonomy. The document lists three different governance mechanisms, HITL, HOTL and HIC, human in the loop, human on the loop, and human in command. It's a gradient of control. Let's break that down. Human in the loop. That's the tightest control. The AI makes a suggestion, but a

### regulation-0168 (p.21)

> (73) High-risk AI systems should be designed and developed in such a way that natural persons can oversee their 
> functioning, ensure that they are used as intended and that their impacts are addressed over the system’s lifecycle. To 
> that end, appropriate human oversight measures should be identified by the provider of the system before its placing 
> on the market or putting into service. In particular, where appropriate, such measures should guarantee that the 
> system is subject to in-built operational constraints that cannot be overridden by the system itself and is responsive 
> to the human operator, and that the natural persons to whom human oversight has been assigned have the necessary 
> competence, training and authority to carry out that role. It is also essential, as appropriate, to ensure that high-risk 
> AI systems include mechanisms to guide and inform a natural person to whom human oversight has been assigned

### regulation-0169 (p.21)

> AI systems include mechanisms to guide and inform a natural person to whom human oversight has been assigned 
> to make informed decisions if, when and how to intervene in order to avoid negative consequences or risks, or stop 
> the system if it does not perform as intended. Considering the significant consequences for persons in the case of an 
> incorrect match by certain biometric identification systems, it is appropriate to provide for an enhanced human 
> oversight requirement for those systems so that no action or decision may be taken by the deployer on the basis of 
> the identification resulting from the system unless this has been separately verified and confirmed by at least two 
> natural persons. Those persons could be from one or more entities and include the person operating or using the 
> system. This requirement should not pose unnecessary burden or delays and it could be sufficient that the separate

### regulation-0445 (p.60)

> Article 14
> Human oversight
> 1. High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine 
> interface tools, that they can be effectively overseen by natural persons during the period in which they are in use.
> 2. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge 
> when a high-risk AI system is used in accordance with its intended purpose or under conditions of reasonably foreseeable 
> misuse, in particular where such risks persist despite the application of other requirements set out in this Section.
> 3. The oversight measures shall be commensurate with the risks, level of autonomy and context of use of the high-risk 
> AI system, and shall be ensured through either one or both of the following types of measures:
> (a) measures identified and built, when technically feasible, into the high-risk AI system by the provider before it is placed 
> on the market or put into service;

## 4. Observed final pipeline output

The text below is the saved model output. It remains subject to the author's grounding and completeness review.

Human-in-the-loop (HITL) is the tightest control where the AI makes a suggestion, but a human has to click approve for every single action. [podcast-0008 | Trustworthy AI podcast | chars 6775:7774]

Human-on-the-loop (HOTL) is where the human monitors the AI system and steps in if things look weird. [podcast-0008 | Trustworthy AI podcast | chars 6775:7774]

## 5. Trace

Citations are checked against the IDs actually supplied to the model. Full citation labels include the source and page. This mechanical check establishes location and context membership, not semantic support.

| Generated claim | Supporting chunk IDs selected by the model |
|---|---|
| Human-in-the-loop (HITL) is the tightest control where the AI makes a suggestion, but a human has to click approve for every single action. | `podcast-0008` |
| Human-on-the-loop (HOTL) is where the human monitors the AI system and steps in if things look weird. | `podcast-0008` |

| Cited chunk ID | Location | Source section | Evidence available for claim review |
|---|---|---|---|
| `podcast-0008` | chars 6775:7774 | transcript | human in command. It's a gradient of control. Let's break that down. Human in the loop. That's the tightest control. The AI makes a suggestion, but a human has to click approve for every single action. But let me play doubles advocate here. If you have an AI processing 10,000 loan applications an hour, is human in the loop even real? That's a huge risk. Or is the human just a rubber stamp because they can't possibly review that fast? It's called automation bias. The human just trust the machine too much or gets fatigued and just clicks. Yes, yes, yes. The guidelines warn about this. Just having a human sitting there isn't enough. They need to have the actual capacity to override the system. OK, so then you have human on the loop where the human monitors and just steps in if things look weird and human in command where the human decides when the system runs and when it dies, which brings up the stop button. Oh, yes, the big red button. The requirement explicitly mentions the capability |

Both definitions occur in `podcast-0008`: HITL requires approval for every action, while HOTL monitors and intervenes when needed. The author assessment remains pending. A citation to a real chunk can still be misleading if a condition or qualification is omitted. The complete evidence above and the original sources are available for review.

## 6. Baseline vs reranked

| Query | Method | Top-1 chunk | Top-1 changed | Top-5 overlap with baseline | Reranking seconds | Pipeline seconds |
|---|---|---|---|---|---|---|
| Q1 | baseline | `regulation-0398` | False | 5/5 | 0.000 | 2.891 |
| Q1 | llm_scoring | `regulation-0398` | False | 3/5 | 13.964 | 17.284 |
| Q1 | cross_encoder | `regulation-0398` | False | 4/5 | 0.350 | 3.386 |
| Q2 | baseline | `podcast-0002` | False | 5/5 | 0.000 | 1.533 |
| Q2 | llm_scoring | `regulation-0060` | True | 3/5 | 11.825 | 13.159 |
| Q2 | cross_encoder | `regulation-0060` | True | 2/5 | 0.392 | 1.850 |
| Q3 | baseline | `podcast-0008` | False | 5/5 | 0.000 | 1.782 |
| Q3 | llm_scoring | `podcast-0008` | False | 5/5 | 13.741 | 15.474 |
| Q3 | cross_encoder | `podcast-0008` | False | 2/5 | 0.440 | 2.022 |
| Q4 | baseline | `regulation-0398` | False | 5/5 | 0.000 | 2.589 |
| Q4 | llm_scoring | `regulation-0750` | True | 3/5 | 9.278 | 11.240 |
| Q4 | cross_encoder | `regulation-0750` | True | 3/5 | 0.349 | 2.319 |
| Q5 | baseline | `regulation-0071` | False | 5/5 | 0.000 | 2.481 |
| Q5 | llm_scoring | `regulation-0095` | True | 4/5 | 11.280 | 13.782 |
| Q5 | cross_encoder | `regulation-0072` | True | 5/5 | 0.368 | 2.709 |

The pipeline timing combines shared candidate retrieval, method-specific reranking, and answer generation. Cached LLM scores use their original recorded API-call durations rather than cache-lookup time. Cross-encoder loading is reported separately. Changes in order and top-5 membership do not by themselves demonstrate better answers.

- llm_scoring: top-1 changed for 3/5 queries; mean reranking time 12.017 seconds.
- cross_encoder: top-1 changed for 3/5 queries; mean reranking time 0.380 seconds.
- LLM scoring calls in this run: 0; cached scoring responses: 50.
- Cross-encoder model loading: 0.874 seconds, separate from per-query ranking.
- Answer-generation calls: 18 (15 comparison outputs, 2 filtered outputs, 1 unsupported-query output).

A fresh run scores 50 query/chunk pairs with the LLM. The dedicated reranker scores those pairs locally with no scoring API calls. Actual charges depend on token usage and provider pricing; this report makes no unsupported dollar-cost estimate. Client value remains dependent on the pending correctness and grounding review.

### Observed answer-level regressions

- Q4: both rerankers promote `regulation-0750` (Article 99, p.115) from rank 3 to rank 1. The baseline answer already uses that third-ranked evidence. Both reranked answers additionally present the EUR 1.5 million figure from `regulation-0758` without identifying the separate Union-institution scope of Article 100. The order improves, but this generated answer does not.
- Q3: the cross-encoder keeps `podcast-0008` at rank 1, but its generated answer cites `podcast-0007` for both definitions. That earlier chunk stops before the HITL approval explanation and contains no HOTL definition. This is a citation-grounding failure despite valid IDs.
- Q5: LLM scoring promotes `regulation-0095`, a recital about predicted offending and profiling, above the social-scoring evidence. Its answer also imports the significant-harm condition from an adjacent part of Article 5.
- Q1: the retrieved Article 5 fragment ends partway through point (b), and generated answers omit much of the prohibited-practices list. The LLM-scored answer also attributes a criminal-risk claim to a chunk that does not contain it. A relevant top result does not establish completeness.

These are AI-assisted review observations based on saved outputs and exact chunks, not completed author assessments. [review_notes.md](review_notes.md) summarizes the checks.

### Metadata filtering

The basic schema contains no structural fields. An Article 5 filter returns zero matches there; the enriched namespace supplies that field and returns matching Article 5 chunks. Both namespaces use the same cached embeddings and stable IDs, so the demonstration isolates schema enrichment without deleting an index.

Observed matches: basic schema 0; enriched schema 5.

The source-filter experiment asks the same social-scoring question once against the regulation and once against the podcast. Both answers are saved in the readable results. The author review distinguishes statutory conditions from ethical commentary; the sources are not interchangeable.

### Manual evaluation status

[manual_evaluation.csv](manual_evaluation.csv) contains 15 rows covering the five fixed queries and three methods. Top-1 relevance, answer correctness, grounding, and notes remain unfilled pending the author's assessment. No human judgment or quality improvement is fabricated.

## 7. Failure or limitation

Unsupported query: What exact amount did the private company BlueFox Robotics spend on GPU hosting in March 2026?

Observed response: I do not know based on the sources.

Observed abstention: True.

Reranking cannot retrieve a missing candidate. A five-chunk context can omit part of a multi-part answer, especially the seven requirements dispersed across the podcast. A model can then supply a plausible list from prior knowledge despite a citation-based prompt. Citation membership checks cannot detect that failure.

The legal corpus is the supplied 2024 PDF, not a verified current consolidated regulation. Recitals, binding articles, and an informal podcast have different evidentiary roles. PDF extraction and heading heuristics can also introduce boundary errors, so exact source locations are preserved.

## 8. Reproducibility

The notebook uses `.env` credentials, excludes secrets from saved outputs, and retains complete evidence. [requirements-lock.txt](requirements-lock.txt) records the executed environment. Repeated uploads use stable IDs in corpus-specific namespaces. Local embedding and relevance caches are ignored by Git.
