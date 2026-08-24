:::titlepage
[[title]]
Chapter 6: Metabolism & Signaling
:::

---

# And Much More is Not Known

![](./images/metabolism/slide_2_img_1.png)

---

# General Principles of Metabolism

1. Fuels are degraded and large molecules are constructed step by step in a series of linked reactions called metabolic pathways .
2. An energy currency common to all life forms, adenosine triphosphate (ATP), links energy-releasing pathways with energy-requiring pathways.
3. The oxidation of carbon fuels powers the formation of ATP.
4. Although there are many metabolic pathways, a limited number of types of reactions and particular intermediates are common to many pathways.
5. Metabolic pathways are highly regulated.

## Links to atlases:

- <a>https://pathways.embl.de/ipath3.cgi</a>
- <a>https://smpdb.ca/view</a>
- <a>https://reactome.org/PathwayBrowser/</a>

---

# Bioenetgetics

![](./images/metabolism/slide_14_img_18.png){height=100}

---

# Glucose Transporters

:::matrix{cols="50/50"}
[[0,0]]
![](./images/metabolism/slide_18_img_20.png){width=90}
[[0,1]]
* Low $K_m$ $\rightarrow$ efficient uptake even at low glucose concentrations.
  GLUT1 & GLUT3 $\rightarrow$ neurons and RBCs always get glucose, even when blood glucose is low.
* High $K_m$ $\rightarrow$ the transporter needs a higher concentration of glucose to work efficiently.
  GLUT2 $\rightarrow$ pancreas & liver only become active transporters when glucose is abundant, making them ideal "sensors" of post-meal glucose spikes.
:::

<div class="dense-table">

| Transporter | Tissue Distribution | Affinity ($K_m$) | Key Role | Notes |
| --- | --- | --- | --- | --- |
| **GLUT1** | Most tissues, esp. RBCs, blood–brain barrier | Low $K_m$ (~$1--2$ mM, **high affinity**) | Basal glucose uptake | Ensures constant supply, esp. to brain & erythrocytes |
| **GLUT2** | Liver, pancreatic $\beta$-cells, kidney, small intestine | High $K_m$ (~$15--20$ mM, **low affinity**) | Glucose sensing & bidirectional transport | Important for insulin secretion and hepatic glucose balance |
| **GLUT3** | Neurons, placenta | Very low $K_m$ (~$1$ mM, **very high affinity**) | Glucose uptake in neurons | Supports constant supply even at low [glucose] |
| **GLUT4** | Skeletal muscle, adipose tissue, heart | **Moderate** $K_m$ (~$5$ mM) | Insulin-responsive glucose uptake (only this one!) | Stored in vesicles; moves to plasma membrane after insulin stimulation |
| **GLUT5** | Small intestine (enterocytes), sperm | Not for glucose – **fructose transporter** ($K_m$ ~$10$ mM) | Dietary fructose absorption | Distinct from other GLUTs |

</div>

---

# Glycolysis

![](./images/metabolism/glycolysis.png)

---

# Regulation of Glycolysis

:::matrix{cols="25/25/50"}
[[0,0:2]]{.dense}
The regulatory enzymes or key enzymes of glycolysis are:
1. Glucokinase/Hexokinase, step 1
2. Phosphofructokinase, step 3. 
3. Pyruvate kinase, step 9

| Enzyme | Activation | Inhibition |
| --- | --- | --- |
| **HK** |  | G-6-P |
| **GK** | Insulin | Glucagon |
| **PFK** | Insulin, AMP<br>F-6-P, PFK-2<br>F2,6-BP | Glucagon, ATP<br>Citrate, Low pH<br>Cyclic AMP |
| **PK** | Insulin, F1,6-BP | Glucagon, ATP<br>Cyclic AMP |
| **PDH** | CoA, NAD | Acetyl CoA, NADH |
[[0:2,2]]
![](./images/metabolism/slide_48_img_70.png){width="70"}
[[1,0]]
![](./images/metabolism/slide_48_img_71.png)
[[1,1]]
![](./images/metabolism/slide_48_img_72.png)
:::

---

# Activity Regulation

:::matrix{cols="50/50"}
[[0,0]]
* **Protein kinases** (PKs) add phosphate groups to specific residues of target proteins, while **protein phosphatases** remove phosphate groups from these residues.
* The catalytic activity of all kinases is highly regulated; commonly it is modulated by the binding of other proteins to the kinase and by changes in the concentrations of various small intracellular signaling molecules and metabolites.
[[0,1]] 
![](./lecture_08_molecular_signaling/images/slide_14_img_12.png)
:::

---

# No Cell Lives in Isolation

