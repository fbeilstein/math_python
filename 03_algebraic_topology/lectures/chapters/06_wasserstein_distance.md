# Comparing Persistence Diagrams

Given two persistence diagrams $\text{Dgm}(X)$ and $\text{Dgm}(Y)$, how do we measure their distance?

**The challenge:** Diagrams may have different numbers of points. 

**Solution:** Add **virtual points** on the diagonal $\Delta = \\{(t, t) : t \ge 0\\}$. A virtual point represents a feature with zero lifetime — it was born and immediately died.

By adding enough virtual points, we can always make two diagrams have the same cardinality, and then look for the best **matching** (bijection) between them.

![](./assets/wasserstein_distance.png){width=60% center}

---

# The $p$-Wasserstein Distance

**Definition.** The **$p$-Wasserstein distance** between persistence diagrams $X$ and $Y$:

$$
W_p(X, Y) = \left( \inf_{\varphi: X \to Y} \sum_{x \in X} \|x - \varphi(x)\|\_\infty^p \right)^{1/p}
$$

where the infimum is over all bijections $\varphi$ between the augmented diagrams (with virtual points on $\Delta$).

**Intuition:** Find the optimal way to match every point in $X$ to a point in $Y$ (or to the diagonal), minimizing the total "transport cost."

- $\|x - \varphi(x)\|\_\infty = \max(|b_x - b_{\varphi(x)}|, |d_x - d_{\varphi(x)}|)$ — the $L^\infty$ distance between matched points
- Unmatched points are sent to their closest projection on the diagonal: $(b, d) \mapsto \left(\frac{b+d}{2}, \frac{b+d}{2}\right)$, at cost $\frac{d-b}{2}$

---

# Bottleneck Distance

**Definition.** The **bottleneck distance** is the limiting case $p \to \infty$:

$$
W_\infty(X, Y) = \inf_{\varphi: X \to Y} \max_{x \in X} \|x - \varphi(x)\|\_\infty
$$

Only the **single worst-matched pair** matters — the maximum over all individual matching costs.

**Comparison:**

| Distance | Sensitive to | Used in |
|----------|-------------|---------|
| $W_1$ | Total displacement of all features | Machine learning, statistical comparisons |
| $W_2$ | Moderate balance of all displacements | Optimization, gradient methods |
| $W_\infty$ (bottleneck) | Worst single mismatch | Stability theorem, theoretical bounds |

**The Stability Theorem** is stated using the bottleneck distance: $W_\infty(\text{Dgm}(X), \text{Dgm}(Y)) \le d_H(X, Y)$.

---

# Computing Wasserstein Distance

The Wasserstein distance reduces to the classical **optimal assignment problem** from combinatorial optimization.

**Algorithm (Hungarian method):**
1. Augment both diagrams with virtual diagonal points to equalize cardinalities
2. Build a cost matrix $C_{ij} = \|x_i - y_j\|_\infty^p$
3. Find the bijection $\varphi^*$ minimizing $\sum C_{i,\varphi(i)}$ — this is the Hungarian algorithm

**Complexity:**
- Hungarian algorithm: $O(n^3)$ for $n$ points
- Bottleneck distance: $O(n^{2.5} \log n)$ via binary search + bipartite matching
- Approximate algorithms exist for large-scale problems

**Software:**
- **GUDHI** (C++/Python) — `gudhi.wasserstein.wasserstein_distance()`
- **Hera** (C++) — optimized for bottleneck and Wasserstein
- **Ripser** (C++/Python) — fast Vietoris-Rips persistence computation

---

# Interactive: Wasserstein Distance

Drag points in two persistence diagrams and watch the optimal matching update in real time.

<button class="demo-btn" onclick="showDemo('https://fbeilstein.github.io/topological_data_analysis/wasserstein_distance/wasserstein_distance.html')">
    Launch Wasserstein Distance Explorer 📐
</button>
