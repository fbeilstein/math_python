# Mathematical Foundations of Quantum Mechanics

## The Arena: $L^2(\mathbb{R}^n, \mathbb{C})$

The state space of quantum mechanics is a **separable complex Hilbert space** $\mathcal{H}$.
For a single particle in $\mathbb{R}^n$, the concrete realization is:
$$
\mathcal{H} = L^2(\mathbb{R}^n, \mathbb{C}) = \left\lbrace f : \mathbb{R}^n \to \mathbb{C} \\;\middle\vert\\; \int_{\mathbb{R}^n} |f(\mathbf{x})|^2\, d^n x < \infty \right\rbrace
$$
with the inner product:
$$
\langle f | g \rangle = \int_{\mathbb{R}^n} \overline{f(\mathbf{x})}\\, g(\mathbf{x})\\, d^n x
$$

**Key properties:**
* **Complete** — every Cauchy sequence converges (unlike $C^\infty_c$)
* **Separable** — admits a countable orthonormal basis $\\{e_n\\}_{n \in \mathbb{N}}$
* Physical states are **rays** in $\mathcal{H}$: the projective Hilbert space $\mathbb{P}\mathcal{H} = S(\mathcal{H})/U(1)$

---

## Bounded vs. Unbounded Operators

:::matrix { cols="50/50" rows="100" height="80%"}

[[0, 0]]
**Bounded operators** $\hat{A} \in B(\mathcal{H})$:
* Defined on **all** of $\mathcal{H}$
* $\|\hat{A}\| = \sup_{\|\psi\|=1} \|\hat{A}\psi\| < \infty$
* Form a $C^*$-algebra under composition
* Example: projection operators $\hat{P}^2 = \hat{P}$

[[0, 1]]
**Unbounded operators** (the ones we actually need!):
* Defined only on a **dense subspace** $D(\hat{A}) \subset \mathcal{H}$
* $\hat{x}$: multiplication by $x$, domain $D(\hat{x}) = \{f \in L^2 : xf \in L^2\}$
* $\hat{p} = -i\hbar\frac{d}{dx}$, domain $D(\hat{p}) = H^1(\mathbb{R})$ (Sobolev space)
* **Hellinger-Toeplitz theorem**: a self-adjoint operator defined on all of $\mathcal{H}$ must be bounded. So $\hat{x}$ and $\hat{p}$ *cannot* be everywhere-defined.

:::

---

## The Adjoint Operator

**Definition.** Let $\hat{A}$ be densely defined on $D(\hat{A})$. The adjoint $\hat{A}^\dagger$ is defined on:

$$
D(\hat{A}^\dagger) = \left\\{ \phi \in \mathcal{H} \\;\middle\|\\; \exists\\, \eta \in \mathcal{H} \text{ s.t. } \langle \eta | \psi \rangle = \langle \phi | \hat{A}\psi \rangle \\;\forall\\, \psi \in D(\hat{A}) \right\\}
$$

and $\hat{A}^\dagger \phi = \eta$. The key distinction:

| Property | Definition | Implication |
|----------|-----------|-------------|
| **Symmetric** | $\langle \hat{A}\phi \mid \psi\rangle = \langle \phi \mid \hat{A}\psi\rangle$ for $\phi, \psi \in D(\hat{A})$ | $\hat{A} \subseteq \hat{A}^\dagger$ (domain of $\hat{A}^\dagger$ may be larger) |
| **Self-adjoint** | $\hat{A} = \hat{A}^\dagger$ **including** $D(\hat{A}) = D(\hat{A}^\dagger)$ | Spectral theorem applies |
| **Essentially s.a.** | $\overline{\hat{A}} = \hat{A}^\dagger$ (closure is self-adjoint) | Unique self-adjoint extension |

> The distinction between symmetric and self-adjoint is crucial. Many operators that "look Hermitian" are only symmetric — the spectral theorem and Stone's theorem require genuine self-adjointness.

---

## Postulates of QM — Mathematician's Formulation

* **P1** --- The state of a quantum system is a unit ray $[\psi] \in \mathbb{P}\mathcal{H}$ in a separable complex Hilbert space $\mathcal{H}$.

* **P2** --- Each observable corresponds to a **self-adjoint** operator $\hat{A}$ on $\mathcal{H}$ (not merely symmetric!).

* **P3** --- **Measurement** of observable $\hat{A}$ on state $|\psi\rangle$: possible outcomes lie in the spectrum $\sigma(\hat{A})$. For a Borel set $B \subseteq \mathbb{R}$, the probability of the outcome falling in $B$ is $P(B) = \langle\psi|E_B|\psi\rangle$, where $E$ is the projection-valued measure of $\hat{A}$ (spectral theorem). Post-measurement state: $E_B|\psi\rangle / \|E_B|\psi\rangle\|$. For non-degenerate discrete spectrum this reduces to $P(a_n) = |\langle a_n|\psi\rangle|^2$.

* **P4** --- **Dynamics**: $i\hbar\frac{d}{dt}|\psi(t)\rangle = \hat{H}|\psi(t)\rangle$. For time-independent $\hat{H}$, the solution is $|\psi(t)\rangle = e^{-i\hat{H}t/\hbar}|\psi(0)\rangle$ (one-parameter unitary group, Stone's theorem). For time-dependent $\hat{H}(t)$, the propagator is a time-ordered exponential (Dyson series).

* **P5** --- **Canonical structure**: position and momentum satisfy the **Weyl relations** $e^{i\alpha\hat{x}}e^{i\beta\hat{p}} = e^{-i\alpha\beta\hbar}e^{i\beta\hat{p}}e^{i\alpha\hat{x}}$. The formal differential form $[\hat{x}_j, \hat{p}_k] = i\hbar\delta_{jk}\hat{I}$ follows on a suitable dense domain but cannot hold as a bounded operator identity (the trace of $[\hat{A},\hat{B}]$ is always zero, while $\text{tr}(i\hbar\hat{I})$ diverges).

* **P6** --- **Composite systems**: the state space of a composite system is the **tensor product** $\mathcal{H} = \mathcal{H}_1 \otimes \mathcal{H}_2$. States that cannot be written as $|\psi_1\rangle \otimes |\psi_2\rangle$ are called **entangled**.

