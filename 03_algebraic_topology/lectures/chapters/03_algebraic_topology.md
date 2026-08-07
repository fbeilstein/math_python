# The Central Idea: Functoriality

Topology is hard to compute directly. How do you prove two spaces are *not* homeomorphic?

**Strategy:** Assign algebraic invariants to spaces and study those instead.

:::matrix { cols="50/50" }
[[0, 0]]
**Definition.** A **functor** $\mathcal{F}: \mathbf{Top} \to \mathbf{Grp}$ from the category of topological spaces to the category of groups assigns:
1. **Objects:** To each space $X \in \text{Ob}(\mathbf{Top})$, a group $\mathcal{F}(X) \in \text{Ob}(\mathbf{Grp})$.
2. **Morphisms:** To each continuous map $f: X \to Y$, a group homomorphism $\mathcal{F}(f): \mathcal{F}(X) \to \mathcal{F}(Y)$.

**Axioms of Functoriality:**
- **Identity Preservation:** $\mathcal{F}(\text{id}\_X) = \text{id}\_{\mathcal{F}(X)}$
- **Composition Preservation:** $\mathcal{F}(g \circ f) = \mathcal{F}(g) \circ \mathcal{F}(f)$

**The Payoff:** If $X \cong Y$ (homeomorphic), then $\mathcal{F}(X) \cong \mathcal{F}(Y)$ (isomorphic). Equivalently: if $\mathcal{F}(X) \ncong \mathcal{F}(Y)$, then $X \ncong Y$.

We cannot always prove spaces *are* the same — but we can often prove they are *different*.

[[0, 1]]
![](./assets/functor_diagram.png){height=350px center}
:::

---

# Homotopy

:::matrix { cols="50/50" }
[[0,0:2]]
**Definition.** Two continuous maps $f, g: X \to Y$ are **homotopic** ($f \simeq g$) if there exists a continuous map $H: X \times [0,1] \to Y$ such that $H(x,0) = f(x)$ and $H(x,1) = g(x)$.

$H$ continuously deforms $f$ into $g$ — a "movie" where each frame is a valid continuous map.

**Definition.** Spaces $X$ and $Y$ are **homotopy equivalent** ($X \simeq Y$) if there exist continuous maps $f: X \to Y$ and $g: Y \to X$ such that $g \circ f \simeq \text{id}_X$ and $f \circ g \simeq \text{id}_Y$.

[[1,0]]
**Examples:**
- $\mathbb{R}^n \simeq \\{\text{pt}\\}$ — Euclidean space is **contractible** (shrink everything to the origin)
- Cylinder $\simeq S^1$ — collapse the height
- $\mathbb{R}^2 \setminus \\{0\\} \simeq S^1$ — the punctured plane retracts onto the unit circle
- Möbius strip $\simeq S^1$ — the strip retracts onto its central circle

Homotopy equivalence is weaker than homeomorphism but preserves all the algebraic invariants we care about.

[[1,1]]
<iframe src="./demos/homotopy/index.html" width="100%" height="450px" style="border: none;"></iframe>

:::

---

# The Fundamental Group $\pi_1$

:::matrix { cols="55/45" }
[[0,0]]
**Definition.** Fix a basepoint $x_0 \in X$. A **loop** at $x_0$ is a continuous map $\gamma: [0,1] \to X$ with $\gamma(0) = \gamma(1) = x_0$.

Two loops are **equivalent** if one can be continuously deformed into the other (keeping endpoints fixed).

The set of equivalence classes $[\gamma]$ forms a group under **path composition**:
$$
\pi_1(X, x_0) = \\{[\gamma] : \gamma \text{ is a loop at } x_0\\}
$$

<div class="smaller-table">

| Space | $\pi_1$ | Intuition |
|-------|---------|-----------|
| $\mathbb{R}^n$ | $0$ | Every loop can be shrunk to a point |
| $S^n, n \ge 2$ | $0$ | Loops on a sphere can slide off |
| $S^1$ | $\mathbb{Z}$ | Winding number: how many times around? |
| $T^2$ | $\mathbb{Z} \times \mathbb{Z}$ | Two independent loops (meridian, longitude) |
| Figure-eight $S^1 \vee S^1$ | $F_2$ | Free group on 2 generators — non-abelian! |
| $\mathbb{RP}^2$ | $\mathbb{Z}_2$ | A loop around the "twist" — go around twice to return |

</div>

[[0,1]]
<iframe src="./demos/pi1/index.html" width="100%" height="600px" style="border: none;"></iframe>

:::

---

# Covering Spaces


:::matrix { cols="50/50" }
[[0,0]]
**Definition.** A continuous surjection $p: \tilde{X} \to X$ is a **covering map** if every point $x \in X$ has a neighborhood $U$ such that $p^{-1}(U)$ is a disjoint union of open sets, each mapped homeomorphically onto $U$ by $p$.

