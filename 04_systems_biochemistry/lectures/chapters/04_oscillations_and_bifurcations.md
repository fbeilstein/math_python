# Non-Equilibrium Biochemical Oscillations

Biological oscillations require open systems driven far from thermodynamic equilibrium by continuous energy dissipation ($\text{ATP} \to \text{ADP} + P_i$).

:::matrix {cols="50/50"}
[[0,0]]
### Thermodynamic Conditions
1. **Open System:** Constant flux of substrate inflow and product removal.
2. **Non-Linear Feedback:** Positive feedback or delayed negative feedback.
3. **Energy Dissipation:** Entropy production rate $\frac{d_i S}{dt} > 0$ sustains limit cycles.

[[0,1]]
### Case Study: Circadian Clocks
The **Cyanobacteria KaiABC** system is a remarkable post-translational oscillator. It maintains a 24-hour cycle of KaiC phosphorylation/dephosphorylation *in vitro* using only three proteins (KaiA, KaiB, KaiC) and ATP.

In **Drosophila** and mammals, circadian rhythms rely on a delayed negative feedback transcription-translation loop (the PER/TIM clock). The PER protein represses its own transcription, but only after a significant time delay caused by nuclear transport and phosphorylation degradation kinetics.
:::

---

# Excitable & Oscillatory Systems (FitzHugh–Nagumo Model)

To understand non-linear phase space dynamics, consider the FitzHugh–Nagumo model representing autocatalytic chemical excitability or membrane potential action potentials.

:::matrix {cols="50/50"}
[[0,0]]
### Governing Equations
$$
\begin{aligned}
\frac{dv}{dt} &= v - \frac{v^3}{3} - w + I_{ext} \\[4pt]
\frac{dw}{dt} &= \epsilon (v + a - b w)
\end{aligned}
$$
- $v$: Fast activator variable (e.g., sodium channel opening).
- $w$: Slow recovery / inhibitor variable (e.g., potassium channel opening, $\epsilon \ll 1$).
- $I_{ext}$: External stimulus current.

[[0,1]]
### Phase Plane Geometry
- **$v$-nullcline:** Cubic curve $w = v - \frac{v^3}{3} + I_{ext}$.
- **$w$-nullcline:** Straight line $w = \frac{v + a}{b}$.

Intersecting the $w$-nullcline along the middle (unstable) branch of the cubic nullcline destabilizes the steady state, generating **limit cycle oscillations**.
:::

---

# Phase Space Trajectories & Vector Fields

:::matrix {cols="50/50"}
[[0,0]]
### Direction Fields & Flow Fields
Every point $(v, w)$ in phase space defines a velocity vector $\mathbf{f}(v, w) = \left( \frac{dv}{dt}, \frac{dw}{dt} \right)$.

Phase space analysis allows global qualitative determination of trajectories without analytical ODE integration.

[[0,1]]
### Vector Arrow Construction
Numerical trajectories sub-sample direction vectors:
$$
\mathbf{u} = \frac{1}{\sqrt{dx^2 + dy^2}} \begin{pmatrix} dx \\ dy \end{pmatrix}
$$
This constructs quiver fields highlighting fast horizontal relaxation towards cubic nullclines followed by slow vertical motion along the outer branches.
:::

---

# Linear Stability & Fixed Point Classification

Linearizing a 2D non-linear system $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$ around a steady state $(v^*, w^*)$:
$$
\frac{d}{dt} \begin{pmatrix} \delta v \\ \delta w \end{pmatrix} = \mathbf{J}(v^*, w^*) \begin{pmatrix} \delta v \\ \delta w \end{pmatrix}
$$

:::matrix {cols="50/50"}
[[0,0]]
### FitzHugh-Nagumo Jacobian Evaluation
Taking partial derivatives evaluated at the fixed point:
$$
\mathbf{J} = \begin{pmatrix} \frac{\partial \dot{v}}{\partial v} & \frac{\partial \dot{v}}{\partial w} \\[4pt] \frac{\partial \dot{w}}{\partial v} & \frac{\partial \dot{w}}{\partial w} \end{pmatrix} = \begin{pmatrix} 1 - (v^*)^2 & -1 \\[4pt] \epsilon & -\epsilon b \end{pmatrix}
$$
The characteristic polynomial is:
$$
\lambda^2 - \text{Tr}(\mathbf{J}) \lambda + \det(\mathbf{J}) = 0
$$

[[0,1]]
### Stability Criteria
- **Trace:** $\text{Tr}(\mathbf{J}) = 1 - (v^*)^2 - \epsilon b$.
- **Determinant:** $\det(\mathbf{J}) = -\epsilon b (1 - (v^*)^2) + \epsilon$.

Stability requires $\text{Tr}(\mathbf{J}) < 0$ and $\det(\mathbf{J}) > 0$. If $(v^*)^2 < 1 - \epsilon b$, the Trace becomes positive, destabilizing the fixed point.
:::

---

# Supercritical Hopf Bifurcation Analysis

A **Hopf bifurcation** occurs when a pair of complex conjugate eigenvalues crosses the imaginary axis ($\text{Re}(\lambda) = 0$).

:::matrix {cols="50/50"}
[[0,0]]
### Zero-Trace Hopf Condition
The exact bifurcation threshold occurs when the Trace is exactly zero:
$$
\text{Tr}(\mathbf{J}) = 1 - (v^*)^2 - \epsilon b = 0 \implies (v^*)^2 = 1 - \epsilon b
$$
By substituting this $v^*$ back into the nullcline equations, we can solve for the critical stimulus parameter $I_{crit}$ where oscillations begin.
At $I_{crit}$, eigenvalues are purely imaginary $\lambda = \pm i \sqrt{\det(\mathbf{J})}$.

[[0,1]]
### Limit Cycle Emergence
- For $I < I_{crit}$: $\text{Tr}(\mathbf{J}) < 0 \implies$ Stable focus (damped oscillations).
- For $I > I_{crit}$: $\text{Tr}(\mathbf{J}) > 0 \implies$ Unstable focus enclosed by a **stable limit cycle attractor**.

The amplitude of the emerging limit cycle grows continuously as $\propto \sqrt{I - I_{crit}}$.
:::
