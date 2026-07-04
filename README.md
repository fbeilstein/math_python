
# Math with Python

A semester course exploring deep mathematical topics through hands-on Python programming. The course is structured as **4 modules** with a kickoff session, each pairing a theory lecture with a practice lab.

## Course Structure

### The Kickoff
**Session 1 — Linear Algebra & Optics** (Combined Lecture + Practice)
- Lecture: [Linear Algebra & Optics](https://fbeilstein.github.io/math_python/00_kickoff/lectures/01_linear_algebra_optics.html)
- Practice: [Optics](https://github.com/fbeilstein/math_python/releases/download/optics_v0/optical_problem.zip)

---

### Module 1: Quantum Mechanics
**Session 2 — Lecture: The Split-Operator Method**
- Time-Dependent Schrödinger Equation, wavepackets, Fourier methods

**Session 3 — Practice: Quantum Tunneling**
- Discretizing space/time, FFT, complex arrays, wavepacket propagation
- Practice: [`quantum_problem`](01_quantum_mechanics/practice/quantum_problem/)

---

### Module 2: Abstract Algebra
**Session 4 — Lecture: Theory of Galois Fields**
- Polynomial arithmetic, finite fields, Reed-Solomon error correction

**Session 5 — Practice: Generating QR Codes**
- Bitwise operations, binary matrix manipulation, encoding strings into scannable QR grids
- Practice: [`qr_problem`](02_abstract_algebra/practice/qr_problem/)
- Related optional problems: [`cayley_problem`](02_abstract_algebra/optional/cayley_problem/), [`rsa_problem`](02_abstract_algebra/optional/rsa_problem/)

---

### Module 3: Algebraic Topology
**Session 6 — Lecture: Theory of Homologies**
- Simplicial complexes, boundary operators, Betti numbers

**Session 7 — Practice: Computing Homologies**
- Matrix reduction (Smith Normal Form), Betti number computation
- Practice: [`homology_problem`](03_algebraic_topology/practice/homology_problem/)

---

### Module 4: Systems Biochemistry
**Session 8 — Lecture: Theory of Biological Networks**
- Enzymatic kinetics, metabolic pathways, ODEs for biochemical systems

**Session 9 — Practice: Simulating Biochemical Systems**
- Glycolytic oscillations in yeast, bioswitches, bifurcation analysis
- Practice: [`biochem_problem`](04_systems_biochemistry/practice/biochem_problem/)

---

## Optional Problem Sets

Additional problems for warm-up or advanced students:

| Problem | Topic |
|---|---|
| [autodiff_duals_problem](optional/autodiff_duals_problem/) | Automatic Differentiation with Dual Numbers |
| [esher_droste_problem](optional/esher_droste_problem/) | Escher-Droste Transformation |
| [evolutionary_game_problem](optional/evolutionary_game_problem/) | Evolutionary Game Theory |
| [fractals_problem](optional/fractals_problem/) | Drawing Fractals |
| [kinematics_problem](optional/kinematics_problem/) | Kinematics with Hypercomplex Numbers |
| [lsh_problem](optional/lsh_problem/) | Locality-Sensitive Hashing |
| [markov_chain_problem](optional/markov_chain_problem/) | Markov Chains |
| [spectral_graph_problem](optional/spectral_graph_problem/) | Spectral Graph Theory |
| [stability_problem](optional/stability_problem/) | Differential Equation Stability |
| [tron_problem](optional/tron_problem/) | Topological Game |

## Lectures

Each module contains its own HTML lecture files. To view lectures locally, you must run the server from the root of the repository:

```bash
# From the math_python root directory:
python -m http.server 8000
# Open http://localhost:8000/00_kickoff/lectures/01_linear_algebra_optics.html
```

The presentation engine is included as a git submodule:

```bash
git clone --recurse-submodules <repo-url>
```

## Download Problem Sets


- [Esher-Droste Transformation](https://github.com/fbeilstein/math_python/releases/download/esher_v0/esher_droste_problem.zip)
- [Generate QR-code](https://github.com/fbeilstein/math_python/releases/download/qr_v1/qr_problem.zip)
- [Compute Homologies](https://github.com/fbeilstein/math_python/releases/download/homology_v0/homology_problem.zip)
- [Compute Autodiff with Dual Numbers](https://github.com/fbeilstein/math_python/releases/download/autodiff_v0/autodiff_duals_problem.zip)
- [Kinematics with Hypercomplex Numbers](https://github.com/fbeilstein/math_python/releases/download/kinematics_v0/kinematics_problem.zip)
- [Drawing Fractals](https://github.com/fbeilstein/math_python/releases/download/fractals_v0/fractals_problem.zip)
- [Elementary Group Theory](https://github.com/fbeilstein/math_python/releases/download/cayley_v0/cayley_problem.zip)
- [Game Theory, Tournament](https://github.com/fbeilstein/math_python/releases/download/tournament_v0/evolutionary_game_problem.zip)
- [Spectral Graph Theory, Segmentation](https://github.com/fbeilstein/math_python/releases/download/spectral_graph_v0/spectral_graph_problem.zip)
- [Markov Chain Problem](https://github.com/fbeilstein/math_python/releases/download/markov_v0/markov_chain_problem.zip)
- [RSA Encryption](https://github.com/fbeilstein/math_python/releases/download/rsa_v0/rsa_problem.zip)
- [Explore Differential Equation Stability](https://github.com/fbeilstein/math_python/releases/download/stability_v0/stability_problem.zip)
- [Quantum Tunneling](https://github.com/fbeilstein/math_python/releases/download/quanta_v0/quantum_problem.zip)
- [Optics](https://github.com/fbeilstein/math_python/releases/download/optics_v0/optical_problem.zip)
- [Topological Game](https://github.com/fbeilstein/math_python/releases/download/topo_v0/tron_problem.zip)
- [Duplicate Documents Search](https://github.com/fbeilstein/math_python/releases/download/lsh_v0/lsh_problem.zip)
