# Retrieval eval, 2026-10-07

43 cases (complex: 1, everyday: 14, term: 14, textbook: 14). Hit = a chunk from a gold section.

| Method | Recall@5 | Recall@10 | MRR | R@5 complex | R@5 everyday | R@5 term | R@5 textbook |
|---|---|---|---|---|---|---|---|
| vector | 93% | 95% | 0.91 | 100% | 79% | 100% | 100% |
| keyword | 81% | 86% | 0.55 | 100% | 57% | 100% | 86% |
| hybrid | 95% | 95% | 0.90 | 100% | 93% | 100% | 93% |
| vector_rerank | 98% | 98% | 0.97 | 100% | 93% | 100% | 100% |
| hybrid_rerank | 98% | 100% | 0.96 | 100% | 93% | 100% | 100% |

## Misses outside the top 5: vector (3)
- #19 Why does a gun kick back when it is fired? (gold 9.3/9.4; got 15.2, 9.7, 5.5)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 17.6; got 15.1, 15.5, 16.3)
- #27 Why does water come out faster when I put my thumb over the end of a garden hose? (gold 14.5; got 14.6, 14.7, 6.4)

## Misses outside the top 5: keyword (8)
- #3 How is linear momentum defined? (gold 9.1; got intro, 11.2, 9.3)
- #13 What determines the speed of a wave on a stretched string? (gold 16.3; got 17.2, 16.1, 16.2)
- #15 Why do I lean back when the bus suddenly starts? (gold 5.2/6.3; got 6.2, 15.2, 8.2)
- #19 Why does a gun kick back when it is fired? (gold 9.3/9.4; got 15.2, 8.1, 8.2)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 17.6; got 16.3, 16.4, 16.3)
- #24 Why does a skydiver stop speeding up after falling for a while? (gold 6.4; got 17.2, 17.2, 13.7)
- #25 Why does a grandfather clock with a swinging weight keep regular time? (gold 15.4; got 3.4, 5.4, 5.6)
- #26 How can a rocket move forward in empty space with nothing to push against? (gold 9.7; got 5.5, 6.2, 13.7)

## Misses outside the top 5: hybrid (2)
- #3 How is linear momentum defined? (gold 9.1; got intro, 13.5, intro)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 17.6; got 16.3, 15.1, 17.4)

## Misses outside the top 5: vector_rerank (1)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 17.6; got 17.5, 15.1, 15.5)

## Misses outside the top 5: hybrid_rerank (1)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 17.6; got 17.5, 15.1, 15.5)
