# Phase, Gauge Symmetry & the Dirac Equation

## Phase as Geometry

:::matrix { cols="50/50" rows="100" height="60%"}

[[0, 0]]
**Global phase has no physical meaning:**

$e^{i\alpha}|\psi\rangle \equiv |\psi\rangle$ for any $\alpha \in \mathbb{R}$.

All probabilities $|\langle a_n|e^{i\alpha}\psi\rangle|^2 = |\langle a_n|\psi\rangle|^2$ are identical.

This is why states live in $\mathbb{P}\mathcal{H}$, not $\mathcal{H}$.

[[0, 1]]
**Relative phase is physical:**

$|\psi\rangle = \frac{1}{\sqrt{2}}(|0\rangle + e^{i\phi}|1\rangle)$

Different $\phi$ → different interference patterns!

**Phase accumulation:** $\psi_n(t) = \phi_n \cdot e^{-iE_n t/\hbar}$

Different energy components rotate at different angular velocities $\omega_n = E_n/\hbar$ → wavepacket dynamics and interference.

:::

**Berry phase (1984):** A quantum state transported adiabatically around a closed loop in parameter space acquires a geometric phase $\gamma = \oint \mathbf{A} \cdot d\mathbf{R}$. This is the holonomy of a $U(1)$-connection on a fiber bundle over parameter space.

---

## Aharonov-Bohm Effect

:::matrix {cols="40/10/50" rows="100" height="80%" }

[[0, 0]]
Electrons pass around a solenoid where $\mathbf{B}=0$ on their path. Yet the **interference pattern shifts!** Phase difference:
$$
\Delta\phi=\frac{e}{\hbar}\oint \mathbf{A} \cdot d\mathbf{l}=\frac{e\Phi_B}{\hbar}
$$
where $\Phi_B$ is the magnetic flux through the solenoid.

[[0, 2]]
**Conclusions:**
* The vector potential $\mathbf{A}$ is **physically real**, not just a mathematical convenience
* Phase is a measurable quantity (via interference)
* First proposed: Aharonov & Bohm (1959)
* Confirmed experimentally: Chambers (1960), Tonomura (1986) with electron holography
* **Mathematically:** the gauge field $\mathbf{A}$ is a connection 1-form on a principal $U(1)$-bundle, and the Aharonov-Bohm phase is its holonomy

:::

---

## Analytic Solutions: Infinite Square Well

The infinite square well $V(x) = 0$ on $[0, L]$, $V = \infty$ outside, gives the eigenvalue problem $\hat{H}\phi = E\phi$ with Dirichlet boundary conditions $\phi(0) = \phi(L) = 0$.

**Eigenfunctions and energies:**

$$
\phi_n(x) = \sqrt{\frac{2}{L}}\sin\left(\frac{n\pi x}{L}\right), \qquad E_n = \frac{n^2\pi^2\hbar^2}{2mL^2}, \quad n = 1, 2, 3, \ldots
$$

**Key observations:**
* Energies are **quantized** — discrete spectrum follows from the compact domain and boundary conditions
* Ground state $E_1 > 0$: **zero-point energy** (a consequence of the uncertainty principle: confinement $\Delta x \leq L$ forces $\Delta p \geq \hbar/2L$)
* Each $\phi_n$ has $n-1$ **nodes** — this is a general theorem (Sturm oscillation theorem)
* The eigenfunctions form a complete orthonormal basis for $L^2([0, L])$ — this is the Fourier sine series

---

## Clifford Algebra and the Dirac Equation

**Problem:** Find $\hat{H}$ linear in $\hat{\mathbf{p}}$ such that $\hat{H}^2 = |\mathbf{p}|^2c^2 + m^2c^4$ (Einstein relation).

**Ansatz:** $\hat{H} = c\,\boldsymbol{\alpha}\cdot\hat{\mathbf{p}} + \beta\,mc^2$

Squaring and requiring $\hat{H}^2 = |\mathbf{p}|^2c^2 + m^2c^4$ demands:

$$
\{\alpha_i, \alpha_j\} = 2\delta_{ij}\hat{I}, \qquad \{\alpha_i, \beta\} = 0, \qquad \beta^2 = \hat{I}
$$

These are the defining relations of the **Clifford algebra** $\text{Cl}(1,3)$.

* No $1\times 1$ or $2\times 2$ matrices satisfy these relations
* Minimal faithful representation: $4\times 4$ matrices (the **Dirac gamma matrices**)
* The wavefunction must be a **4-component spinor** $\psi = (\psi_1, \psi_2, \psi_3, \psi_4)^T$
* Electron spin emerges **algebraically** — not as a postulate, but as a consequence of marrying QM with relativity
* Two extra components → **antimatter** (predicted 1928, discovered 1932)

---

## Devices Using Quantum Effects

| Device | Quantum Effect | Key Physics |
|--------|---------------|-------------|
| **Laser** | Stimulated emission | Population inversion, coherent photons |
| **LED** | Electron-hole recombination | Bandgap determines color |
| **Scanning Tunneling Microscope** | Quantum tunneling | $I \propto e^{-2\kappa d}$ → atomic resolution |
| **MRI** | Nuclear spin precession | Larmor frequency in magnetic field |
| **Flash memory** | Fowler-Nordheim tunneling | Electrons through oxide barrier |
| **Atomic clock** | Hyperfine transitions | Cs-133: 9,192,631,770 Hz defines the second |
| **Solar cell** | Photoelectric effect | Photon → electron-hole pair |
| **Electron microscope** | de Broglie wavelength | $\lambda \ll$ visible light → nm resolution |
