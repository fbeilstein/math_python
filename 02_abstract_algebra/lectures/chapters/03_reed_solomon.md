# Error Correction: The Problem

Digital data gets corrupted — scratched CDs, noisy channels, damaged QR codes.

| Strategy | Detect | Correct | Overhead |
|----------|--------|---------|----------|
| Parity bit | 1 bit error | 0 | 1 bit per block |
| Hamming(7,4) | 2 bit errors | 1 bit error | 3 bits per 4 |
| Reed-Solomon | $2t$ symbol errors | $t$ symbol errors | $2t$ symbols per block |

**Key insight:** RS operates on **symbols** (whole bytes), not bits. A burst error corrupting 8 consecutive bits counts as 1 symbol error. This makes RS ideal for physical media where errors come in bursts.

---

# Reed-Solomon Codes

**Idea:** Represent data as a polynomial $m(x)$ over $GF(p^n)$. Append redundancy by evaluating at known field elements. Any corruption changes the polynomial, and we can algebraically locate and fix the errors.

A code with $2t$ parity symbols can correct up to $t$ symbol errors.


<div style="text-align: center; margin-top: 30px;">
<div style="color: #58a6ff; font-size: 0.85em; margin-bottom: 8px;">Reed-Solomon Codeword ($n = k + 2t$ symbols)</div>
<div style="display: inline-flex; align-items: center; gap: 4px;">
  <div style="background: #58a6ff; color: white; padding: 20px 60px; border-radius: 6px; font-weight: bold; font-size: 1.1em;">Data<br><span style="font-size: 0.8em; font-weight: normal;">($k$ symbols)</span></div>
  <div style="background: #ff7b72; color: white; padding: 20px 40px; border-radius: 6px; font-weight: bold; font-size: 1.1em;">Parity<br><span style="font-size: 0.8em; font-weight: normal;">($2t$ symbols)</span></div>
  <div style="font-size: 1.6em; color: #484f58; margin: 0 8px;">→</div>
  <div style="color: #ffd700; font-size: 1.1em;">$m(x) \cdot x^{2t} \bmod g(x)$</div>
</div>
<div style="color: #7ee787; margin-top: 12px; font-size: 0.9em;">Can correct up to $t$ errors</div>
</div>


---

# The Generator Polynomial

We define $2t$ roots $\alpha^0, \alpha^1, \ldots, \alpha^{2t-1}$ and build:

$$g(x) = \prod_{i=0}^{2t-1} (x - \alpha^i)$$

Every valid codeword $c(x)$ is divisible by $g(x)$. Encoding computes:

$$c(x) = m(x) \cdot x^{2t} - \big[m(x) \cdot x^{2t} \bmod g(x)\big]$$

The remainder becomes the parity symbols appended to the message.

**Example:** For $t=1$ (correct 1 error) in $GF(2^3)$:

$g(x) = (x - 1)(x - \alpha) = x^2 + \alpha^3 x + \alpha$

(Remember: in $GF(2)$, subtraction = addition, and $1 + \alpha = \alpha^3$.)

---

# Worked Example: Encoding

In $GF(2^3)$ with primitive polynomial $x^3 + x + 1$, let's encode message $[5, 3]$ with $t = 1$ ($2t = 2$ parity symbols).

**Step 1:** Generator polynomial: $g(x) = x^2 + 3x + 2$ (using integer representation: $\alpha^3 = 3$, $\alpha = 2$).

**Step 2:** Shift message: $m(x) \cdot x^2 = 5x^3 + 3x^2$.

**Step 3:** Divide $5x^3 + 3x^2$ by $g(x) = x^2 + 3x + 2$ over $GF(2^3)$:

| Step | Quotient term | Operation |
|------|--------------|-----------|
| Lead: $5x^3 \div x^2$ | $5x$ | $5x \cdot g(x) = 5x^3 + 5 \cdot 3 \cdot x^2 + 5 \cdot 2 \cdot x$ |
| | | Use tables: $5 \cdot 3 = \text{exp}[\text{log}[5] + \text{log}[3]] = \text{exp}[6+1] = \text{exp}[7] = \text{exp}[0] = 1$ |
| Subtract | | New remainder: $(3 \oplus 1)x^2 + (0 \oplus 10)x = 2x^2 + \ldots$ |

**Result:** Codeword = $[5, 3, r_1, r_0]$ — message + parity.

---

# Syndromes: Detecting Errors

A received message $r(x) = c(x) + e(x)$ may contain errors $e(x)$.

Since $c(\alpha^i) = 0$ for all roots, the **syndromes** $S_i = r(\alpha^i) = e(\alpha^i)$ depend only on the errors.

$$S_i = r(\alpha^i) = \sum_{\text{error positions } j} Y_j \cdot X_j^i$$

where $X_j = \alpha^{n-1-j}$ are error locators and $Y_j$ are error magnitudes.

- All syndromes zero → no errors
- Some non-zero → errors exist, and syndromes encode their positions and values

**Computing syndromes** is polynomial evaluation — Horner's method:

$$r(\alpha^i) = (\cdots((r_0 \cdot \alpha^i + r_1) \cdot \alpha^i + r_2) \cdots )$$

---

