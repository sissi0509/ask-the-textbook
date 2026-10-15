# Label review: `retrieval_cases.jsonl`

For each question: is the **gold** section really where the answer lives? Is another section *also* correct?
Mark ✅ (keep), ✏️ (change: write the new gold), or ❌ (drop the question). ⚠️ = vector_rerank's top-1 isn't gold, so look closer.

Top 3 = vector_rerank's results (section, subsection).
**5 of 55 flagged ⚠️.**


### #1 (textbook) What does Newton's second law state?
- **Gold:** 1:5.3 Newton's Second Law
- 1. 1:5.3 Newton's Second Law ✓
- 2. 1:5.3 Newton's Second Law › Newton’s Second Law and Momentum ✓
- 3. 1:5.3 Newton's Second Law › Newton’s Second Law and Momentum ✓
- **Your call:** 

### #2 (textbook) What is the work-energy theorem?
- **Gold:** 1:7.3 Work-Energy Theorem
- 1. 1:7.3 Work-Energy Theorem ✓
- 2. 1:7.3 Work-Energy Theorem › Glossary ✓
- 3. 1:7.3 Work-Energy Theorem ✓
- **Your call:** 

### #3 (textbook) How is linear momentum defined?
- **Gold:** 1:9.1 Linear Momentum
- 1. 1:9.1 Linear Momentum › Glossary ✓
- 2. 1:9.1 Linear Momentum ✓
- 3. 1:9.1 Linear Momentum ✓
- **Your call:** 

### #4 (textbook) What is the difference between conservative and non-conservative forces?
- **Gold:** 1:8.2 Conservative and Non-Conservative Forces
- 1. 1:8.2 Conservative and Non-Conservative Forces ✓
- 2. 1:8.2 Conservative and Non-Conservative Forces ✓
- 3. 1:8.2 Conservative and Non-Conservative Forces › Glossary ✓
- **Your call:** 

### #5 (textbook) What are the conditions for static equilibrium?
- **Gold:** 1:12.1 Conditions for Static Equilibrium
- 1. 1:12.1 Conditions for Static Equilibrium ✓
- 2. 1:12.1 Conditions for Static Equilibrium ✓
- 3. 1:12.1 Conditions for Static Equilibrium › Glossary ✓
- **Your call:** 

### #6 (textbook) What is simple harmonic motion?
- **Gold:** 1:15.1 Simple Harmonic Motion
- 1. 1:15.1 Simple Harmonic Motion › Glossary ✓
- 2. 1:15.1 Simple Harmonic Motion › Glossary ✓
- 3. 1:15.1 Simple Harmonic Motion › The Period and Frequency of a Mass on a Spring ✓
- **Your call:** 

### #7 (textbook) How is torque defined?
- **Gold:** 1:10.6 Torque
- 1. 1:10.6 Torque › Defining Torque ✓
- 2. 1:10.6 Torque › Defining Torque ✓
- 3. 1:10.6 Torque › Defining Torque ✓
- **Your call:** 

### #8 (textbook) What are Kepler's laws of planetary motion?
- **Gold:** 1:13.5 Kepler's Laws of Planetary Motion
- 1. 1:13.5 Kepler's Laws of Planetary Motion › Kepler’s First Law ✓
- 2. 1:13.5 Kepler's Laws of Planetary Motion › Kepler’s Third Law ✓
- 3. 1:13.5 Kepler's Laws of Planetary Motion › Glossary ✓
- **Your call:** 

### #9 (textbook) What is an elastic collision?
- **Gold:** 1:9.4 Types of Collisions
- 1. 1:9.4 Types of Collisions › Elastic ✓
- 2. 1:9.4 Types of Collisions › Glossary ✓
- 3. 1:9.4 Types of Collisions ✓
- **Your call:** 

### #10 (textbook) What is the difference between average velocity and instantaneous velocity?
- **Gold:** 1:3.1 Position, Displacement, and Average Velocity; 1:3.2 Instantaneous Velocity and Speed
- 1. 1:3.2 Instantaneous Velocity and Speed › Speed ✓
- 2. 1:3.2 Instantaneous Velocity and Speed › Instantaneous Velocity ✓
- 3. 1:3.2 Instantaneous Velocity and Speed › Instantaneous Velocity ✓
- **Your call:** 

