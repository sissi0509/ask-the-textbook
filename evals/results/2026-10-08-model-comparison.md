# Model comparison, 2026-10-08

55 cases. Hit = a chunk from a gold section. Reranking re-sorts the top 30 vector results. Time = average per question on this machine.

| Embedding model | Reranker | Recall@5 | Recall@10 | MRR | ms / question |
|---|---|---|---|---|---|
| bge-small-en-v1.5 | none | 95% | 95% | 0.90 | 52 |
| bge-small-en-v1.5 | ms-marco-MiniLM-L-6-v2 | 98% | 98% | 0.94 | 422 |
| bge-small-en-v1.5 | ms-marco-MiniLM-L-12-v2 | 98% | 100% | 0.94 | 670 |
| bge-base-en-v1.5 | none | 93% | 95% | 0.92 | 51 |
| bge-base-en-v1.5 | ms-marco-MiniLM-L-6-v2 | 96% | 98% | 0.94 | 359 |
| bge-base-en-v1.5 | ms-marco-MiniLM-L-12-v2 | 96% | 98% | 0.93 | 709 |
| all-MiniLM-L6-v2 | none | 96% | 100% | 0.90 | 60 |
| all-MiniLM-L6-v2 | ms-marco-MiniLM-L-6-v2 | 98% | 100% | 0.94 | 333 |
| all-MiniLM-L6-v2 | ms-marco-MiniLM-L-12-v2 | 100% | 100% | 0.94 | 591 |
