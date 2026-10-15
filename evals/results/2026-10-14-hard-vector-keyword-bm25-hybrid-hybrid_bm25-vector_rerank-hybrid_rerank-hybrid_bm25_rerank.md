# Retrieval eval, 2026-10-14 (`retrieval_cases_hard.jsonl`)

55 cases (everyday: 34, term: 21). Hit = a chunk from a gold section.
By topic: Mechanics: 11, Oscillations & Waves: 1, Thermodynamics: 12, Electricity & Magnetism: 13, Optics: 11, Modern Physics: 7.

| Method | Recall@5 | Recall@10 | MRR | R@5 everyday | R@5 term | R@5 vol 1 | R@5 vol 2 | R@5 vol 3 |
|---|---|---|---|---|---|---|---|---|
| vector | 89% | 93% | 0.81 | 88% | 90% | 83% | 96% | 83% |
| keyword | 60% | 75% | 0.44 | 53% | 71% | 58% | 64% | 56% |
| bm25 | 95% | 95% | 0.83 | 91% | 100% | 100% | 92% | 94% |
| hybrid | 87% | 91% | 0.73 | 85% | 90% | 92% | 84% | 89% |
| hybrid_bm25 | 96% | 98% | 0.86 | 94% | 100% | 100% | 92% | 100% |
| vector_rerank | 96% | 100% | 0.85 | 94% | 100% | 92% | 96% | 100% |
| hybrid_rerank | 95% | 98% | 0.84 | 91% | 100% | 92% | 92% | 100% |
| hybrid_bm25_rerank | 96% | 100% | 0.85 | 94% | 100% | 92% | 96% | 100% |

## Recall@5 by topic

| Method | Mechanics | Oscillations & Waves | Thermodynamics | Electricity & Magnetism | Optics | Modern Physics |
|---|---|---|---|---|---|---|
| vector | 82% | 100% | 100% | 92% | 82% | 86% |
| keyword | 55% | 100% | 75% | 54% | 36% | 86% |
| bm25 | 100% | 100% | 92% | 92% | 91% | 100% |
| hybrid | 91% | 100% | 92% | 77% | 82% | 100% |
| hybrid_bm25 | 100% | 100% | 92% | 92% | 100% | 100% |
| vector_rerank | 91% | 100% | 92% | 100% | 100% | 100% |
| hybrid_rerank | 91% | 100% | 92% | 92% | 100% | 100% |
| hybrid_bm25_rerank | 91% | 100% | 92% | 100% | 100% | 100% |

## Misses outside the top 5: vector (6)
- #111 Bragg's law (gold 3:4.6; got 1:12.4, 3:6.5, 3:8.5)
- #118 work function (gold 3:6.2; got 1:7.1, 1:7.1, 1:10.8)
- #137 Why do road signs shine so brightly in my headlights at night? (gold 3:1.2; got 2:16.5, 2:10.2, 2:16.5)
- #143 Why does a hot air balloon rise? (gold 1:14.4; got 2:1.3, 2:1.3, 2:1.6)
- #145 What makes the northern lights glow? (gold 2:11.3; got 3:6.1, 2:16.5, 2:16.5)
- #152 Why does the water push harder on me the deeper I swim in a pool? (gold 1:14.1; got 1:intro, 1:14.6, 1:5.5)