### #11 (textbook) How do you add vectors using their components?
- **Gold:** 1:2.2 Coordinate Systems and Components of a Vector; 1:2.3 Algebra of Vectors
- 1. 1:2.3 Algebra of Vectors ✓
- 2. 1:2.2 Coordinate Systems and Components of a Vector ✓
- 3. 1:2.3 Algebra of Vectors ✓
- **Your call:** 

### #12 (textbook) What is centripetal acceleration?
- **Gold:** 1:4.4 Uniform and Nonuniform Circular Motion; 1:6.3 Centripetal Force
- 1. 1:4.4 Uniform and Nonuniform Circular Motion › Glossary ✓
- 2. 1:4.4 Uniform and Nonuniform Circular Motion › Centripetal Acceleration ✓
- 3. 1:6.3 Centripetal Force ✓
- **Your call:** 

### #13 (textbook) What determines the speed of a wave on a stretched string?
- **Gold:** 1:16.3 Wave Speed on a Stretched String
- 1. 1:16.3 Wave Speed on a Stretched String ✓
- 2. 1:16.3 Wave Speed on a Stretched String › Speed of Compression Waves in a Fluid ✓
- 3. 1:16.3 Wave Speed on a Stretched String › Speed of Compression Waves in a Fluid ✓
- **Your call:** 

### #14 (textbook) What is a standing wave?
- **Gold:** 1:16.6 Standing Waves and Resonance; 1:17.4 Normal Modes of a Standing Sound Wave
- 1. 1:16.6 Standing Waves and Resonance › Glossary ✓
- 2. 1:16.6 Standing Waves and Resonance › Standing Waves ✓
- 3. 1:16.6 Standing Waves and Resonance › Standing Waves ✓
- **Your call:** 

### ⚠️ #15 (everyday) Why do I lean back when the bus suddenly starts?
- **Gold:** 1:5.2 Newton's First Law; 1:6.3 Centripetal Force  
  _note: 6.3 (Inertial Forces) uses the same example: being pushed back into a jet seat. Added after reviewing T5 answers; it was wrongly scored as a miss._
- 1. 2:13.6 Electric Generators and Back Emf › Back Emf
- 2. 2:10.2 Resistors in Series and Parallel › Practical Implications
- 3. 1:None Introduction
- **Your call:** 

### #16 (everyday) Why does a spinning ice skater speed up when she pulls her arms in?
- **Gold:** 1:11.3 Conservation of Angular Momentum
- 1. 1:11.3 Conservation of Angular Momentum ✓
- 2. 1:11.2 Angular Momentum
- 3. 1:11.3 Conservation of Angular Momentum ✓
- **Your call:** 

### #17 (everyday) Why does a siren sound higher when the ambulance comes toward me and lower after it passes?
- **Gold:** 1:17.7 The Doppler Effect
- 1. 1:17.7 The Doppler Effect ✓
- 2. 1:17.3 Sound Intensity
- 3. 1:17.2 Speed of Sound › Derivation of the Speed of Sound in Air
- **Your call:** 

### #18 (everyday) Why does a huge ship made of steel float?
- **Gold:** 1:14.4 Archimedes’ Principle and Buoyancy
- 1. 1:14.4 Archimedes’ Principle and Buoyancy › Density and Archimedes’ Principle ✓
- 2. 1:14.1 Fluids, Density, and Pressure › Density
- 3. 1:14.4 Archimedes’ Principle and Buoyancy › Density and Archimedes’ Principle ✓
- **Your call:** 

### ⚠️ #19 (everyday) Why does a gun kick back when it is fired?
- **Gold:** 1:9.3 Conservation of Linear Momentum; 1:9.4 Types of Collisions
- 1. 2:13.3 Motional Emf
- 2. 1:9.4 Types of Collisions › Explosions ✓
- 3. 1:5.5 Newton’s Third Law
- **Your call:** 

### #20 (everyday) Why is it easier to open a door when you push far from the hinges?
- **Gold:** 1:10.6 Torque
- 1. 1:10.6 Torque › Defining Torque ✓
- 2. 1:6.2 Friction › Static and Kinetic Friction
- 3. 3:1.6 Huygens’s Principle › Diffraction
- **Your call:** 

### #21 (everyday) Why do astronauts on the space station look weightless?
- **Gold:** 1:13.2 Gravitation Near Earth's Surface; 1:13.4 Satellite Orbits and Energy
- 1. 1:13.4 Satellite Orbits and Energy › Circular Orbits ✓
- 2. 1:13.7 Einstein's Theory of Gravity › The Principle of Equivalence
- 3. 3:5.3 Time Dilation › The Twin Paradox
- **Your call:** 