# Worked Example: Decoding (Part 1 — Syndromes)

Take our codeword $c = [5, 3, r_1, r_0]$ and introduce one error at position 0:

$$r = [5 \oplus e, 3, r_1, r_0]$$

**Compute syndromes** at roots $\alpha^0 = 1$ and $\alpha^1 = \alpha$:

$S_0 = r(1) = r_0 + r_1 + 3 + (5 \oplus e)$

$S_1 = r(\alpha) = r_0 + r_1 \cdot \alpha + 3 \cdot \alpha^2 + (5 \oplus e) \cdot \alpha^3$

Since $c$ was valid ($c(\alpha^i) = 0$), only the error contributes:

$S_0 = e \cdot X_1^0 = e$

$S_1 = e \cdot X_1^1 = e \cdot \alpha^3$ (since error is at position 0, $X_1 = \alpha^{n-1-0} = \alpha^3$)

The syndromes *are* the error — we just need to decode them.

---

# Error Locator Polynomial (PGZ)

Define the **Error Locator Polynomial**: $\Lambda(x) = \prod_{j} (1 - X_j x)$

The **Key Equation** relates $\Lambda$ to the syndromes:

$$\Lambda(x) \cdot S(x) \equiv \Omega(x) \pmod{x^{2t}}$$

Expanding: the coefficient of $x^k$ for $k \geq t$ must be zero, giving a linear system:

$$\begin{pmatrix} S_0 & S_1 & \cdots & S_{t-1} \\\\ S_1 & S_2 & \cdots & S_t \\\\ \vdots & & \ddots & \vdots \\\\ S_{t-1} & S_t & \cdots & S_{2t-2} \end{pmatrix} \begin{pmatrix} \Lambda_t \\\\ \Lambda_{t-1} \\\\ \vdots \\\\ \Lambda_1 \end{pmatrix} = - \begin{pmatrix} S_t \\\\ S_{t+1} \\\\ \vdots \\\\ S_{2t-1} \end{pmatrix}$$

Solve via **Gaussian Elimination over $GF(p^n)$** — the *exact same algorithm* as over $\mathbb{R}$, but using log/exp tables for arithmetic.

---

# Worked Example: Decoding (Part 2 — Error Location)

For $t = 1$, the "matrix" is $1 \times 1$: $S_0 \cdot \Lambda_1 = -S_1$.

$$\Lambda_1 = -S_1 / S_0 = S_1 / S_0 \quad (\text{in } GF(2),\ -1 = 1)$$

The error locator polynomial: $\Lambda(x) = \Lambda_1 x + 1$.

**Chien Search:** Evaluate $\Lambda(\alpha^{-i})$ for $i = 0, 1, \ldots, n-1$:

If $\Lambda(\alpha^{-i}) = 0$, then position $i$ has an error.

From our example: $\Lambda_1 = S_1/S_0 = (e \cdot \alpha^3) / e = \alpha^3$.

$\Lambda(\alpha^{-0}) = \alpha^3 \cdot 1 + 1 = \alpha^3 + 1 = \alpha + 1 + 1 = \alpha \neq 0$ — not here.

$\Lambda(\alpha^{-3}) = \alpha^3 \cdot \alpha^{-3} + 1 = 1 + 1 = 0$ ✓ — error at position 0!

---

# Worked Example: Decoding (Part 3 — Correction)

**Error magnitude:** For $t = 1$, it's simply $Y_1 = S_0 = e$.

**Correct:** $r_{\text{corrected}}[0] = r[0] - Y_1 = r[0] \oplus e = (5 \oplus e) \oplus e = 5$ ✓

The full decoding pipeline:

| Step | Math | What you implement |
|------|------|--------------------|
| 1. Syndromes | Evaluate $r(\alpha^i)$ | `calculate_syndromes` |
| 2. Error Locator | Solve linear system | `pgz_error_locator` |
| 3. Error Positions | Find roots of $\Lambda$ | `chien_search` |
| 4. Error Magnitudes | Solve Vandermonde system | `linear_error_magnitudes` |
| 5. Correct | Subtract errors | Trivial |

---

# Gaussian Elimination over $GF(p^n)$

The algorithm is **identical** to what you know from linear algebra over $\mathbb{R}$:

1. **Find pivot** — first nonzero entry in the column
2. **Swap rows** — same as usual
3. **Normalize** — divide by pivot (using $\text{exp}[-\text{log}[\text{pivot}]]$)
4. **Eliminate** — subtract multiples (using log/exp for multiply, XOR for add)

The *only* difference from real-valued Gaussian elimination is replacing floating-point operations with finite field operations. No new algorithm to learn.

Because this algorithm is mathematically identical across all fields, our laboratory provides a fully generic `solve_linear(A, b)` utility. You will use it twice:
- **PGZ:** solve for the error locator polynomial coefficients
- **Magnitudes:** solve the Vandermonde system for error values

---

# Interactive: RS Encoder / Decoder

<iframe src="demos/rs_demo.html" style="width: 100%; height: 62vh; border: 1px solid #30363d; border-radius: 8px;"></iframe>

---

# QR Code Anatomy


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
| **Data region** | Interleaved data + RS parity symbols |

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
