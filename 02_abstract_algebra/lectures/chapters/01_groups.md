# Groups

A **group** $(G, \cdot)$ is a set $G$ with a binary operation satisfying:
1. **Closure**: $a \cdot b \in G$
2. **Associativity**: $(a \cdot b) \cdot c = a \cdot (b \cdot c)$
3. **Identity**: $\exists\\, e \in G$ such that $e \cdot a = a \cdot e = a$
4. **Inverse**: $\forall a \in G, \exists\\, a^{-1}$ such that $a \cdot a^{-1} = e$

If $a \cdot b = b \cdot a$ for all $a$, $b$, the group is **abelian** (commutative).

---

# $\mathbb{Z}_n$: Integers modulo $n$

The simplest group: $\{0, 1, \ldots, n-1\}$ under addition mod $n$.

:::matrix { cols="50/50" rows="100" height="85%"}

[[0, 0]]
![](./assets/z6_clock.png){height=80% center}

[[0, 1]]
**Properties:**
- Identity: $0$
- Inverse of $a$: $n - a$
- Always abelian
- Always **cyclic**: element $1$ generates everything
- $|\mathbb{Z}_n| = n$

**Example:** In $\mathbb{Z}_6$:

$3 + 5 = 8 \equiv 2 \pmod{6}$

$\text{inv}(4) = 6 - 4 = 2$

:::

---

# $U(n)$: the multiplicative group

$U(n) = \{a \in \mathbb{Z}_n \mid \gcd(a, n) = 1\}$ under multiplication mod $n$.

These are exactly the elements of $\mathbb{Z}_n$ that have multiplicative inverses.

![](./assets/un_comparison.png){width=80% center}


When $p$ is prime, $U(p) = \{1, 2, \ldots, p-1\}$ is always cyclic. A generator is called a **primitive root**.

This is the multiplicative group of the field $GF(p)$ — the starting point for all finite field constructions.

---

# Multiplication Tables (Cayley Tables)

A group's entire structure is captured by its multiplication table. Each row and column is a permutation of the elements (Latin square property).

:::matrix { cols="50/50" height="60%"}

[[0, 0]]
![](./assets/cayley_table_z4.png){height=85% center}

[[0, 1]]
![](./assets/cayley_table_u8.png){height=85% center}

:::

$\mathbb{Z}_4$: diagonal stripes — every element has a unique order. $U(8)$: every non-identity element squares to $1$ — no generator exists, so $U(8)$ is **not cyclic**. In fact, $U(8) \cong \mathbb{Z}_2 \times \mathbb{Z}_2$.

---

# Interactive: Multiplication Table Explorer

<iframe src="demos/multiplication_table.html" style="width: 100%; height: 62vh; border: 1px solid #30363d; border-radius: 8px;"></iframe>

---

# Cayley Graphs

Every group can be visualized as a directed graph. Given generators $S \subset G$:

- **Nodes** = group elements
- **Edges** = right-multiplication by a generator: $g \xrightarrow{s} g \cdot s$

:::matrix { cols="33/33/33" height="60%"}

[[0, 0]]
![](./assets/cayley_z6.png){height=90% center}

[[0, 1]]
![](./assets/cayley_d3.png){height=90% center}

[[0, 2]]
![](./assets/cayley_d4.png){height=90% center}

:::

The Cayley graph encodes the entire group structure: subgroups appear as sub-graphs, cosets as layers.

---

# Interactive: Cayley Graph Explorer

<iframe src="demos/cayley_explorer.html" style="width: 100%; height: 62vh; border: 1px solid #30363d; border-radius: 8px;"></iframe>

---

# Cyclic Groups & Generators

A group $G$ is **cyclic** if there exists $g \in G$ such that $G = \{g^0, g^1, g^2, \ldots, g^{n-1}\}$.

**Theorem:** Every finite cyclic group of order $n$ is isomorphic to $\mathbb{Z}_n$.

**Theorem (Primitive Root):** $U(p) \cong \mathbb{Z}_{p-1}$ for every prime $p$. In particular, there exists $\alpha \in U(p)$ such that $\alpha, \alpha^2, \ldots, \alpha^{p-1} = 1$ generates all nonzero elements.

