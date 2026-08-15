
:::titlepage

[[title]]
Chapter 5: Translating Network Diagrams to ODEs
:::

---

# The Graphical Language of Systems Biology

To translate biological schematics into rigorous mathematical models, we must follow strict translation rules. Every node represents a **state variable** (a chemical species whose concentration changes over time), and every edge (arrow) represents a **kinetic term** in the differential equation.

:::matrix {cols="50/50"}
[[0,0]]
### 1. Solid Arrows (Mass Transfer)
Solid arrows represent actual chemical transformations or mass flow. They directly consume reactants ($-$) and produce products ($+$).
- $\ce{A -> B}$: Irreversible conversion.
- $\ce{A <=> B}$: Reversible conversion.
- $\ce{\emptyset -> A}$: Zero-order synthesis (from an infinite pool).
- $\ce{A -> \emptyset}$: First-order degradation / clearance.

[[0,1]]
### 2. Dashed Arrows (Regulation)
Dashed arrows represent flow of *information*, not mass. They modify the rates of solid arrows without being consumed themselves.
- $A \dashrightarrow B \text{ (or } + \text{)}$: **Activation** (Positive feedback / allosteric promotion).
- $A \dashv B \text{ (or } - \text{)}$: **Inhibition** (Negative feedback / repression).
:::

---

# How to Read a Diagram: Systematic Algorithm

Given any network diagram, follow these steps to write down the ODE for species $X$:

:::matrix {cols="50/50"}
[[0,0]]
### Step-by-step procedure

1. **List all solid arrows involving $X$.**
   - Arrow *into* $X$ → **positive** term in $dX/dt$.
   - Arrow *out of* $X$ → **negative** term in $dX/dt$.
2. **Determine the rate law** for each solid arrow:
   - From $\emptyset$: zero-order ($V_{in}$).
   - First-order decay: $k \cdot [X]$.
   - Bimolecular: $k \cdot [A][B]$.
   - Saturating (enzyme): $V_{max} [S] / (K_m + [S])$.
3. **Apply regulatory modifiers.** For each dashed arrow landing on the reaction:
   - **Activator** $A$: multiply the rate by $[A]$, or by a Hill function $[A]^n/(K^n + [A]^n)$.
   - **Inhibitor** $I$: multiply by $1/(1 + ([I]/K)^n)$.
4. **Sum all terms** to get $dX/dt$.

[[0,1]]
### Quick reference

| Diagram Element | ODE Contribution to $dX/dt$ |
|-----------------|----------------------------|
| $\emptyset \to X$ | $+V_{in}$ |
| $X \to \emptyset$ | $-k_{out}[X]$ |
| $A + X \to P$ | $-k[A][X]$ |
| $\emptyset \to X$ with activator $A$ | $+k \cdot [A]$ |
| $\emptyset \to X$ with repressor $I$ | $+\frac{V_0}{1+([I]/K)^n}$ |
| $X \to P$ via enzyme $E$ | $-\frac{V_{max}[X]}{K_m + [X]}$ |
:::

---

# Rule 1a: Open Systems — Synthesis & Decay

The simplest biochemical model: a species $X$ is produced at a constant rate and degraded proportionally to its concentration.

:::matrix {cols="50/50"}
[[0,0]]
### Schematic Diagram
![](./images/diagrams/rule1a_open_system.svg) {width="80%"}

[[0,1]]
### ODE Translation
**Zero-order synthesis & First-order decay:**
$$ \frac{d[X]}{dt} = V_{in} - k_{out}[X] $$

At steady state ($d[X]/dt = 0$):
$$ [X]\_{eq} = \frac{V\_{in}}{k_{out}} $$

This is the fundamental building block of *every* open biochemical system: constant supply vs. proportional loss.
:::

---

# Rule 1b: Bimolecular Mass Action

When two species collide and react, the rate is proportional to the product of their concentrations.

:::matrix {cols="50/50"}
[[0,0]]
### Schematic Diagram
![](./images/diagrams/rule1b_bimolecular.svg) {width="80%"}

[[0,1]]
### ODE Translation
**Bimolecular Mass Action:**
$$ \frac{d[Z]}{dt} = +k_1 [X][Y] $$
$$ \frac{d[X]}{dt} = -k_1 [X][Y] $$
$$ \frac{d[Y]}{dt} = -k_1 [X][Y] $$

Both reactants are *consumed* (negative terms) while the product is *created* (positive term). Note the **conservation law**: $[X]+[Z] = \text{const}$ if $X$ has no other source.
:::

---

# Rule 2: Enzymatic Catalysis (Michaelis-Menten)

When a reaction is driven by an enzyme, the mass-action assumption fails at high substrate concentrations due to enzyme saturation.

