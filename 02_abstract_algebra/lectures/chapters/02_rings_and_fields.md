# From Groups to Rings

A **ring** $(R, +, \cdot)$ has two operations:
- $(R, +)$ is an abelian group
- $\cdot$ is associative and distributes over $+$

A **field** is a ring where $(R \setminus \{0\}, \cdot)$ is also a group (every nonzero element has a multiplicative inverse).

| Structure | Addition | Multiplication | Example |
|-----------|----------|----------------|---------|
| Group | ✓ | — | $(\mathbb{Z}_n, +)$ |
| Ring | ✓ (abelian group) | ✓ (associative, distributive) | $\mathbb{Z}_n$, $\mathbb{Z}[x]$ |
| Field | ✓ | ✓ (inverses exist) | $\mathbb{Q}$, $\mathbb{R}$, $GF(p)$ |

---

# Zero Divisors: Why Primes Matter

In $\mathbb{Z}_6$: $2 \cdot 3 \equiv 0$. Two nonzero elements multiply to zero.

This breaks everything: if $ab = 0$ and $a \neq 0$, we can't "divide by $a$" — the cancellation law fails.

:::matrix { cols="50/50" height="65%"}

[[0, 0]]
![](./assets/cayley_table_z6_mul.png){height=85% center}

[[0, 1]]
![](./assets/cayley_table_z5_mul.png){height=85% center}

:::

$\mathbb{Z}_6$: zeros appear in the table body (zero divisors). $\mathbb{Z}_5$: every row is a permutation of $\{0,1,2,3,4\}$ — no zero divisors. **$\mathbb{Z}_n$ is a field $\iff$ $n$ is prime.**

---

# Ideals & Quotient Rings

An **ideal** $I \subseteq R$ is a subgroup of $(R, +)$ that absorbs multiplication: $r \cdot I \subseteq I$ for all $r \in R$.

The **quotient ring** $R/I$ has elements $\{a + I\}$ with operations $(a+I) + (b+I) = (a+b)+I$ and $(a+I)(b+I) = ab + I$.

**Example:** $\mathbb{Z}/n\mathbb{Z} \cong \mathbb{Z}_n$, where $I = \langle n \rangle = n\mathbb{Z}$.

**Universal property:** Any ring homomorphism $\phi: R \to S$ with $I \subseteq \ker\phi$ factors uniquely through $R/I$:

$$R \xrightarrow{\\;\pi\\;} R/I \xrightarrow{\\;\bar{\phi}\\;} S$$

Same diagram as for groups — the universal property is a *pattern* that repeats across algebraic structures.

---

# Polynomial Rings & Their Universal Property

Polynomials with coefficients in a ring $R$ form the polynomial ring $R[x]$.

**Universal property:** $R[x]$ is the **free commutative $R$-algebra on one generator**. Any ring homomorphism $\phi: R \to S$ and any choice of element $s \in S$ extends uniquely to $\bar{\phi}: R[x] \to S$ via $x \mapsto s$:

$$R[x] \xrightarrow{\\;\bar{\phi}\\;} S, \qquad f(x) \mapsto f(s)$$

**Consequence:** $GF(p)[x] / \langle P(x) \rangle$ is the smallest ring containing $GF(p)$ and a root of $P(x)$.

When $P(x)$ is irreducible, this quotient is a **field** — and that's exactly how we construct $GF(p^n)$.

---

# Polynomial Division over $GF(p)$

**Division Algorithm:** For any $f(x), g(x) \in GF(p)[x]$ with $g \neq 0$, there exist unique $q(x), r(x)$ such that:

$$f(x) = q(x) \cdot g(x) + r(x), \quad \deg r < \deg g$$

**Worked Example** in $GF(3)$: divide $f = 2x^2 + 1$ by $g = x + 2$.

| Step | Operation | Result |
|------|-----------|--------|
| 1 | $2x^2 \div x = 2x$ | First quotient term |
| 2 | $2x \cdot (x+2) = 2x^2 + 4x \equiv 2x^2 + x$ | Subtract |
| 3 | $(2x^2+1)-(2x^2+x) = -x+1 \equiv 2x+1$ | New remainder |
| 4 | $2x \div x = 2$ | Second quotient term |
| 5 | $2(x+2) = 2x+4 \equiv 2x+1$ | Subtract |
| 6 | $(2x+1)-(2x+1) = 0$ | Done |

