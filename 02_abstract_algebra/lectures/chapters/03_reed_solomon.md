

# Error Correction: The Problem

Digital data gets corrupted — scratched CDs, noisy channels, damaged QR codes.

| Strategy | Detect | Correct | Overhead |
|----------|--------|---------|----------|
| Parity bit | 1 bit error | 0 | 1 bit per block |
| Hamming(7,4) | 2 bit errors | 1 bit error | 3 bits per 4 |
| Reed-Solomon | $2t$ symbol errors | $t$ symbol errors | $2t$ symbols per block |

**Key insight:** RS operates on **symbols** (whole bytes), not bits. A burst error corrupting 8 consecutive bits counts as 1 symbol error. This makes RS ideal for physical media where errors come in bursts.

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

---

# The Polynomial Setup

**Concept:** Instead of treating the codeword as a column vector $\vec{c}$, we can treat it as a polynomial $c(x)$ where the coefficients are the transmitted symbols. 

**Key insight:** The Galois field $GF(p^n)$ is cyclic, meaning it has a **primitive element** $\alpha$ such that its powers generate all non-zero elements of the field exactly once.

**The Generator:** We construct a generator polynomial $g(x)$ whose roots are exactly the first $2t$ consecutive powers of our **primitive element** $\alpha$:
$$
g(x) = (x - \alpha^0)(x - \alpha^1)\cdots(x - \alpha^{2t-1})
$$

**The Codeword:** We encode our message polynomial $m(x)$ such that the resulting codeword polynomial $c(x)$ is a perfect multiple of $g(x)$
$$
c(x) = m(x) g(x). 
$$
Because $c(x)$ is a multiple of $g(x)$, evaluating $c(x)$ at any of the roots $\alpha^0, \dots, \alpha^{2t-1}$ must yield exactly $0$.

> **The Degree Cap:** By the generalization of Fermat's Little Theorem, $x^q = x$ for all elements $x \in GF(q = p^n)$ --- every polynomial *function* can be fully represented by a polynomial of degree at most $q-1$, thus $\deg(m(x)) + \deg(g(x)) \le q-2$.

---

**Example in GF(5):** Let's build a $t=1$ code using primitive root $\alpha=2$.

| Element | $0$ | $1$ | $2$ | $3$ | $4$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Power of $\alpha=2$** | N/A | $2^0$ | $2^1$ | $2^3$ | $2^2$ |

Because $2t=2$, the roots of our generator are $\alpha^0=1$ and $\alpha^1=2$:
$$
g(x) = (x - 1)(x - 2) = x^2 - 3x + 2 \equiv 2 + 2x + x^2 \pmod 5
$$
If our message is $m(x) = 2x + 3$, we encode it by multiplying:
$$
\begin{aligned}
c(x) &= m(x)g(x) = (3 + 2x)(2 + 2x + x^2) = 6 + 10x + 7x^2 + 2x^3\\\\
     &\equiv 1 + 0x + 2x^2 + 2x^3 \pmod 5
\end{aligned}
$$
Extracting the coefficients yields the transmitted symbols: $\vec{c} = [1, 0, 2, 2]^T$.

---

# The Matrix Setup

**Concept:** the matrix $H$ with primitive elelements $\alpha^j$
$$
\require{html}
H=
\underbrace{\left.\begin{bmatrix}
1 & 1 & \cdots & 1\\\\
1 & \alpha & \cdots & \alpha^{n-1}\\\\
\vdots & \vdots & \ddots & \vdots\\\\
1 & \alpha^{2t-1} & \cdots & \alpha^{(2t-1)(n-1)}
\end{bmatrix}\right\\}}_{\text{codeword symbols }(n)} \\hspace{-2cm}
\style{
display:inline-block;
transform:rotate(-90deg);
transform-origin:left center;
}{
\text{parity checks }(2t)
}\\hspace{-2cm}; \quad h\_{i,j} = (\alpha^j)^i; \quad
\vec{h}_k = 
\begin{bmatrix} 
(\alpha^k)^0 \\\\ 
(\alpha^k)^1 \\\\ 
(\alpha^k)^2 \\\\ 
\vdots 
\end{bmatrix}
$$

**Note:** evaluating $H\vec{c}$ is equivalent to evaluating polynomial $c(x)$ at the roots $\alpha^k$ for $k=0, \dots, 2t-1$. 


