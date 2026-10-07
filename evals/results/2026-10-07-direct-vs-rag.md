# Direct LLM vs. RAG, 2026-10-07

| | Total cost | Avg time per answer |
|---|---|---|
| Direct LLM | $0.21 | 8.1s |
| RAG | $0.29 | 9.9s |

## Counterfactuals: planted facts (rolled back afterwards)

| Planted change | Question | Direct LLM | RAG |
|---|---|---|---|
| 343 m/s → **296 m/s** | According to the textbook, what is the speed of sound in air at 20°C? | used memory ❌ | mentioned both ⚠️ |
| 9.80 m/s^2 → **7.30 m/s^2** | According to the textbook, what is the value of g, the acceleration due to gravity on Earth? | used memory ❌ | mentioned both ⚠️ |
| 6.67 × 10^(−11) → **5.12 × 10^(−11)** | According to the textbook, what is the value of the universal gravitational constant G? | used memory ❌ | followed the source ✅ |
| 1.602 × 10^(−19) → **1.875 × 10^(−19)** | According to the textbook, what is the smallest unit of electric charge, e? | used memory ❌ | mentioned both ⚠️ |
| 1000 kg/m^3 → **1250 kg/m^3** | According to the textbook, what is the density of water at 4.0 °C? | neither value ⚠️ | mentioned both ⚠️ |
| 3.00 × 10^8 m/s → **2.40 × 10^8 m/s** | According to the textbook, what is the speed of light in a vacuum? | used memory ❌ | mentioned both ⚠️ |

**RAG followed the planted fact in 1/6 cases.**

## Normal questions: side by side

### Why do I lean back when the bus suddenly starts?

**Direct LLM** (245 words, 7.9s, $0.014)

Here's the surprising part: **nothing actually pushes you backward.** The bus moves forward *underneath* you, and your body hasn't caught up yet.

**The intuition:** Your body "wants" to keep doing whatever it's already doing. If you're sitting still, you tend to stay still. When the bus lurches forward, the floor grabs your feet (through friction) and the seat pushes your back, but your upper body isn't being pushed directly at first. So your feet and hips go forward with the bus while your head and shoulders lag behind. To you, that *feels* like being thrown backward.

**An everyday picture:** Put a coin on a sheet of paper and yank the paper quickly. The coin barely moves. The paper slides out from under it. You're the coin; the bus is the paper.

**The physics:** This tendency to resist changes in motion is called **inertia**, and it's the heart of **Newton's first law**: an object stays at rest or moves at constant velocity unless a net force acts on it. Newton's second law makes it quantitative:

$$\vec{F}_{\text{net}} = m\vec{a}$$

If the net horizontal force on your upper body is (nearly) zero, its acceleration is (nearly) zero, while the bus accelerates forward at $a$. *Relative to the bus*, you appear to accelerate backward at $a$. That's why it feels like a backward force, even though, seen from the sidewalk, you're just staying put.

**Check yourself:** When the moving bus suddenly *brakes*, which way do you lurch, and why?

**RAG** (268 words, 8.8s, $0.018; sources: Vol. 1 §6.3 Centripetal Force › Inertial Forces and Noninertial (Accelerated) Frames: The Coriolis Force; Vol. 1 Introduction)

**Short answer:** you don't really get pushed backward. Your body tries to stay where it was while the bus moves forward underneath you.

**The intuition**

Picture yourself standing on a bus at a red light. When the light turns green, the bus floor lurches forward. Your feet are on the floor, so they go with it. The rest of your body hasn't been pushed yet, so it tends to stay put. From your point of view inside the bus, it *feels* like something shoved you backward. But from the sidewalk, you'd see the bus moving forward while your upper body lags behind.

**What the textbook says**