### #22 (everyday) Why can a car slide off a curved road when the road is icy?
- **Gold:** 1:6.2 Friction; 1:6.3 Centripetal Force
- 1. 1:6.3 Centripetal Force › Banked Curves ✓
- 2. 1:11.1 Rolling Motion › Rolling Motion without Slipping
- 3. 1:None Introduction
- **Your call:** 

### ⚠️ #23 (everyday) Why do two guitar strings that are slightly out of tune make a wobbling wah-wah sound?
- **Gold:** 1:17.6 Beats
- 1. 1:17.5 Sources of Musical Sound › Resonance
- 2. 1:15.1 Simple Harmonic Motion
- 3. 1:15.5 Damped Oscillations
- **Your call:** 

### #24 (everyday) Why does a skydiver stop speeding up after falling for a while?
- **Gold:** 1:6.4 Drag Force and Terminal Speed
- 1. 1:6.4 Drag Force and Terminal Speed › Terminal Velocity ✓
- 2. 1:6.4 Drag Force and Terminal Speed › Terminal Velocity ✓
- 3. 1:6.4 Drag Force and Terminal Speed › Terminal Velocity ✓
- **Your call:** 

### #25 (everyday) Why does a grandfather clock with a swinging weight keep regular time?
- **Gold:** 1:15.4 Pendulums
- 1. 1:15.4 Pendulums ✓
- 2. 3:5.3 Time Dilation
- 3. 1:15.1 Simple Harmonic Motion
- **Your call:** 

### #26 (everyday) How can a rocket move forward in empty space with nothing to push against?
- **Gold:** 1:9.7 Rocket Propulsion
- 1. 1:9.7 Rocket Propulsion ✓
- 2. 1:5.5 Newton’s Third Law
- 3. 1:9.7 Rocket Propulsion › Physical Analysis ✓
- **Your call:** 

### #27 (everyday) Why does water come out faster when I put my thumb over the end of a garden hose?
- **Gold:** 1:14.5 Fluid Dynamics
- 1. 1:14.5 Fluid Dynamics › Flow Rate and its Relation to Velocity ✓
- 2. 2:5.1 Electric Charge › Discoveries
- 3. 1:6.4 Drag Force and Terminal Speed
- **Your call:** 

### #28 (everyday) Why does the ocean rise and fall twice a day?
- **Gold:** 1:13.6 Tidal Forces
- 1. 1:13.6 Tidal Forces › Lunar Tides ✓
- 2. 1:13.6 Tidal Forces › Lunar Tides ✓
- 3. 1:13.6 Tidal Forces ✓
- **Your call:** 

### #29 (term) Bernoulli's equation
- **Gold:** 1:14.6 Bernoulli’s Equation
- 1. 1:14.6 Bernoulli’s Equation › Glossary ✓
- 2. 1:14.6 Bernoulli’s Equation › Bernoulli’s principle ✓
- 3. 1:14.6 Bernoulli’s Equation › Energy Conservation and Bernoulli’s Equation ✓
- **Your call:** 

### #30 (term) Pascal's principle
- **Gold:** 1:14.3 Pascal's Principle and Hydraulics
- 1. 1:14.3 Pascal's Principle and Hydraulics › Pascal’s Principle ✓
- 2. 1:14.3 Pascal's Principle and Hydraulics › Glossary ✓
- 3. 1:14.3 Pascal's Principle and Hydraulics ✓
- **Your call:** 

### #31 (term) Young's modulus
- **Gold:** 1:12.3 Stress, Strain, and Elastic Modulus
- 1. 1:12.3 Stress, Strain, and Elastic Modulus › Tensile or Compressive Stress, Strain, and Young’s Modulus ✓
- 2. 1:12.3 Stress, Strain, and Elastic Modulus › Glossary ✓
- 3. 1:12.3 Stress, Strain, and Elastic Modulus › Tensile or Compressive Stress, Strain, and Young’s Modulus ✓
- **Your call:** 

### #32 (term) moment of inertia of a thin rod
- **Gold:** 1:10.5 Calculating Moments of Inertia
- 1. 1:10.5 Calculating Moments of Inertia › A uniform thin rod with an axis through the center ✓
- 2. 1:10.5 Calculating Moments of Inertia › A uniform thin rod with an axis through the center ✓
- 3. 1:10.5 Calculating Moments of Inertia › A uniform thin rod with an axis through the center ✓
- **Your call:** 

