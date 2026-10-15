# Retrieval eval, 2026-10-14 (`retrieval_cases_hard.jsonl`)

37 cases (everyday: 16, term: 21). Hit = a chunk from a gold section.
By topic: Mechanics: 4, Oscillations & Waves: 1, Thermodynamics: 8, Electricity & Magnetism: 7, Optics: 11, Modern Physics: 6.

| Method | Recall@5 | Recall@10 | MRR | R@5 everyday | R@5 term | R@5 vol 1 | R@5 vol 2 | R@5 vol 3 |
|---|---|---|---|---|---|---|---|---|
| vector | 92% | 97% | 0.87 | 94% | 90% | 100% | 100% | 82% |
| keyword | 65% | 78% | 0.47 | 56% | 71% | 80% | 73% | 53% |
| bm25 | 97% | 97% | 0.88 | 94% | 100% | 100% | 100% | 94% |
| hybrid | 92% | 92% | 0.79 | 94% | 90% | 100% | 93% | 88% |
| hybrid_bm25 | 100% | 100% | 0.93 | 100% | 100% | 100% | 100% | 100% |
| vector_rerank | 100% | 100% | 0.90 | 100% | 100% | 100% | 100% | 100% |
| hybrid_rerank | 100% | 100% | 0.90 | 100% | 100% | 100% | 100% | 100% |
| hybrid_bm25_rerank | 100% | 100% | 0.90 | 100% | 100% | 100% | 100% | 100% |

## Recall@5 by topic

| Method | Mechanics | Oscillations & Waves | Thermodynamics | Electricity & Magnetism | Optics | Modern Physics |
|---|---|---|---|---|---|---|
| vector | 100% | 100% | 100% | 100% | 82% | 83% |
| keyword | 75% | 100% | 88% | 57% | 36% | 83% |
| bm25 | 100% | 100% | 100% | 100% | 91% | 100% |
| hybrid | 100% | 100% | 100% | 86% | 82% | 100% |
| hybrid_bm25 | 100% | 100% | 100% | 100% | 100% | 100% |
| vector_rerank | 100% | 100% | 100% | 100% | 100% | 100% |
| hybrid_rerank | 100% | 100% | 100% | 100% | 100% | 100% |
| hybrid_bm25_rerank | 100% | 100% | 100% | 100% | 100% | 100% |

## Misses outside the top 5: vector (3)
- #111 Bragg's law (gold 3:4.6; got 1:12.4, 3:6.5, 3:8.5)
- #118 work function (gold 3:6.2; got 1:7.1, 1:7.1, 1:10.8)
- #137 Why do road signs shine so brightly in my headlights at night? (gold 3:1.2; got 2:16.5, 2:10.2, 2:16.5)

## Misses outside the top 5: keyword (13)
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

## Misses outside the top 5: bm25 (1)
- #131 Why can't I read the board from the back of the classroom, and what kind of glasses fix it? (gold 3:2.5; got 1:1.7, 1:16.2, 3:3.1)

## Misses outside the top 5: hybrid (3)
- #101 Hall voltage (gold 2:11.6; got 3:9.6, 2:9.4, 2:15.1)
- #111 Bragg's law (gold 3:4.6; got 3:1.3, 3:6.5, 1:5.3)
- #136 How can doctors look inside your stomach with a thin bendy tube? (gold 3:1.4; got 1:17.5, 1:17.4, 1:17.5)

## Misses outside the top 5: hybrid_bm25 (0)

## Misses outside the top 5: vector_rerank (0)

## Misses outside the top 5: hybrid_rerank (0)

## Misses outside the top 5: hybrid_bm25_rerank (0)
