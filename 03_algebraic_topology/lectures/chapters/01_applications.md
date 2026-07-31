# Where This Math Lives

Topology is not abstract — it is the mathematical language behind some of the most powerful tools in modern science and engineering.

<div class="smaller-table">

| Domain | What Topology Detects | Key Technique |
|--------|----------------------|---------------|
| **Sensor networks** | Coverage holes in surveillance grids | $H_k$ of Rips complex |
| **Cosmology** | Cosmic voids, filaments, and walls | Persistent $H_0, H_1, H_2$ of galaxy point clouds |
| **Molecular biology** | Protein folding, drug binding pockets | Persistence diagrams + Wasserstein distance |
| **Materials science** | Amorphous vs crystalline structure | Persistent homology of atom configurations |
| **Neuroscience** | Functional brain connectivity patterns | Persistent $H_1$ of correlation networks (Blue Brain Project) |
| **Time series** | Periodicity, quasi-periodicity detection | Takens embedding → sliding window persistence |
| **NLP** | Document and language similarity | Persistence of word embedding point clouds |
| **Image recognition** | Texture and shape descriptors | Cubical persistence on pixel grids |
| **Robotics** | Configuration space obstacles | $H_1$ detects topological obstacles |
| **Financial markets** | Crash detection, regime change | Persistent homology of correlation networks |
| **DNA analysis** | Knotting, linking, entanglement | Persistent Jones polynomials |

</div>

---

# Sensor Networks: Finding Coverage Holes

**Problem:** Given a network of sensors with limited range, does the network cover the entire region? Where are the gaps?

**Topology's answer:** Build the Rips complex $\text{VR}_\epsilon$ from the sensor positions. If $H\_1(\\text{VR}\_\epsilon) \neq 0$, there exist coverage holes. The generators of $H_1$ localize them.

Robert Ghrist (2005): *"Homological methods provide a coordinate-free, robust criterion for coverage verification."*

This works even when sensors don't know their own coordinates — only pairwise communication ranges matter.

# Cosmology: The Shape of the Universe

Galaxies are not uniformly distributed. They form a **cosmic web** of filaments, walls, sheets, and voids.

- $H_0$: connected components (galaxy clusters)
- $H_1$: filamentary loops
- $H_2$: enclosed voids

Persistent homology reveals the multi-scale structure that classical statistics misses entirely.

