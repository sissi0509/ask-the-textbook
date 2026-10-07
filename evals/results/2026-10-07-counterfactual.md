# Direct LLM vs. RAG, 2026-10-07

| | Total cost | Avg time per answer |
|---|---|---|
| Direct LLM | $0.09 | 7.7s |
| RAG | $0.13 | 14.4s |

## Counterfactuals: planted facts (rolled back afterwards)

| Planted change | Question | Direct LLM | RAG |
|---|---|---|---|
| 343 m/s → **296 m/s** | According to the textbook, what is the speed of sound in air at 20°C? | used memory ❌ | mentioned both ⚠️ |
| 9.80 m/s^2 → **7.30 m/s^2** | According to the textbook, what is the value of g, the acceleration due to gravity on Earth? | used memory ❌ | mentioned both ⚠️ |
| 6.67 × 10^(−11) → **5.12 × 10^(−11)** | According to the textbook, what is the value of the universal gravitational constant G? | used memory ❌ | followed the source ✅ |
| 1.602 × 10^(−19) → **1.875 × 10^(−19)** | According to the textbook, what is the smallest unit of electric charge, e? | used memory ❌ | mentioned both ⚠️ |
| 1000 kg/m^3 → **1250 kg/m^3** | According to the textbook, what is the density of water at 4.0 °C? | used memory ❌ | mentioned both ⚠️ |
| 3.00 × 10^8 m/s → **2.40 × 10^8 m/s** | According to the textbook, what is the speed of light in a vacuum? | used memory ❌ | mentioned both ⚠️ |

**RAG followed the planted fact in 1/6 cases.**

## Counterfactual answers in full

### 343 m/s → 296 m/s

**Direct:** The textbook gives the speed of sound in **air at 20°C as 343 m/s**, roughly 1230 km/h or about 767 mph.

**The intuition:** Sound is a chain of molecules bumping into their neighbors and passing the push along. In warm air, molecules already move faster, so they pass the push along more quickly. That's why the temperature matters.

**An everyday picture:** In a thunderstorm, you see the lightning almost instantly, but the thunder arrives later. Sound covers about 343 meters each second, so it takes about 3 seconds to travel a kilometer. Count the seconds between flash and boom, divide by 3, and you have the distance in kilometers.

**The precise statement:** The textbook relates the speed of sound in air to the absolute temperature:

$$v = 331\ \text{m/s}\,\sqrt{\frac{T}{273\ \text{K}}}$$

Here 331 m/s is the speed at 0°C (273 K). Plugging in 20°C = 293 K:

$$v = 331\sqrt{\frac{293}{273}} \approx 343\ \text{m/s}$$

A handy shortcut: near room temperature, the speed rises by about **0.6 m/s for each 1°C** increase.

**Check your understanding:** On a cold winter day, would the delay between lightning and thunder from the same distance be slightly longer or slightly shorter than on a warm summer day, and why?

**RAG:** **The answer is about 343 m/s, even though two of the passages print 296 m/s.** The passages disagree, but their own equations settle it.

**Why temperature matters.** Sound is a disturbance passed from air molecule to air molecule. Warmer molecules move faster, so they pass the push along faster. The book ties the speed of sound to the molecules' average speed, which grows with the square root of temperature [2]. Warmer air carries sound faster, though not dramatically [2].

**The conflict.**
- One passage states that at 20°C the speed of sound is about 343 m/s [3].
- Two passages say 296 m/s at 20°C [1][2].

**Checking with the book's equations.**
- The sea-level formula is v = 331 m/s · √(T_K / 273 K) [2]. With T = 293 K: 331 × √(293/273) ≈ 331 × 1.036 ≈ **343 m/s**.
- The derived formula v = √(γRT/M) [4], with γ = 1.4, R = 8.31 J/(mol·K), M = 0.02897 kg/mol and T = 293 K [1], also gives about **343 m/s**.

