# Error Correction: The Problem

Digital data gets corrupted — scratched CDs, noisy channels, damaged QR codes.

| Strategy | Detect | Correct | Overhead |
|----------|--------|---------|----------|
| Parity bit | 1 bit error | 0 | 1 bit per block |
| Hamming(7,4) | 2 bit errors | 1 bit error | 3 bits per 4 |
| Reed-Solomon | $2t$ symbol errors | $t$ symbol errors | $2t$ symbols per block |

**Key insight:** RS operates on **symbols** (whole bytes), not bits. A burst error corrupting 8 consecutive bits counts as 1 symbol error. This makes RS ideal for physical media where errors come in bursts.

---

# When Polynomials Become Numbers

How do we represent bytes algebraically? We define an **extension field** $GF(p^n)$. 

Instead of reducing integers modulo a prime $p$, we reduce **polynomials** modulo a primitive polynomial $f(x)$ of degree $n$. 

1. **Multiply** two elements: Perform standard polynomial multiplication.
2. **Reduce**: Take the remainder modulo $f(x)$.

**The Duck-Typing Philosophy:**
Because the rules of arithmetic (distributivity, associativity) apply universally, a `Polynomial` class implemented purely using Python's `__add__` and `__mul__` operators works flawlessly whether the coefficients are integers in $\mathbb{R}$ or polynomials themselves evaluated modulo $f(x)$!

---

# The Matrix Setup

**Concept:** We engineer our codeword $\vec{c}$ to live in the null-space of a Vandermonde parity-check matrix $H$, meaning $H\vec{c} = \vec{0}$.

**Definition:** Define a primitive field element $\alpha$. Define every element in the matrix by its row $i$ and column $j$:
$$h_{i,j} = \alpha^{i \cdot j}$$

**The Columns:** Because of this definition, the $j$-th column, $\vec{h}_j$, is exactly the geometric sequence of the base $\alpha^j$:
$$
\vec{h}_j = \begin{bmatrix} (\alpha^j)^0 \\\\ (\alpha^j)^1 \\\\ (\alpha^j)^2 \\\\ \vdots \end{bmatrix}
$$

---

# Example: Matrix Setup in GF(5)

Let's build a $t=1$ error-correcting code in $GF(5)$ using primitive root $\alpha=2$. 
Since $t=1$, our parity-check matrix $H$ needs $2t=2$ rows ($i=0, 1$). Let's use 4 columns ($j=0, 1, 2, 3$).
Because $h_{i,j} = (\alpha^j)^i = (2^j)^i$, our matrix evaluates to:
$$
H = \begin{bmatrix} (2^0)^0 & (2^1)^0 & (2^2)^0 & (2^3)^0 \\\\ (2^0)^1 & (2^1)^1 & (2^2)^1 & (2^3)^1 \end{bmatrix} = \begin{bmatrix} 1^0 & 2^0 & 4^0 & 3^0 \\\\ 1^1 & 2^1 & 4^1 & 3^1 \end{bmatrix} = \begin{bmatrix} 1 & 1 & 1 & 1 \\\\ 1 & 2 & 4 & 3 \end{bmatrix} \pmod 5
$$
We find a valid codeword in the null-space ($H\vec{c} = \vec{0}$): $\vec{c} = [2, 2, 1, 0]^T$.

---

# The Syndrome (Extracting the Columns)

**Concept:** Interference adds an unknown sparse error vector $\vec{e}$. We receive $\vec{r} = \vec{c} + \vec{e}$.

**The Math:** Multiplying by $H$ annihilates the codeword ($H\vec{c} = \vec{0}$) and leaves the syndrome vector: $\vec{s} = H\vec{r} = H\vec{e}$.

**The Mechanism:** By the fundamental definition of matrix multiplication, $H\vec{e}$ is a linear combination of the columns of $H$. The non-zero elements of $\vec{e}$ literally extract and scale specific columns from $H$.

**Formula:** Let $E$ be the set of corrupted column indices.
$$
\vec{s} = \sum_{j \in E} e_j \vec{h}_j
$$

---

# Example: The Syndrome in GF(5)

We transmit $\vec{c} = [2, 2, 1, 0]^T$. An error strikes at index $j=2$ with magnitude 3: $\vec{e} = [0, 0, 3, 0]^T$.
We receive $\vec{r} = [2, 2, 4, 0]^T$.

The receiver computes the syndrome vector $\vec{s} = H\vec{r}$:
$$
\vec{s} = \begin{bmatrix} 1 & 1 & 1 & 1 \\\\ 1 & 2 & 4 & 3 \end{bmatrix} \begin{bmatrix} 2 \\\\ 2 \\\\ 4 \\\\ 0 \end{bmatrix} = \begin{bmatrix} 8 \\\\ 22 \end{bmatrix} = \begin{bmatrix} 3 \\\\ 2 \end{bmatrix} \pmod 5
$$
Notice this is exactly $e_2$ scaling the column $\vec{h}_2$:
$$
\vec{s} = 3 \cdot \begin{bmatrix} 1 \\\\ 4 \end{bmatrix} = \begin{bmatrix} 3 \\\\ 12 \end{bmatrix} = \begin{bmatrix} 3 \\\\ 2 \end{bmatrix}
$$
So our known syndromes are $s_0 = 3, s_1 = 2$.