:::matrix {cols="50/50"}
[[0,0]]
### Schematic Diagram
![](./images/diagrams/rule2_michaelis_menten.svg) {width="80%"}

(Where $E$ acts catalytically and is **not consumed**.)

[[0,1]]
### ODE Translation
**Standard Michaelis-Menten:**
$$ \frac{d[S]}{dt} = - \frac{V_{max}[S]}{K_M + [S]} $$
$$ \frac{d[P]}{dt} = + \frac{V_{max}[S]}{K_M + [S]} $$

Where $V\_{max} = k\_{cat}[E]\_{tot}$. At very high $[S] \gg K_M$, the rate saturates at $V\_{max}$. At low $[S] \ll K\_M$, the rate is approximately linear: $\approx (V\_{max}/K\_M)[S]$.
:::

---

# Rule 3a: Allosteric Activation

A regulatory molecule $A$ can *enhance* the rate of a chemical reaction without itself being consumed. This is modeled by multiplying the basal rate by a function of $[A]$.

:::matrix {cols="50/50"}
[[0,0]]
### Schematic Diagram
![](./images/diagrams/rule3a_activation.svg) {width="80%"}

(Activator $A$ boosts the production of $B$ via a dashed $(+)$ arrow.)

[[0,1]]
### ODE Translation
**Linear proportional activation:**
$$ \frac{d[B]}{dt} = k_0 \cdot [A] - k_d [B] $$

**Saturating (Hill) activation** (if $A$ binds cooperatively):
$$ \frac{d[B]}{dt} = V_{max} \frac{[A]^n}{K^n + [A]^n} - k_d [B] $$

In both cases, the **degradation term** $-k_d [B]$ is essential for reaching a steady state.
:::

---

# Rule 3b: Hill-Type Repression

A repressor molecule $I$ can *suppress* the synthesis of a species. The Hill function models the switch-like shutoff characteristic of cooperative binding.

:::matrix {cols="50/50"}
[[0,0]]
### Schematic Diagram
![](./images/diagrams/rule3b_repression.svg) {width="80%"}

(Inhibitor $I$ blocks the production of $X$ via a dashed $\dashv$ arrow.)

[[0,1]]
### ODE Translation
**Hill-type repression:**
$$ \frac{d[X]}{dt} = V_0 \frac{1}{1 + \left(\frac{[I]}{K}\right)^n} - k_d [X] $$

- $n = 1$: Hyperbolic (gradual) shutoff.
- $n = 2$: Sigmoidal shutoff.
- $n \to \infty$: Binary switch (step function).

The **Hill coefficient** $n$ is the key parameter controlling the *sharpness* of the biological switch.
:::

---

# The Hill Function: Derivation & Interpretation

The Hill function arises from cooperative ligand binding. If a protein has $n$ identical, perfectly cooperative binding sites for a ligand $L$:

:::matrix {cols="50/50"}
[[0,0]]
### Derivation
The all-or-nothing binding equilibrium is:
$$ P + nL \rightleftharpoons PL_n, \qquad K_d = \frac{[P][L]^n}{[PL_n]} $$

The fraction of occupied protein:
$$ \theta = \frac{[PL_n]}{[P]+[PL_n]} = \frac{[L]^n}{K_d + [L]^n} = \frac{[L]^n}{K^n + [L]^n} $$

where $K = K_d^{1/n}$ is the **half-saturation constant** ($\theta = 0.5$ when $[L] = K$).

[[0,1]]
### Key properties

| $n$ | Shape | Biological meaning |
|-----|-------|--------------------|
| 1 | Michaelis-Menten hyperbola | No cooperativity |
| 2–4 | Sigmoidal | Moderate cooperativity |
| $\gg 1$ | Step function | Ultra-switch |

The Hill function unifies Michaelis-Menten kinetics ($n=1$) and Boolean logic ($n \to \infty$). Real biological switches (hemoglobin, lac operon) typically have $n \approx 2$–$4$.

**Activation form:** $\frac{[A]^n}{K^n + [A]^n}$

**Repression form:** $\frac{K^n}{K^n + [I]^n} = \frac{1}{1 + ([I]/K)^n}$
:::

---

# Rule 4: Covalent Modification (Goldbeter-Koshland)

When a protein flips between inactive ($W$) and active ($W^{\star}$) states via phosphorylation, the total protein is conserved: $[W]_{tot} = [W] + [W^{\star}]$.

:::matrix {cols="50/50"}
[[0,0]]
### Schematic Diagram
![](./images/diagrams/rule4_goldbeter.svg) {width="80%"}
We track the active fraction $y = [W^{\star}] / [W]_{tot}$.