### #33 (term) Doppler effect formula
- **Gold:** 1:17.7 The Doppler Effect
- 1. 1:17.7 The Doppler Effect › Derivation of the Observed Frequency due to the Doppler Shift ✓
- 2. 1:17.7 The Doppler Effect › Derivation of the Observed Frequency due to the Doppler Shift ✓
- 3. 1:17.7 The Doppler Effect › Derivation of the Observed Frequency due to the Doppler Shift ✓
- **Your call:** 

### #34 (term) escape velocity
- **Gold:** 1:13.3 Gravitational Potential Energy and Total Energy
- 1. 1:13.3 Gravitational Potential Energy and Total Energy › Escape velocity ✓
- 2. 1:13.3 Gravitational Potential Energy and Total Energy › Energy and gravitationally bound objects ✓
- 3. 1:13.3 Gravitational Potential Energy and Total Energy › Glossary ✓
- **Your call:** 

### #35 (term) impulse-momentum theorem
- **Gold:** 1:9.2 Impulse and Collisions
- 1. 1:9.2 Impulse and Collisions › Effect of Impulse ✓
- 2. 1:9.2 Impulse and Collisions › Glossary ✓
- 3. 1:9.2 Impulse and Collisions › Effect of Impulse ✓
- **Your call:** 

### #36 (term) scalar product of two vectors
- **Gold:** 1:2.4 Products of Vectors
- 1. 1:2.4 Products of Vectors › The Scalar Product of Two Vectors (the Dot Product) ✓
- 2. 1:2.4 Products of Vectors › The Scalar Product of Two Vectors (the Dot Product) ✓
- 3. 1:2.4 Products of Vectors ✓
- **Your call:** 

### #37 (term) terminal velocity
- **Gold:** 1:6.4 Drag Force and Terminal Speed
- 1. 1:6.4 Drag Force and Terminal Speed › Terminal Velocity ✓
- 2. 1:6.4 Drag Force and Terminal Speed › Glossary ✓
- 3. 1:6.4 Drag Force and Terminal Speed › Terminal Velocity ✓
- **Your call:** 

### #38 (term) parallel axis theorem
- **Gold:** 1:10.5 Calculating Moments of Inertia
- 1. 1:10.5 Calculating Moments of Inertia › The Parallel-Axis Theorem ✓
- 2. 1:10.5 Calculating Moments of Inertia › The Parallel-Axis Theorem ✓
- 3. 1:10.5 Calculating Moments of Inertia › Glossary ✓
- **Your call:** 

### #39 (term) significant figures
- **Gold:** 1:1.6 Significant Figures
- 1. 1:1.6 Significant Figures › Glossary ✓
- 2. 1:1.6 Significant Figures › Zeros ✓
- 3. 1:1.6 Significant Figures › Significant figures in this text ✓
- **Your call:** 

### #40 (term) Fermi estimate
- **Gold:** 1:1.5 Estimates and Fermi Calculations
- 1. 1:1.5 Estimates and Fermi Calculations › Glossary ✓
- 2. 1:1.5 Estimates and Fermi Calculations ✓
- 3. 1:1.5 Estimates and Fermi Calculations ✓
- **Your call:** 

### #41 (term) Reynolds number
- **Gold:** 1:14.7 Viscosity and Turbulence
- 1. 1:14.7 Viscosity and Turbulence › Measuring Turbulence ✓
- 2. 1:14.7 Viscosity and Turbulence › Glossary ✓
- 3. 1:14.7 Viscosity and Turbulence › Measuring Turbulence ✓
- **Your call:** 

### #42 (term) damped harmonic oscillator
- **Gold:** 1:15.5 Damped Oscillations
- 1. 1:15.5 Damped Oscillations › Glossary ✓
- 2. 2:15.5 Resonance in an AC Circuit
- 3. 1:15.5 Damped Oscillations ✓
- **Your call:** 

### #43 (complex) What is the origin of redshift: the Doppler effect or relativity? Which one is the real explanation?
- **Gold:** 1:17.7 The Doppler Effect; 3:5.7 Doppler Effect for Light; 3:11.6 The Big Bang  
  _note: Comparison question across volumes: Doppler for sound (1:17.7), Doppler effect for light (3:5.7), cosmological redshift and Hubble's law (3:11.6). With only Volume 1 loaded, the answer should say relativity and cosmology aren't covered._
- 1. 1:17.7 The Doppler Effect ✓
- 2. 1:17.7 The Doppler Effect › Derivation of the Observed Frequency due to the Doppler Shift ✓
- 3. 3:11.6 The Big Bang › Glossary ✓
- **Your call:** 

