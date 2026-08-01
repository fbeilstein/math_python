# Topology: From Sand to Structure

:::matrix { cols="50/50" rows="100" height="85%"}

[[0, 0]]
![](./assets/sand_through_fingers.jpg){height=80% center}

[[0, 1]]

A bare set is like sand — elements slip through your fingers with no coherence, no continuity, no notion of "nearby."

**Topology glues points together into a structure**, giving meaning to neighborhoods, paths, and deformations.

The price of this glue? We must specify which points are neighbors to which. This is performed by defining the topology $\tau$ on $X$, which is equivalent to specifying the collection of subsets we call "open."

:::

---

# Topological Spaces

**Definition.** Let $X$ be a non-empty set. A collection $\tau$ of subsets of $X$ is called **a topology** on $X$ if:

1. $X \in \tau$ and $\emptyset \in \tau$
2. The union of any (finite or infinite) family of sets in $\tau$ belongs to $\tau$
3. The intersection of any **finite** family of sets in $\tau$ belongs to $\tau$

The pair $(X, \tau)$ is called a **topological space**. Members of $\tau$ are called **open sets**.

**Examples:**
- **Discrete topology:** $\tau = \mathcal{P}(X)$ (every subset is open) — maximum resolution, every point is isolated
- **Indiscrete topology:** $\tau = \\{X, \emptyset\\}$ — no resolution at all, all points are "glued together"
- **Standard topology on $\mathbb{R}$:** open sets are unions of open intervals $(a, b)$

---

# Basis for a Topology

**Definition.** A collection $\mathcal{B} \subseteq \tau$ is a **basis** for the topology $\tau$ if every open set $U \in \tau$ can be written as a union of elements of $\mathcal{B}$.

**Why this matters:** We don't need to specify every open set — just a generating family.

**Examples:**
- Open intervals $(a, b)$ form a basis for the standard topology on $\mathbb{R}$
- Open balls $B(x, r) = \\{y \mid d(x,y) < r\\}$ form a basis for any metric topology
- Open rectangles $(a,b) \times (c,d)$ form a basis for the standard topology on $\mathbb{R}^2$

**Comparing topologies:** If $\tau_1 \supset \tau_2$, we say $\tau_1$ is **finer** (more open sets, sharper resolution) and $\tau_2$ is **coarser**.

$$
\underbrace{\tau_1}\_{\text{finer}} \supset \underbrace{\tau_2}\_{\text{coarser}}
$$

---

# Building New Spaces

Three fundamental constructions produce new topological spaces from existing ones:

**Subspace topology.** Let $Y \subseteq X$. Define $\tau_Y = \\{U \cap Y : U \in \tau_X\\}$. 

**Product topology.** On $X \times Y$, the basis consists of products $U \times V$ where $U \in \tau_X$, $V \in \tau_Y$.

**Quotient topology.** Given a surjection $p: X \to Y$, define $U \subseteq Y$ to be open iff $p^{-1}(U) \in \tau_X$. This "glues" points together.

:::matrix { cols="50/50" rows="100" height="50%"}

[[0, 0]]
![](./assets/quotient_space_topology_example.png){height=90% center}

[[0, 1]]
**Key examples of quotient spaces:**
- **Torus** $T^2$: identify opposite edges of $[0,1]^2$
- **Möbius strip**: identify one pair of edges with a twist
- **Klein bottle**: identify both pairs with one twisted
- $\mathbb{R}/\mathbb{Z} \cong S^1$: wrap the real line into a circle

:::

---

# Continuity

Two equivalent definitions of a continuous map $f: X \to Y$:

**(A) Pointwise ("close points stay close"):** For every $x \in X$ and every open set $V$ containing $f(x)$, there exists an open set $U$ containing $x$ such that $f(U) \subseteq V$.

**(B) Global (preimages):** For every open set $V \in \tau_Y$, the preimage $f^{-1}(V) \in \tau_X$.

**Proof of equivalence.**
$(B) \Rightarrow (A)$: Given $x$ and $V \ni f(x)$, take $U = f^{-1}(V)$. By (B), $U$ is open. Since $f(x) \in V$, we have $x \in U$. And $f(U) \subseteq V$ by construction. ✓

