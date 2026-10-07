# Retrieval eval, 2026-10-07

55 cases (complex: 1, everyday: 20, term: 17, textbook: 17). Hit = a chunk from a gold section.

| Method | Recall@5 | Recall@10 | MRR | R@5 complex | R@5 everyday | R@5 term | R@5 textbook | R@5 vol 1 | R@5 vol 2 | R@5 vol 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| vector | 95% | 95% | 0.90 | 100% | 85% | 100% | 100% | 93% | 100% | 100% |
| keyword | 73% | 82% | 0.52 | 100% | 55% | 94% | 71% | 72% | 67% | 83% |
| hybrid | 91% | 93% | 0.82 | 100% | 85% | 100% | 88% | 91% | 83% | 100% |
| vector_rerank | 98% | 98% | 0.94 | 100% | 95% | 100% | 100% | 98% | 100% | 100% |
| hybrid_rerank | 95% | 98% | 0.93 | 100% | 85% | 100% | 100% | 93% | 100% | 100% |

## Misses outside the top 5: vector (3)
- #19 Why does a gun kick back when it is fired? (gold 1:9.3/1:9.4; got 2:13.3, 3:8.6, 1:15.2)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:15.1, 1:15.5, 1:16.3)
- #27 Why does water come out faster when I put my thumb over the end of a garden hose? (gold 1:14.5; got 1:14.6, 1:14.7, 1:6.4)

## Misses outside the top 5: keyword (15)
- #1 What does Newton's second law state? (gold 1:5.3; got 1:10.7, 1:1.1, 3:6.4)
- #3 How is linear momentum defined? (gold 1:9.1; got 1:intro, 3:5.9, 1:11.2)
- #8 What are Kepler's laws of planetary motion? (gold 1:13.5; got 1:13.1, 1:1.1, 1:intro)
- #13 What determines the speed of a wave on a stretched string? (gold 1:16.3; got 1:17.2, 1:16.1, 1:16.1)
- #15 Why do I lean back when the bus suddenly starts? (gold 1:5.2/1:6.3; got 1:6.2, 2:13.6, 1:8.2)
- #19 Why does a gun kick back when it is fired? (gold 1:9.3/1:9.4; got 2:13.3, 2:13.6, 2:13.6)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:16.3, 1:16.4, 1:16.3)
- #24 Why does a skydiver stop speeding up after falling for a while? (gold 1:6.4; got 1:17.2, 2:2.4, 1:17.2)
- #25 Why does a grandfather clock with a swinging weight keep regular time? (gold 1:15.4; got 3:5.2, 1:3.4, 3:5.3)
- #26 How can a rocket move forward in empty space with nothing to push against? (gold 1:9.7; got 1:5.5, 1:6.2, 1:13.7)
- #27 Why does water come out faster when I put my thumb over the end of a garden hose? (gold 1:14.5; got 2:1.3, 1:17.4, 3:10.5)
- #41 Reynolds number (gold 1:14.7; got 3:11.2, 3:11.2, 3:11.2)
- #45 Why do I get a small shock when I touch a doorknob after walking across a carpet? (gold 2:5.1/2:5.2; got 1:1.5, 2:10.6, 1:6.2)
- #49 What is Faraday's law of induction? (gold 2:13.1; got 2:16.1, 1:1.1, 2:intro)
- #50 Why does a straw look bent when it stands in a glass of water? (gold 3:1.3/3:2.3; got 2:1.3, 3:9.4, 2:1.5)

## Misses outside the top 5: hybrid (5)
- #3 How is linear momentum defined? (gold 1:9.1; got 1:intro, 1:intro, 1:13.5)
- #19 Why does a gun kick back when it is fired? (gold 1:9.3/1:9.4; got 2:13.3, 2:13.6, 2:13.6)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:16.3, 1:17.4, 1:15.1)
- #25 Why does a grandfather clock with a swinging weight keep regular time? (gold 1:15.4; got 3:5.3, 3:5.2, 3:5.3)
- #49 What is Faraday's law of induction? (gold 2:13.1; got 2:13.3, 2:16.1, 2:intro)

## Misses outside the top 5: vector_rerank (1)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:17.5, 1:15.1, 1:15.5)

## Misses outside the top 5: hybrid_rerank (3)
- #15 Why do I lean back when the bus suddenly starts? (gold 1:5.2/1:6.3; got 1:6.2, 2:13.6, 2:10.2)
- #19 Why does a gun kick back when it is fired? (gold 1:9.3/1:9.4; got 2:13.3, 1:5.5, 2:13.6)
- #23 Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound? (gold 1:17.6; got 1:17.5, 1:15.1, 1:15.5)