Since our polynomial $c(x) = m(x)g(x)$ is a multiple of $g(x)$ and the roots of $g(x)$ are $\alpha^0, \dots, \alpha^{2t-1}$, it follows that $c(\alpha^k) = 0$ for all $k=0, \dots, 2t-1$ --- it is in the null-space of $H$ by construction, i.e., $H\vec{c} = \vec{0}$.


---

# Example: Matrix Setup in GF(5)

Let's build a $t=1$ error-correcting code in $GF(5)$ using primitive root $\alpha=2$. 


Since $t=1$, our parity-check matrix $H$ needs $2t=2$ rows ($i=0, 1$). Let's use 4 columns ($j=0, 1, 2, 3$).


Because $h_{i,j} = (\alpha^j)^i = (2^j)^i$, our matrix evaluates to:
$$
H = 
\begin{bmatrix} 
(2^0)^0 & (2^1)^0 & (2^2)^0 & (2^3)^0 \\\\ 
(2^0)^1 & (2^1)^1 & (2^2)^1 & (2^3)^1 
\end{bmatrix} = 
\begin{bmatrix} 
1^0 & 2^0 & 4^0 & 3^0 \\\\ 
1^1 & 2^1 & 4^1 & 3^1 
\end{bmatrix} = 
\begin{bmatrix} 
1 & 1 & 1 & 1 \\\\ 
1 & 2 & 4 & 3 
\end{bmatrix} \pmod 5
$$


We can check that our codeword $\vec{c} = [1, 0, 2, 2]^T$ from the polynomial setup indeed falls into the null-space of this matrix:
$$
\begin{aligned}
H\vec{c} &= 
\begin{bmatrix} 
1 & 1 & 1 & 1 \\\\ 
1 & 2 & 4 & 3 
\end{bmatrix}
\begin{bmatrix} 
1 \\\\ 
0 \\\\ 
2 \\\\ 
2 
\end{bmatrix} = 
\begin{bmatrix} 
1(1) + 1(0) + 1(2) + 1(2) \\\\ 
1(1) + 2(0) + 4(2) + 3(2) 
\end{bmatrix} = 
\begin{bmatrix} 
1 + 0 + 2 + 2 \\\\ 
1 + 0 + 8 + 6
\end{bmatrix} =
\begin{bmatrix} 
5 \\\\ 
15 
\end{bmatrix} \\\\ &\equiv 
\begin{bmatrix} 
0 \\\\ 
0 
\end{bmatrix} \pmod 5
\end{aligned}
$$


---

# The Syndrome (Extracting the Columns)

**Concept:** Interference adds an unknown sparse error vector $\vec{e}$. We receive $\vec{r} = \vec{c} + \vec{e}$. Multiplying by $H$ annihilates the codeword ($H\vec{c} = \vec{0}$) and leaves the syndrome vector: $\vec{s} = H\vec{r} = H\vec{e}$.

**Formula:** Let $E$ be the set of corrupted column indices.
$$
\vec{s} = \sum_{j \in E} e_j \vec{h}_j
$$

If we assume there are $\nu \le 2t$ errors, we can show that $\\{h_j | j \in E\\}$ are linearly independent. To see this construct new matrix $H'$ that contains columns $h_j$ trimmed to the first $\nu$ entries
$$
H' = 
\begin{bmatrix}
1 & 1 & \cdots & 1 \\\\
\alpha^{j_1} & \alpha^{j_2} & \cdots & \alpha^{j_\nu} \\\\
\vdots & \vdots & \ddots & \vdots \\\\
\alpha^{(\nu-1)j_1} & \alpha^{(\nu-1)j_2} & \cdots & \alpha^{(\nu-1)j_\nu}
\end{bmatrix}.
$$
$H'$ is a Vandermonde matrix, thus has no-zero determinant, thus

> if an error vector $\vec{e}$ has $\nu \le 2t$ non-zero elements, $H\vec{e} \neq 0$ --- any error in $\nu \le 2t$ symbols can be **detected** (not corrected).


---

# Example: The Syndrome in GF(5)

