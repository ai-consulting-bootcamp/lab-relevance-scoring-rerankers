# Grounding review notes

This is a final review of the observed experiment. It supports the manual evaluation and does not replace it. All raw answers remain in `artifacts/experiment.json` and `artifacts/answers_and_evidence.md`.

## Three grounding risks

1. **A correct source ID can still be the wrong evidence.** The Q3 cross-encoder answer cites `podcast-0007` for both HITL and HOTL definitions. That chunk ends before the approval-per-action explanation and contains no HOTL monitoring definition. Both definitions are in `podcast-0008`, which was ranked first. The baseline and LLM-scored answers cite that supporting chunk correctly. ID validation passes the cross-encoder response, but semantic grounding does not.
2. **A matching number can lose its scope.** For Q4, both reranked answers add the EUR 1.5 million figure from `regulation-0758` (Article 100, p.117) without distinguishing the Union-institution scope from Article 99's general regime. The baseline answer uses `regulation-0750` (Article 99(3), p.115). Reranking moves the Article 99 evidence from third to first, yet the generated answer becomes less precise. Qualifications elsewhere in Article 99 also require attention.
3. **Chunk boundaries and topical overlap distort completeness.** Q1 uses an Article 5 chunk that cuts off during point (b), so a relevant top result still fails to cover the full prohibited-practices list. The LLM-scored answer adds a criminal-risk claim with an unsupported citation to `regulation-0398`. For Q5, LLM scoring promotes `regulation-0095`, about predicted offending, rather than the social-scoring passage. The answer mixes a significant-harm condition from another part of Article 5 into social scoring.

## Two trace checks

- The selected proof uses Q3's baseline answer. Both claims map to `podcast-0008`, and the original transcript slice `[6775:7774]` reproduces that chunk exactly. The comparison preserves the cross-encoder's unsupported `podcast-0007` citations instead of rewriting its observed answer.
- The Article 5 filter returns no matches in the basic namespace and five matches in the enriched namespace. Each enriched result has `source_type=regulation`, `section=article`, and `article=Article 5`. Source hashes, complete candidate pools, score components, and source coordinates are saved independently of the prose proof.

## One simplification

Baseline retrieval remains a reasonable default for this small corpus when it already supplies the needed evidence. The local cross-encoder is faster than the LLM scorer in this run, but adding ranking complexity is not justified solely by a changed top result. A focused claim-to-evidence review and preserving article scope address the observed failures more directly than another reranking layer.

## Assessment status

The unsupported-company question produced the exact abstention response. All five queries completed under all three methods. The author's top-1 relevance, correctness, and grounding ratings remain pending in `manual_evaluation.csv`; no human-rated success rate is claimed.
