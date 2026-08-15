:::titlepage
[[title]]
Chapter 3: Enzyme Kinetics & Inhibition
:::

---

# Michaelis–Menten model

:::matrix {cols="50/50"}
[[0,0]]
The **Michaelis–Menten** model accounts for the kinetic properties of many enzymes
$$
E + S \underset{k_{-1}}{\overset{k_1}{\rightleftharpoons}} ES \underset{k_{-2}}{\overset{k_2}{\rightleftharpoons}} E + P,
$$
at times close to zero (hence, $V_0$) when there is negligible product formation and thus no back reaction
$$
k_{-2} [E][P] \approx 0.
$$
Thus we get a system of differential equations that describe the process
$$
\begin{aligned} 
\frac{d[E]}{dt} &= -k_1[E][S] + k_{-1}[ES] + k_2[ES], \\\\ 
\frac{d[S]}{dt} &= -k_1[E][S] + k_{-1}[ES], \\\\ 
\frac{d[ES]}{dt} &= k_1[E][S] - k_{-1}[ES] - k_2[ES], \\\\ 
\frac{d[P]}{dt} &= k_2[ES]. 
\end{aligned}
$$

[[0,1]]
**Assumption:** The total enzyme concentration remains constant, meaning that free enzyme plus enzyme bound in the enzyme–substrate complex is conserved
$$
[E]\_{\text{tot}} = [E] + [ES],
$$
where $[E]_{\text{tot}}$ is the total enzyme concentration during the reaction.


**Assumption (Briggs-Haldane):** It is assumed that the concentration of the enzyme--substrate complex remains approximately constant during the reaction:
$$
0 = \frac{d[ES]}{dt} = k_1[E][S] - (k_{-1} + k_2)[ES].
$$
From the above relations, the reaction velocity $V$ is:
$$
V\_0 = \frac{d[P]}{dt} = k\_2[ES] = \frac{k\_2 [E]\_{\text{tot}}[S]}{\dfrac{k\_{-1} + k\_2}{k\_1} + [S]}.
$$
:::

---

# Michaelis constant

:::matrix {cols="50/50"}
[[0,0]]
$$
K_M = \frac{k_{-1} + k_2}{k_1}.
$$
At very high substrate concentration, essentially all enzyme is bound:
$$
[ES] \approx [E]\_{\text{tot}}.
$$
Thus the maximum velocity is:
$$
V\_{\text{max}} = k\_2 [E]\_{\text{tot}}.
$$
Finally, the **Michaelis-Menten equation** is obtained:
$$
V\_0 = \frac{V\_{\text{max}}[S]}{K\_M + [S]}.
$$

[[0,1]]
![](./images/enzyme_kinetics/slide_77_img_140.png) {width="100%"}

:::

---

# The significance of $K_M$

$$
V\_0 = \frac{V\_{\text{max}}[S]}{K\_M + [S]}.
$$
The significance of $K_M$ is clear when we set $[S] = K\_M$: $V = v\_{\text{max}} / 2$, thus, $K\_M$ is equal to the substrate concentration at which the reaction rate is half its maximal value.

## Example

