:::titlepage
[[title]]
Chapter 1: Chemical Equilibrium & pH

:::

---

# Explanation of Thermodynamic Quantities: $\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ$

| Term | Name | Explanation |
| :--- | :--- | :--- |
| $\color{#279B61}{\Delta G^\circ}$ | <span style="color: #279B61; font-weight: bold;">Gibbs free-energy change</span> | Represents the difference in energy between products and reactants. A negative $\Delta G^\circ$ indicates an **exergonic** reaction that proceeds spontaneously with a favorable equilibrium constant. Conversely, a positive $\Delta G^\circ$ denotes an **endergonic** reaction, which is nonspontaneous and has an unfavorable equilibrium constant. |
| $\color{#D91E76}{\Delta H^\circ}$ | <span style="color: #D91E76; font-weight: bold;">Enthalpy change</span> | The overall heat associated with a reaction, reflecting the net difference in bond strengths between newly formed bonds and those broken. A negative $\Delta H^\circ$ signifies an **exothermic** process where heat is released. A positive $\Delta H^\circ$ signifies an **endothermic** process where heat is absorbed. |
| $\color{#2B8CBE}{\Delta S^\circ}$ | <span style="color: #2B8CBE; font-weight: bold;">Entropy change</span> | The shift in the system's molecular disorder or randomness resulting from a reaction. A negative $\Delta S^\circ$ means the system becomes less random; a positive $\Delta S^\circ$ indicates an increase in molecular randomness. |

---

# Gibbs free energy ($G$)

* $G = H - TS$
* The change in free energy for a process, $\Delta G$, equals the maximum useful work that can be done by the system on its surroundings in a spontaneous process occurring at constant temperature and pressure.
* The sign of G tells us whether the reaction is spontaneous at constant **pressure** and **temperature**:

$$
\begin{array}{c}
\Delta G = \Delta H - T\Delta S \\\\[0.5em]
\Delta S\_{\text{univ}} = \Delta S\_{\text{sys}} + \Delta S\_{\text{surr}} = \Delta S\_{\text{sys}} + \left( -\frac{\Delta H_{\text{sys}}}{T} \right) \\\\[0.5em]
-T\Delta S\_{\text{univ}} = -T\Delta S\_{\text{sys}} + \Delta H_{\text{sys}} = \Delta G \\\\[0.5em]
\Delta S_{\text{univ}} {\color{#009900}\Large\uparrow} \qquad \Delta G {\color{red}\Large\downarrow}
\end{array}
$$

* If $\Delta G < 0$, the reaction is spontaneous in the forward direction.
* If $\Delta G = 0$, the reaction is at equilibrium.
* If $\Delta G > 0$, the reaction in the forward direction is nonspontaneous (work must be done to make it occur) but the reverse reaction is spontaneous.
---

# Equilibrium

:::matrix{ cols="70/30" }
[[0,0]]
$$
G = H - TS = U + PV - TS
$$
$$
dG = \underline{dU + PdV} + VdP - \underline{TdS} - SdT
$$
$$
dG = VdP - SdT
$$
$$
dG\_{\text{mol}} = V\_{\text{mol}}dP - S_{\text{mol}}dT
$$
$$
\color{pink}{\boldsymbol{\downarrow}}
$$
$$
\left( \frac{\partial G\_{\text{mol}}}{\partial P} \right)\_T = \underline{V_{\text{mol}}}
$$
$$
\text{at constant } T \quad 
\left[ 
\begin{aligned} 
  & G_{\text{mol}} - G^{\circ} = \int_{P_0}^{P} \frac{RT}{P} dP \\\\ 
  & G_{\text{mol}} - G^{\circ} = RT \ln \frac{P}{P_0} 
\end{aligned} 
\right.
$$
For a mix of ideal gases of reactants and products:
$$
\alpha \mathbf{A} + \beta \mathbf{B} \rightleftharpoons \rho \mathbf{R} + \sigma \mathbf{S}
$$
$$
\Delta G\_{\text{mol}} - \Delta G^{\circ} = RT \ln Q \hspace{2cm} Q = \frac{P\_{\mathbf{R}}^\rho P\_{\mathbf{S}}^\sigma}{P\_{\mathbf{A}}^\alpha P\_{\mathbf{B}}^\beta}
$$
[[0,1]]
$$
\bbox[#FCAECA, 20px, border-radius: 15px]{
\begin{array}{c}
\text{The First Law of} \\\\
\text{Thermodynamics} \\\\[1em]
TdS = dU + PdV
\end{array}
}
$$
$$
\bbox[#FCAECA, 20px, border-radius: 15px]{
\begin{array}{c}
\text{For ideal gas} \\\\[0.5em]
PV = NRT \\\\[0.5em]
V_{\text{mol}} = \frac{RT}{P}
\end{array}
}
$$
'mol' - per 1 mole
:::

---

# Reaction Equilibrium

:::matrix {cols="70/30"}
[[0,0]]
$$
\begin{array}{rl}
\Delta G = \Delta G^\circ + RT \ln Q & \color{#2C5485}{\longleftarrow \text{reaction quotient}} \\\\
0 = \Delta G^\circ + RT \ln K & \color{#2C5485}{\longleftarrow \text{equilibrium constant}} \\\\
\Delta G^\circ = -RT \ln K & \\\\
\ln K = \frac{\Delta G^\circ}{-RT} & \\\\
K = e^{-\Delta G^\circ / RT} &
\end{array}
$$
In determining the value of $Q$, the concentrations of gases are always expressed as **partial pressures** in atmospheres and solutes are expressed as their concentrations in **molarities**.
$$ 
\alpha \mathbf{A} + \beta \mathbf{B} \rightleftharpoons \rho \mathbf{R} + \sigma \mathbf{S} 
$$
$$ 
Q = \frac{\{\mathbf{R}\}^\rho \{\mathbf{S}\}^\sigma}{\{\mathbf{A}\}^\alpha \{\mathbf{B}\}^\beta} \qquad \color{#2C5485}{\longleftarrow \text{activities}} 
$$

*   If $Q < K$, then the reaction will **move to the right**.
*   If $Q > K$, then the reaction will **move to the left**.
*   If $Q = K$, then the reaction is at equilibrium
[[0,1]]
![](./images/slide_18_img_47.png){ width=80 }
![](./images/slide_18_img_51.png){ width=80 }
:::
---

# Dynamic Equilibrium

:::matrix{cols="70/30"}
[[0,0]]
**Thermodynamic equilibrium** is the state of a system in which all macroscopic flows of energy and matter cease, all types of equilibrium (mechanical, thermal, and chemical) are satisfied, and the system's macroscopic properties remain constant in time.
[[1,0]]
**Dynamic equilibrium** is the microscopic realization of thermodynamic equilibrium: opposing processes occur simultaneously at equal rates, so that no net macroscopic change takes place.
[[2,0]]
:::matrix{cols="10/50/40"}
[[0,0]]
**Examples:**
[[0,1]] 
* evaporation $\leftrightarrow$ condensation, 
* dissolution $\leftrightarrow$ recrystallization,
* dissociation $\leftrightarrow$ recombination,
* reversible chemical reactions, 
* etc
[[0,2]]
**Generalization of mechanical equilibrium**
:::
[[3,0:2]]
**Relation:** Dynamic equilibrium is the **microscopic mechanism** that sustains thermodynamic equilibrium.
[[0,1]]
**WHAT HAPPENS**<br>
**Perspective of thermodynamics**
[[1,1]]
**HOW IT HAPPENS**<br>
**Perspective of Stat.mechanics**
[[2,1]]
![](./images/slide_19_img_54.png){width=60}
:::
:::matrix{cols="50/50"}
[[0,0]]
**evaporation ↔ condensation**
![](./images/slide_19_img_52.png){width="40%"}
[[0,1]]
**reversible chemical reactions**
![](./images/slide_19_img_53.png){width="70%"}
:::
![rect](40 32 60 25){color=red width=4px}

---

# Dynamic Equilibrium Model

![youtube](bDtkv8q-YGQ){width=90}

---


# Le Châtelier’s principle

## (Le Chatelier–Braun principle, equilibrium law)

:::matrix {cols="50/50" gap="30px"}
[[0,0]]
If the equilibrium of a system is disturbed by a change in one or more of the determining factors (as temperature, pressure, or concentration) the system tends to adjust itself to a new equilibrium by **counteracting** as far as possible the effect of the change.
![](./images/slide_22_img_58.png)
[[0,1]]
Discovered in 1884 by extending the reasoning from the **Van't Hoff relation**:
$$
\begin{aligned}
\Delta G^\circ &= -RT \ln K \\\\[0.5em]
\Delta H^\circ - T\Delta S^\circ &= -RT \ln K \\\\[0.5em]
\frac{\Delta H^\circ}{RT} - \frac{\Delta S^\circ}{R} &= -\ln K
\end{aligned}
$$
Differentiate by $T$,<br>
assuming $\Delta H^\circ, \Delta S^\circ$ do not depend on $T$
$$
\frac{\Delta H^\circ}{RT^2} = \frac{d\ln K}{dT} \qquad\qquad \bbox[#FFB6D9, 15px, border-radius: 10px]{\text{Van 't Hoff equation}}
$$
$$
\begin{array}{c|c}
\text{exothermic: } \Delta H^\circ < 0 \quad & \quad \text{endothermic: } \Delta H^\circ > 0 \\\\[1.5em]
T {\color{#4CAF50}\Large\uparrow} \quad K {\color{#F44336}\Large\downarrow} \quad & \quad T {\color{#4CAF50}\Large\uparrow} \quad K {\color{#4CAF50}\Large\uparrow} \\\\[1.5em]
\text{reaction shifts left} \quad & \quad \text{reaction shifts right}
\end{array}
$$
:::

---

# Temperature and Le Châtelier's principle

![youtube](z_iLK7gm_fo){width=90}

---

# Definition of pH

:::matrix{cols="70/30"}
[[0,0]]
## Protons' properties
* Protons are highly reactive: In fact, an isolated proton is so reactive that it will even add on to a molecule of methane in the gas phase to give $\ce{CH5+}$ in a strongly exothermic reaction (can be seen during mass-spectroscopy)
* Protons solvate
* Protons can rapidly move in water
* We will characterize solutions by the concentration of $[\ce{H+}]$


Thus we will be concerned with their fate as they can significantly influence the chemistry of the processes

**Note:** Different books use interchangeably $[\ce{H+}]$ and $[\ce{H3O+}]$, we will do the same.

## pH

The measure of proton concentration is pH. Note that $[\ce{H3O+}]$ is measured in mol/L often designated M. Logarithm taken is base 10, **NOT** natural.
$$
\text{pH} = -\log[\ce{H3O+}]
$$
[[0,1]]
![](./images/slide_7_img_11.png){width=90}

---


# Autoprotolysis of Water

$$
\ce{H2O + H2O <=> H3O+ (aq) + OH- (aq)}
$$

:::matrix{cols="50/50"}
[[0,0]]
![](./images/slide_8_img_13.png){width=70}
[[0,1]]
![](./images/slide_8_img_16.png){width=50}

## Dynamic equilibrium:

Law of mass action:
$$
k\_1 \cdot [\ce{H2O}] \cdot [\ce{H2O}] = k\_2 \cdot [\ce{H3O+}] \cdot [\ce{OH-}]
$$
$$
k = \frac{k\_1}{k\_2} = \frac{[\ce{H3O+}] \cdot [\ce{OH-}]}{\underbrace{[\ce{H2O}] \cdot [\ce{H2O}]}_{\textbf{approximate constant}}}
$$
::: 

$$
K_{\text{W}} = [\ce{H3O+}][\ce{OH-}] = 10^{-14} \text{ mol}^2 \text{ dm}^{-6} \text{ at } 25~^\circ\text{C}
$$

---

# Autoprotolysis of Water

$$
\ce{H2O + H2O <=> H3O+ (aq) + OH- (aq)}
$$
In this reaction, one molecule of water is acting as a base, receiving a proton from the other, which in turn is acting as an acid by donating a proton. From the equation we see that, for every hydronium ion formed, we must also form a hydroxide ion and so in pure water the concentrations of hydroxide and hydronium ions are equal.
$$
[\ce{H3O+}] = [\ce{OH-}] = 10^{-7} \text{ mol dm}^{-3}
$$
The product of these two concentrations is known as the ionization constant of water, $K\_{\text{W}}$ 
(or as the ionic product of water, or maybe sometimes as the autoprotolysis constant, $K\_{\text{AP}}$)
$$
K_{\text{W}} = [\ce{H3O+}][\ce{OH-}] = 10^{-14} \text{ mol}^2 \text{ dm}^{-6} \text{ at } 25~^\circ\text{C}
$$
This is a constant in aqueous solutions, albeit a very, very small one. 
This means that, if we know the hydronium ion concentration, we also know the hydroxide concentration and vice versa since the product of the two concentrations always equals $10^{-14}$.

**NOTE:** $\text{p}K\_{\text{w}} = -\log(K\_{\text{w}}) = \text{pH} + \text{pOH}$
$\text{pH} + \text{pOH} = 14$

---

# Arbitrary Acid or Base

> 🔴 For any acid and any base
$$
{\ce{AH + B <=> BH+ + A-}}
$$
where $\ce{AH}$ is an acid and $\ce{A-}$ is its conjugate base and $\ce{B}$ is a base and $\ce{BH+}$ is its conjugate acid, that is, *every acid has a conjugate base associated with it and every base has a conjugate acid associated with it.*

:::matrix{cols="50/50"}
[[0,0]]
![](./images/slide_13_img_25.png){width=70}
[[0,1]]
![](./images/slide_13_img_26.png){width=70}
:::

* Water can act both as acid and base
* We will always suppose water as a solvent (concentration much greater)
* $[\ce{H3O+}]$ and $[\ce{H+}]$ will be used interchangeably
* pH-meter measures concentration of $\ce{H+}$
* NOTE: $[\ce{H+}][\ce{OH-}] = 10^-14$

---

:::matrix{cols="50/50" gap="30px"}
[[0,0]]
# Example: Strong Acid

$$
\ce{HNO3 (aq) + H2O (l) -> H3O+ (aq) + NO3- (aq)}
$$
**Note:** Strong acid = complete ionization. 
So for every mole of the monoprotic acid we'll get mole of $\ce{H+}$ ions and a mole of conjugated base. 
Situation may be a bit more complicated for diprotic acids.


In a $0.20 \text{ M}$ solution of $\ce{HNO3 (aq)}$, $[\ce{H+}] = [\ce{NO3-}] = 0.20 \text{ M}$.


**Note:** we neglect autoionization of water, for pure water $[\ce{H+}] \sim 10^{-7} \text{ M}$. 
If the concentration of acid will be $10^{-6} \text{ M}$ or less, it would be preferable to consider water autoionization as well.
$$
\text{pH} = -\log\_{10}([\ce{H+}]) = -\log\_{10}(0.2) \approx 0.7
$$

[[0,1]]
# Example: Strong Base 
## (negligible acid)

$$
\ce{Ca(OH)2 (aq) -> Ca^2+(aq) + 2 OH- (aq)}
$$
**Note:** Strong base = complete ionization.
In a $0.0011 \text{ M}$ solution of $\ce{Ca(OH)2 (aq)}$, $[\ce{OH-}] = 2[\ce{Ca^2+}] = 0.0022 \text{ M}$.


**Note:** we neglect $\ce{OH-}$ from autoionization of water since for pure water $[\ce{OH-}] \sim 10^{-7} \text{ M}$. 
If the concentration of the base will be $10^{-6} \text{ M}$ or less, it would be preferable to consider water autoionization as well.

We suppose there is much more water $[\ce{H2O}] = 56 \text{ M}$, thus $[\ce{H+}][\ce{OH-}] = 10^{-14}$. 
So we have
$$
[\ce{H+}] = \frac{10^{-14}}{0.0022} = 4.55 \times 10^{-12}.
$$
As a result
$$
\text{pH} = -\log_{10}(4.55 \times 10^{-12}) \approx 11.34
$$
:::

---


# Buffers in Action

:::matrix{cols="70/30"}
[[0:2,0]]
* Most cases weak acid and a salt are used. 
* Most practical cases salt is considered as fully dissociated, $[\ce{H+}]$ from water and $[\ce{A-}]$ from acid neglected
![](./images/slide_26_img_46.png){width=90}
[[0,1]]
![](./images/slide_26_img_47.png){width=80}
[[1,1]]
![](./images/slide_26_img_48.png){width=150}
:::

---

# Notable buffers in human body

1. **Bicarbonate buffer** ($\ce{H2CO3 / HCO3-}$)
   * Most important extracellular buffer, especially in blood plasma.
   * Works with the lungs (exhaling $\ce{CO2}$) and kidneys (adjusting $\ce{HCO3-}$) for rapid and long-term control.
   * Maintains blood pH near 7.4.
2. **Phosphate buffer** ($\ce{H2PO4- / HPO4^2-}$)
   * Important in intracellular fluid and renal tubules.
   * Has a $\text{p}K_a \approx 6.8$, close to physiological pH, so it is effective inside cells.
3. **Protein buffer systems**
   * Proteins act as buffers via ionizable side chains (e.g., histidine imidazole group).
   * Very important inside cells and in plasma (albumin is a major buffer in blood).
4. **Hemoglobin buffer**
   * A subset of the protein buffer system but often mentioned separately.
   * Hemoglobin binds both protons ($\ce{H+}$) and $\ce{CO2}$ (as carbamino groups).
   * Works in tandem with the bicarbonate system (Bohr effect, Haldane effect).
   * Crucial for pH regulation during gas transport in blood.

---

# Briggs–Rauscher

## Inorganic chemical reactions may exhibit complicated dynamic behaviour

![youtube](oBGSMiHhdWw) {width="80%" left="10%"}

---

# Belousov-Zhabotinsky

## Inorganic chemical reactions may exhibit complicated dynamic behaviour

![youtube](XU2AV5SSi6g) {width="80%" left="10%"}