* Many cells sense physical stimuli: mechanical pressure (touch), heat, light, variety of environmental chemicals, including nutrients such as sugars and amino acids as well as oxygen, toxic compounds, and diverse molecules that convey taste (tastants) and odor (odorants), levels of oxygen, etc.
* Many types of cells release particular chemicals that can influence the behavior of another cell; these are often called **extracellular** signaling molecules, or simply **signals**. 
You can think about signals in the brain or hormones.
* In the vertebrate eye, light is transmitted through the transparent corneal tissue and focused by the lens tissue, eventually impinging on the neural retina. 
The precise arrangement of tissues in the eye cannot be disturbed without impairing its function. 
Such coordination in the construction of the lens and retina is accomplished by one group of cells communicating an organizing change in the behavior or developmental trajectory of an adjacent set of cells. This kind of interaction is known as an **induction**.
* The cell that receives a signal — termed the **target cell** — must be able to detect the signaling molecule. 
Typically, the signaling molecule binds noncovalently to a specific protein in the cell, typically called the **receptor**, that contains a binding site for the signaling molecule. 
The signaling molecule that binds a receptor is often called the **ligand** of the receptor. 
Receptors bind a single type of molecule or a group of closely related molecules.
* The release and reception of such signals is a fundamental process, known as **cellular communication**, that shapes the development and function of every living organism.

---

# Generalized signal transduction pathway

![](./lecture_08_molecular_signaling/images/slide_5_img_1.png){width=100}


**Generalized signal transduction pathway.** 
The series of steps leading from initial detection to the final **response** is termed a **signal transduction pathway**. 
Signal transduction pathways ultimately lead to activation (or in some cases inhibition) of one or more **effector proteins** — often enzymes or transcription factors or cytoskeletal proteins — that lead directly to changes in cellular activities

---

# Receptor Kinetics

:::matrix{cols="50/50"}
[[0,0]]
$$
\mathrm{R} + \mathrm{L} \overset{k\_{\mathrm{off}}}{\underset{k\_{\mathrm{on}}}{\leftrightharpoons}} \mathrm{R} * \mathrm{L}
$$
$$
[\mathrm{R}][\mathrm{L}] k\_{\mathrm{on}} = [\mathrm{R} * \mathrm{L}] k\_{\mathrm{off}}
$$
$$
K_{\mathrm{d}} = \frac{[\mathrm{R}][\mathrm{L}]}{[\mathrm{R} * \mathrm{L}]}
$$

* Resembles Michaelis-Menten kinetics (think why).
* $K_d$ (**dissociation constant**) is  the lower the ligand concentration required to bind $50\%$ of the cell-surface receptors.
* Example (to feel the numbers): $K_d$ for insulin in liver $1.4\times 10^{-10} \text{M}$. 
The normal concentration of insulin in the blood is about $5\times 10^{-12} \text{M}$. 
After the meal $2.5\times 10^{-11} \text{M}$.
[[0,1]]
![](./lecture_08_molecular_signaling/images/slide_17_img_18.png){width=100}
:::

---

# Receptor Types

![](./lecture_08_molecular_signaling/images/slide_28_img_39.png){width=100}

---
# The Four Main Types of Receptor

:::matrix{cols="25/25/25/25"}
[[0,0:4]]

|  | Type 1: ligand-gated ion channels | Type 2: G-protein-coupled receptors | Type 3: receptor kinases | Type 4: nuclear receptors |
| --- | --- | --- | --- | --- |
| Location | Membrane | Membrane | Membrane | Intracellular |
| Effector | Ion channel | Channel or enzyme | Protein kinases | Gene transcription |
| Coupling | Direct | G-protein | Direct | Via DNA |
| Examples | Nicotinic acetylcholine receptor, GABAA receptor | Muscarinic acetylcholine receptor, adrenoceptors | Insulin, growth factors, cytokine receptors | Steroid receptors |
| Structure | Oligomeric assembly of subunits surrounding central pore | Monomeric or oligomeric assembly of subunits comprising seven transmembrane helices with intracellular G-protein-coupling domain | Single transmembrane helix linking extracellular receptor domain to intracellular kinase domain | Monomeric structure with separate receptor- and DNA-binding domains |

[[1,0]]
![](./lecture_08_molecular_signaling/images/slide_29_img_41.png)
[[1,1]]
![](./lecture_08_molecular_signaling/images/slide_29_img_42.png)
[[1,2]]
![](./lecture_08_molecular_signaling/images/slide_29_img_43.png)
[[1,3]]
![](./lecture_08_molecular_signaling/images/slide_29_img_44.png)
:::

---

# Signal Transduction

**Receptor signals are transduced inside the cell in one of three ways to initiate actions inside the cell:**

1. Exchange of GDP for GTP by GTP-binding proteins (G proteins) on the cytoplasmic side of the plasma membrane, which leads to generation of second messengers, including cAMP, phospholipid breakdown products, and Ca2+.
2. Receptor-mediated activation of phosphorylation cascades that in turn trigger activation of various enzymes. This is the action of the receptor tyrosine kinases. Protein kinases and protein phosphatases act as
effectors.
3. Conformation changes that open ion channels or recruit proteins into nuclear transcription complexes.