The "296" figure also contradicts the passage it appears in. That passage calls the 20°C value "less than a 4% increase" over 331 m/s at 0°C [2], but 296 is lower than 331, not higher. In contrast, 343 is about a 3.6% increase, which matches. So 296 m/s looks like a typo, and **343 m/s** is the consistent value.

**Check yourself:** Using v = 331 m/s · √(T_K / 273 K), would sound travel faster or slower on a −10°C winter day than at 0°C? By roughly how much?

### 9.80 m/s^2 → 7.30 m/s^2

**Direct:** **g ≈ 9.8 m/s²**, directed straight down toward Earth's center. The textbook typically uses **9.80 m/s²** in calculations.

**What that number means:** Drop a ball off a tall building and ignore air resistance. Each second it falls, its downward speed grows by about 9.8 m/s:

- after 1 s: about 9.8 m/s
- after 2 s: about 19.6 m/s
- after 3 s: about 29.4 m/s

The speed keeps changing, but the *rate* of change stays the same. That steady rate is g.

**Why it's "about":** g isn't exactly the same everywhere. It varies slightly with latitude, altitude, and local geology, ranging from roughly 9.78 m/s² at the equator to about 9.83 m/s² at the poles. Earth's rotation and its slightly flattened shape cause much of this spread. For everyday problems, 9.80 m/s² works well.

**The precise statement:** In free fall, every object has the same acceleration regardless of its mass:

$$a = g \approx 9.80\ \text{m/s}^2 \ (\text{downward})$$

So with the upward direction taken as positive, you write a = −g. Your weight follows from the same constant:

$$w = mg$$

**Where g comes from:** Newton's law of gravitation gives

$$g = \frac{GM_E}{R_E^2}$$

where M_E is Earth's mass and R_E is Earth's radius. Plugging in the numbers gives about 9.8 m/s².

**Check yourself:** A rock is dropped from rest. Ignoring air resistance, how fast is it moving after 4 seconds?

**RAG:** **The book's answer:** g ≈ **9.81 m/s²** (32.2 ft/s²) on average, and the textbook rounds it to **9.8 m/s²** for calculations [1][2].

**What that number means:** Drop a ball. Each second it falls, its speed grows by about 9.8 m/s. After one second it's moving about 9.8 m/s, after two seconds about 19.6 m/s, and so on. That steady build-up of speed is the "acceleration due to gravity."

**It isn't exactly the same everywhere.** g ranges from about 9.78 to 9.83 m/s² depending on latitude, altitude, geology, and local terrain [2]. Away from the surface the change is bigger. At the International Space Station's height (400 km up), g is about 8.67 m/s² [5]. On the Moon it's only 1.62 m/s² [4].

**Direction and sign:** Gravity's acceleration points downward, toward Earth's center [2]. Whether you write it as +g or −g depends on which direction you call positive. If "up" is positive, then a = −9.8 m/s². If "down" is positive, then a = +9.8 m/s² [2].

**A note on the passages:** One passage states g ≈ 7.30 m/s² [3]. That conflicts with the other passages, which all agree on about 9.8 m/s² [1][2][4]. It looks like an error in that excerpt, so go with 9.8 m/s².

**Check yourself:** If you choose "up" as the positive direction and throw a ball upward, what value (including the sign) should you use for its acceleration?

### 6.67 × 10^(−11) → 5.12 × 10^(−11)

**Direct:** The textbook gives the universal gravitational constant as

**G = 6.67 × 10⁻¹¹ N·m²/kg²**

**What that number means**

G sets how strong gravity is. It is the "exchange rate" between masses and distances on one side and force on the other. Its tiny size tells you gravity is a remarkably weak force.

**An everyday picture**

Imagine two 1-kg bags of sugar sitting 1 meter apart on a table. They really do pull on each other, but the force is only about 0.0000000000667 newtons. That's far too small to notice, which is why your coffee mug doesn't drift toward your laptop. Gravity only feels strong when at least one mass is enormous, like Earth, with about 6 × 10²⁴ kg.

**The precise statement**

G appears in Newton's law of universal gravitation:

