# Retrieval eval, 2026-10-14

55 cases (complex: 1, everyday: 20, term: 17, textbook: 17). Hit = a chunk from a gold section.
By topic: Mechanics: 34, Oscillations & Waves: 9, Thermodynamics: 3, Electricity & Magnetism: 3, Optics: 2, Modern Physics: 4.

| Method | Recall@5 | Recall@10 | MRR | R@5 complex | R@5 everyday | R@5 term | R@5 textbook | R@5 vol 1 | R@5 vol 2 | R@5 vol 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| bm25 | 91% | 95% | 0.82 | 100% | 90% | 94% | 88% | 91% | 83% | 100% |
| hybrid | 91% | 93% | 0.82 | 100% | 85% | 100% | 88% | 91% | 83% | 100% |
| hybrid_bm25 | 95% | 96% | 0.85 | 100% | 90% | 100% | 94% | 93% | 100% | 100% |
| vector_rerank | 98% | 98% | 0.94 | 100% | 95% | 100% | 100% | 98% | 100% | 100% |
| hybrid_rerank | 95% | 98% | 0.93 | 100% | 85% | 100% | 100% | 93% | 100% | 100% |
| hybrid_bm25_rerank | 96% | 98% | 0.94 | 100% | 90% | 100% | 100% | 95% | 100% | 100% |

## Recall@5 by topic

| Method | Mechanics | Oscillations & Waves | Thermodynamics | Electricity & Magnetism | Optics | Modern Physics |
|---|---|---|---|---|---|---|
| bm25 | 91% | 89% | 100% | 67% | 100% | 100% |
| hybrid | 94% | 78% | 100% | 67% | 100% | 100% |
| hybrid_bm25 | 94% | 89% | 100% | 100% | 100% | 100% |
| vector_rerank | 100% | 89% | 100% | 100% | 100% | 100% |
| hybrid_rerank | 94% | 89% | 100% | 100% | 100% | 100% |
| hybrid_bm25_rerank | 97% | 89% | 100% | 100% | 100% | 100% |

## Misses outside the top 5: bm25 (5)
- #3 How is linear momentum defined? (gold 1:9.1; got 1:11.2, 1:12.1, 1:11.2)
- #15 Why do I lean back when the bus suddenly starts? (gold 1:5.2/1:6.3; got 2:10.3, 1:7.1, 1:15.2)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:16.3, 1:16.3, 2:16.5)
- #40 Fermi estimate (gold 1:1.5; got 3:9.4, 3:9.4, 3:9.4)
- #49 What is Faraday's law of induction? (gold 2:13.1; got 2:13.7, 2:13.2, 2:13.3)

## Misses outside the top 5: hybrid (5)
- #3 How is linear momentum defined? (gold 1:9.1; got 1:intro, 1:intro, 1:13.5)
- #19 Why does a gun kick back when it is fired? (gold 1:9.3/1:9.4; got 2:13.3, 2:13.6, 2:13.6)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:16.3, 1:17.4, 1:15.1)
- #25 Why does a grandfather clock with a swinging weight keep regular time? (gold 1:15.4; got 3:5.3, 3:5.2, 3:5.3)
- #49 What is Faraday's law of induction? (gold 2:13.1; got 2:13.3, 2:16.1, 2:intro)

## Misses outside the top 5: hybrid_bm25 (3)
- #3 How is linear momentum defined? (gold 1:9.1; got 1:11.2, 1:9.6, 1:intro)
- #15 Why do I lean back when the bus suddenly starts? (gold 1:5.2/1:6.3; got 1:11.4, 1:15.5, 2:13.6)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:16.3, 1:15.1, 1:16.3)

## Misses outside the top 5: vector_rerank (1)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:17.5, 1:15.1, 1:15.5)

## Misses outside the top 5: hybrid_rerank (3)
- #15 Why do I lean back when the bus suddenly starts? (gold 1:5.2/1:6.3; got 1:6.2, 2:13.6, 2:10.2)
- #19 Why does a gun kick back when it is fired? (gold 1:9.3/1:9.4; got 2:13.3, 1:5.5, 2:13.6)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:17.5, 1:15.1, 1:15.5)

## Misses outside the top 5: hybrid_bm25_rerank (2)
- #15 Why do I lean back when the bus suddenly starts? (gold 1:5.2/1:6.3; got 2:13.6, 2:10.2, 1:intro)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:17.5, 1:15.1, 1:15.5)
