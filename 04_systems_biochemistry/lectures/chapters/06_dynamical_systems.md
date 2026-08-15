

:::titlepage
[[title]]
Chapter 6: Dynamical Systems, Synergetics & Catastrophe Theory
:::
---


# Linearization & the Jacobian Matrix

To analyze the behavior of a nonlinear system near a fixed point, we **linearize** the system. This is the bridge from "translating diagrams to equations" to "classifying dynamics".

:::matrix {cols="50/50"}
[[0,0]]
### The method
Given a 2D system:
$$ \dot{x} = f(x,y), \qquad \dot{y} = g(x,y) $$

1. **Find the fixed point** $(x^\star, y^\star)$ by solving $f = g = 0$.
2. **Compute the Jacobian matrix:**
$$
\mathbf{J} = \begin{pmatrix}
\frac{\partial f}{\partial x} & \frac{\partial f}{\partial y} \\
\frac{\partial g}{\partial x} & \frac{\partial g}{\partial y}
\end{pmatrix}\bigg|_{(x^\star,y^\star)}
$$
3. Near the fixed point, the system behaves like $\dot{\mathbf{u}} \approx \mathbf{J}\mathbf{u}$, where $\mathbf{u} = \mathbf{x} - \mathbf{x}^\star$.
4. The **eigenvalues** of $\mathbf{J}$ determine the local dynamics.

[[0,1]]
### Worked Example: Open system with feedback
Consider: $\dot{X} = V_{in} - k_{out} X$ with $V_{in} = 5$, $k_{out} = 2$.

**Fixed point:** $X^\star = V_{in}/k_{out} = 2.5$.

**Jacobian:** $J = \frac{\partial}{\partial X}(V_{in} - k_{out}X) = -k_{out} = -2$.

Since $J < 0$, the fixed point is **stable** (perturbations decay exponentially). The rate of return is $e^{-2t}$.

For a 2D system, the eigenvalues $\lambda_{1,2}$ of $\mathbf{J}$ are:
$$ \lambda = \frac{\tau \pm \sqrt{\tau^2 - 4\Delta}}{2} $$
where $\tau = \operatorname{Tr}(\mathbf{J})$ and $\Delta = \det(\mathbf{J})$.

:::


---

# Phase Portraits & Fixed Point Classification

A dynamical system $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$ is fully described by its vector field. Near any fixed point $\mathbf{x}^*$ (where $\mathbf{f}(\mathbf{x}^*) = 0$), the behavior is determined by the **Jacobian matrix**:

$$
\mathbf{J} = \begin{pmatrix}
\frac{\partial f_1}{\partial x_1} & \frac{\partial f_1}{\partial x_2} \\
\frac{\partial f_2}{\partial x_1} & \frac{\partial f_2}{\partial x_2}
\end{pmatrix}\bigg|_{\mathbf{x}^*}
$$

:::matrix {cols="50/50"}
[[0,0]]{.dense}
### The Trace-Determinant Plane
The eigenvalues $\lambda_{1,2}$ of a $2 \times 2$ Jacobian are:
$$ \lambda = \frac{\tau \pm \sqrt{\tau^2 - 4\Delta}}{2} $$
where $\tau = \operatorname{Tr}(\mathbf{J}) = J_{11} + J_{22}$ and $\Delta = \det(\mathbf{J}) = J_{11}J_{22} - J_{12}J_{21}$.

| Condition | Type |
|-----------|------|
| $\Delta < 0$ | **Saddle point** (one $\lambda > 0$, one $\lambda < 0$) |
| $\Delta > 0$, $\tau < 0$ | **Stable** (node or spiral) |
| $\Delta > 0$, $\tau > 0$ | **Unstable** (node or spiral) |
| $\Delta > 0$, $\tau^2 < 4\Delta$ | **Spiral** (complex $\lambda$) |
| $\Delta > 0$, $\tau^2 > 4\Delta$ | **Node** (real $\lambda$) |
| $\Delta > 0$, $\tau = 0$ | **Center** (purely imaginary $\lambda$) |