**Result:** $q(x) = 2x + 2$, $r(x) = 0$. So $(x+2) \mid (2x^2+1)$ in $GF(3)$.

---

# Interactive: Polynomial Calculator over $GF(p)$

<iframe src="demos/poly_calculator.html" style="width: 100%; height: 62vh; border: 1px solid #30363d; border-radius: 8px;"></iframe>

---

# Irreducible Polynomials

A polynomial $p(x) \in GF(p)[x]$ is **irreducible** if it cannot be factored into polynomials of lower degree over $GF(p)$.

**Analogy:** Irreducible polynomials are to $GF(p)[x]$ what primes are to $\mathbb{Z}$.

| $\mathbb{Z}$ | $GF(p)[x]$ |
|----|-----|
| Prime number $p$ | Irreducible polynomial $p(x)$ |
| $\mathbb{Z}/p\mathbb{Z} = GF(p)$ (a field!) | $GF(p)[x] / \langle p(x) \rangle$ (also a field!) |
| $\mathbb{Z}/6\mathbb{Z}$ has zero divisors | Reducible polynomial → quotient has zero divisors |

**Example over $GF(2)$:**
- $x^2 + 1 = (x+1)^2$ — reducible (since $1 + 1 = 0$ in $GF(2)$)
- $x^2 + x + 1$ — irreducible (no roots: $f(0) = 1$, $f(1) = 1$)

---

# Constructing $GF(p^n)$

Just as $\mathbb{C} = \mathbb{R}[x]/\langle x^2 + 1 \rangle$ extends $\mathbb{R}$ by adjoining $i = \sqrt{-1}$, we construct $GF(p^n)$ by adjoining a root of an irreducible polynomial of degree $n$.

![](./assets/field_construction.png){width=95% center}

In $GF(p^n) = GF(p)[x] / \langle P(x) \rangle$:
- Elements are polynomials of degree $< n$ with coefficients in $GF(p)$
- Addition: coefficient-wise mod $p$
- Multiplication: polynomial multiply, then reduce mod $P(x)$

There are exactly $p^n$ such polynomials → $|GF(p^n)| = p^n$.

---

# Building $GF(4)$ by Hand

$GF(4) = GF(2)[x] / \langle x^2 + x + 1 \rangle$. Let $\alpha$ be a root, so $\alpha^2 + \alpha + 1 = 0$, i.e., $\alpha^2 = \alpha + 1$.

:::matrix { cols="50/50" gap="5%" height="78%"}

[[0, 0]]

The multiplicative group $GF(4)^* = \{1, \alpha, \alpha+1\}$ is cyclic of order $3$.

| Element | Poly | Power |
|---------|------|-------|
| $0$ | $0$ | — |
| $1$ | $1$ | $\alpha^0$ |
| $\alpha$ | $x$ | $\alpha^1$ |
| $\alpha+1$ | $x+1$ | $\alpha^2$ |

[[0, 1]]