**The fundamental example:** $p: \mathbb{R} \to S^1$, $t \mapsto e^{2\pi i t}$.

The real line wraps around the circle infinitely many times. Each point of $S^1$ has exactly $\mathbb{Z}$ preimages.

**Why coverings matter:**
- The **universal cover** $\tilde{X}$ is the unique simply connected covering space
- **Deck transformations** (self-homeomorphisms of $\tilde{X}$ preserving $p$) form a group isomorphic to $\pi_1(X)$
- Subgroups of $\pi_1(X)$ $\longleftrightarrow$ intermediate covering spaces (Galois correspondence!)

[[0,1]]
<iframe src="./demos/covering_space/index.html" width="100%" height="600px" style="border: none;"></iframe>

[[1,0:2]]
**Examples:**
- $\mathbb{R}$ is the universal cover of $S^1$, with deck transformations $t \mapsto t + n$ ($n \in \mathbb{Z}$)
- $S^n$ is the universal cover of $\mathbb{RP}^n$, with deck group $\mathbb{Z}_2$ (the antipodal map)
:::

---

# Van Kampen's Theorem

:::matrix { cols="50/50" }
[[0,0]]
**Problem:** How do we compute $\pi_1$ of a space built from simpler pieces?

**Van Kampen's Theorem.** If $X = U \cup V$ where $U, V, U \cap V$ are open and path-connected, then:
$$
\pi_1(X) \cong \pi_1(U) *\_{\pi_1(U \cap V)} \pi_1(V)
$$

This is the **amalgamated free product** — take the free product of $\pi_1(U)$ and $\pi_1(V)$, then impose relations coming from $\pi_1(U \cap V)$.

**Applications:**
- **Wedge sum (one-point union):** $\pi_1(S^1 \vee S^1) \cong \mathbb{Z} * \mathbb{Z} = F_2$ (free group — take $U, V$ as neighborhoods of each circle, overlap is contractible)
- **Sphere:** $\pi_1(S^n) = 0$ for $n \ge 2$ (cover with two contractible caps whose overlap is a cylinder, inclusions are $\mathbb{Z}\to e$)
- **Torus:** $\pi_1(T^2) \cong \langle a, b \mid aba^{-1}b^{-1} = 1 \rangle \cong \mathbb{Z} \times \mathbb{Z}$ (the commutator relation forces commutativity)

[[0,1]]
![](./assets/vankampen.svg){width=100% center} &nbsp;

:::

---

:::matrix { cols="50/50" }

[[0,0]]
**A Deep Dive: The Plane with Holes**
To see how relations mechanically "kill" elements, let's algebraically construct a plane with one hole ($X = \mathbb{R}^2 \setminus \{q\}$) by gluing two more complex spaces together. We know $\pi_1(X) \cong \mathbb{Z}$.

*   **Set U**: The plane missing two holes $p$ and $q$. $\pi_1(U) = \langle a_1, a_2 \rangle$.
*   **Set V**: The plane missing two holes $q$ and $r$. $\pi_1(V) = \langle b_1, b_2 \rangle$.
*   **Union**: $U \cup V = \mathbb{R}^2 \setminus \{q\} = X$. (Because $U$ fills in hole $r$, and $V$ fills in hole $p$).
*   **Intersection**: $U \cap V = \mathbb{R}^2 \setminus \{p, q, r\}$. The intersection has 3 holes! $\pi_1(U \cap V) = \langle c_1, c_2, c_3 \rangle$.

**The Amalgamation (The Relations)**
We trace the 3 generators of the intersection as they inject into $U$ and $V$:
1.  $c_1$ (around $p$): In $U$, this is $a_1$. In $V$, hole $p$ is filled, so the loop is contractible ($1$). $\implies a_1 = 1$.
2.  $c_2$ (around $q$): In $U$, this is $a_2$. In $V$, this is $b_1$. $\implies a_2 = b_1$.
3.  $c_3$ (around $r$): In $U$, hole $r$ is filled, so it is contractible ($1$). In $V$, this is $b_2$. $\implies 1 = b_2$.

The free product is $\langle a_1, a_2, b_1, b_2 \rangle$. Applying our three relations, we brutally kill $a_1$ and $b_2$, and glue $a_2$ directly to $b_1$. The resulting group is precisely $\langle a_2 \rangle \cong \mathbb{Z}$.

[[0,1]]
![](./assets/vankampen_holes.svg){width=100% center} &nbsp;

:::

---

# Higher Homotopy Groups

:::matrix { cols="50/50" }

[[0,0]]
For $n \ge 1$, we define $\pi_n(X)$ using maps from $S^n$ (instead of $S^1 = $ loops):
$$
\pi_n(X, x_0) = \text{homotopy classes of maps } (S^n, \text{pt}) \to (X, x_0)
$$

