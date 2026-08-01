# The Central Idea: Functoriality

Topology is hard to compute directly. How do you prove two spaces are *not* homeomorphic?

**Strategy:** Assign algebraic invariants to spaces and study those instead.

A **functor** $F$ from topology to algebra sends:
- Spaces $X$ → algebraic objects $F(X)$ (groups, vector spaces, ...)
- Continuous maps $f: X \to Y$ → homomorphisms $F(f): F(X) \to F(Y)$

**The Payoff:** If $X \cong Y$ (homeomorphic), then $F(X) \cong F(Y)$ (isomorphic). Equivalently: if $F(X) \ncong F(Y)$, then $X \ncong Y$.

We cannot always prove spaces *are* the same — but we can often prove they are *different*.

---

# Homotopy

**Definition.** Two continuous maps $f, g: X \to Y$ are **homotopic** ($f \simeq g$) if there exists a continuous map $H: X \times [0,1] \to Y$ such that $H(x,0) = f(x)$ and $H(x,1) = g(x)$.

$H$ continuously deforms $f$ into $g$ — a "movie" where each frame is a valid continuous map.

**Definition.** Spaces $X$ and $Y$ are **homotopy equivalent** ($X \simeq Y$) if there exist continuous maps $f: X \to Y$ and $g: Y \to X$ such that $g \circ f \simeq \text{id}_X$ and $f \circ g \simeq \text{id}_Y$.

**Examples:**
- $\mathbb{R}^n \simeq \\{\text{pt}\\}$ — Euclidean space is **contractible** (shrink everything to the origin)
- Cylinder $\simeq S^1$ — collapse the height
- $\mathbb{R}^2 \setminus \\{0\\} \simeq S^1$ — the punctured plane retracts onto the unit circle
- Möbius strip $\simeq S^1$ — the strip retracts onto its central circle

Homotopy equivalence is weaker than homeomorphism but preserves all the algebraic invariants we care about.

---

# The Fundamental Group $\pi_1$

**Definition.** Fix a basepoint $x_0 \in X$. A **loop** at $x_0$ is a continuous map $\gamma: [0,1] \to X$ with $\gamma(0) = \gamma(1) = x_0$.

Two loops are **equivalent** if one can be continuously deformed into the other (keeping endpoints fixed).

The set of equivalence classes $[\gamma]$ forms a group under **path composition**:
$$
\pi_1(X, x_0) = \\{[\gamma] : \gamma \text{ is a loop at } x_0\\}
$$


| Space | $\pi_1$ | Intuition |
|-------|---------|-----------|
| $\mathbb{R}^n$ | $0$ | Every loop can be shrunk to a point |
| $S^n, n \ge 2$ | $0$ | Loops on a sphere can slide off |
| $S^1$ | $\mathbb{Z}$ | Winding number: how many times around? |
| $T^2$ | $\mathbb{Z} \times \mathbb{Z}$ | Two independent loops (meridian, longitude) |
| Figure-eight $S^1 \vee S^1$ | $F_2$ | Free group on 2 generators — non-abelian! |
| $\mathbb{RP}^2$ | $\mathbb{Z}_2$ | A loop around the "twist" — go around twice to return |

---

# Covering Spaces

**Definition.** A continuous surjection $p: \tilde{X} \to X$ is a **covering map** if every point $x \in X$ has a neighborhood $U$ such that $p^{-1}(U)$ is a disjoint union of open sets, each mapped homeomorphically onto $U$ by $p$.

**The fundamental example:** $p: \mathbb{R} \to S^1$, $t \mapsto e^{2\pi i t}$.

The real line wraps around the circle infinitely many times. Each point of $S^1$ has exactly $\mathbb{Z}$ preimages.

**Why coverings matter:**
- The **universal cover** $\tilde{X}$ is the unique simply connected covering space
- **Deck transformations** (self-homeomorphisms of $\tilde{X}$ preserving $p$) form a group isomorphic to $\pi_1(X)$
- Subgroups of $\pi_1(X)$ $\longleftrightarrow$ intermediate covering spaces (Galois correspondence!)

**Examples:**
- $\mathbb{R}$ is the universal cover of $S^1$, with deck transformations $t \mapsto t + n$ ($n \in \mathbb{Z}$)
- $S^n$ is the universal cover of $\mathbb{RP}^n$, with deck group $\mathbb{Z}_2$ (the antipodal map)

