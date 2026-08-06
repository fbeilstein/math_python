# Commutators & the Heisenberg Algebra

## The Commutator as Lie Bracket

The **commutator** $[\hat{A}, \hat{B}] = \hat{A}\hat{B} - \hat{B}\hat{A}$ equips the space of operators with a **Lie algebra** structure:

| Axiom | Statement |
|-------|----------|
| **Bilinearity** | $[\alpha\hat{A} + \beta\hat{B},\, \hat{C}] = \alpha[\hat{A},\hat{C}] + \beta[\hat{B},\hat{C}]$ |
| **Antisymmetry** | $[\hat{A}, \hat{B}] = -[\hat{B}, \hat{A}]$ |
| **Jacobi identity** | $[\hat{A}, [\hat{B}, \hat{C}]] + [\hat{B}, [\hat{C}, \hat{A}]] + [\hat{C}, [\hat{A}, \hat{B}]] = 0$ |

**Leibniz rule** (the commutator acts as a derivation):

$$
[\hat{A}, \hat{B}\hat{C}] = [\hat{A}, \hat{B}]\hat{C} + \hat{B}[\hat{A}, \hat{C}]
$$

> The canonical commutation relation $[\hat{x}, \hat{p}] = i\hbar\hat{I}$ is the defining relation of the **Heisenberg algebra** $\mathfrak{h}_1$: a 3-dimensional Lie algebra spanned by $\{\hat{x}, \hat{p}, \hat{I}\}$ with $\hat{I}$ central.

---

## The Stone–von Neumann Theorem

**Theorem (Stone–von Neumann, 1931).** Any irreducible unitary representation of the Heisenberg commutation relations (in the Weyl form $e^{i\alpha\hat{x}}e^{i\beta\hat{p}} = e^{-i\alpha\beta\hbar}e^{i\beta\hat{p}}e^{i\alpha\hat{x}}$) on a separable Hilbert space is unitarily equivalent to the **Schrödinger representation**:

$$
\hat{x}\psi(x) = x\psi(x), \qquad \hat{p}\psi(x) = -i\hbar\frac{d\psi}{dx}
$$

**Significance for mathematicians:**
* The "position representation" is **not a choice** — it is the **unique** irreducible representation (up to equivalence)
* The Weyl form is necessary because $[\hat{x}, \hat{p}] = i\hbar$ is ill-defined for unbounded operators on all of $\mathcal{H}$
* Finite-dimensional analogue fails: no finite matrices satisfy $[A, B] = cI$ with $c \neq 0$ (take the trace of both sides!)

---

## Uncertainty as a Cauchy-Schwarz Inequality

**Theorem (Robertson–Schrödinger).** For any state $|\psi\rangle$ and any two self-adjoint operators $\hat{A}, \hat{B}$:

$$
\boxed{\Delta A \cdot \Delta B \geq \frac{1}{2}\left|\langle[\hat{A}, \hat{B}]\rangle\right|}
$$

where $\Delta A = \sqrt{\langle\hat{A}^2\rangle - \langle\hat{A}\rangle^2}$.

**Proof sketch (purely Hilbert space):**
1. Define $|f\rangle = (\hat{A} - \langle A\rangle)|\psi\rangle$, $|g\rangle = (\hat{B} - \langle B\rangle)|\psi\rangle$
2. Apply Cauchy-Schwarz: $|\langle f|g\rangle|^2 \leq \|f\|^2\|g\|^2$
3. Note $\|f\|^2 = (\Delta A)^2$, $\|g\|^2 = (\Delta B)^2$
4. Decompose: $\langle f|g\rangle = \frac{1}{2}\langle[\hat{A},\hat{B}]\rangle + \frac{1}{2}\langle\{\hat{A}-\langle A\rangle, \hat{B}-\langle B\rangle\}\rangle$
5. Take imaginary part: $|\text{Im}\\,\langle f|g\rangle| = \frac{1}{2}|\langle[\hat{A},\hat{B}]\rangle|$

For $\hat{x}, \hat{p}$: $[\hat{x},\hat{p}] = i\hbar\hat{I}$, so $\Delta x\\,\Delta p \geq \hbar/2$.

**Fourier-analytic interpretation:** $\psi(x)$ and $\tilde{\psi}(p)$ are Fourier duals. The uncertainty principle is the **bandwidth theorem** — a function cannot be simultaneously narrow and have a narrow Fourier transform.

---

## Angular Momentum: the Lie Algebra $\mathfrak{so}(3)$

The angular momentum operators satisfy: $[\hat{L}\_i, \hat{L}\_j] = i\hbar\\,\epsilon\_\{ijk\}\\,\hat{L}\_k$

This is the Lie algebra $\mathfrak{so}(3) \cong \mathfrak{su}(2)$ (as real Lie algebras).

:::matrix { cols="50/50" rows="100" height="80%"}

[[0, 0]]
**Algebraic quantization (no PDE needed!):**

Define **ladder operators** $\hat{L}_\pm = \hat{L}_x \pm i\hat{L}_y$.

Commutation relations:
* $[\hat{L}\_z, \hat{L}\_\pm] = \pm\hbar\\,\hat{L}\_\pm$
* $[\hat{L}\_+, \hat{L}\_-] = 2\hbar\\,\hat{L}\_z$

The **Casimir operator** $\hat{L}^2 = \hat{L}_x^2 + \hat{L}_y^2 + \hat{L}_z^2$ commutes with all $\hat{L}_i$ (it's in the center of the universal enveloping algebra).

[[0, 1]]
**Representation theory:**

Joint eigenvalues of $\{\hat{L}^2, \hat{L}_z\}$:
* $\hat{L}^2|l,m\rangle = \hbar^2 l(l+1)|l,m\rangle$
* $\hat{L}_z|l,m\rangle = \hbar m|l,m\rangle$

Quantization: $l \in \{0, \tfrac{1}{2}, 1, \tfrac{3}{2}, \ldots\}$, $m \in \{-l, -l+1, \ldots, l\}$

$\hat{L}_\pm$ act as raising/lowering operators on $m$.

Integer $l$: orbital angular momentum ($\to$ spherical harmonics $Y_l^m$)

Half-integer $l$: **spin** (no classical analogue; $SU(2)$ double cover of $SO(3)$)

:::