$(A) \Rightarrow (B)$: Let $V \in \tau_Y$. For each $x \in f^{-1}(V)$, (A) gives an open $U_x$ with $x \in U_x$ and $f(U_x) \subseteq V$. Then $f^{-1}(V) = \bigcup_x U_x$ — a union of open sets — which is open. ✓

Definition (A) is the direct generalization of the $\epsilon$-$\delta$ definition from analysis: $V$ plays the role of the $\epsilon$-ball, $U$ plays the role of the $\delta$-ball. Definition (B) is far more elegant and is the standard formulation in topology.

---

# Homeomorphism

**Definition.** A **homeomorphism** is a bijection $f: X \to Y$ such that both $f$ and $f^{-1}$ are continuous. We write $X \cong Y$.

Homeomorphic spaces are **topologically identical** — they share all topological properties.

**Examples:**
- $(0,1) \cong \mathbb{R}$ via $f(x) = \tan(\pi x - \pi/2)$
- Coffee mug $\cong$ donut (both have genus 1)
- $[0,1] \ncong S^1$ (removing a point from $[0,1]$ can disconnect it; removing a point from $S^1$ cannot)

A property preserved by homeomorphisms is called a **topological invariant** — these are what topology studies.

---

# Separability Axioms

The **separation axioms** describe how well a topology can distinguish individual points:

| Axiom | Name | Requirement |
|-------|------|-------------|
| $T_0$ | Kolmogorov | For any $x \neq y$, $\exists$ open set containing one but not the other |
| $T_1$ | Fréchet | For any $x \neq y$, each has a neighborhood not containing the other |
| $T_2$ | **Hausdorff** | For any $x \neq y$, $\exists$ **disjoint** open sets $U \ni x$, $V \ni y$ |
| $T_3$ | Regular | $T_1$ + points and closed sets can be separated by open sets |
| $T_4$ | Normal | $T_1$ + disjoint closed sets can be separated by open sets |

$$T_4 \implies T_3 \implies T_2 \implies T_1 \implies T_0$$

**Why Hausdorff matters:** Limits of sequences are unique in Hausdorff spaces. All metric spaces are Hausdorff. Manifolds are required to be Hausdorff.

---

# Connectedness

**Definition.** A **separation** of $X$ is a pair of disjoint non-empty open sets $U, V$ such that $X = U \cup V$.
A space is **connected** if no separation exists.

**Definition.** $X$ is **path-connected** if for any $x, y \in X$, there exists a continuous map $\gamma: [0,1] \to X$ with $\gamma(0) = x$, $\gamma(1) = y$.

**Key facts:**
- Path-connected $\implies$ connected (but NOT conversely!)
- **Counterexample:** The topologist's sine curve $\\{(x, \sin(1/x)) : x > 0\\} \cup \\{(0,0)\\}$ is connected but not path-connected
- Continuous image of a connected space is connected
- $\mathbb{R}^n \setminus \\{0\\}$ is connected for $n \ge 2$, but $\mathbb{R} \setminus \\{0\\}$ is disconnected

**Connected components** partition any space into maximal connected subsets. Later we will see: $H_0$ counts them.

---

# Compactness

**Definition.** A space $X$ is **compact** if every open cover has a finite subcover:
$$
X \subseteq \bigcup_{i \in I} U_i \quad \implies \quad \exists \\; i_1, \dots, i_n : \\; X \subseteq U_{i_1} \cup \cdots \cup U_{i_n}
$$

**Heine-Borel Theorem.** A subset of $\mathbb{R}^n$ is compact $\iff$ it is **closed** and **bounded**.