---

# The Parallel Geometric Progressions

**Concept:** Expand the vector equation to look at a single row $i$ of the syndrome vector.

**The Math:**
$$
s_i = \sum_{j \in E} e_j h_{i,j}
$$

Substitute the hardcoded matrix definition $h_{i,j} = \alpha^{i \cdot j} = (\alpha^j)^i$:
$$
s_i = \sum_{j \in E} e_j (\alpha^j)^i
$$

**The Reveal:** The sequence of syndromes ($s_0, s_1, s_2 \dots$) moving down the rows $i$ is exactly a sum of parallel geometric progressions. The initial scalar is the error magnitude ($e_j$), and the base of the progression is strictly defined by the physical matrix column index ($\alpha^j$).

---

# The Linear Combination & The Substitution

**Concept:** We have a sequence of known syndromes, and we want to find the unknown locations ($j \in E$). We start by taking $v+1$ consecutive syndromes (where $v$ is the number of errors) and combining them using undetermined coefficients $\Lambda_0, \Lambda_1, \dots, \Lambda_v$.

**The Combination:**
$$
\text{Sum} = \sum_{k=0}^v \Lambda_k s_{i+k}
$$

**The Substitution:** Substitute our geometric formula for the syndromes into this combination:
$$
\text{Sum} = \sum_{k=0}^v \Lambda_k \left( \sum_{j \in E} e_j (\alpha^j)^{i+k} \right)
$$

---

# The Algebraic Regrouping (The Polynomial Emerges)

**Concept:** We can rearrange the sums. Instead of grouping by the syndrome index $k$, we group by the physical error location $j$.

**The Regrouping:** Pull the $e_j$ and the base $(\alpha^j)^i$ to the outside:
$$
\text{Sum} = \sum_{j \in E} e_j (\alpha^j)^i \left[ \sum_{k=0}^v \Lambda_k (\alpha^j)^k \right]
$$

**The Reveal:** Look exactly at the inner bracket. It is the definition of a polynomial! If we define $\Lambda(x) = \sum_{k=0}^v \Lambda_k x^k$, then the bracket is simply $\Lambda(\alpha^j)$. The massive sum collapses into:
$$
\text{Sum} = \sum_{j \in E} e_j (\alpha^j)^i \Lambda(\alpha^j)
$$

---

# The Wipeout (The PGZ Matrix)

**Concept:** We have total control over the coefficients $\Lambda_k$, meaning we control the shape and roots of the polynomial $\Lambda(x)$.

**The Logic:** If we intentionally design $\Lambda(x)$ so that its roots are *exactly* the extracted column bases (i.e., $\Lambda(\alpha^j) = 0$ for all $j \in E$), then every single term in our sum gets wiped out.

**The Equation:** The entire right side collapses to 0.
$$
\sum_{k=0}^v \Lambda_k s_{i+k} = 0
$$

**The Conclusion:** Because the syndromes $s$ are known values, this forces a linear system of equations (The PGZ Toeplitz matrix). By solving this matrix for $\Lambda_k$, we build the polynomial, find its roots, and mathematically expose the hidden column bases $\alpha^j$.

---

# Example: The Wipeout in GF(5)

We know $v=1$, so our combination uses $\Lambda_0$ and $\Lambda_1$. The equation $\sum_{k=0}^1 \Lambda_k s_{i+k} = 0$ for $i=0$ gives:
$$
\Lambda_0 s_0 + \Lambda_1 s_1 = 0 \pmod 5
$$
Substitute our known syndromes $s_0=3, s_1=2$. To avoid the trivial solution (all zeros), we set the leading coefficient $\Lambda_1 = 1$:
$$
\Lambda_0 (3) + 1 (2) = 0 \implies 3\Lambda_0 = -2 \equiv 3 \pmod 5
$$
Dividing by 3 gives $\Lambda_0 = 1$. Our polynomial is $\Lambda(x) = \Lambda_1 x^1 + \Lambda_0 x^0 = x + 1$.

**Finding the Root:** We evaluate $\Lambda(x) = x+1$ and find its root is $x = 4 \pmod 5$. 
Because the roots of $\Lambda(x)$ are exactly the extracted column bases $\alpha^j$, we know $\alpha^j = 4$.
Since $\alpha=2$, we solve $2^j = 4 \implies j=2$.
**We mathematically exposed the hidden column base! The error is at index 2!**

---

# Example: Recovering the Magnitude (Vandermonde)