We transmit $\vec{c} = [2, 2, 1, 0]^T$. An error strikes at index $j=2$ with magnitude 3: 
$$
\vec{e} = [0, 0, 3, 0]^T.
$$
We receive $\vec{r} = [2, 2, 4, 0]^T$.

The receiver computes the syndrome vector $\vec{s} = H\vec{r}$:
$$
\vec{s} = 
\begin{bmatrix} 
1 & 1 & 1 & 1 \\\\ 
1 & 2 & 4 & 3 
\end{bmatrix} 
\begin{bmatrix} 
2 \\\\ 2 \\\\ 4 \\\\ 0 
\end{bmatrix} = 
\begin{bmatrix} 
8 \\\\ 
22 
\end{bmatrix} = 
\begin{bmatrix} 
3 \\\\ 
2 
\end{bmatrix} \pmod 5
$$
Notice this is exactly $e_2$ scaling the column $\vec{h}_2$:
$$
\vec{s} = 3 \cdot 
\begin{bmatrix} 
1 \\\\ 
4 
\end{bmatrix} = 
\begin{bmatrix} 
3 \\\\ 
12 
\end{bmatrix} = 
\begin{bmatrix} 
3 \\\\ 
2 
\end{bmatrix}
$$
So our known syndromes are $s_0 = 3, s_1 = 2$.

---

We start with exactly $2t$ equations and $v$ unknown errors at locations $\alpha^{j_1} \dots \alpha^{j_v}$.

$$
\begin{aligned} 
s_0 &= e_1 + e_2 + e_3 + \dots + e_v \\\\
s_1 &= e_1 \alpha^{j_1} + e_2 \alpha^{j_2} + e_3 \alpha^{j_3} + \dots + e_v \alpha^{j_v} \\\\
s_2 &= e_1 (\alpha^{j_1})^2 + e_2 (\alpha^{j_2})^2 + e_3 (\alpha^{j_3})^2 + \dots + e_v (\alpha^{j_v})^2 \\\\ 
s_3 &= e_1 (\alpha^{j_1})^3 + e_2 (\alpha^{j_2})^3 + e_3 (\alpha^{j_3})^3 + \dots + e_v (\alpha^{j_v})^3 \\\\ 
&\vdots \\\\ 
s_{2t-1} &= e_1 (\alpha^{j_1})^{2t-1} + e_2 (\alpha^{j_2})^{2t-1} + e_3 (\alpha^{j_3})^{2t-1} + \dots + e_v (\alpha^{j_v})^{2t-1} 
\end{aligned}
$$

**First Sweep: Eliminate $e_1$**

Apply the filter $(s_k - \alpha^{j_1} s_{k-1})$ to every adjacent pair. 
The $e_1$ variable is completely annihilated, 
while the geometric structure of the surviving errors is preserved.

$$
\begin{aligned} 
s_1 - \alpha^{j_1} s_0 &= e_2 (\alpha^{j_2} - \alpha^{j_1}) + e_3 (\alpha^{j_3} - \alpha^{j_1}) + \dots + e_v (\alpha^{j_v} - \alpha^{j_1}) \\\\
s_2 - \alpha^{j_1} s_1 &= e_2 \alpha^{j_2} (\alpha^{j_2} - \alpha^{j_1}) + e_3 \alpha^{j_3} (\alpha^{j_3} - \alpha^{j_1}) + \dots + e_v \alpha^{j_v} (\alpha^{j_v} - \alpha^{j_1}) \\\\
s_3 - \alpha^{j_1} s_2 &= e_2 (\alpha^{j_2})^2 (\alpha^{j_2} - \alpha^{j_1}) + e_3 (\alpha^{j_3})^2 (\alpha^{j_3} - \alpha^{j_1}) + \dots + e_v (\alpha^{j_v})^2 (\alpha^{j_v} - \alpha^{j_1}) \\\\
&\vdots \\\\
s_{2t-1} - \alpha^{j_1} s_{2t-2} &= e_2 (\alpha^{j_2})^{2t-2} (\alpha^{j_2} - \alpha^{j_1}) + e_3 (\alpha^{j_3})^{2t-2} (\alpha^{j_3} - \alpha^{j_1}) + \dots + e_v (\alpha^{j_v})^{2t-2} (\alpha^{j_v} - \alpha^{j_1}) 
\end{aligned}
$$

---


**Second Sweep: Eliminate $e_2$**