**Why compactness is powerful:**
- Continuous functions on compact spaces attain their maximum and minimum (**Extreme Value Theorem**)
- Continuous bijection from a compact space to a Hausdorff space is automatically a homeomorphism
- In metric spaces: compact $\iff$ sequentially compact (every sequence has a convergent subsequence)
- Product of compact spaces is compact (**Tychonoff's Theorem**)

**Key examples:** $[0,1]$ is compact; $(0,1)$ is not. $S^n$ is compact; $\mathbb{R}^n$ is not.

---

# Metric Spaces

**Definition.** A **metric** on $X$ is a function $d: X \times X \to \mathbb{R}$ satisfying:
1. $d(x,y) \ge 0$ with $d(x,y) = 0 \iff x = y$ (positive definiteness)
2. $d(x,y) = d(y,x)$ (symmetry)
3. $d(x,z) \le d(x,y) + d(y,z)$ (triangle inequality)

Every metric induces a topology via open balls $B(x,r) = \\{y : d(x,y) < r\\}$.

**Not every topology is metrizable!** A topology $\tau$ comes from a metric only if it satisfies certain conditions (e.g., the Urysohn metrization theorem: regular + second-countable $\implies$ metrizable).

**Important metrics:**
- Euclidean: $d(x,y) = \|x - y\|_2$
- Manhattan: $d(x,y) = \sum |x_i - y_i|$
- Chebyshev: $d(x,y) = \max |x_i - y_i|$
- Discrete: $d(x,y) = \begin{cases} 0 & x = y \\\\ 1 & x \neq y \end{cases}$

All these metrics on $\mathbb{R}^n$ generate the **same** topology!

---

# Manifolds

**Definition.** A topological space $M$ is an **$n$-dimensional manifold** if:
1. $M$ is **locally Euclidean**: every point has a neighborhood homeomorphic to $\mathbb{R}^n$
2. $M$ is **Hausdorff**
3. $M$ is **second-countable** (has a countable basis)

A homeomorphism $\varphi: U \to \mathbb{R}^n$ on a neighborhood $U$ is called a **chart**. A collection of charts covering $M$ is an **atlas**.

**Examples:**
<div class="smaller-table">

| Manifold | Dimension | Compact? | Orientable? |
|----------|-----------|----------|-------------|
| $S^n$ (sphere) | $n$ | Yes | Yes |
| $T^2$ (torus) | 2 | Yes | Yes |
| $\mathbb{RP}^2$ (projective plane) | 2 | Yes | No |
| Klein bottle | 2 | Yes | No |
| Möbius strip | 2 | No | No |
| $\mathbb{R}^n$ | $n$ | No | Yes |

</div>

---

# Whitney Embedding Theorem

Can every abstract manifold be realized as a subset of some Euclidean space?

**Whitney Embedding Theorem.** Every smooth $m$-dimensional manifold can be smoothly embedded into $\mathbb{R}^{2m}$.

This is remarkable: no matter how abstractly we define a manifold, it always has a concrete realization as a surface (or higher-dimensional object) sitting inside ordinary Euclidean space.

**Practical implication:** When we do topological data analysis on point clouds in $\mathbb{R}^d$, we are not losing generality — Whitney guarantees that the manifold we're looking for could live there.

**Example:** The Klein bottle cannot be embedded in $\mathbb{R}^3$ without self-intersection, but it embeds perfectly in $\mathbb{R}^4$.

---

# Euler Characteristic: A Preview

The **Euler characteristic** $\chi$ is one of the oldest topological invariants. For a polyhedron with $V$ vertices, $E$ edges, and $F$ faces:
$$
\chi = V - E + F
$$

:::matrix { cols="50/50" }
[[0, 0]]
<div class="smaller-table">

| Surface | $V - E + F$ | $\chi$ |
|---------|-------------|--------|
| Tetrahedron | $4 - 6 + 4$ | $2$ |
| Cube | $8 - 12 + 6$ | $2$ |
| Torus | $-$ | $0$ |
| Klein bottle | $-$ | $0$ |
| $\mathbb{RP}^2$ | $-$ | $1$ |
| Genus-$g$ surface | $-$ | $2 - 2g$ |

</div>
[[0, 1]]

* **Euler's formula:** For any convex polyhedron, $\chi = 2$.
* Later we will see that $\chi$ is connected to homology via the **Betti numbers**:
$$
\chi = \sum_{p=0}^{n} (-1)^p \beta_p = \beta_0 - \beta_1 + \beta_2 - \cdots
$$
This transforms an elementary counting formula into a deep algebraic invariant.


:::