The book describes the same effect when a jet takes off. It feels as if you are being pushed back into your seat, "yet a physicist would say that you tend to remain stationary while the seat pushes forward on you" [5]. That backward "push" is called an **inertial force**. It is a *fictitious* force that only seems to exist because you are watching from a frame of reference that is accelerating [5]. The underlying idea is **Newton's first law**: an object keeps doing what it was doing unless a force changes its motion [5]. Newton's laws are what describe how forces change motion [3].

So on the bus:
- **Real force:** the floor (or your seat) pushes you forward.
- **Apparent force:** the "backward shove" you feel, which comes from your own inertia.

**Check yourself:** If the bus is already moving and the driver slams on the brakes, which way will you lurch, and what is actually happening to your body?

---

### Why does a spinning ice skater speed up when she pulls her arms in?

**Direct LLM** (261 words, 7.1s, $0.013)

**The intuition:** A spinning object carries a certain "amount of spin" that can't change unless something outside twists it. When the skater pulls her arms in, she doesn't add or remove any spin. She just rearranges her mass. Mass far from the axis is "expensive" to spin, so with the same amount of spin she can turn much faster once her mass is closer in.

**Everyday picture:** Sit on an office chair, holding something heavy (a couple of books) out at arm's length, and have a friend give you a gentle spin. Now pull the books to your chest. You'll suddenly whirl faster. Push them back out and you slow down.

**Plain words to physics terms:**
- "How hard it is to spin something" is the **moment of inertia**, *I*. It grows with mass and *especially* with distance from the axis: *I* = Σ*mr²*.
- "How fast it spins" is the **angular velocity**, *ω*.
- "Amount of spin" is the **angular momentum**, *L* = *Iω*.

The ice exerts almost no twisting force (torque) on her, so *L* stays constant:

$$I_1\omega_1 = I_2\omega_2$$

Pulling her arms in shrinks *I*. Since *r* is squared, halving the arms' distance cuts their contribution by four. So *ω* must rise to keep the product the same.

**Bonus detail:** Her kinetic energy, ½*Iω²*, actually *increases*. That extra energy comes from the work her muscles do pulling her arms inward against their tendency to fly outward.

**Check yourself:** If a skater reduces her moment of inertia to one-third of its original value, what happens to her spin rate?

**RAG** (267 words, 8.6s, $0.018; sources: Vol. 1 §11.3 Conservation of Angular Momentum; Vol. 1 §11.3 Conservation of Angular Momentum; Vol. 1 §11.3 Conservation of Angular Momentum)

**The big idea:** a spinning skater has a fixed "amount of spin," and pulling her arms in forces that same spin to show up as faster turning.

**Why her spin amount stays fixed:** Something has to twist her (a torque) to change her spin. On ice there's very little friction, and what friction there is acts right at her pivot point, so the torque on her is negligible [1]. That's why she can spin for so long, and why her angular momentum stays constant [1].

**The trade-off:** Angular momentum depends on two things: how her mass is arranged around the spin axis (moment of inertia, *I*) and how fast she turns (angular velocity, *ω*). If one goes down, the other must go up to keep the product the same:

$$L' = L \quad\Rightarrow\quad I'\omega' = I\omega$$

Pulling her arms and legs in reduces her moment of inertia, so *I′* is smaller. To keep angular momentum constant, *ω′* must increase [1].

**A neat twist about energy:** Her rotational kinetic energy is ½*Iω*² [4], and it actually *increases* when she pulls in [3]. That extra energy comes from the work she does pulling her arms inward against their tendency to keep moving outward [3]. If she extends her arms again, she returns to her original spin rate and her original kinetic energy [3].

The passages I have don't explain in detail *why* pulling mass toward the axis lowers the moment of inertia. They only state that it does [1].

**Check yourself:** If the skater extends her arms so her moment of inertia doubles, what happens to her spin rate?

---

### Why do I get a small shock when I touch a doorknob after walking across a carpet?

**Direct LLM** (323 words, 11.6s, $0.020)