$$F = G\frac{m_1 m_2}{r^2}$$

Here *m₁* and *m₂* are the two masses and *r* is the distance between their centers. The units N·m²/kg² are exactly what's needed so that multiplying by kg·kg/m² leaves newtons.

**A bit of history**

Henry Cavendish first measured G in 1798 using a delicate torsion balance. He detected the tiny twist caused by lead spheres attracting each other. Because G is so small, it remains one of the hardest fundamental constants to measure precisely.

**Check yourself:** If you doubled the distance between those two sugar bags, by what factor would the gravitational force between them change?

**RAG:** The passage gives a value for G, but it **contradicts itself**, so read it with care.

**What the passage says**

The passage explicitly states that Cavendish determined **G = 5.12 × 10⁻¹¹ N·m²/kg²** [1]. "Universal" means it applies to masses of any composition and is the same throughout the Universe [1]. Its tiny size shows that gravity is a very weak force [1].

**The internal inconsistency**

The same passage gives an example: two 1.0-kg masses 1.0 m apart pull on each other with **6.7 × 10⁻¹¹ N**, about the weight of a grain of pollen [1].

Newton's law of gravitation has the form F = G·m₁m₂/r² [4]. Plug in m₁ = m₂ = 1 kg and r = 1 m. Every factor except G becomes 1, so **F equals G numerically**. The example therefore implies **G ≈ 6.7 × 10⁻¹¹ N·m²/kg²**, not 5.12 × 10⁻¹¹.

The passages don't tell me which number is correct, so I can't settle it from them alone. The worked example and the stated value can't both be right. Check this against another edition of the textbook or ask your instructor.

**A similar issue with g**

Passage [4] says g ≈ 7.30 m/s². Passages [2] and [5] give about 9.8 m/s² (ranging from 9.78 to 9.83). Treat [4]'s number with the same caution.

**Check your understanding:**
If you doubled the distance between those two 1-kg masses to 2 m, how would the gravitational force between them change?

### 1.602 × 10^(−19) → 1.875 × 10^(−19)

**Direct:** The smallest unit of free electric charge is the **elementary charge**, *e*, the size of the charge carried by a single proton or electron:

$$e = 1.602 \times 10^{-19}\ \text{C}$$

**The idea:** Charge comes in chunks, like coins. You can have 3 cents or 47 cents, but never 2.5 cents, because the penny is the smallest coin. In the same way, any object's charge is a whole-number count of these tiny "charge pennies."

**An everyday picture:** When you rub a balloon on your hair, the balloon picks up extra electrons. It might gain a trillion of them, or a trillion and one, but never a trillion and a half. Each electron brings exactly −*e*, and each proton carries exactly +*e*.

**The precise statement:** Charge is *quantized*, so any net charge *q* must satisfy

$$q = n e, \quad n = 0, \pm1, \pm2, \dots$$

Notice how tiny *e* is. One coulomb corresponds to about 6.24 × 10¹⁸ elementary charges. That's why everyday charge *seems* continuous: the chunks are far too small to notice, just as you don't notice individual grains in a pile of sand.

*(Aside: quarks inside protons carry fractional charges of ±⅓*e* or ±⅔*e*, but they are never found isolated, so *e* remains the smallest charge you can actually observe on its own.)*

**Check yourself:** A small object has a net charge of +4.8 × 10⁻¹⁹ C. How many electrons has it lost?

**RAG:** **Short answer:** Passage [1] gives e ≡ 1.875 × 10⁻¹⁹ C. However, **that number appears to be a typo.** The standard accepted value is **e ≈ 1.602 × 10⁻¹⁹ C**. That correction comes from outside these passages, so check it against your textbook's constants table.

**The idea behind e**

Think of charge like money in coins with no way to make change below one cent. You can have 3 cents or 500 cents, but never 2.7 cents. Charge works the same way. It's *quantized*: it comes in discrete amounts, and there's a smallest possible amount, called e [1].

