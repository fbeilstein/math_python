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
