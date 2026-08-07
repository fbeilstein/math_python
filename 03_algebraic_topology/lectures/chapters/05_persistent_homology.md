# From Data to Topology

In practice, we often start not with a simplicial complex, not even with a topological space, but rather a **point cloud** $X = \\{x_1, \dots, x_N\\} \subset \mathbb{R}^d$.

**The fundamental problem:** there is nothing interesting about the topology of $X$ — it's just $N$ disconnected points.

**The question:** Is there any topological space naturally associated with $X$ whose topology we can study?

**Idea 1:** Thicken each point into a ball of radius $\epsilon$ and study the topology of the union $\bigcup_{i} B(x_i, \epsilon)$. We can trangulate this union to get a simplicial complex and apply our tools.

**Idea 2:** Directly associate an abstract simplicial comlex with $X$ and study with our methods. 

![](./assets/point_cloud_thickening.png){width=60% center}

---

# Čech Complex

:::matrix {cols="50/50"}
[[0,0]]
**Definition.** The **Čech complex** $\check{C}\_\epsilon(X)$ at scale $\epsilon$ is the abstract simplicial complex where:
$$
\sigma = \\{x_{i_0}, \dots, x_{i_k}\\} \in \check{C}\_\epsilon(X) \quad \iff \quad \bigcap_{j=0}^{k} B(x_{i_j}, \epsilon) \neq \emptyset
$$

A simplex exists iff the $\epsilon$-balls around **all** its vertices have a common point of intersection.

**Note:** May be much-much higher-dimensional than the original point cloud.

[[0,1]]
**Nerve Theorem.** If all intersections $\bigcap B(x_{i_j}, \epsilon)$ are contractible (which is the case for convex sets like balls), then:
$$
|\check{C}\_\epsilon(X)| \simeq \bigcup_{i} B(x_i, \epsilon)
$$

The Čech complex has the same homotopy type as the union of balls! Its homology exactly captures the topology of the thickened point cloud.

**Drawback:** Checking if $k+1$ balls have a common intersection is computationally expensive for $k \ge 2$.
:::

# Vietoris-Rips Complex

:::matrix {cols="50/50"}
[[0,0]]
**Definition.** The **Vietoris-Rips complex** $\text{VR}\_\epsilon(X)$ at scale $\epsilon$:
$$
\sigma = \\{x_{i_0}, \dots, x_{i_k}\\} \in \text{VR}\_\epsilon(X) \quad \iff \quad d(x_{i_a}, x_{i_b}) \le 2\epsilon \;\; \forall \; a, b
$$

A simplex exists iff **all pairwise distances** are at most $2\epsilon$. We only need the distance matrix! In practice, Vietoris-Rips is the standard choice for computational TDA.

[[0,1]]
**Comparison with Čech:**
$$
\check{C}\_\epsilon(X) \subseteq \text{VR}\_\epsilon(X) \subseteq \check{C}\_{\epsilon\sqrt{2}}(X)
$$

The Rips complex is a (slightly coarser) approximation to the Čech complex, but is **much cheaper to compute**: we only check pairs, never higher-order intersections.
:::

---


# Filtrations

As $\epsilon$ grows, we get a nested sequence of different simplicial complexes
$
\emptyset = \mathcal{K}\_{\epsilon_0} \subseteq \mathcal{K}\_{\epsilon_1} \subseteq \mathcal{K}\_{\epsilon_2} \subseteq \cdots \subseteq \mathcal{K}\_{\epsilon_N}
$
called a **filtration**.

**Question:** Which simplex to study? **Unexpected Answer:** None of them — study the **evolution of the entire filtration**!

The inclusion maps $\mathcal{K}\_{\epsilon_i} \hookrightarrow \mathcal{K}\_{\epsilon_{i+1}}$ induce homomorphisms on homology:
$
H_p(\mathcal{K}\_{\epsilon_i}) \to H_p(\mathcal{K}\_{\epsilon_{i+1}})
$

These homomorphisms let us **track** individual homology classes as they evolve across the filtration.

<iframe src="./demos/filtration/filtration.html" width="100%" height="550px" style="border:1px solid #ddd; border-radius: 8px; margin: 20px 0;"></iframe>

---

# Persistence Diagrams

**Definition.** A **persistence diagram** is a multiset of points in the upper-half plane:
$$
\text{Dgm}(X) = \\{(b_i, d_i) : i=1, \dots, n \\} \subset \\{(b, d) : 0 \le b < d \le \infty\\}
$$

:::matrix {cols="20/80"}
[[0,0]]
Each point $(b_i, d_i)$ represents a homology class that is **born** at scale $b_i$ and **dies** at scale $d_i$ in a filtration.

**Persistence:** $\text{pers} = d - b$ measures how long a feature survives.
- **Long-lived features** ($d - b$ large) → genuine topological signal
- **Short-lived features** ($d - b$ small) → likely noise

[[0,1]]
<iframe src="./demos/persistence_diagrams/persistence_diagrams_demo.html" width="100%" height="600px" style="border:1px solid #ddd; border-radius: 8px; margin: 20px 0;"></iframe>
:::


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

# Interactive: Persistent Homology Explorer

Explore how the Čech complex evolves as the radius parameter grows, and watch the persistence diagram update in real time.

<button class="demo-btn" onclick="showDemo('https://fbeilstein.github.io/topological_data_analysis/persistent_homology_explorer/persistent_homology_explorer.html')">
    Launch Persistent Homology Explorer 🔬
</button>
