# Lab Proof: First match ≠ right match

## 1. What I built

I built a RAG workflow using a podcast transcript about Trustworthy AI and the EU AI Act PDF. It uses OpenAI embeddings and Pinecone to retrieve text chunks with source metadata and filters. I compared baseline retrieval with Cohere reranking and checked whether the generated answers were supported by the cited passages.

[Notebook](relevance_scoring_rerankers.ipynb)

## 2. Query

What fines apply for using a prohibited AI practice?

## 3. Retrieved evidence

| Method | Rank | Chunk ID | Page | Score |
|---|---:|---|---:|---:|
| Baseline | 1 | regulation-346 | 51 | 0.6700 |
| Baseline | 3 | regulation-700 | 115 | 0.6298 |
| Cohere reranked | 1 | regulation-700 | 115 | 0.8077 |
| Cohere reranked | 2 | regulation-708 | 117 | 0.7975 |

Similarity scores and reranker scores use different scales and are
not directly comparable.


#1 | Score: 0.8077
{'article': 99.0, 'chunk_id': 'regulation-700', 'page': 115.0, 'section': 'article', 'source_name': 'EU AI Act (Reg. 2024/1689)', 'source_type': 'regulation'}
any subsequent amendment to them.
3. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative 
fines of up to EUR 35 000 000 or, if the offender is an undertaking, up to 7 % of its total worldwide annual turnover for the 
preceding financial year, whichever is higher.
4. Non-compliance with any of the following provisions related to operators or notified bodies, other than those laid 
down in Articles 5, shall be subject to administrative fines of up to EUR 15 000 000 or, if the offender is an undertaking, up 
to 3 % of its total worldwide annual turnover for the preceding financial year, whichever is higher:
(a) obligations of providers pursuant to Article 16;
(b) obligations of authorised representatives pursuant to Article 22;
(c) obligations of importers pursuant to Article 23;
(d) obligations of distributors pursuant to Article 24;
(e) obligations of deployers pursuant to Article 26;

#2 | Score: 0.7975
{'article': 100.0, 'chunk_id': 'regulation-708', 'page': 117.0, 'section': 'article', 'source_name': 'EU AI Act (Reg. 2024/1689)', 'source_type': 'regulation'}
with regard to the same subject matter;
(e) any similar previous infringements by the Union institution, body, office or agency;
(f) the manner in which the infringement became known to the European Data Protection Supervisor, in particular 
whether, and if so to what extent, the Union institution, body, office or agency notified the infringement;
(g) the annual budget of the Union institution, body, office or agency.
2. Non-compliance with the prohibition of the AI practices referred to in Article 5 shall be subject to administrative 
fines of up to EUR 1 500 000.
3. The non-compliance of the AI system with any requirements or obligations under this Regulation, other than those 
laid down in Article 5, shall be subject to administrative fines of up to EUR 750 000.
4. Before taking decisions pursuant to this Article, the European Data Protection Supervisor shall give the Union


## 4. Final output — preserved model responses

### Baseline

=== Baseline ===
Non-compliance with the prohibition of AI practices referred to in Article 5 shall be subject to administrative fines of up to EUR 35,000,000 or, if the offender is an undertaking, up to 7% of its total worldwide annual turnover for the preceding financial year, whichever is higher [EU AI Act (Reg. 2024/1689), p.115, regulation-700].


### Cohere reranked

=== Cohere reranked ===
The fines for using a prohibited AI practice, as outlined in Article 5 of the EU AI Act, depend on the nature of the infringement. Non-compliance with the prohibition of the AI practices referred to in Article 5 is subject to administrative fines of up to EUR 35,000,000 or, if the offender is an undertaking, up to 7% of its total worldwide annual turnover for the preceding financial year, whichever is higher [EU AI Act (Reg. 2024/1689), p.115, regulation-700]. 

Additionally, if the infringement is identified by a Union institution, body, office, or agency, the fines for non-compliance with the prohibition of the AI practices referred to in Article 5 are capped at EUR 1,500,000 [EU AI Act (Reg. 2024/1689), p.117, regulation-708].

## 5. Trace

| Output claim | Evidence | Verification |
|---|---|---|
| Both answers report fines of up to EUR 35,000,000 or, for an undertaking, up to 7% of its worldwide annual turnover for the preceding financial year, whichever is higher. | regulation-700, page 115, Article 99(3) | The passage supports these limits. This does not establish complete coverage of all exceptions or other applicable provisions. |
| The reranked answer says the EUR 1,500,000 limit applies when a Union institution identifies an infringement. | regulation-708, page 117; regulation-706, page 116 | This interpretation is incorrect. Article 100 concerns fines imposed on Union institutions, bodies, offices and agencies, not infringements identified by them. |

### Additional evidence used to verify the error

The following passage was retrieved after reviewing the generated answers.
It was used for verification and was not added to their original context.

 {'article': 100.0, 'chunk_id': 'regulation-706', 'page': 116.0, 'section': 'article', 'source_name': 'EU AI Act (Reg. 2024/1689)', 'source_type': 'regulation'}
Article 100
Administrative fines on Union institutions, bodies, offices and agencies
1. The European Data Protection Supervisor may impose administrative fines on Union institutions, bodies, offices and 
agencies falling within the scope of this Regulation. When deciding whether to impose an administrative fine and when 
deciding on the amount of the administrative fine in each individual case, all relevant circumstances of the specific situation 
shall be taken into account and due regard shall be given to the following:
EN OJ L, 12.7.2024
116/144 ELI: http://data.europa.eu/eli/reg/2024/1689/oj

The original model responses are preserved unchanged.

## 6. Baseline vs reranked

The chunk regulation-700 moved from rank 3 to rank 1 after reranking.
Both generated answers used this passage.

The reranked answer also added an incorrect interpretation of
Article 100. In this example, improving the first result did not
produce a better answer.

The Cohere reranking call took 0.20 seconds. This measurement
excludes retrieval and answer generation.

## 7. Failure or limitation

A better retrieval order does not guarantee a correct answer.
A relevant chunk may not include the heading that explains
who the rule applies to.

In this example, the model cited a relevant passage but
misinterpreted its scope. Checking citations alone is therefore
not enough: the claims must also be checked against the source
and its surrounding context.