### #44 (everyday) Why does a balloon stick to the wall after I rub it on my hair?
- **Gold:** 2:5.1 Electric Charge; 2:5.2 Conductors, Insulators, and Charging by Induction
- 1. 2:5.1 Electric Charge › Discoveries ✓
- 2. 2:5.1 Electric Charge › Discoveries ✓
- 3. 1:6.2 Friction › Atomic-Scale Explanations of Friction
- **Your call:** 

### #45 (everyday) Why do I get a small shock when I touch a doorknob after walking across a carpet?
- **Gold:** 2:5.1 Electric Charge; 2:5.2 Conductors, Insulators, and Charging by Induction
- 1. 2:5.1 Electric Charge › Discoveries ✓
- 2. 2:1.6 Mechanisms of Heat Transfer › Conduction
- 3. 1:6.2 Friction › Static and Kinetic Friction
- **Your call:** 

### #46 (textbook) What does the first law of thermodynamics state?
- **Gold:** 2:3.3 First Law of Thermodynamics
- 1. 2:3.3 First Law of Thermodynamics ✓
- 2. 2:3.3 First Law of Thermodynamics ✓
- 3. 2:3.3 First Law of Thermodynamics ✓
- **Your call:** 

### #47 (term) Carnot cycle
- **Gold:** 2:4.5 The Carnot Cycle
- 1. 2:4.5 The Carnot Cycle ✓
- 2. 2:4.5 The Carnot Cycle › Glossary ✓
- 3. 2:4.5 The Carnot Cycle ✓
- **Your call:** 

### #48 (everyday) How does a refrigerator keep food cold?
- **Gold:** 2:4.3 Refrigerators and Heat Pumps
- 1. 2:4.3 Refrigerators and Heat Pumps ✓
- 2. 2:4.3 Refrigerators and Heat Pumps ✓
- 3. 2:4.4 Statements of the Second Law of Thermodynamics
- **Your call:** 

### ⚠️ #49 (textbook) What is Faraday's law of induction?
- **Gold:** 2:13.1 Faraday’s Law
- 1. 2:13.7 Applications of Electromagnetic Induction
- 2. 2:13.1 Faraday’s Law ✓
- 3. 2:13.1 Faraday’s Law › Glossary ✓
- **Your call:** 

### #50 (everyday) Why does a straw look bent when it stands in a glass of water?
- **Gold:** 3:1.3 Refraction; 3:2.3 Images Formed by Refraction
- 1. 3:2.3 Images Formed by Refraction › Refraction at a Plane Interface—Apparent Depth ✓
- 2. 1:16.6 Standing Waves and Resonance › Standing Waves
- 3. 3:None Introduction
- **Your call:** 

### #51 (everyday) Why do we see a rainbow after it rains?
- **Gold:** 3:1.5 Dispersion
- 1. 3:1.5 Dispersion ✓
- 2. 3:1.5 Dispersion ✓
- 3. 3:1.5 Dispersion ✓
- **Your call:** 

### #52 (textbook) What is the photoelectric effect?
- **Gold:** 3:6.2 Photoelectric Effect
- 1. 3:6.2 Photoelectric Effect ✓
- 2. 3:6.2 Photoelectric Effect › Glossary ✓
- 3. 3:6.2 Photoelectric Effect › Glossary ✓
- **Your call:** 

### #53 (term) time dilation
- **Gold:** 3:5.3 Time Dilation
- 1. 3:5.3 Time Dilation ✓
- 2. 3:5.3 Time Dilation › Glossary ✓
- 3. 3:5.3 Time Dilation ✓
- **Your call:** 

### ⚠️ #54 (everyday) How do we know the universe is expanding?
- **Gold:** 3:11.6 The Big Bang
- 1. 3:11.7 Evolution of the Early Universe › Dark Matter and Dark Energy
- 2. 3:11.7 Evolution of the Early Universe
- 3. 3:11.6 The Big Bang › Structure and Dynamics of the Universe ✓
- **Your call:** 

### #55 (term) Heisenberg uncertainty principle
- **Gold:** 3:7.2 The Heisenberg Uncertainty Principle
- 1. 3:7.2 The Heisenberg Uncertainty Principle ✓
- 2. 3:7.2 The Heisenberg Uncertainty Principle › Glossary ✓
- 3. 3:7.2 The Heisenberg Uncertainty Principle › Momentum and Position ✓
- **Your call:** 