Apply the next filter, using $\alpha^{j_2}$, strictly to the new equations. The $e_2$ terms are now annihilated.

$$
\begin{aligned} 
(s_2 - \alpha^{j_1} s_1) - \alpha^{j_2} (s_1 - \alpha^{j_1} s_0) &= e_3 (\alpha^{j_3} - \alpha^{j_1})(\alpha^{j_3} - \alpha^{j_2}) + \dots\\\\ 
&+ e_v (\alpha^{j_v} - \alpha^{j_1})(\alpha^{j_v} - \alpha^{j_2}) \\\\
(s_3 - \alpha^{j_1} s_2) - \alpha^{j_2} (s_2 - \alpha^{j_1} s_1) &= e_3 \alpha^{j_3} (\alpha^{j_3} - \alpha^{j_1})(\alpha^{j_3} - \alpha^{j_2}) + \dots\\\\ 
&+ e_v \alpha^{j_v} (\alpha^{j_v} - \alpha^{j_1})(\alpha^{j_v} - \alpha^{j_2}) \\\\
&\vdots \\\\
(s_{2t-1} - \alpha^{j_1} s_{2t-2}) - \alpha^{j_2} (s_{2t-2} - \alpha^{j_1} s_{2t-3}) &= e_3 (\alpha^{j_3})^{2t-3} (\alpha^{j_3} - \alpha^{j_1})(\alpha^{j_3} - \alpha^{j_2}) + \dots \\\\
&+ e_v (\alpha^{j_v})^{2t-3} (\alpha^{j_v} - \alpha^{j_1})(\alpha^{j_v} - \alpha^{j_2}) 
\end{aligned}
$$


We repeat this elimination exactly $v$ times until every single error is targeted and killed. Every elimination step uses the same multipliers $(\alpha^{j_1},\ldots,\alpha^{j_v})$. Since each block of equations undergoes the same sequence of operations, the resulting recurrence has the same coefficients $(\Lambda_i)$.

$$
\begin{aligned} 
s_v + \Lambda_{v-1} s_{v-1} + \dots + \Lambda_1 s_1 + \Lambda_0 s_0 &= 0 \\\\
s_{v+1} + \Lambda_{v-1} s_v + \dots + \Lambda_1 s_2 + \Lambda_0 s_1 &= 0 \\\\
s_{v+2} + \Lambda_{v-1} s_{v+1} + \dots + \Lambda_1 s_3 + \Lambda_0 s_2 &= 0 \\\\
&\vdots \\\\ 
s_{2t-1} + \Lambda_{v-1} s_{2t-2} + \dots + \Lambda_1 s_{2t-v} + \Lambda_0 s_{2t-v-1} &= 0 
\end{aligned}
$$

---

Now we used $t$ first equations to eliminate the first $t$ errors, we are left with $2t - t = t$ equations and we have $v \leq t$ unknown errors. 
This means we can solve the system of linear equations and recover $\Lambda_0, \dots, \Lambda_{v-1}, \Lambda_v=1$.


How do we now get $\alpha^j$?

Note interesting property:
$$
\sum_{k=0}^{v} \Lambda_k s_{i+k} = \sum_{k=0}^{v} \Lambda_k \left( \sum_{j \in E} e_j (\alpha^j)^{i+k} \right) = 0
$$
Group by the error terms $e_j$, pulling the row offset outside the inner sum since it does not depend on $k$.
$$
\sum_{j \in E} e_j (\alpha^j)^i \left( \sum_{k=0}^{v} \Lambda_k (\alpha^j)^k \right) = 0
$$

The lest equation is true for any $e_j$ thus the term in the parenthesis must be 0.
Note this is a polynomial of degree $v$ and it has roots $\alpha^{j}, j \in E$.

> The Chien Search basically checks all elements of the field against this equation and finds the roots, i.e. locates the errors.

---

# Example: Solving the PGZ System in GF(5)

