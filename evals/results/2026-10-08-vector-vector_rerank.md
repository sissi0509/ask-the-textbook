# Retrieval eval, 2026-10-08

55 cases (complex: 1, everyday: 20, term: 17, textbook: 17). Hit = a chunk from a gold section.
By topic: Mechanics: 34, Oscillations & Waves: 9, Thermodynamics: 3, Electricity & Magnetism: 3, Optics: 2, Modern Physics: 4.

| Method | Recall@5 | Recall@10 | MRR | R@5 complex | R@5 everyday | R@5 term | R@5 textbook | R@5 vol 1 | R@5 vol 2 | R@5 vol 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| vector | 95% | 95% | 0.90 | 100% | 85% | 100% | 100% | 93% | 100% | 100% |
| vector_rerank | 98% | 98% | 0.94 | 100% | 95% | 100% | 100% | 98% | 100% | 100% |

## Recall@5 by topic

| Method | Mechanics | Oscillations & Waves | Thermodynamics | Electricity & Magnetism | Optics | Modern Physics |
|---|---|---|---|---|---|---|
| vector | 94% | 89% | 100% | 100% | 100% | 100% |
| vector_rerank | 100% | 89% | 100% | 100% | 100% | 100% |

## Misses outside the top 5: vector (3)
- #19 Why does a gun kick back when it is fired? (gold 1:9.3/1:9.4; got 2:13.3, 3:8.6, 1:15.2)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:15.1, 1:15.5, 1:16.3)
- #27 Why does water come out faster when I put my thumb over the end of a garden hose? (gold 1:14.5; got 1:14.6, 1:14.7, 1:6.4)

## Misses outside the top 5: vector_rerank (1)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:17.5, 1:15.1, 1:15.5)