**Why this matters:** In $GF(p^n)$, the multiplicative group $GF(p^n)^*$ is also cyclic of order $p^n - 1$. The generator $\alpha$ is a root of a **primitive polynomial** — this is the key to constructing extension fields.

---

# The Dihedral Group $D_n$

The symmetries of a regular $n$-gon form the **dihedral group** $D_n$ of order $2n$.

- **Rotations** $\{e, r, r^2, \ldots, r^{n-1}\}$ form a cyclic normal subgroup $\langle r \rangle \cong \mathbb{Z}_n$
- **Reflections** $\{s, sr, sr^2, \ldots, sr^{n-1}\}$ form a coset

**Key relation:** $srs^{-1} = r^{-1}$ — conjugating a rotation by a reflection *reverses* it. This is why $D_n$ is non-abelian for $n \geq 3$.

**Presentation:** $D_n = \langle\\, r, s \mid r^n = s^2 = e,\ srs = r^{-1}\\,\rangle$

**Semi-direct product:** $D_n \cong \mathbb{Z}_n \rtimes \mathbb{Z}_2$, where $\mathbb{Z}_2$ acts on $\mathbb{Z}_n$ by inversion. The "twist" distinguishes this from the direct product $\mathbb{Z}_n \times \mathbb{Z}_2$.

---

# Subgroups & Lagrange's Theorem

A **subgroup** $H \leq G$ is a subset closed under the group operation and inverses.

**Lagrange's Theorem:** If $H \leq G$ and $G$ is finite, then $|H|$ divides $|G|$.

The **index** $[G:H] = |G| / |H|$ counts the number of distinct cosets.

:::matrix { cols="50/50" height="65%"}

[[0, 0]]
![](./assets/coset_partition.png){height=90% center}

[[0, 1]]
**Left cosets** of $H$ in $G$:

$$gH = \{g \cdot h \mid h \in H\}$$

Cosets partition $G$ into blocks of equal size $|H|$. Two elements are in the same coset iff $g_1^{-1} g_2 \in H$.

**Example:** $H = \langle s \rangle = \{e, s\}$ in $D_3$.

$|D_3| = 6$, $|H| = 2$, so $[D_3 : H] = 3$ cosets.
:::

---

# Homomorphisms, Kernels, and Images

A **group homomorphism** $\phi: G \to H$ preserves structure: $\phi(ab) = \phi(a)\phi(b)$.

The **kernel** $\ker\phi = \{g \in G \mid \phi(g) = e_H\}$ measures "what gets collapsed."

The **image** $\mathrm{im}\\,\phi = \{\phi(g) \mid g \in G\}$ is what $G$ "looks like" inside $H$.

**Key facts:**
- $\ker\phi$ is always a normal subgroup of $G$
- $\mathrm{im}\\,\phi$ is always a subgroup of $H$
- $\phi$ is injective $\iff$ $\ker\phi = \{e\}$

**Example:** $\phi: \mathbb{Z} \to \mathbb{Z}_n$, $\phi(k) = k \bmod n$.
- $\ker\phi = n\mathbb{Z} = \{\ldots, -n, 0, n, 2n, \ldots\}$
- $\mathrm{im}\\,\phi = \mathbb{Z}_n$ (surjective)

---

# Normal Subgroups & Quotient Groups

A subgroup $H$ is **normal** ($H \trianglelefteq G$) if it is invariant under conjugation:

$$gHg^{-1} = H \quad \text{for all } g \in G$$

Equivalently: left cosets = right cosets, so $gH = Hg$.

**When $H$ is normal**, the set of cosets $G/H$ itself forms a group under $[g_1H] \cdot [g_2H] = [(g_1 g_2)H]$.

**Examples:**
- Every subgroup of an abelian group is normal
- The **center** $Z(G) = \{z \in G \mid zg = gz \ \forall g\}$ is always normal
- The **commutator subgroup** $[G,G] = \langle aba^{-1}b^{-1} \rangle$ is always normal
- $G/[G,G]$ is always abelian — the "abelianization" of $G$