**Addition** (XOR — it's a vector space over $GF(2)$):

| $+$ | $0$ | $1$ | $\alpha$ | $\alpha{+}1$ |
|---|---|---|---|---|
| $0$ | $0$ | $1$ | $\alpha$ | $\alpha{+}1$ |
| $1$ | $1$ | $0$ | $\alpha{+}1$ | $\alpha$ |
| $\alpha$ | $\alpha$ | $\alpha{+}1$ | $0$ | $1$ |
| $\alpha{+}1$ | $\alpha{+}1$ | $\alpha$ | $1$ | $0$ |

:::

---

# $GF(4)$ Multiplication

Using $\alpha^2 = \alpha + 1$ and $\alpha^3 = \alpha \cdot \alpha^2 = \alpha(\alpha+1) = \alpha^2 + \alpha = 1$:

| $\times$ | $0$ | $1$ | $\alpha$ | $\alpha{+}1$ |
|---|---|---|---|---|
| $0$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $0$ | $1$ | $\alpha$ | $\alpha{+}1$ |
| $\alpha$ | $0$ | $\alpha$ | $\alpha{+}1$ | $1$ |
| $\alpha{+}1$ | $0$ | $\alpha{+}1$ | $1$ | $\alpha$ |

Every nonzero row is a permutation — no zero divisors. Division is well-defined. $GF(4)$ is a field.

**Verify:** $\alpha \cdot \alpha = \alpha^2 = \alpha + 1$ ✓. $\alpha \cdot (\alpha+1) = \alpha^2 + \alpha = (\alpha+1) + \alpha = 1$ ✓.

So $\alpha^{-1} = \alpha + 1$ and $(\alpha+1)^{-1} = \alpha$. Multiplicative inverses via log/exp: $\alpha^{-1} = \alpha^{3-1} = \alpha^2 = \alpha + 1$.

---

# Primitive Polynomials

An irreducible polynomial is **primitive** if its root $\alpha$ generates the entire multiplicative group $GF(p^n)^*$.

$$GF(p^n)^* = \{\alpha^0, \alpha^1, \alpha^2, \ldots, \alpha^{p^n-2}\} \cong \mathbb{Z}_{p^n - 1}$$

**Test for primitivity:** $P(x)$ is primitive iff:
1. $x^{p^n - 1} \equiv 1 \pmod{P(x)}$
2. $x^{k} \not\equiv 1 \pmod{P(x)}$ for all proper divisors $k$ of $p^n - 1$

This is exactly the same as testing whether an integer is a primitive root of $U(p)$, but for polynomials.

---

# Log/Exp Tables: Fast Arithmetic in $GF(p^n)$

Since $GF(p^n)^*$ is cyclic, every nonzero element is $\alpha^k$ for some $k$.

We precompute two lookup tables:
- $\text{exp}[k] = \alpha^k$ (as integer encoding)
- $\text{log}[v] = k$ such that $\alpha^k = v$

Then: $a \cdot b = \text{exp}[(\text{log}[a] + \text{log}[b]) \bmod (p^n - 1)]$ — **one addition and two table lookups!**

![](./assets/gf8_table.png){width=65% center}

---

# Uniqueness & the Frobenius Endomorphism

**Theorem:** For every prime power $q = p^n$, there exists a unique field of order $q$ (up to isomorphism).

It doesn't matter which irreducible polynomial you pick — you always get the same field. The choice only affects the representation.

**Frobenius endomorphism:** The map $\phi: x \mapsto x^p$ is a field automorphism of $GF(p^n)$ (it fixes $GF(p)$ pointwise). The Galois group is:

$$\mathrm{Gal}(GF(p^n) / GF(p)) = \langle \phi \rangle \cong \mathbb{Z}_n$$

Connection to Chapter 1: the Galois group is itself a cyclic group! Its generator is the Frobenius map, and its order equals the degree of the extension.

---

# Why $GF(2^8)$?

A byte is 8 bits → $2^8 = 256$ possible values → exactly $|GF(2^8)|$.

| Operation | $GF(2^8)$ | Hardware |
|-----------|-----------|----------|
| Addition | XOR of coefficients | Single XOR instruction |
| Multiplication | Log/exp table lookup | 256-byte table (one cache line) |
| Inverse | $\text{exp}[(255 - \text{log}[a]) \bmod 255]$ | Same table |

The algebra perfectly matches the machine word. This is why $GF(2^8)$ appears everywhere:
- **Reed-Solomon** (QR codes, CDs, DVDs, RAID-6)
- **AES encryption** (the S-box is $x \mapsto x^{-1}$ in $GF(2^8)$)
- **CRC checksums** (polynomial division over $GF(2)$)

The primitive polynomial used by QR codes: $x^8 + x^4 + x^3 + x^2 + 1$.

---

# Representing Polynomials in Code

For the practice problems, polynomials are **lists of coefficients from highest to lowest degree:**

$$2x^3 + 0x^2 + x + 4 \quad\longleftrightarrow\quad \texttt{[2, 0, 1, 4]}$$

Addition is elementwise (mod $p$). The tricky part is long division — you'll implement it yourself.

Field elements of $GF(p^n)$ are represented as **integers** by treating coefficients as digits in base $p$:

$$\alpha^2 + \alpha + 1 \quad\longleftrightarrow\quad 1 \cdot 2^2 + 1 \cdot 2^1 + 1 \cdot 2^0 = 7$$

With log/exp tables, multiplication becomes:

```python
def gf_mul(a, b, log_t, exp_t, q):
    """Multiply in GF(q) using precomputed tables."""
    if a == 0 or b == 0: return 0
    return exp_t[(log_t[a] + log_t[b]) % (q - 1)]
```

This one-liner is given — the challenge is building the tables themselves.