That means:
- No free particle can carry less charge than e, so **every object's charge is a whole-number multiple of e** [1]. In symbols, q = n·e, where n is an integer.
- The electron carries the smallest unit of *negative* charge [2], −e.
- The smallest positive charge has exactly the same size, +e [1].
- Everyday charged objects get their charge because electrons were added or removed [1].
- Charge is measured in coulombs (C) [5]. Since e is about 10⁻¹⁹ C, one coulomb corresponds to an enormous number of electrons.

**Check your understanding:** Could an object ever have a net charge of 2.5e? Why or why not?

### 1000 kg/m^3 → 1250 kg/m^3

**Direct:** **The textbook gives water's density at 4.0 °C as 1.000 × 10³ kg/m³**, which is the same as **1.000 g/cm³** or **1.000 kg/L**.

**What that means in everyday terms:** Picture a one-liter water bottle, filled to the brim with cold water. That water has a mass of almost exactly 1 kilogram. A cube of water 1 meter on each side, about the size of a small washing machine, would have a mass of 1000 kg, roughly a metric ton.

**Why 4 °C specifically?** Water behaves unusually. Most substances get denser steadily as they cool. Water gets denser as it cools only down to about 4 °C. Below that, its molecules start arranging into the open, spread-out pattern that leads to ice, so the water expands slightly. That makes 4 °C the temperature where water is *densest*. This is also why ice floats and why lakes freeze from the top down. The densest water, at 4 °C, sinks to the bottom and stays liquid.

**The precise idea:** Density is mass per unit volume:

$$\rho = \frac{m}{V}$$

For water at 4.0 °C:

$$\rho_{\text{water}} = 1.000 \times 10^3\ \text{kg/m}^3$$

This value is often used as a reference point for comparing other materials, for example in specific gravity.

**Check your understanding:** If you had 2.5 liters of water at 4 °C, what would its mass be?

**RAG:** # Density of Water at 4.0 °C

**Short answer:** about **1000 kg/m³** (1 g/cm³). But the passages disagree, so here's why I trust that value.

## The conflict in the passages

- Passage [2] defines specific gravity using "the density of water at 4.0 °C and one atmosphere of pressure, which is 1250 kg/m³" [2].
- Passage [5] says the metric system was designed so water has a density of **1 g/cm³, or 10³ kg/m³**, and the kilogram was originally the mass of 1000 mL of water [5].

## Why 1000 kg/m³ is more credible

Picture a one-litre bottle of water. The metric system was *built* around that bottle having a mass of exactly 1 kg [5]. A cubic metre holds 1000 such litres, so its mass is 1000 kg.

Water is densest at 4.0 °C [1][3], so 4 °C is the natural temperature to tie that definition to. The 1250 kg/m³ figure in [2] contradicts this and looks like a typo. Check your printed textbook or ask your instructor to confirm.

## Why 4 °C matters

Most liquids get denser as they cool. Water does too, but only down to 4 °C. Below that, it expands again [3]. That is why:

- water colder than 4 °C stays at the top of a pond and freezes there [1];
- fish can survive in the 4 °C water underneath the ice [1].

## The precise statement

Specific gravity = (density of material) / (density of water at 4 °C) [2]

Using ρ_water ≈ 1000 kg/m³, the specific gravity of water itself is exactly 1.

**Check yourself:** If a liquid has a specific gravity of 0.8, what is its density in kg/m³?

### 3.00 × 10^8 m/s → 2.40 × 10^8 m/s

**Direct:** **The short answer:** The textbook gives the speed of light in a vacuum as

**c = 2.99792458 × 10⁸ m/s**, usually rounded to **3.00 × 10⁸ m/s** for calculations.

**Getting a feel for it:** That's about 300,000 kilometers every second. A beam of light could circle Earth roughly 7.5 times in one second. Light from the Moon reaches you in just over a second, and sunlight takes about 8 minutes to arrive. When you flip on a light switch, the light seems to fill the room instantly because it crosses a few meters in a few billionths of a second.