---

# Van Kampen's Theorem

**Problem:** How do we compute $\pi_1$ of a space built from simpler pieces?

**Van Kampen's Theorem.** If $X = U \cup V$ where $U, V, U \cap V$ are open and path-connected, then:
$$
\pi_1(X) \cong \pi_1(U) *\_{\pi_1(U \cap V)} \pi_1(V)
$$

This is the **amalgamated free product** — take the free product of $\pi_1(U)$ and $\pi_1(V)$, then impose relations coming from $\pi_1(U \cap V)$.

**Applications:**
- **Wedge sum:** $\pi_1(S^1 \vee S^1) \cong \mathbb{Z} * \mathbb{Z} = F_2$ (free group — take $U, V$ as neighborhoods of each circle, overlap is contractible)
- **Sphere:** $\pi_1(S^n) = 0$ for $n \ge 2$ (cover with two contractible caps whose overlap is connected)
- **Torus:** $\pi_1(T^2) \cong \langle a, b \mid aba^{-1}b^{-1} = 1 \rangle \cong \mathbb{Z} \times \mathbb{Z}$ (the commutator relation forces commutativity)

---

# Higher Homotopy Groups

For $n \ge 1$, we define $\pi_n(X)$ using maps from $S^n$ (instead of $S^1 = $ loops):
$$
\pi_n(X, x_0) = \text{homotopy classes of maps } (S^n, \text{pt}) \to (X, x_0)
$$

**Key property:** For $n \ge 2$, $\pi_n$ is always **abelian** (higher-dimensional spheres can "slide past" each other).

**The bad news:** Higher homotopy groups are notoriously difficult to compute.

| | Result | Year |
|---|--------|------|
| $\pi_3(S^2)$ | $\cong \mathbb{Z}$ | Hopf, 1931 |
| $\pi_4(S^3)$ | $\cong \mathbb{Z}_2$ | Freudenthal, 1937 |
| $\pi_n(S^n)$ | $\cong \mathbb{Z}$ | Hopf |
| $\pi_{n+1}(S^n)$ | $\cong \mathbb{Z}_2$ for $n \ge 3$ | Freudenthal |

The Hopf fibration $S^3 \to S^2$ (with fiber $S^1$) is one of the deepest objects in topology — it shows that the structure of spheres is far richer than dimension alone suggests.

**Conclusion:** We need a more computable invariant. Enter **homology**.

---

# From $\pi_1$ to $H_1$: The Abelianization

Recall from Module 2 (Abstract Algebra): the **commutator subgroup** $[G, G] = \langle aba^{-1}b^{-1} \rangle$ is always a normal subgroup, and the quotient $G / [G, G]$ is the largest abelian quotient of $G$ — the **abelianization** $G^{ab}$.

**Hurewicz Theorem (for $\pi_1$).** For any path-connected space $X$:
$$
H_1(X; \mathbb{Z}) \cong \pi_1(X)^{ab} = \pi_1(X) / [\pi_1(X), \pi_1(X)]
$$

The first homology group is exactly the abelianization of the fundamental group!

<div class="smaller-table">

| Space | $\pi_1$ | $\pi_1^{ab} = H_1$ |
|-------|---------|---------------------|
| $S^1$ | $\mathbb{Z}$ | $\mathbb{Z}$ (already abelian) |
| $T^2$ | $\mathbb{Z} \times \mathbb{Z}$ | $\mathbb{Z}^2$ (already abelian) |
| Figure-eight | $F_2 = \mathbb{Z} * \mathbb{Z}$ | $\mathbb{Z}^2$ (abelianization kills the non-commutativity) |
| $\mathbb{RP}^2$ | $\mathbb{Z}_2$ | $\mathbb{Z}_2$ (already abelian — this is torsion!) |
| $S^n, n \ge 2$ | $0$ | $0$ |

</div>

**The beautiful connection:** Abelianization from algebra (Module 2) meets topology. Homology trades the full non-abelian structure of $\pi_1$ for computability.

---

# Why Homology?

The fundamental group $\pi_1$ is powerful but:
- **Non-abelian** — hard to compute, hard to compare
- **Only sees loops** — misses higher-dimensional holes (cavities, voids)
- **Higher $\pi_n$ are nearly impossible** to compute in general

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