[[0,1]]
### Interactive Phase Explorer
<iframe src="./demos/phase_portrait.html" width="100%" height="450px" style="border:1px solid #ccc; border-radius: 8px;"></iframe>
:::

---

# The Hopf Bifurcation

What happens when a stable steady state *loses* stability? If the eigenvalues cross the imaginary axis ($\tau = 0, \Delta > 0$), a **limit cycle** is born. This is how biological rhythms (circadian clocks, heartbeats, glycolytic oscillations) emerge.

:::matrix {cols="50/50"}
[[0,0]]
### The Glycolytic Oscillator
Consider the Bier-Bakker-Westerhoff model of yeast glycolysis:
$$ \frac{dG}{dt} = V_{in} - k_1 G \cdot ATP $$
$$ \frac{dATP}{dt} = 2k_1 G \cdot ATP - \frac{k_p \cdot ATP}{ATP + K_m} $$

with $V_{in} = 0.36$, $k_1 = 0.02$, $k_p = 6.0$.

As the parameter $K_m$ is varied, the Jacobian's trace passes through zero, causing a **supercritical Hopf bifurcation**:
- $K_m$ large → $\tau < 0$ → stable spiral (damped oscillations).
- $K_m$ small → $\tau > 0$ → unstable spiral, trajectories settle onto a stable **limit cycle** (sustained oscillations).

[[0,1]]
### Limit Cycle Birth
<iframe src="./demos/hopf_bifurcation.html" width="100%" height="450px" style="border:1px solid #ccc; border-radius: 8px;"></iframe>
:::

---

# Bistability & Hysteresis

Biological switches require **bistability**: the coexistence of two stable steady states. This is typically achieved via **positive feedback** (mutual activation or mutual inhibition).

:::matrix {cols="50/50"}
[[0,0]]
### The Saddle-Node Bifurcation

Consider the Tyson mutual co-activation switch:
$$ \frac{dR}{dt} = k_1 S - k_2 R \cdot E $$
$$ \frac{dE}{dt} = k_3 (E_{tot} - E) \cdot R - k_4 E $$

Here $R$ activates $E$ and $E$ activates $R$ (positive feedback loop). For certain parameter ranges, the nullclines intersect **three times**: two stable nodes separated by an unstable saddle point.

As the stimulus $S$ increases past a threshold, the lower stable state vanishes in a **saddle-node bifurcation**, forcing a discontinuous jump to the upper state. Decreasing $S$ does not reverse the jump immediately — this creates a **hysteresis loop**.

[[0,1]]
### The Biological Toggle Switch
<iframe src="./demos/bio_switch.html" width="100%" height="450px" style="border:1px solid #ccc; border-radius: 8px;"></iframe>
:::

---

# Catastrophe Theory & The Cusp

Catastrophe theory (René Thom, 1972) classifies how **continuous** parameter changes cause **discontinuous**, abrupt shifts in equilibria. The canonical model is the **Cusp Catastrophe**.

:::matrix {cols="50/50"}
[[0,0]]
### The Potential & Equilibrium Manifold
The system is governed by a potential:
$$V(x) = \frac{1}{4}x^4 - \frac{1}{2}ax^2 - bx$$
Setting $V'(x) = 0$ yields the equilibrium condition:
$$ \boxed{x^3 - ax - b = 0} $$
or equivalently, $\dot{x} = -V'(x) = -x^3 + ax + b$.

- $a$ (**Splitting factor**, e.g. Wee1 activity): Controls whether the system is mono- or bistable. When $a > 0$, the potential has two wells.
- $b$ (**Normal factor**, e.g. Cyclin concentration): Tilts the potential, selecting which well the system occupies.

