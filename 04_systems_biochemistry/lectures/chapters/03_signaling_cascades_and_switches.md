# Multi-Tier Signaling Cascades (MAPK / ERK Network)

Protein phosphorylation cycles are organized into hierarchical multi-tier cascades, such as the Mitogen-Activated Protein Kinase (MAPK) pathway.

:::matrix {cols="50/50"}
[[0,0]]
### 3-Tier Cascade Architecture
$$
\text{Signal} \to \text{MAPKKK} \xrightarrow{E_1} \text{MAPKKK}^* \xrightarrow{} \text{MAPKK}^* \xrightarrow{} \text{MAPK}^*
$$
- **MAPKKK:** Raf kinase.
- **MAPKK:** MEK (dual-specificity kinase).
- **MAPK:** ERK (extracellular signal-regulated kinase).

[[0,1]]
### Biological Phenomenon: Xenopus Oocytes
In *Xenopus* (frog) oocytes, progesterone induces maturation into eggs. This process is mediated by the MAPK cascade.
Because of the **compounding Goldbeter–Koshland ultrasensitive steps**, the cascade converts a graded (continuous) progesterone stimulus into a digital, all-or-none biological decision: the cell either matures completely or not at all.
:::

---

# Synthetic Gene Toggle Switch (Gardner–Cantor–Collins)

Bistable switches allow genetic networks to maintain memory of transient environmental signals.

:::matrix {cols="50/50"}
[[0,0]]
### Mutual Repression Architecture
Two repressor genes ($u$ and $v$) mutually inhibit each other's transcription (e.g., LacI and TetR repressors):
$$
\begin{aligned}
\frac{du}{dt} &= \frac{\alpha_1}{1 + v^\beta} - u \\[4pt]
\frac{dv}{dt} &= \frac{\alpha_2}{1 + u^\gamma} - v
\end{aligned}
$$
where $\alpha_1, \alpha_2$ are effective synthesis rates and $\beta, \gamma$ are cooperativity exponents (Hill coefficients).

[[0,1]]
### Nullcline Intersection Geometry
Setting derivatives to zero yields the nullclines:
- $u$-nullcline: $u = \frac{\alpha_1}{1 + v^\beta}$
- $v$-nullcline: $v = \frac{\alpha_2}{1 + u^\gamma}$

Substituting the $v$-nullcline into the $u$-nullcline yields the steady state polynomial:
$$
u = \frac{\alpha_1}{1 + \left( \frac{\alpha_2}{1 + u^\gamma} \right)^\beta}
$$
When $\beta, \gamma > 1$, this algebraic equation possesses **3 real roots** corresponding to fixed points.
:::

---

# Hysteresis & Biological Commitment Points

:::matrix {cols="50/50"}
[[0,0]]
### Saddle-Node Bifurcations & Hysteresis
Of the 3 roots derived previously:
- **2 Stable Nodes:** $(\text{High } u, \text{Low } v)$ and $(\text{Low } u, \text{High } v)$.
- **1 Unstable Saddle Point:** Acts as the threshold separating the basins of attraction.

Varying an external induction parameter $S$ shifts the nullclines, causing stable nodes and unstable saddles to coalesce and annihilate at **saddle-node bifurcation thresholds** $S_{lower}$ and $S_{upper}$.
The system exhibits **hysteresis**: the state path during parameter increase differs from the path during parameter decrease.

[[0,1]]
### Biological Relevance
- **Cell Cycle Transitions:** Cyclin B / Cdk1 activation during G2/M entry exhibits bistable hysteresis. This prevents partial mitosis and ensures the cell commits irreversibly to division.
- **Lac Operon:** Transient lactose induction permanently switches bacterial metabolism to utilization mode until nutrients are completely exhausted.
:::