$$
\ce{\underset{\text{Ethanol}}{CH3CH2OH} + NAD+ 
<=>[\substack{ \textcolor{#2b8cb8}{\text{Alcohol}} \\\\ \textcolor{#2b8cb8}{\text{dehydrogenase}} }] 
\underset{\text{Acetaldehyde}}{CH3CHO} + NADH + H+}
$$
$$
\ce{CH3CHO + NAD+ + H2O 
<=>[\substack{ \textcolor{#2b8cb8}{\text{Aldehyde}} \\\\ \textcolor{#2b8cb8}{\text{dehydrogenase}} }]
\underset{\text{Acetate}}{CH3COO-} + NADH + 2H+}
$$

Most people have two forms of the aldehyde dehydrogenase, a low $K\_M$ mitochondrial form and a high $K\_M$ cytoplasmic form. 
In susceptible persons, the mitochondrial enzyme is less active owing to the substitution of a single amino acid (ALDH2 gene, is a common trait in East Asian people), and acetaldehyde is processed only by the cytoplasmic enzyme. 
Because this enzyme has a high $K_M$, it achieves a high rate of catalysis only at very high concentrations of acetaldehyde. 
Consequently, less acetaldehyde is converted into acetate; excess acetaldehyde escapes into the blood and accounts for the physiological effects: facial flushing and rapid heart rate (tachycardia) after ingesting even small amounts of alcohol.

---

# A double-reciprocal or Lineweaver–Burk equation

:::matrix {cols="50/50"}
[[0,0]]
$$
\frac{1}{V\_0} = \frac{K\_M}{V\_{\text{max}}} \cdot \frac{1}{[S]} + \frac{1}{V\_{\text{max}}}.
$$
[[0,1]]
For many enzymes, experimental evidence suggests that the $K\_M$ value provides an approximation of the substrate concentration in vivo
[[1,0]] {.dense}
$K_{\text{M}}$ values of some enzymes
| Enzyme | Substrate | $K_{\text{M}}$ (μM) |
| --- | --- | --- |
| Chymotrypsin | Acetyl-L-tryptophanamide | 5000 |
| Lysozyme | Hexa-$N$-acetylglucosamine | 6 |
| $\beta$-Galactosidase | Lactose | 4000 |
| Threonine deaminase | Threonine | 5000 |
| Carbonic anhydrase | $\ce{CO2}$ | 8000 |
| Penicillinase | Benzylpenicillin | 50 |
| Pyruvate carboxylase | Pyruvate | 400 |
|  | $\ce{HCO3^-}$ | 1000 |
|  | ATP | 60 |
| Arginine-tRNA synthetase | Arginine | 3 |
|  | tRNA | 0.4 |
|  | ATP | 300 |
[[1,1]]
![](./images/enzyme_kinetics/slide_79_img_145.png) {height="100%"}
[[2,0:2]]
The $K\_M$ values of enzymes range widely. 
For most enzymes, $K\_M$ lies between $10^{-1}$ and $10^{-7}$ M. 
The $K\_M$ value for an enzyme depends on the particular substrate and on environmental conditions such as pH, temperature, and ionic strength.


<button class="demo-btn" onclick="showDemo('https://learncheme.github.io/demos/EnzymeInhibitionKinetics/index.html')">
    Launch 3rd Party Demo
</button>
::: 

---

# Kinetic Inhibition Mechanisms

:::matrix {cols="25/25/50"}
[[0,0]]
![](./images/enzyme_kinetics/slide_81_img_150.png) {width="90%"}
[[0,1]]
$$
\ce{E + S <=>[$k_1$][$k_{-1}$] ES <=>[$k_2$][$k_{-2}$] E + P}
$$
[[1,0:2]]
No inhibition, pure Michaelis-Menten kinetics
[[0:2,2]]
![](./images/enzyme_kinetics/slide_81_img_152.png) {width="60%"}
[[2,2]]
![](./images/enzyme_kinetics/slide_81_img_153.png) {width="60%"}
[[2,0:2]]
$$
V\_0 = \frac{V\_{\text{max}}[S]}{K\_M + [S]}. \qquad 
\frac{1}{V\_0} = \frac{K\_M}{V\_{\text{max}}} \cdot \frac{1}{[S]} + \frac{1}{V\_{\text{max}}}.
$$
**Inhibition**:
* **Irreversible** (dissociates very slowly from its target enzyme; tightly bound either covalently or noncovalently)
* **Reversible** (rapid dissociation)
   - competitive, 
   - noncompetitive, 
   - uncompetitive.

:::
---

# Competitive Inhibitor

:::matrix {cols="25/25/50"}
[[0,0]]
![](./images/enzyme_kinetics/slide_82_img_157.png) {width="90%"}
[[0,1]]
![](./images/enzyme_kinetics/slide_82_img_159.png) {width="90%"}
[[1,0:2]]
A **competitive inhibitor** binds at the active site and thus prevents the substrate from binding;
[[0:2,2]]
![](./images/enzyme_kinetics/slide_82_img_156.png) {width="60%"}
[[2,2]]
![](./images/enzyme_kinetics/slide_82_img_160.png) {width="60%"}
[[2,0:2]]
$$
K\_i = [\text{E}][\text{I}]/[\text{EI}] \qquad 
K\_{\text{M}}^{\text{app}} = K\_{\text{M}}(1 + [\text{I}]/K\_i)
$$
$$
\frac{1}{V\_0} = \frac{1}{V\_{\text{max}}} + \frac{K\_{\text{M}}}{V\_{\text{max}}} \left( 1 + \frac{[\text{I}]}{K\_i} \right) \left( \frac{1}{[\text{S}]} \right)
$$

The effect of a competitive inhibitor is to increase the apparent value of $K\_M$
:::


---


# Uncompetitive Inhibitor

:::matrix {cols="25/25/50"}
[[0,0]]
![](./images/enzyme_kinetics/slide_83_img_163.png) {width="90%"}
[[0,1]]
![](./images/enzyme_kinetics/slide_83_img_164.png) {width="90%"}
[[1,0:2]]
In **uncompetitive inhibition**, the inhibitor binds only to the ES complex.
[[0:2,2]]
![](./images/enzyme_kinetics/slide_83_img_165.png) {width="50%"}
[[2,2]]
![](./images/enzyme_kinetics/slide_83_img_166.png) {width="50%"}
[[2,0:2]]
$$
\frac{1}{V\_0} = \frac{K\_{\text{M}}}{V\_{\text{max}}} \frac{1}{[\text{S}]} + \frac{1}{V\_{\text{max}}} \left( 1 + \frac{[\text{I}]}{K\_{\text{i}}} \right)
$$
ESI, does not go on to form any product. Lowers $V\_\text{max}$ and $K\_M$ because unproductive ESI depletes ES

:::

---

# Noncompetitive Inhibitor

:::matrix {cols="25/25/50"}
[[0,0]]
![](./images/enzyme_kinetics/slide_84_img_168.png) {width="90%"}
[[0,1]]
![](./images/enzyme_kinetics/slide_84_img_169.png) {width="90%"}
[[1,0:2]]
In **noncompetitive inhibition**, the inhibitor can bind to E or to ES complex.
[[0:2,2]]
![](./images/enzyme_kinetics/slide_84_img_170.png) {width="50%"}
[[2,2]]
![](./images/enzyme_kinetics/slide_84_img_171.png) {width="50%"}
[[2,0:2]]
$$
V\_{\text{max}}^{\text{app}} = \frac{V\_{\text{max}}}{1 + [\text{I}]/K\_{\text{i}}}
$$
However, the ESI does not proceed to form product. In pure
noncompetitive inhibition, the $K\_i$ for the inhibitor binding to E is the same as for binding to ES complex. 
The value of $V\_{\text{max}}$ is decreased to a new value called $V\_{\text{max}}^{\text{app}}$, whereas the value of $K\_M$ is unchanged.
:::

---

<div class="matrix-cell dense">

| Drug (example) | Inhibition type/class | Mechanism of action / Notes |
| --- | --- | --- |
| Aspirin (acetylsalicylic acid) | Irreversible (covalent) | Acetylates a serine residue in cyclooxygenase (COX-1/2) → blocks prostaglandin & thromboxane synthesis. |
| Penicillin | Irreversible (suicide substrate) | β-lactam ring covalently binds to transpeptidase (DD-peptidase), blocking bacterial cell wall crosslinking. |
| Methotrexate | Competitive | Competes with folate at dihydrofolate reductase (DHFR) active site → inhibits nucleotide synthesis. |
| Allopurinol | Suicide inhibitor | Converted to oxypurinol, which binds tightly to xanthine oxidase → lowers uric acid (used in gout). |
| Statins (e.g. atorvastatin) | Competitive | Resemble HMG-CoA; block HMG-CoA reductase → reduce cholesterol synthesis. |
| ACE inhibitors (e.g. captopril) | Competitive | Mimic angiotensin I substrate; inhibit angiotensin-converting enzyme (ACE) → lower blood pressure. |
| Physostigmine | Reversible covalent (carbamate) | Carbamoylates acetylcholinesterase → prolongs acetylcholine action at synapses. |
| Organophosphates (e.g. sarin, malathion) | Irreversible | Phosphorylate active-site serine in acetylcholinesterase → accumulation of acetylcholine (toxic). |
| Disulfiram | Irreversible | Inhibits aldehyde dehydrogenase → acetaldehyde buildup after alcohol intake (used in alcoholism therapy). |
| Sulfonamides | Competitive (antimetabolite) | Mimic PABA → inhibit dihydropteroate synthase in bacteria, blocking folate synthesis. |
| Memantine | Uncompetitive (open-channel blocker) | Used in Alzheimer's. Binds inside the NMDA receptor channel only when it's open → prevents excessive Ca²⁺ influx without fully blocking normal activity. |
| Ketamine | Noncompetitive (allosteric/open-channel block) | NMDA receptor antagonist; binds to a site distinct from glutamate → anesthetic and antidepressant effects. |
| Theophylline (and caffeine) | Noncompetitive / allosteric | Inhibit phosphodiesterase (PDE) → increase cAMP levels; also antagonize adenosine receptors. |
| NNRTIs (e.g., efavirenz, nevirapine) | Noncompetitive (allosteric) | Bind to a hydrophobic pocket on HIV reverse transcriptase distinct from the active site → distort the enzyme and block activity. |
| Foscarnet | Noncompetitive | Antiviral; binds to the pyrophosphate binding site of viral DNA polymerase → prevents cleavage of pyrophosphate from dNTPs. |

</div>

---

# Allosteric enzymes do not obey Michaelis–Menten kinetics

:::matrix {cols="50/50"}
[[0:2,0]]
An important group of enzymes that do not obey Michaelis–Menten kinetics are the **allosteric enzymes**. 
These enzymes consist of multiple subunits and multiple active sites. 


Allosteric enzymes often display **sigmoidal plots** of the reaction velocity $V\_0$ versus substrate concentration $[S]$. 
In allosteric enzymes, the binding of substrate to one active site can alter the properties of other active sites in the same enzyme molecule. 
A possible outcome of this interaction between subunits is that the binding of substrate becomes cooperative; that is, the binding of substrate to one active site facilitates the binding of substrate to the other active sites. 


In addition, the activity of an allosteric enzyme may be altered by regulatory molecules that reversibly bind to specific sites other than the catalytic sites. 
The catalytic properties of allosteric enzymes can thus be adjusted to meet the immediate needs of a cell. 
For this reason, allosteric enzymes are key regulators of metabolic pathways.
[[0,1]]
![](./images/enzyme_kinetics/slide_80_img_148.png) {width="50%"}
[[1,1]]
![](./images/enzyme_kinetics/slide_80_img_149.png) {width="50%"}
:::

<div style="position: absolute; left: 75%; top: 30%;">
allosteric
</div>

<div style="position: absolute; left: 75%; top: 70%;">
Michaelis-Menten
</div>

---
# Allosteric Effects and Hill equation

:::matrix {cols="60/40"}
[[0,0]]
## Michaelis–Menten Kinetics

$$
v\_0 = \frac{d[P]}{dt} = k\_2[ES] = \frac{k\_2[E]\_{\text{tot}}[S]}{K\_M + [S]}
\qquad\text{thus}\qquad
[ES] = \frac{[E]\_{\text{tot}}[S]}{K\_M + [S]}.
$$

## Hill Kinetics 

Describes allosteric effects (note: designations in Wikipedia and etc are different)
$$
\frac{[ES]}{[E]\_{\text{tot}}} = \frac{[S]^n}{K\_A^n + [S]^n}.
$$
[[0,1]]
## The Bohr Effect (haemoglobin)
![](./images/enzyme_kinetics/slide_93_img_177.png?v=1) {width="80%"}
[[1,0:2]]
* $n > 1$ **Positively cooperative binding:** Once one ligand molecule is bound to the enzyme, its affinity for other ligand molecules increases. For example, the Hill coefficient of oxygen binding to haemoglobin (an example of positive cooperativity) falls within the range of 1.7–3.2.
* $n < 1$ **Negatively cooperative binding:** Once one ligand molecule is bound to the enzyme, its affinity for other ligand molecules decreases.
* $n = 1$ **Noncooperative (completely independent) binding:** The affinity of the enzyme for a ligand molecule is not dependent on whether or not other ligand molecules are already bound. When $n = 1$, we obtain a model that can be modeled by Michaelis–Menten kinetics in which $K\_A = K\_M$ the Michaelis–Menten constant.
:::

---

# Activity regulation

**1. Allosteric Control.** Allosteric proteins contain distinct regulatory sites and multiple functional sites. The binding of small signal molecules at regulatory sites controls the activity of these proteins. Moreover, allosteric proteins show the property of cooperativity: activity at one functional site affects the activity at others. 

**2. Multiple Forms of Enzymes.** **Isozymes**, or **isoenzymes** are homologous enzymes within a single organism that catalyze the same reaction but differ slightly in structure and more obviously in $K\_M$ and $V\_\text{max}$ values as well as in regulatory properties. Often, isozymes are expressed in a distinct tissue or organelle or at a distinct stage of development.

**3. Reversible Covalent Modification.** The catalytic properties of many enzymes are markedly altered by the covalent attachment of a modifying group, commonly a phosphoryl group. 

**4. Proteolytic Activation.** A different regulatory strategy is used to irreversibly convert an inactive enzyme into an active one. Many enzymes are activated by the hydrolysis of a few peptide bonds or even one such bond in inactive precursors called **zymogens** or **proenzymes**. 

**5. Controlling the Amount of Enzyme Present.** This important form of regulation usually takes place at the level of **transcription**.


---

# Biochemical systems theory, BST

**For curious mind**:
* Mogilner, Alex, Roy Wollman, and Wallace F. Marshall. "Quantitative modeling in cell biology: what is it good for?." Developmental cell 11, no. 3 (2006): 279-287.
* Igoshin, Oleg A., Albert Goldbeter, Dale Kaiser, and George Oster. "A biochemical oscillator explains several aspects of Myxococcus xanthus behavior during development." Proceedings of the National Academy of Sciences 101, no. 44 (2004): 15760-15765.
* Bier, Martin, Barbara M. Bakker, and Hans V. Westerhoff. "How yeast cells synchronize their glycolytic oscillations: a perturbation analytic treatment." Biophysical Journal 78, no. 3 (2000): 1087-1093.
* Tyson, John J., Katherine C. Chen, and Bela Novak. "Sniffers, buzzers, toggles and blinkers: dynamics of regulatory and signaling pathways in the cell." Current opinion in cell biology 15, no. 2 (2003): 221-231.

<iframe src="./demos/bio_switch.html" width="100%" height="400px" style="border: none;"></iframe>

---


# Briggs–Rauscher

## Inorganic chemical reactions may exhibit complicated dynamic behaviour as well.

![youtube](oBGSMiHhdWw) {width="80%" left="10%"}

---

# Belousov-Zhabotinsky

## Inorganic chemical reactions may exhibit complicated dynamic behaviour as well.

![youtube](XU2AV5SSi6g) {width="80%" left="10%"}