---

# First Isomorphism Theorem

$$G / \ker\phi \\;\cong\\; \mathrm{im}\\,\phi$$

Every homomorphism $\phi: G \to H$ factors through the quotient by its kernel:

$$G \xrightarrow{\\;\pi\\;} G/\ker\phi \xrightarrow{\\;\bar{\phi}\\;} \mathrm{im}\\,\phi$$

where $\pi$ is the canonical projection and $\bar{\phi}$ is the induced isomorphism.

**Universal property of quotients:** $G/N$ is the "most general" group that $G$ maps to while collapsing $N$. Any $\phi: G \to H$ with $N \subseteq \ker\phi$ factors uniquely through $G/N$.

**Example:** $\phi: \mathbb{Z} \to \mathbb{Z}_6$, $k \mapsto k \bmod 6$.
- $\ker\phi = 6\mathbb{Z}$
- Theorem says: $\mathbb{Z}/6\mathbb{Z} \cong \mathbb{Z}_6$ ✓
- The quotient construction $\mathbb{Z}_n = \mathbb{Z}/n\mathbb{Z}$ is a *consequence*, not a definition.

---

# Product Groups & Classification

The **direct product** $G \times H$ has componentwise operations: $(g_1, h_1) \cdot (g_2, h_2) = (g_1 g_2, h_1 h_2)$.

**Key fact:** $\mathbb{Z}\_m \times \mathbb{Z}\_n \cong \mathbb{Z}\_{mn}$ if and only if $\gcd(m, n) = 1$.

So $\mathbb{Z}\_2 \times \mathbb{Z}\_3 \cong \mathbb{Z}\_6$, but $\mathbb{Z}\_2 \times \mathbb{Z}\_2 \ncong \mathbb{Z}\_4$ (every element of $\mathbb{Z}\_2 \times \mathbb{Z}\_2$ has order $\leq 2$).

**Fundamental Theorem of Finite Abelian Groups:** Every finite abelian group is isomorphic to a direct product of cyclic groups of prime-power order:

$$G \cong \mathbb{Z}\_{p\_1^{a\_1}} \times \mathbb{Z}\_{p\_2^{a\_2}} \times \cdots \times \mathbb{Z}\_{p\_k^{a\_k}}$$

This decomposition is unique (up to reordering). Finite abelian groups are completely classified.

---

# Free Groups & Presentations

The **free group** $F(S)$ on generators $S$ is the universal group: every function $f: S \to G$ to any group $G$ extends uniquely to a homomorphism $\bar{f}: F(S) \to G$.

$$S \xhookrightarrow{\\;\iota\\;} F(S) \xrightarrow{\\;\bar{f}\\;} G$$

Elements of $F(S)$ are reduced words in the generators and their formal inverses.

A **group presentation** $\langle S \mid R \rangle = F(S) / \langle\langle R \rangle\rangle$ — quotient by the normal closure of the relations:

$$D_4 = \langle\\, r, s \mid r^4 = s^2 = e,\ srs = r^{-1}\\,\rangle$$

This is exactly what you type into the warm-up problem dashboard. The SymPy engine solves the word problem via the Todd-Coxeter coset enumeration algorithm.

---

# Python: Modular Arithmetic Essentials

The tools you'll need for the practice problems:

```python
# Modular arithmetic is native in Python
7 % 5           # → 2
(-3) % 5        # → 2  (Python always returns non-negative)

# Modular inverse: pow(a, -1, n) — requires gcd(a,n) = 1
pow(3, -1, 7)   # → 5, because 3 * 5 = 15 ≡ 1 (mod 7)

# Modular exponentiation: pow(base, exp, mod)
pow(2, 10, 1000)  # → 24, fast even for huge exponents

# Testing if g is a primitive root of U(p):
g, p = 3, 7
{pow(g, k, p) for k in range(1, p)}  # → {1, 2, 3, 4, 5, 6} = all of U(7) ✓
```

Python's built-in `pow` with three arguments uses fast modular exponentiation — $O(\log n)$ multiplications. This is the same algorithm behind RSA.