[[0,1]]
### The Bifurcation Set (Cusp Curve)
The fold occurs when the discriminant vanishes:
$$4a^3 - 27b^2 = 0 \quad\Longrightarrow\quad b = \pm\sqrt{\tfrac{4}{27}a^3}$$

This defines a cusp-shaped region in the $(a, b)$ control plane. Inside this region, there are **three** real roots (bistability). Outside, there is only **one** (monostability).

When a trajectory crosses the fold from inside, the system undergoes a **catastrophic jump** to the other stable branch.
:::
---

# Interactive Cusp Surface
<iframe src="./demos/cusp_surface.html" width="100%" height="60%" style="border:1px solid #ccc; border-radius: 8px;"></iframe>

---

# Spatial Synergetics & Turing Patterns

Alan Turing (1952) proved that **reaction-diffusion** systems can spontaneously break spatial symmetry. If an activator diffuses slowly and an inhibitor diffuses rapidly, a homogeneous state can become unstable to spatial perturbations.

:::matrix {cols="50/50"}
[[0,0]]
### The Schnakenberg Model
A minimal activator-inhibitor reaction-diffusion system:
$$ \frac{\partial u}{\partial t} = a - u + u^2 v + D_u \nabla^2 u $$
$$ \frac{\partial v}{\partial t} = b - u^2 v + D_v \nabla^2 v $$

**Homogeneous steady state:** $u_0 = a + b$, $v_0 = b/(a+b)^2$.

### The four Turing conditions
For diffusion-driven instability, all four must hold:
1. $f_u + g_v < 0$ (stable without diffusion: $\tau < 0$)
2. $f_u g_v - f_v g_u > 0$ (stable without diffusion: $\Delta > 0$)
3. $D_v f_u + D_u g_v > 0$ (diffusion destabilizes)
4. $(D_v f_u + D_u g_v)^2 > 4 D_u D_v (f_u g_v - f_v g_u)$ (positive $\sigma(k)$ for some $k$)

Condition 3 strictly requires $D_v \gg D_u$.

[[0,1]]
### Dispersion Relation & Pattern Formation
Consider perturbations $\sim e^{\sigma t + ikx}$. The growth rate $\sigma(k)$ is the largest eigenvalue of:
$$ \mathbf{J}(k) = \mathbf{J}_0 - k^2 \mathbf{D} = \begin{pmatrix} f_u - D_u k^2 & f_v \\ g_u & g_v - D_v k^2 \end{pmatrix} $$

If $\sigma(k) > 0$ for some band of wavenumbers $k$, spatial patterns grow spontaneously from noise.

<iframe src="./demos/turing_patterns.html" width="100%" height="460px" style="border:1px solid #ccc; border-radius: 8px;"></iframe>
:::

---

# The Oregonator: Chemical Oscillations in the BZ Reaction

The BZ reaction is the classic example of non-equilibrium chemical thermodynamics. Modeled by the **Oregonator**, it exhibits striking macroscopic color oscillations.

:::matrix {cols="50/50"}
[[0,0]]
### Dimensionless Oregonator
The full FKN model simplifies to a dimensionless 2-variable system (in the limit of fast $Y$ dynamics):
$$ \epsilon \frac{dx}{d\tau} = x(1 - x) - f z \frac{x - q}{x + q} $$
$$ \frac{dz}{d\tau} = x - z $$

where:
- $x \propto [HBrO_2]$, $z \propto [Ce^{4+}]$
- $\epsilon \ll 1$ (time-scale separation → relaxation oscillations)
- $q \ll 1$ (sets the switching threshold)
- $f \approx 1$ (stoichiometric factor)

This is a classic **relaxation oscillator**: slow accumulation of $z$ punctuated by fast bursts in $x$.

[[0,1]]
### Oregonator Animation
<iframe src="./demos/bz_oscillator.html" width="100%" height="550px" style="border:1px solid #ccc; border-radius: 8px;"></iframe>
:::