We know $v=1$, so our PGZ system of equations uses $\Lambda_0$ and $\Lambda_1$. The equation $\sum_{k=0}^1 \Lambda_k s_{i+k} = 0$ for $i=0$ gives:
$$
\Lambda_1 s_1 + \Lambda_0 s_0 = 0 \pmod 5
$$
Substitute our known syndromes $s_0=3, s_1=2$. By convention, we set $\Lambda_1 = 1$:
$$
1 (2) + \Lambda_0 (3) = 0 \implies 3\Lambda_0 = -2 \equiv 3 \pmod 5
$$
Dividing by 3 gives $\Lambda_0 = 1$. Our error locator polynomial is therefore:
$$
\Lambda(x) = \Lambda_1 x^1 + \Lambda_0 x^0 = x + 1
$$

**Chien Search:** We evaluate $\Lambda(x) = x+1$ across the elements of the field to find its roots. It evaluates to $0$ when $x = 4 \pmod 5$. 
Because the roots of $\Lambda(x)$ correspond exactly to the corrupted column bases $\alpha^j$, we know $\alpha^j = 4$.
Since $\alpha=2$, we solve $2^j = 4 \implies j=2$.
**We mathematically exposed the hidden column base! The error is at index 2!**

---

# Example: Recovering the Magnitude (Vandermonde)

Now that we know $E = \\{2\\}$ and the base is $\alpha^2 = 4$, we return to our syndrome equation:
$$s_i = \sum_{j \in E} e_j (\alpha^j)^i$$
For $i=0$:
$$s_0 = e_2 (4)^0$$
$$3 = e_2 (1) \implies e_2 = 3$$

We have perfectly recovered the exact error vector $\vec{e} = [0, 0, 3, 0]^T$ using pure matrix algebra!

---


# Example: Magnitudes for Multiple Errors

To see the full matrix structure for multiple errors, suppose we are in $GF(7)$ with primitive root $\alpha=3$ and a code capable of $t=2$ corrections. 

After running Chien Search, we discover $v=2$ errors at indices $j_1=\textcolor{red}{1}$ and $j_2=\textcolor{blue}{4}$. 
The column bases for our errors are $\textcolor{red}{\alpha^1=3}$ and $\textcolor{blue}{\alpha^4=4}$. 

Assume our calculated full syndrome vector (which has $2t = 4$ elements) is:
$\vec{S} = [\textcolor{magenta}{s_0}, \textcolor{green}{s_1}, s_2, s_3]^T = [\textcolor{magenta}{0}, \textcolor{green}{5}, 0, 3]^T \pmod 7$

Because we found exactly $v=2$ errors, we **trim** $\vec{S}$ down to its first $v$ elements to form $\vec{S}'$. We only need these first 2 equations to solve for the $v=2$ unknown magnitudes $Y_1$ and $Y_2$: 
$\vec{S}' = [\textcolor{magenta}{s_0}, \textcolor{green}{s_1}]^T = [\textcolor{magenta}{0}, \textcolor{green}{5}]^T$

We construct the system:
$$
H' Y = 
\begin{bmatrix}
(\textcolor{red}{\alpha^1})^0 & (\textcolor{blue}{\alpha^4})^0 \\\\
(\textcolor{red}{\alpha^1})^1 & (\textcolor{blue}{\alpha^4})^1 
\end{bmatrix}
\begin{bmatrix}
Y_1 \\\\
Y_2
\end{bmatrix} = \begin{bmatrix}
\textcolor{red}{1} & \textcolor{blue}{1} \\\\
\textcolor{red}{3} & \textcolor{blue}{4}
\end{bmatrix}
\begin{bmatrix}
Y_1 \\\\
Y_2
\end{bmatrix} = \begin{bmatrix}
\textcolor{magenta}{0} \\\\
\textcolor{green}{5}
\end{bmatrix}  \pmod 7
$$


Solving this via standard Gaussian elimination:
- Subtract $3 \times$ Row 1 from Row 2 to eliminate $Y_1$:
  - New Row 2: $3 - 3(1) = 0$, $4 - 3(1) = 1$, $5 - 3(0) = 5$.
  - This gives $Y_2 = 5$.
- Substitute $Y_2 = 5$ into Row 1:
  - $1 \cdot Y_1 + 1 \cdot (5) = 0 \implies Y_1 = -5 \equiv 2 \pmod 7$.

We have successfully recovered both error magnitudes $Y_1=2$ and $Y_2=5$ simultaneously!

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

<iframe src="demos/rs_demo.html?v=2" style="width: 100%; height: 62vh; border: 1px solid #30363d; border-radius: 8px;"></iframe>

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