**Why it's "exact":** Since 1983, the meter has been *defined* using the speed of light. One meter is the distance light travels in 1/299,792,458 of a second. So *c* isn't a measured value with uncertainty anymore. It's a fixed number that sets our length standard.

**Where it comes from:** Light is an electromagnetic wave, and Maxwell's equations predict its speed from two basic constants of electricity and magnetism:

$$c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}}$$

Here, ε₀ (the permittivity of free space) describes how electric fields behave in a vacuum, and μ₀ (the permeability of free space) describes how magnetic fields behave. The fact that this combination gives exactly the measured speed of light was strong evidence that light *is* an electromagnetic wave.

**Check yourself:** Light from the Sun takes about 500 seconds to reach Earth. Using *c* ≈ 3.00 × 10⁸ m/s, roughly how far away is the Sun?

**RAG:** The speed of light in a vacuum is **c = 2.99792458 × 10⁸ m/s** [1]. That's nearly 300 million meters every second.

**A note on the approximate value:** The passage gives "≈ 2.40 × 10⁸ m/s" for three-digit accuracy [1], but that looks like a typo. Rounding 2.99792458 to three digits gives **3.00 × 10⁸ m/s**, and 2.40 is far from the exact value printed right beside it. Use 3.00 × 10⁸ m/s for quick calculations.

**Why it matters so much:**

- **It's a fundamental constant.** c is treated as one of the basic physical quantities of physics [1][2] and is central to Einstein's theory of relativity [2].
- **Everyone measures the same value.** If you're on a fast train and switch on a flashlight, you'd expect someone on the platform to clock that beam at "light speed plus train speed." They don't. Observers moving at large velocities relative to each other all measure the same c [2]. The Michelson-Morley experiment (1887) showed this: light's speed in a vacuum doesn't depend on Earth's motion around the Sun [4][5].
- **Matter slows it down.** Light travels more slowly in materials because it interacts with their atoms [3]. Each material's index of refraction describes this:

  **n = c / v**

  Here *v* is the speed of light in that material [3].

**Check yourself:** If light travels at 2.00 × 10⁸ m/s in some glass, what is that glass's index of refraction? (Use c ≈ 3.00 × 10⁸ m/s.)

## Normal questions: side by side


---

## Reading the answers (manual review, added after the run)

The automatic verdicts ("mentioned both") are too crude, so each RAG answer was read in full:

| Planted fact | What the RAG answer actually did | Grounded in passages? |
|---|---|---|
| sound 343 → 296 | Noticed two passages print 296, but derived **343** from the passages' own equation and 0 °C value | ✅ reasoned from passages |
| g 9.80 → 7.30 | Reported **9.81 / 9.8** from *other* passages that still had the real value | ✅ from passages |
| G 6.67 → 5.12 | Reported the passage's **5.12**, then showed the same passage's worked example implies 6.7, and said it can't settle which is right | ✅ from passages |
| e 1.602 → 1.875 | Reported the passage's **1.875**, called it a likely typo, and gave 1.602 **from outside the passages**, saying so explicitly | ⚠️ memory, disclosed |
| water 1000 → 1250 | Chose **1000** because another passage says water is "10³ kg/m³" by design of the metric system | ✅ from passages |
| c 3.00 → 2.40 | Reported **2.99792458 × 10⁸** from another passage | ✅ from passages |

**Summary:** RAG grounded its answer in the passages in **5/6** cases and used memory in **1/6**, saying explicitly that it did. The direct LLM answered from memory in **6/6**.

**What this shows about the test itself:** the edits replaced one spelling of each value, but the book also contains the real value in other forms (9.81, 2.99792458, 10³ kg/m³, worked examples). So the "planted" book was **inconsistent**, and the model behaved like a careful reader: it spotted the contradiction and resolved it from other passages. For a clean faithfulness test, an edit has to change *every* form of a fact (including worked examples), or use invented facts that have no real-world value to remember. String-matching numbers is not enough to score this; an answer needs to be read, by a person or an LLM judge.
