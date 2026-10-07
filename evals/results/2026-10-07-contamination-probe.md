# Contamination probe, 2026-10-07

Model: `claude-opus-5-5` (effort low), no retrieval. Book: OpenStax University Physics, Volume 1.

## 1. Section recall: memory (LLM) vs. retrieval (our RAG)

| Question | Truth | LLM from memory | RAG top hit |
|---|---|---|---|
| Why do I lean back when the bus suddenly starts? | 5.2 | 5.2 Newton's First Law ✅ | 6.2 Friction ❌ |
| Why does a spinning skater speed up when she pulls her arms in? | 11.3 | 11.3 Conservation of Angular Momentum ✅ | 11.3 Conservation of Angular Momentum ✅ |
| Why does a huge steel ship float? | 14.4 | 14.4 Archimedes' Principle and Buoyancy ✅ | 14.4 Archimedes’ Principle and Buoyancy ✅ |
| What is the parallel axis theorem? | 10.5 | 10.5 Calculating Moments of Inertia ✅ | 10.5 Calculating Moments of Inertia ✅ |
| What are Kepler's laws of planetary motion? | 13.5 | 13.5 Kepler's Laws of Planetary Motion ✅ | 13.5 Kepler's Laws of Planetary Motion ✅ |
| Why do two slightly out-of-tune guitar strings make a wah-wah sound? | 17.6 | 17.6 Beats ✅ | 17.5 Sources of Musical Sound ❌ |
| What is the difference between conservative and non-conservative forces? | 8.2 | 8.2 Conservative and Non-Conservative Forces ✅ | 8.2 Conservative and Non-Conservative Forces ✅ |
| How does a rocket move in empty space? | 9.7 | 9.7 Rocket Propulsion ✅ | 9.7 Rocket Propulsion ✅ |

**LLM from memory: 8/8 · RAG: 6/8**

## 2. Verbatim continuation (memorization)

First 15 words of a real paragraph → model continues; score = share of the true next 25 words reproduced in order.

| Section | Prompt | Model continued | Actual next words | Overlap |
|---|---|---|---|---|
| 5.2 | Note the repeated use of the verb “remains.” We can think of this law as … | UNKNOWN | preserving the status quo of motion. Also note the expression “constant velocity;” this means that the object maintains a path along a straight line, since | 0% |
| 11.3 | So far, we have looked at the angular momentum of systems consisting of point particles … | (ran out of tokens) | and rigid bodies. We have also analyzed the torques involved, using the expression that relates the external net torque to the change in angular momentum,. | 0% |
| 14.6 | There are many common examples of pressure dropping in rapidly moving fluids. For instance, shower … | (ran out of tokens) | curtains have a disagreeable habit of bulging into the shower stall when the shower is on. The reason is that the high-velocity stream of water | 4% |
| 9.7 | Now we deal with the case where the mass of an object is changing. We … | (ran out of tokens) | analyze the motion of a rocket, which changes its velocity (and hence its momentum) by ejecting burned fuel gases, thus causing it to accelerate in | 4% |
| 17.7 | The characteristic sound of a motorcycle buzzing by is an example of the Doppler effect. … | (ran out of tokens) | Specifically, if you are standing on a street corner and observe an ambulance with a siren sounding passing at a constant speed, you notice two | 0% |

**Average verbatim overlap: 2%**

---

**Notes (added after the run):**
- The two 4% rows are scoring artifacts: the model produced no continuation ("ran out of tokens" while thinking), and the score counted common words. The runner now reports these as "no attempt"; read the true memorization score as **0%**.
- **Reading:** the model knows the book's *structure* (8/8 section numbers and titles from memory, better than our retriever's top-1 at 6/8) but did not reproduce its *text* (0 of 5 continuations). Caveat: models are trained not to reproduce copyrighted text verbatim, so 0% doesn't prove the text was never seen. It does show the model won't hand back the book's wording.
- **Implication for the eval:** contamination is real at the *knowledge* level. A correct answer doesn't prove retrieval worked, so answer evals must check **faithfulness** (is every claim supported by the retrieved passages?), not just correctness.
- **Implication for retrieval:** the model knows bus → §5.2 and wah-wah → §17.6, the two questions retrieval misses. That's direct evidence HyDE should help: let the model's knowledge write a textbook-style query.