**Key property:** For $n \ge 2$, $\pi_n$ is always **abelian** (higher-dimensional spheres can "slide past" each other).

**How do we compose maps in higher dimensions?** 
Just like loops ($I^1$), we compose maps on $I^n$ by gluing their domains along **one** chosen dimension. For $f, g: (I^n, \partial I^n) \to (X, x_0)$, the standard composition $f * g$ concatenates along the first coordinate:
$$
(f * g)(t_1, t_2, \dots, t_n) = 
\begin{cases} 
f(2t_1, t_2, \dots, t_n) & 0 \le t_1 \le 1/2 \\\\
g(2t_1 - 1, t_2, \dots, t_n) & 1/2 \le t_1 \le 1 
\end{cases}
$$
Because the boundary $\partial I^n$ maps entirely to the constant basepoint $x_0$, the "empty space" around the non-trivial parts of $f$ and $g$ is flexible. As the demo proves, the existence of at least one *extra* dimension ($n \ge 2$) gives the domains enough "room" to shrink, move into different lanes, and slide past each other horizontally. This forces $f * g \simeq g * f$, making $\pi_n$ abelian!

[[0,1]]
<iframe src="./demos/pi2_abelian/index.html" width="100%" height="580px" style="border: none;"></iframe>


:::

---

# From $\pi_1$ to $H_1$: The Abelianization

:::matrix { cols="45/55" }

[[0,0]]
Recall from Module 2 (Abstract Algebra): the **commutator subgroup** $[G, G] = \langle aba^{-1}b^{-1} \rangle$ is always a normal subgroup. The quotient $G / [G, G]$ is the **abelianization** $G^{ab}$.

**Hurewicz Theorem (for $\pi_1$).** For any path-connected space $X$:
$$
H_1(X; \mathbb{Z}) \cong \pi_1(X)^{ab} = \pi_1(X) / [\pi_1(X), \pi_1(X)]
$$

The first homology group is exactly the abelianization of the fundamental group.
- **Homotopy ($\pi_1$)** evaluates paths parametrically. The parameter $t$ *hard-wires* the paths in strict sequence. 
- **Homology ($H_1$)** evaluates formal sums of independent chains.

<div class="smaller-table">

| Space | $\pi_1$ | $\pi_1^{ab} = H_1$ |
|-------|---------|---------------------|
| $S^1$ | $\mathbb{Z}$ | $\mathbb{Z}$ (abelian) |
| $T^2$ | $\mathbb{Z} \times \mathbb{Z}$ | $\mathbb{Z}^2$ (abelian) |
| $S^1 \vee S^1$ | $F_2 = \mathbb{Z} * \mathbb{Z}$ | $\mathbb{Z}^2$ (commutator vanishes) |

</div>

[[0,1]]
<iframe src="./demos/hurewicz/index.html" width="100%" height="780px" style="border: none;"></iframe>

:::

---

# Why Homology?

:::matrix {cols="50/50"}
[[0,0]]
The fundamental group $\pi_1$ is powerful but:
- **Non-abelian** — hard to compute, hard to compare
- **Only sees loops** — misses higher-dimensional holes (cavities, voids)
- **Higher $\pi_n$ are nearly impossible** to compute in general

**The bad news:** Higher homotopy groups are notoriously difficult to compute.

<div class="smaller-table">

| | Result | Year |
|---|--------|------|
| $\pi_3(S^2)$ | $\cong \mathbb{Z}$ | Hopf, 1931 |
| $\pi_4(S^3)$ | $\cong \mathbb{Z}_2$ | Freudenthal, 1937 |
| $\pi_n(S^n)$ | $\cong \mathbb{Z}$ | Hopf |
| $\pi_{n+1}(S^n)$ | $\cong \mathbb{Z}_2$ for $n \ge 3$ | Freudenthal |

</div>

The Hopf fibration $S^3 \to S^2$ (with fiber $S^1$) is one of the deepest objects in topology — it shows that the structure of spheres is far richer than dimension alone suggests.


[[0,1]]
**Homology groups** $H_n(X)$ fix all three problems:

<div class="smaller-table">

| Property | $\pi_n$ | $H_n$ |
|----------|---------|-------|
| Abelian? | Only for $n \ge 2$ | **Always** |
| Computable? | Generally no | **Yes — via linear algebra** |
| Detects $n$-dim holes? | Yes | **Yes** |

</div>

**What $H_n$ detects:**
- $H_0$: connected components
- $H_1$: loops, tunnels (= abelianized $\pi_1$)
- $H_2$: enclosed cavities, voids
- $H_n$: $n$-dimensional "holes"

**Next chapter:** We build the algebraic machinery — simplicial complexes, chain groups, boundary operators — that makes homology computable.


:::