## Misses outside the top 5: keyword (22)
- #101 Hall voltage (gold 2:11.6; got 3:9.6, 2:15.1, 2:9.4)
- #106 Brewster's angle (gold 3:1.7; got 3:1.4, 1:2.2, 3:2.2)
- #107 Malus's law (gold 3:1.7; got 1:1.1, 2:intro, 2:16.1)
- #109 RC time constant (gold 2:10.5; got 1:17.2, 3:5.2, 3:5.5)
- #111 Bragg's law (gold 3:4.6; got 1:1.1, 2:intro, 2:16.1)
- #118 work function (gold 3:6.2; got 3:7.1, 1:7.1, 1:3.6)
- #123 Why do bridges have little gaps built into the road? (gold 2:1.3; got 3:9.5, 1:11.1, 1:15.6)
- #127 Why does most of an iceberg hide under the water? (gold 1:14.4; got 2:1.3, 3:10.5, 2:1.5)
- #130 How do fishing sunglasses let you see into the water without the shine on top? (gold 3:1.7; got 2:1.3, 2:1.5, 3:2.3)
- #131 Why can't I read the board from the back of the classroom, and what kind of glasses fix it? (gold 3:2.5; got 1:5.2, 1:intro, 3:9.4)
- #133 Why do I get zapped by the doorknob after shuffling across the rug? (gold 2:5.1; got 1:1.5, 1:6.2, 2:10.2)
- #136 How can doctors look inside your stomach with a thin bendy tube? (gold 3:1.4; got 3:2.4, 1:17.5, 1:17.5)
- #137 Why do road signs shine so brightly in my headlights at night? (gold 3:1.2; got 1:11.1, 1:17.7, 3:2.2)
- #138 Why do I feel heavier for a second when the elevator starts going up? (gold 1:6.1; got 1:6.3, 1:3.3, 1:10.7)
- #139 Why do astronauts on the space station float around? (gold 1:13.4/1:5.4; got 1:13.7, 3:5.3, 2:5.4)
- #143 Why does a hot air balloon rise? (gold 1:14.4; got 2:1.3, 2:1.6, 2:1.6)
- #144 How does an induction stove heat the pan without getting hot itself? (gold 2:13.5; got 2:4.2, 2:1.6, 2:1.5)
- #145 What makes the northern lights glow? (gold 2:11.3; got 2:16.1, 2:9.5, 3:1.7)
- #147 What part of sunlight gives you a sunburn? (gold 2:16.5; got 1:14.2, 3:2.4, 1:16.6)
- #148 Why is the grass wet in the early morning even when it didn't rain? (gold 2:2.2/2:1.5; got 3:7.1, 3:11.7, 3:6.4)
- #152 Why does the water push harder on me the deeper I swim in a pool? (gold 1:14.1; got 2:1.3, 1:5.5, 1:6.2)
- #154 How does a fridge keep the inside cold while the back of it feels warm? (gold 2:4.3; got 2:6.4, 2:13.6, 2:1.6)

## Misses outside the top 5: bm25 (3)
- #131 Why can't I read the board from the back of the classroom, and what kind of glasses fix it? (gold 3:2.5; got 1:1.7, 1:16.2, 3:3.1)
- #144 How does an induction stove heat the pan without getting hot itself? (gold 2:13.5; got 2:1.6, 2:4.4, 2:4.4)
- #148 Why is the grass wet in the early morning even when it didn't rain? (gold 2:2.2/2:1.5; got 3:11.7, 1:3.4, 3:11.7)

## Misses outside the top 5: hybrid (7)
- #101 Hall voltage (gold 2:11.6; got 3:9.6, 2:9.4, 2:15.1)
- #111 Bragg's law (gold 3:4.6; got 3:1.3, 3:6.5, 1:5.3)
- #136 How can doctors look inside your stomach with a thin bendy tube? (gold 3:1.4; got 1:17.5, 1:17.4, 1:17.5)
- #143 Why does a hot air balloon rise? (gold 1:14.4; got 2:1.3, 2:1.6, 2:1.6)
- #144 How does an induction stove heat the pan without getting hot itself? (gold 2:13.5; got 2:1.6, 2:1.6, 2:intro)
- #145 What makes the northern lights glow? (gold 2:11.3; got 3:intro, 3:8.5, 2:16.5)
- #148 Why is the grass wet in the early morning even when it didn't rain? (gold 2:2.2/2:1.5; got 2:1.6, 1:7.1, 1:14.7)

## Misses outside the top 5: hybrid_bm25 (2)
- #144 How does an induction stove heat the pan without getting hot itself? (gold 2:13.5; got 2:1.6, 2:1.6, 2:1.6)
- #148 Why is the grass wet in the early morning even when it didn't rain? (gold 2:2.2/2:1.5; got 1:7.1, 2:1.6, 1:14.7)

## Misses outside the top 5: vector_rerank (2)
- #148 Why is the grass wet in the early morning even when it didn't rain? (gold 2:2.2/2:1.5; got 2:1.6, 1:intro, 1:14.7)
- #152 Why does the water push harder on me the deeper I swim in a pool? (gold 1:14.1; got 1:5.5, 1:6.4, 1:6.2)

## Misses outside the top 5: hybrid_rerank (3)
- #145 What makes the northern lights glow? (gold 2:11.3; got 3:6.1, 2:16.5, 3:1.4)
- #148 Why is the grass wet in the early morning even when it didn't rain? (gold 2:2.2/2:1.5; got 2:1.6, 1:intro, 3:1.5)
- #152 Why does the water push harder on me the deeper I swim in a pool? (gold 1:14.1; got 1:5.5, 1:6.4, 1:6.2)

## Misses outside the top 5: hybrid_bm25_rerank (2)
- #148 Why is the grass wet in the early morning even when it didn't rain? (gold 2:2.2/2:1.5; got 2:intro, 2:1.6, 1:intro)
- #152 Why does the water push harder on me the deeper I swim in a pool? (gold 1:14.1; got 1:5.5, 1:6.4, 1:6.2)
