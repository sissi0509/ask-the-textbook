# Retrieval eval, 2026-10-07

43 cases (complex: 1, everyday: 14, term: 14, textbook: 14). Hit = a chunk from a gold section.

| Method | Recall@5 | Recall@10 | MRR | R@5 complex | R@5 everyday | R@5 term | R@5 textbook |
|---|---|---|---|---|---|---|---|
| hybrid | 93% | 93% | 0.89 | 100% | 86% | 100% | 93% |
| hybrid_rerank | 95% | 98% | 0.96 | 100% | 86% | 100% | 100% |

## Misses outside the top 5: hybrid (3)
- #3 How is linear momentum defined? (gold 9.1; got intro, intro, 13.5)
- #15 Why do I lean back when the bus suddenly starts? (gold 5.2; got 6.3, 6.2, 11.4)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 17.6; got 16.3, 15.1, 16.3)

## Misses outside the top 5: hybrid_rerank (2)
- #15 Why do I lean back when the bus suddenly starts? (gold 5.2; got 6.2, intro, 6.3)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 17.6; got 17.5, 15.1, 15.5)
