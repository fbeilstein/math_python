# From Data to Topology

In practice, we start not with a simplicial complex but with a **point cloud** $X = \\{x_1, \dots, x_N\\} \subset \mathbb{R}^d$.

**The fundamental problem:** What is the "shape" of $X$? We want to detect topological features (clusters, loops, voids), but a finite point set has trivial topology — it's just $N$ disconnected points.

**Idea:** Thicken each point into a ball of radius $\epsilon$ and study the topology of the union $\bigcup_{i} B(x_i, \epsilon)$.

**The dilemma:**
- $\epsilon$ too small → disconnected dust, $\beta_0 = N$, no structure
- $\epsilon$ too large → single blob, $\beta_0 = 1$, all structure drowned
- Just right → reveals the underlying topology

**Solution:** Don't choose a single $\epsilon$. Use **all scales simultaneously** and track which features persist.

---

# Čech Complex

**Definition.** The **Čech complex** $\check{C}\_\epsilon(X)$ at scale $\epsilon$ is the abstract simplicial complex where:
$$
\sigma = \\{x_{i_0}, \dots, x_{i_k}\\} \in \check{C}\_\epsilon(X) \quad \iff \quad \bigcap_{j=0}^{k} B(x_{i_j}, \epsilon) \neq \emptyset
$$

A simplex exists iff the $\epsilon$-balls around **all** its vertices have a common point of intersection.

**Nerve Theorem.** If all intersections $\bigcap B(x_{i_j}, \epsilon)$ are contractible (which is the case for convex sets like balls), then:
$$
|\check{C}\_\epsilon(X)| \simeq \bigcup_{i} B(x_i, \epsilon)
$$

The Čech complex has the same homotopy type as the union of balls! Its homology exactly captures the topology of the thickened point cloud.

**Drawback:** Checking if $k+1$ balls have a common intersection is computationally expensive for $k \ge 2$.

---

# Vietoris-Rips Complex

**Definition.** The **Vietoris-Rips complex** $\text{VR}\_\epsilon(X)$ at scale $\epsilon$:
$$
\sigma = \\{x_{i_0}, \dots, x_{i_k}\\} \in \text{VR}\_\epsilon(X) \quad \iff \quad d(x_{i_a}, x_{i_b}) \le 2\epsilon \;\; \forall \; a, b
$$

A simplex exists iff **all pairwise distances** are at most $2\epsilon$. We only need the distance matrix!

**Comparison with Čech:**
$$
\check{C}\_\epsilon(X) \subseteq \text{VR}\_\epsilon(X) \subseteq \check{C}\_{\epsilon\sqrt{2}}(X)
$$

The Rips complex is a (slightly coarser) approximation to the Čech complex, but is **much cheaper to compute**: we only check pairs, never higher-order intersections.

![](./assets/rips_vs_alpha.png){width=80% center}

In practice, Vietoris-Rips is the standard choice for computational TDA.

---

# Filtrations

As $\epsilon$ grows, we get a nested sequence of simplicial complexes:
$$
\emptyset = \mathcal{K}\_{\epsilon_0} \subseteq \mathcal{K}\_{\epsilon_1} \subseteq \mathcal{K}\_{\epsilon_2} \subseteq \cdots \subseteq \mathcal{K}\_{\epsilon_N}
$$

This is called a **filtration**. At each step, new simplices are born (edges appear, triangles fill in, etc.).

The inclusion maps $\mathcal{K}\_{\epsilon_i} \hookrightarrow \mathcal{K}\_{\epsilon_{i+1}}$ induce homomorphisms on homology:
$$
H_p(\mathcal{K}\_{\epsilon_i}) \to H_p(\mathcal{K}\_{\epsilon_{i+1}})
$$

These homomorphisms let us **track** individual homology classes as they evolve across the filtration.

![](./assets/filtration_steps.png){width=90% center}

---

# Birth and Death of Features

As $\epsilon$ increases through the filtration, homology classes are **born** and **die**:

**Birth ($b$):** The scale at which a new homology class first appears.
- A new connected component ($H_0$): when a point first enters
- A new loop ($H_1$): when edges close a cycle that isn't yet filled
- A new cavity ($H_2$): when triangles enclose a void

**Death ($d$):** The scale at which the class becomes trivial.
- A component dies: when it merges with an older component (elder rule)
- A loop dies: when it gets filled in by a triangle
- A cavity dies: when it gets filled in by tetrahedra

**Persistence:** $\text{pers} = d - b$ measures how long a feature survives.
- **Long-lived features** ($d - b$ large) → genuine topological signal
- **Short-lived features** ($d - b$ small) → likely noise

---

# Persistence Diagrams

Each topological feature is represented as a point $(b, d)$ in the **persistence diagram**:

$$
\text{Dgm}_p(X) = \\{(b_i, d_i) : \text{each } H_p \text{ class } i\\} \subset \\{(b, d) : 0 \le b < d \le \infty\\}
$$

**Reading the diagram:**
- Points **far from the diagonal** $d = b$ → significant, persistent features
- Points **close to the diagonal** → noise, ephemeral fluctuations
- Points on the line $d = \infty$ → features that never die (e.g., the last connected component)

**Color coding by dimension:**
- $H_0$ features (components) — typically in one color
- $H_1$ features (loops) — in another
- $H_2$ features (cavities) — in a third

The persistence diagram is a **complete topological summary** of the point cloud at all scales simultaneously.

---

# Barcodes

An equivalent representation: each feature is a horizontal bar $[b, d)$:

| Feature | Birth | Death | Bar |
|---------|-------|-------|-----|
| Component A | 0.0 | 0.5 | ━━━━━ |
| Component B | 0.0 | $\infty$ | ━━━━━━━━━━━━→ |
| Loop 1 | 0.3 | 0.7 | ━━━━━━━ |
| Loop 2 | 0.4 | 0.45 | ━ |

**Barcodes vs persistence diagrams:**
- Barcodes are visually clearer for reading individual features
- Persistence diagrams are better for comparing datasets (via distances)
- They carry exactly the same information — just different visualizations

![](./assets/torus_persistence.png){width=90% center}

---

# Stability Theorem

The most important theoretical result in persistent homology:

**Stability Theorem (Cohen-Steiner, Edelsbrunner, Harer, 2007).**

If two point clouds $X$ and $Y$ are close (in Hausdorff distance), then their persistence diagrams are close (in bottleneck distance):

$$
d_B\big(\text{Dgm}(X), \text{Dgm}(Y)\big) \le d_H(X, Y)
$$

**Why this matters:**
- Small perturbations in data → small perturbations in the diagram
- Outliers and noise produce short bars (near the diagonal), not catastrophic changes
- Persistent homology is **robust** — it works on real, noisy, sampled data

This is **the** reason persistent homology has become a standard tool in applied mathematics. Without stability, the entire framework would be a mathematical curiosity with no practical value.

---

# Interactive: Persistent Homology Explorer

Explore how the Čech complex evolves as the radius parameter grows, and watch the persistence diagram update in real time.

<button class="demo-btn" onclick="showDemo('https://fbeilstein.github.io/topological_data_analysis/persistent_homology_explorer/persistent_homology_explorer.html')">
    Launch Persistent Homology Explorer 🔬
</button>