Now that we know $E = \{2\}$ and the base is $\alpha^2 = 4$, we return to our syndrome equation:
$$s_i = \sum_{j \in E} e_j (\alpha^j)^i$$
For $i=0$:
$$s_0 = e_2 (4)^0$$
$$3 = e_2 (1) \implies e_2 = 3$$

We have perfectly recovered the exact error vector $\vec{e} = [0, 0, 3, 0]^T$ using pure matrix algebra!

---

# The Engineering Reality: Decoder Algorithms

The mathematical derivations we just performed form the foundation of all Reed-Solomon decoders. However, in industrial applications, engineers optimize these steps for silicon (ASICs):

1. **Solving the Linear Combination ($\Lambda_k$):**
   - **PGZ (Peterson-Gorenstein-Zierler):** Direct matrix inversion. $O(v^3)$. Simple but slow.
   - **Berlekamp-Massey:** An iterative shift-register algorithm. $O(v^2)$. The industry standard for hardware.
   - **Euclidean Algorithm:** Uses polynomial greatest common divisors. $O(v^2)$. Standard in software.

2. **Finding the Roots (The Column Bases):**
   - **Chien Search:** A highly optimized hardware algorithm that brute-force evaluates $\Lambda(x)$ for all field elements simultaneously using parallel multipliers.

3. **Finding the Magnitudes ($e_j$):**
   - **Forney Algorithm:** Computes the Vandermonde matrix inversion implicitly using a formal derivative of $\Lambda(x)$, avoiding full matrix division.

---

# Gaussian Elimination over $GF(p^n)$

To solve both the PGZ Toeplitz system and the Magnitudes Vandermonde system, we need to solve $Ax = b$.

The algorithm is **mathematically identical** to what you know from linear algebra over $\mathbb{R}$:
1. Find pivot (first non-zero entry)
2. Swap rows
3. Normalize (divide by pivot)
4. Eliminate (subtract multiples)

**Duck-Typing Magic:** Because our `GaloisFieldElement` objects override Python's `__add__`, `__mul__`, `__truediv__`, and `__bool__` operators, a completely generic `solve_linear(A, b)` function works flawlessly without knowing what field it's in!

**Industrial Reality Check:** While our code dynamically multiplies polynomials modulo $f(x)$ for pedagogy, industrial ASICs (like hardware QR scanners) heavily rely on precomputed `log` / `exp` lookup tables to achieve $O(1)$ multiplication speeds over $GF(2^8)$.

---

# Interactive: RS Encoder / Decoder

<iframe src="demos/rs_demo.html" style="width: 100%; height: 62vh; border: 1px solid #30363d; border-radius: 8px;"></iframe>

---

# QR Code Anatomy

:::matrix { cols="50/50"}

[[0, 0]]
![](./assets/QR_Format_Information.svg){height=90% center style="background-color: white;"}
[[1, 0]] { text-align: center; }
Format Information & Masking

[[0, 1]]
![](./assets/QR_Ver3_Codeword_Ordering.svg){height=90% center style="background-color: white;"}
[[1, 1]] { text-align: center; }
Codeword Interleaving

:::

---

<style>
  .shrink-qr-slide p, 
  .shrink-qr-slide table, 
  .shrink-qr-slide th, 
  .shrink-qr-slide td, 
  .shrink-qr-slide li {
    font-size: 75% !important;
  }
</style>
<div class="shrink-qr-slide">
A QR code is a $21 \times 21$ (or larger) matrix that uses Reed-Solomon over $GF(2^8)$.

| Component | Purpose |
|-----------|---------|
| **Finder patterns** (3 corners) | Orientation & alignment for scanners |
| **Timing patterns** | Grid calibration (alternating B/W) |
| **Format info** | EC level + mask pattern (BCH-encoded) |
| **Data region** | Interleaved data + RS parity symbols read in a zig-zag |

The standard defines four error correction levels:

| Level | Recovery | Parity overhead |
|-------|----------|----------------|
| L | ~7% | Low |
| M | ~15% | Medium |
| Q | ~25% | Quartile |
| H | ~30% | High |

In your practice problem, you implement the full algebraic pipeline and generate a real, scannable QR code.

</div>

---

# Beyond QR: Where This Math Lives

The algebra you've learned appears throughout modern technology:

| Application | Uses |
|-------------|------|
| **AES encryption** | S-box = multiplicative inverse in $GF(2^8)$ |
| **Shamir's Secret Sharing** | Polynomial interpolation over finite fields |
| **Cloud storage** (Google, Facebook) | RS-based erasure codes for redundancy |
| **DNA data storage** | RS codes correct sequencing errors |
| **Deep space communication** | Voyager, Mars rovers use RS concatenated codes |
| **RAID-6** | Double-parity using $GF(2^8)$ arithmetic |

Reed-Solomon was invented in 1960. Over 60 years later, the same mathematics protects your data on every digital device you own.