## The short version
Walking on carpet **rubs electrons off one material and onto the other**. You slowly build up extra charge, and the doorknob gives that charge a quick path out. The tiny spark is the charge jumping across the air.

## Step by step
1. **Charging by rubbing.** Your shoe soles and the carpet hold onto electrons with different strengths. Each step shifts a few electrons between them, so you end up with a net charge, often extra electrons.
2. **Nowhere to go.** Carpet, shoe soles, and dry air are all insulators. The charge can't leak away, so it piles up on your body with each step.
3. **The metal knob.** A doorknob is a conductor, usually connected to a large metal object or to the ground. As your finger gets close, the voltage between you and the knob is squeezed across a tiny air gap, so the electric field in that gap becomes very strong.
4. **The spark.** When that field gets strong enough, the air itself breaks down and briefly conducts. Your extra charge rushes across in a tiny fraction of a second, and your nerves feel it as a zap.

## The physics
Your body acts like a small capacitor:

$$Q = CV$$

Typical values are a body capacitance of $C \approx 100\ \text{pF}$ and a voltage of $V \approx 10\ \text{kV}$. That gives a charge of only about $Q \approx 1\ \mu\text{C}$.

The spark jumps when the field in the gap,

$$E \approx \frac{V}{d},$$

exceeds the breakdown strength of air, about $3\times10^6\ \text{V/m}$. The stored energy is only about

$$U = \tfrac{1}{2}CV^2 \approx 5\ \text{mJ}.$$

That's why the shock stings but doesn't hurt you.

You get shocked more often in dry winter air. In humid air, moisture lets the charge slowly leak away before it can build up.

**Check yourself:** Why do you usually get no shock if you touch the doorknob with a metal key first?

**RAG** (276 words, 11.1s, $0.024; sources: Vol. 2 §5.1 Electric Charge › Discoveries; Vol. 2 §10.6 Household Wiring and Electrical Safety › Shock Hazards; Vol. 2 §10.6 Household Wiring and Electrical Safety › Shock Hazards)

**Short answer:** It's **static electricity**, the same family of effects as a balloon sticking to a wall. The passages I have name the effect but don't explain the step-by-step mechanism.

**Intuition first.** Think of the other everyday examples your textbook groups with the doorknob zap: run a comb through your hair and it picks up bits of paper, or rub a balloon on a wall and it sticks [1]. In each case, rubbing or scraping two materials together leaves something behind that makes objects attract or produce a spark. Your textbook lists "getting shocked by a doorknob (or a friend) after shuffling your feet on some types of carpeting" as the most annoying of these static effects [1]. So shuffling across carpet works like rubbing that balloon, just with your feet.

**What you feel.** The "shock" is an electric current passing through your body. Very small currents pass through you harmlessly and you don't even notice them. The threshold of sensation is only about 1 mA, and shocks below about 5 mA are unpleasant but apparently harmless [5]. The effects of a shock range from a slight sensation at the point of contact all the way up to serious harm for large currents [4]. A doorknob zap is the "slight sensation" end of that range.

**What's missing:** My passages don't explain *how* rubbing separates electric charge, why some carpets work better than others, or why the spark jumps to a metal doorknob in particular. Your textbook's sections on electric charge and conductors would cover that.

**Check yourself:** Which other everyday example in the passage is caused by the same kind of effect as the doorknob shock?

---

### How does a refrigerator keep food cold?

**Direct LLM** (271 words, 7.6s, $0.015)

**Big idea:** A refrigerator doesn't "make cold." It *pumps heat out* of the food compartment and dumps it into your kitchen. Heat naturally flows from hot to cold, so pushing it the other way takes work, which is why the fridge needs electricity.

**Everyday picture:** Think of bailing water out of a boat. Water flows in on its own; you have to do work to scoop it out and toss it overboard. The fridge "bails" heat out of the cold box.

**How it works:** A special fluid (the refrigerant) circulates in a loop:

1. **Inside the fridge:** The refrigerant is at low pressure, so it boils at a very low temperature. As it evaporates, it absorbs heat from the food. This is like sweat cooling your skin.
2. **Compressor:** It squeezes the vapor, making it hotter than the room.
3. **Coils on the back:** The hot vapor releases heat into the kitchen and condenses back to liquid. (Feel those coils. They're warm!)
4. **Expansion valve:** The liquid's pressure drops, it cools sharply, and the cycle repeats.

**Precise statement:** Energy conservation for one cycle gives

$$Q_h = Q_c + W$$

where $Q_c$ is heat removed from inside, $W$ is the work done by the compressor, and $Q_h$ is the heat released to the room. The second law of thermodynamics says $W$ can't be zero, because heat won't flow cold→hot by itself. Efficiency is measured by the coefficient of performance:

$$K_R = \frac{Q_c}{W}$$

Typical fridges have $K_R \approx 2$–$6$.

**Check yourself:** If you leave the fridge door open in a closed room, does the room get warmer, cooler, or stay the same? Why?

**RAG** (280 words, 10.4s, $0.022; sources: Vol. 2 §4.3 Refrigerators and Heat Pumps; Vol. 2 §4.3 Refrigerators and Heat Pumps; Vol. 2 §4.4 Statements of the Second Law of Thermodynamics; Vol. 2 §4.3 Refrigerators and Heat Pumps)

# How a refrigerator keeps food cold

**The intuition:** Think of heat like water that naturally runs downhill, from warm places to cold ones. Your kitchen is warmer than your milk, so heat keeps leaking in. A refrigerator is like a **pump that carries water back uphill**. It doesn't create "cold." It keeps hauling heat *out* of the inside and dumping it into the room.

**What actually happens:** A refrigerator removes heat Q_c from the cold space inside (your food) and discards heat Q_h to the warmer surrounding air [1][2]. That uphill pumping isn't free. A motor moves a coolant through the coils, and that motor's work W is what you pay for on your electricity bill [1]. If you've felt warmth near the back or underside of a fridge, that's the heat being exhausted to the room.

Why do you need the work at all? A "perfect" refrigerator that moves heat from cold to hot with no work is exactly what the Clausius statement of the second law rules out [3].

**Measuring how good it is:** The coefficient of performance compares the heat removed to the work you supply [4]:

K_R = Q_c / W = Q_c / (Q_h − Q_c)

A higher K_R means more heat pulled out of the food per unit of electrical work.

**A gap:** The passages I have don't explain the step-by-step coolant cycle, such as how the coolant absorbs heat inside and releases it outside. They only say the motor moves coolant through the coils [1].

**Check yourself:** Using K_R = Q_c/(Q_h − Q_c), which is larger, the heat dumped into your kitchen (Q_h) or the heat removed from the food (Q_c)? Why?

---

### Why do we see a rainbow after it rains?

**Direct LLM** (252 words, 8.3s, $0.014)

**The big idea:** sunlight looks white, but it's really a mix of all colors. Raindrops act like millions of tiny prisms that sort those colors by direction.

**Picture it:** Stand with your back to the sun and spray a garden hose into the air. A little rainbow appears in the mist. After a storm, the sky is full of leftover droplets, so you get the giant version.

**What happens inside one drop:**
1. Sunlight enters the drop and **bends** (refracts) because light slows down in water.
2. It **reflects** off the back of the drop.
3. It bends again as it leaves.

The key is that water bends each color by a slightly different amount. Violet bends more than red. This color-dependent bending is called **dispersion**. Each color exits the drop at its own angle, measured from the line running from the sun through your head: about **42° for red** and **40° for violet**.

So the drops 42° away send red to your eye, and the drops 40° away send violet. All the drops at a given angle form a circle around the point opposite the sun, which is why you see an arc of colors.

**The precise version (Snell's law):**

$$n_1 \sin\theta_1 = n_2 \sin\theta_2$$

For water, the index of refraction *n* is slightly larger for violet light (≈1.34) than for red light (≈1.33). That small difference spreads the colors apart.

**Check yourself:** If you see a rainbow in the late afternoon, which direction are you facing: east or west? Why?

**RAG** (271 words, 8.5s, $0.021; sources: Vol. 3 §1.5 Dispersion; Vol. 3 §1.5 Dispersion; Vol. 3 §1.5 Dispersion)

After rain, the air is full of tiny water drops, and each one acts like a small glass prism that sorts sunlight into its colors.

**The intuition:** Picture shining a flashlight into a clear glass of water. The beam bends as it enters. Now imagine that each color bends by a slightly different amount. White sunlight is really a mixture of all visible colors [3], so when it bends, the colors fan out. Raindrops do this, and that is the rainbow.

**What happens inside one drop:**
1. Sunlight enters the drop and **refracts** (bends) [2].
2. It **reflects** off the back of the drop [2]. This step doesn't separate colors, because reflection doesn't depend on wavelength [2].
3. It refracts again as it leaves [2].

**Why the colors separate:** A material's index of refraction, *n*, depends on wavelength. In water and glass, *n* is largest for violet light, so violet bends more than red [5]. Spreading white light out by wavelength in this way is called **dispersion** [3].

**Why it looks the way it does:**
- You see a rainbow only when you face *away* from the Sun [2].
- The arc shape comes from the fact that each color reaches your eye at a specific angle relative to the Sun's direction [2].
- A dark, stormy sky behind the drops makes the colors stand out [2].

If light reflects *twice* inside the drops, you may see a fainter secondary rainbow above the main one, with its colors in reverse order [2].

**Check yourself:** Why would standing with the Sun directly in front of you prevent you from seeing a rainbow?

---

### What is the photoelectric effect?

**Direct LLM** (251 words, 7.3s, $0.012)

**The big idea:** Light can knock electrons out of a metal, but whether it works depends on the light's *color* (frequency), not its brightness.

**Picture this:** Imagine trying to knock coconuts out of a tree by throwing things at it. Throwing thousands of ping-pong balls won't dislodge a single coconut, because each ball is too weak. But one baseball, thrown hard enough, does the job. Light behaves the same way. It arrives in little packets called **photons**, and each photon either has enough energy to free an electron or it doesn't.

**What experiments show:**
- Shine dim blue or ultraviolet light on a metal, and electrons pop out immediately.
- Shine extremely bright red light, and *nothing* happens.
- Making the light brighter only increases the *number* of electrons ejected, not their speed.

This puzzled physicists, because the wave picture predicted that brighter light of any color should eventually work. Einstein explained it in 1905: each photon's energy depends only on its frequency.

**The precise statement:**

$$E_{\text{photon}} = hf$$

where $h = 6.63 \times 10^{-34}\ \text{J·s}$ is Planck's constant. An electron needs a minimum energy, the **work function** $\phi$, to escape the metal. Any leftover energy becomes kinetic energy:

$$K_{\max} = hf - \phi$$

If $hf < \phi$, no electrons escape, no matter how intense the light.

This was key evidence that light has a particle nature.

**Check yourself:** If you double the brightness of light that is *already* ejecting electrons, what happens to the maximum kinetic energy of those electrons?

**RAG** (256 words, 10.0s, $0.017; sources: Vol. 3 §6.2 Photoelectric Effect; Vol. 3 §6.2 Photoelectric Effect › Glossary; Vol. 3 §6.2 Photoelectric Effect › Glossary; Vol. 3 §6.2 Photoelectric Effect › Glossary; Vol. 3 §6.2 Photoelectric Effect › Glossary)

**The big idea:** Shine the right kind of light on a metal and the metal throws out electrons. The light is absorbed, and that absorbed energy knocks electrons loose from the surface [1].

**A picture to hold onto:** Imagine tossing balls at coconuts on a shelf. Gentle tosses do nothing, no matter how many you throw. But once your throws are "sharp" enough, coconuts start falling off. The analogy has a catch: in the photoelectric effect, what matters isn't how hard you throw but the light's **frequency** (equivalently, its wavelength). The light must have a short enough wavelength, meaning a frequency above a certain **threshold frequency**, before any electrons come off [1].

**The precise statement:** When a metal surface is exposed to monochromatic (single-frequency) electromagnetic radiation above a threshold frequency, the radiation is absorbed and the surface emits electrons. This is the **photoelectric effect** [1][2]. The emitted electrons are called **photoelectrons** [1][3].

**In a circuit:** If you make that metal one electrode of a circuit, it's called a **photoelectrode** [4]. When you illuminate it, the emitted electrons carry a current through the circuit, called the **photocurrent** [5]. So light can directly switch on an electric current.

**What's missing:** The passages I have don't explain *why* a threshold frequency exists, or how to calculate the energy of the ejected electrons. That explanation involves the particle-like nature of light, which these excerpts don't cover.

**Check yourself:** If light below the threshold frequency shines on a metal, what happens to photoelectron emission? And would the circuit carry a photocurrent?

---

### How do we know the universe is expanding?

**Direct LLM** (249 words, 8.2s, $0.016)

**Short answer:** almost every distant galaxy is moving away from us, and the farther away it is, the faster it recedes. That pattern is exactly what you'd see if space itself were stretching.

**How we can tell galaxies are receding:** You know how an ambulance siren drops in pitch as it drives away? Its sound waves get stretched out. Light behaves similarly. Each element (hydrogen, for example) emits light at specific, known wavelengths, like a fingerprint. When astronomers look at distant galaxies, those fingerprints show up shifted toward longer, redder wavelengths. This is called **redshift**.

**Why that means expansion:** Picture raisin bread rising in the oven. From any raisin, every other raisin moves away, and raisins twice as far away separate twice as fast. No raisin is "the center." Edwin Hubble found galaxies behave the same way (1929).

**The precise statement (Hubble's law):**

$$v = H_0 \, d$$

Here *v* is a galaxy's recession speed (from its redshift), *d* is its distance, and $H_0 \approx 70$ km/s per megaparsec. Redshift is measured as

$$z = \frac{\lambda_{\text{observed}} - \lambda_{\text{emitted}}}{\lambda_{\text{emitted}}}$$

Strictly, this redshift comes from space stretching the light during its journey, not from galaxies flying through space. But the Doppler picture is a good first intuition.

**Supporting evidence:** The cosmic microwave background, a faint glow filling the sky, is leftover light from a hot early universe, now stretched to microwave wavelengths.

**Check yourself:** If galaxy B is three times farther away than galaxy A, how should their recession speeds compare?

**RAG** (269 words, 9.5s, $0.022; sources: Vol. 3 §11.7 Evolution of the Early Universe › Dark Matter and Dark Energy; Vol. 3 §11.6 The Big Bang › Big Bang Model; Vol. 3 §11.6 The Big Bang › Structure and Dynamics of the Universe; Vol. 3 §11.6 The Big Bang › Structure and Dynamics of the Universe)

**The short answer:** we see it in the light from distant galaxies. Their light shows *redshifts*, and those redshifts suggest the universe is expanding. In fact, the measured redshifts are larger than expected, which suggests it is expanding *at an increasing rate* [1].

**A picture to hold onto:** imagine dots drawn on a balloon. As you blow it up, every dot moves away from every other dot. No dot is "the center"; each one sees all the others receding [5]. Galaxies are like those dots, and the stretching balloon skin is space-time itself [5]. So when we look out and see galaxies moving away from us, it doesn't mean Earth is special. An observer in any galaxy would see the same thing [5].

**The more precise version:** in general relativity, the size of the universe is tracked by a *scale factor* a(t), which grows over time if the universe expands [3]. For a flat universe:

d²a/dt² = −(4πG/3)(ρ + 3p)a [4]

For ordinary matter, ρ + 3p > 0, so the expansion should *slow down*. The observed speed-up therefore hints at something with negative pressure, which is linked to the mysterious *dark energy* [1][4].

**What's missing:** the passages I have don't explain how a redshift is measured or why it signals a galaxy moving away. They also don't cover the detailed law relating a galaxy's distance to its redshift. Your textbook's earlier sections are the place to look for those.

**Check yourself:** in the balloon model, why would an observer on *any* dot conclude that they are at the center of the expansion, and why would they be wrong?

---

### What is the origin of redshift: the Doppler effect or relativity? Which one is the real explanation?

**Direct LLM** (248 words, 10.8s, $0.020)

**Short answer:** both, because "redshift" names an effect (light arriving with a longer wavelength than it was emitted with) that can have several causes. The right explanation depends on the situation.

**1. Motion: Doppler redshift.** Picture a car horn dropping in pitch as the car drives away. A receding light source does the same thing: each wave crest is emitted from a little farther away, so crests arrive more spread out. At high speeds, relativity adds time dilation, giving the textbook's relativistic Doppler formula:

$$\lambda_{\text{obs}} = \lambda_s\sqrt{\frac{1+v/c}{1-v/c}}$$

This is the right picture for stars orbiting in our galaxy or for nearby galaxies.

**2. Gravity: gravitational redshift.** Light climbing out of a gravitational well loses energy, much like a ball thrown upward slows down. Since a photon can't slow below *c*, its frequency drops instead. This comes from general relativity.

**3. Expansion: cosmological redshift.** For distant galaxies, the best description is that space itself stretches while the light travels, like a wave drawn on a rubber band being pulled:

$$1+z = \frac{a_{\text{now}}}{a_{\text{then}}}$$

Here *a* is the scale factor, a measure of the "size" of the universe.

**The subtle part:** these aren't fully separate. Cosmological redshift can be viewed as many tiny Doppler shifts added up along the light's path. Over large distances, though, the expansion picture is cleaner and avoids paradoxes like "galaxies receding faster than light."

**Check yourself:** Light from a galaxy has *z* = 1. By what factor has the universe expanded since that light was emitted?

**RAG** (248 words, 9.9s, $0.024; sources: Vol. 1 §17.7 The Doppler Effect; Vol. 1 §17.7 The Doppler Effect; Vol. 1 §17.7 The Doppler Effect › Derivation of the Observed Frequency due to the Doppler Shift; Vol. 3 §11.6 The Big Bang › Glossary)

**Short answer:** My passages explain redshift in two ways, the Doppler effect and cosmological expansion. They don't discuss relativity, so I can't tell you from them which explanation is "the real one."

**Start with sound.** Picture riding a train past a warning horn. The pitch drops as you pass because the frequency you hear depends on relative motion between you and the source [1]. That change in frequency is the Doppler shift [1].

**The same idea applies to light.** Doppler shifts happen for *any* wave when the source and observer move relative to each other, including light [4]. When a galaxy moves away from us, its light arrives at a lower frequency and therefore a longer wavelength. That longer wavelength is the redshift [5]. Astronomers use these shifts to find how fast stars and galaxies are moving relative to us [4].

**A second description.** The glossary defines redshift differently, as the lengthening of light's wavelength "due to cosmological expansion" [3]. This attributes the stretch to the expansion of the universe rather than to a galaxy simply moving through space.

**What I can't answer:** The book passages I have don't cover relativity. They also don't explain how the Doppler picture and the expansion picture relate, or whether one is more fundamental. To settle "Doppler or relativity," check your textbook's chapters on special relativity and cosmology.

**Check yourself:** If a galaxy were moving *toward* us, would its light shift to higher or lower frequency, and would that be a redshift?

---