[[0,1]]
### ODE Translation
The rate of change for the active fraction $y$:
$$
\frac{dy}{dt} = v_1 \frac{1 - y}{K_1 + (1 - y)} - v_2 \frac{y}{K_2 + y}
$$
- $v_1 \propto [K]$ (Kinase velocity).
- $v_2 \propto [P]$ (Phosphatase velocity).
- $K_1, K_2$ are the Michaelis constants relative to $[W]_{tot}$.

When $K_1, K_2 \ll 1$ (zero-order regime), this system exhibits **ultrasensitivity**: a small change in $v_1/v_2$ causes a near-switch-like change in $y$.
:::

---

# Conservation Laws

Many biochemical systems have **conserved quantities** that reduce the number of independent variables and constrain the dynamics.

:::matrix {cols="50/50"}
[[0,0]]
### The Principle
If species are only interconverted (not created or destroyed from external sources), their **total amount** is constant:
$$[W] + [W^{\star}] = [W]_{tot} = \text{const}$$

This lets us eliminate one variable:
$$[W] = [W]_{tot} - [W^{\star}]$$

So a 2-variable system becomes a **1-variable ODE**.

[[0,1]]
### General rule

For any closed sub-network where mass is neither created from $\emptyset$ nor destroyed to $\emptyset$, the **sum of all species** in the sub-network is conserved.

**Examples:**
- Enzyme-substrate: $[E] + [ES] = [E]_{tot}$
- Phosphorylation cycle: $[W] + [W^*] = [W]_{tot}$
- GTPase switch: $[G_{GDP}] + [G_{GTP}] = [G]_{tot}$

**Why it matters:** Conservation laws often reduce the dimensionality of the system, making analytical solutions possible.
:::

---

# Worked Example 1: The Gierer-Meinhardt Turing System

This generic biochemical network contains all the core ingredients required for spontaneous symmetry breaking and spatial pattern formation: **local auto-activation coupled with long-range inhibition**.

:::matrix {cols="50/50"}
[[0,0]]
### Schematic Diagram
![](./images/diagrams/example1_turing.svg) {width="100%"}
(Activator $A$ drives production of itself and $I$. Inhibitor $I$ shuts down $A$. Both degrade over time.)

[[0,1]]
### ODE Translation
**The Activator Equation:**
Has a basal synthesis $V_0$, autocatalysis promoted by $A^2$ but repressed by $I$, and first-order decay.
$$ \frac{d[A]}{dt} = \frac{k_1 [A]^2}{[I]} - k_A [A] + V_0 $$

**The Inhibitor Equation:**
Driven exclusively by the Activator $A$, and decays over time.
$$ \frac{d[I]}{dt} = k_2 [A]^2 - k_I [I] $$

(This generic pattern underlies biological phenomena from zebra stripes to tissue morphogenesis!)
:::

---

# Worked Example 2: Belousov-Zhabotinsky (Oregonator)

The famous color-changing chemical oscillator. The Oregonator model (Field, Körös, Noyes) simplifies the complex BZ reaction into three core species: $\ce{HBrO2}$ ($X$), $\ce{Br-}$ ($Y$), and $\ce{Ce^{4+}}$ ($Z$).

:::matrix {cols="40/30/30"}
[[0,0]]
### Schematic Diagram

![](./images/diagrams/example2_oregonator.svg) {width="100%"}

[[0,1]]
The five FKN reaction channels:
- $R_1$: $A + Y \xrightarrow{k_1} X$ (initiation)
- $R_2$: $X + Y \xrightarrow{k_2} \text{products}$ (mutual annihilation)
- $R_3$: $A + X \xrightarrow{k_3} 2X + 2Z$ (autocatalysis!)
- $R_4$: $2X \xrightarrow{k_4} \text{products}$ (disproportionation)
- $R_5$: $Z \xrightarrow{k_5} fY$ (recovery)

$A = [\ce{BrO3-}]$ is a constant pool.

[[0,2]]
### ODE Translation
**The Oregonator System:**
$$ \frac{dX}{dt} = k_1 A Y - k_2 X Y + k_3 A X - 2k_4 X^2 $$
$$ \frac{dY}{dt} = -k_1 A Y - k_2 X Y + \frac{1}{2} f k_5 Z $$
$$ \frac{dZ}{dt} = 2 k_3 A X - k_5 Z $$

**Reading the equations from the diagram:**
- $+k_1 AY$ in $dX/dt$: reaction $R_1$ produces $X$ from $A+Y$ ✓
- $-k_2 XY$ in $dX/dt$: reaction $R_2$ consumes both $X$ and $Y$ ✓
- $+k_3 AX$ in $dX/dt$: reaction $R_3$ autocatalytically doubles $X$ ✓
- The $f$ factor is a stoichiometric parameter ($f \approx 1$).
:::
