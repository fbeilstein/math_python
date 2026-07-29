# Spectral Theory & Measurement

## The Spectral Theorem (Unbounded Self-Adjoint Operators)

**Theorem (von Neumann).** Let $\hat{A}$ be a self-adjoint operator on a separable Hilbert space $\mathcal{H}$. Then there exists a unique **projection-valued measure** $E : \mathcal{B}(\mathbb{R}) \to B(\mathcal{H})$ such that:

$$
\hat{A} = \int_{\sigma(\hat{A})} \lambda\\; dE_\lambda
$$

where $\sigma(\hat{A}) \subseteq \mathbb{R}$ is the spectrum.

**Properties of the spectral measure $E$:**
* $E_B$ is an orthogonal projection for each Borel set $B \subseteq \mathbb{R}$
* $E_\emptyset = 0$, $E_\mathbb{R} = \hat{I}$
* $E_{B_1 \cap B_2} = E_{B_1} E_{B_2}$ (projections onto joint eigenspaces)
* $E_{B_1 \cup B_2} = E_{B_1} + E_{B_2}$ for disjoint $B_1, B_2$
* $\sigma$-additivity in the strong operator topology

---

## Types of Spectrum

The spectrum $\sigma(\hat{A})$ decomposes into:

| Type | Characterization | Example |
|------|-----------------|---------|
| **Discrete (point)** | $\hat{A} \| a_n \rangle = a_n \| a_n \rangle $, eigenvectors $\in \mathcal{H}$ | Hamiltonian of harmonic oscillator |
| **Continuous** | No normalizable eigenvectors; "eigenstates" $\notin \mathcal{H}$ | Position $\hat{x}$, momentum $\hat{p}$ |
| **Residual** | Not in point or continuous spectrum | Does not occur for self-adjoint operators |

**For discrete spectrum:** $E_{\{a_n\}} = |a_n\rangle\langle a_n|$, and

$$
\hat{A} = \sum_n a_n |a_n\rangle\langle a_n|, \qquad \sum_n |a_n\rangle\langle a_n| = \hat{I} \quad \text{(resolution of identity)}
$$

**For continuous spectrum** (e.g., $\hat{x}|x'\rangle = x'|x'\rangle$): the "eigenstates" $|x'\rangle$ live in the **rigged Hilbert space** (Gel'fand triple):

$$
\mathcal{S}(\mathbb{R}) \hookrightarrow L^2(\mathbb{R}) \hookrightarrow \mathcal{S}'(\mathbb{R})
$$

where $|x'\rangle \in \mathcal{S}'(\mathbb{R})$ (tempered distributions), with $\langle x|x'\rangle = \delta(x - x')$.

---

## The Born Rule from Spectral Theory

**Measurement of $\hat{A}$ on state $|\psi\rangle$:**

The probability of finding the result in a Borel set $B \subseteq \mathbb{R}$ is:

$$
P_\psi(B) = \langle\psi| E_B |\psi\rangle = \|E_B|\psi\rangle\|^2
$$

This is a **probability measure** on $(\mathbb{R}, \mathcal{B}(\mathbb{R}))$ by the properties of $E$.

* Discrete spectrum: $P_\psi(\{a_n\}) = |\langle a_n|\psi\rangle|^2$ (Born rule)
* Continuous spectrum: $P_\psi([a, b]) = \int_a^b |\psi(\lambda)|^2\, d\lambda$

**Post-measurement state** (von Neumann projection postulate):

$$
|\psi\rangle \\;\xrightarrow{\text{measure } a_n}\\; \frac{E_{\{a_n\}}|\psi\rangle}{\|E_{\{a_n\}}|\psi\rangle\|}  = |a_n\rangle
$$

---

## Functional Calculus

**Theorem.** For any Borel-measurable function $f : \mathbb{R} \to \mathbb{C}$, the operator $f(\hat{A})$ is defined by:

$$
f(\hat{A}) = \int_{\sigma(\hat{A})} f(\lambda)\\; dE_\lambda
$$

with domain $D(f(\hat{A})) = \left\\{\psi \in \mathcal{H} : \int |f(\lambda)|^2\\, d\|E_\lambda\psi\|^2 < \infty\right\\}$.

**Why this matters for QM:**

The operator exponential $e^{i\hat{A}t}$ for **unbounded** $\hat{A}$ is defined via functional calculus — **not** by the Taylor series (which may not converge on the domain of $\hat{A}$):

$$
e^{i\hat{A}t} = \int_{\sigma(\hat{A})} e^{i\lambda t}\\; dE_\lambda
$$

> The Taylor series $e^{i\hat{A}t} = \sum_{n=0}^\infty \frac{(i\hat{A}t)^n}{n!}$ is valid only for bounded $\hat{A}$ or on analytic vectors. For the Hamiltonian $\hat{H}$ (unbounded!), the rigorous definition requires the spectral theorem. This is not a technicality — it's the mathematical content of quantum dynamics.
