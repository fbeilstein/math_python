import numpy as np
from math import gcd
from itertools import product
from .core import Group, GroupElement, ConcreteGroupElement

# ────────────────────────────────────────────────────────────
# Factory methods: build ConcreteGroup from various sources
# ────────────────────────────────────────────────────────────

def from_Zn(n):
    """Cyclic group Z_n under addition mod n."""
    labels = [str(i) for i in range(n)]
    table = [[(i + j) % n for j in range(n)] for i in range(n)]
    return Group(labels, table, identity=0, generators=[1 if n > 1 else 0])


def from_Un(n):
    """Multiplicative group U(n) = units of Z_n."""
    elems = [k for k in range(1, n) if gcd(k, n) == 1]
    idx = {e: i for i, e in enumerate(elems)}
    labels = [str(e) for e in elems]
    m = len(elems)
    table = [[idx[(elems[i] * elems[j]) % n] for j in range(m)] for i in range(m)]
    gen_idx = []
    generated = {1}
    for e in elems:
        if len(generated) == m: break
        if e not in generated:
            gen_idx.append(idx[e])
            # closure with new generator
            new_gen = set(generated)
            q = list(new_gen)
            while q:
                c = q.pop(0)
                for g_idx in gen_idx:
                    nxt = (c * elems[g_idx]) % n
                    if nxt not in new_gen:
                        new_gen.add(nxt)
                        q.append(nxt)
            generated = new_gen
            
    return Group(labels, table, identity=idx[1], generators=gen_idx)


def _sup(k):
    """Unicode superscript for small integers."""
    s = '⁰¹²³⁴⁵⁶⁷⁸⁹'
    return ''.join(s[int(c)] for c in str(k))


def from_Dn(n):
    """Dihedral group D_n of order 2n.
    Elements: (k, f) where k in [0,n), f in {0,1}.
    r = rotation, s = reflection.
    """
    elems = []
    labels = []
    for f in range(2):
        for k in range(n):
            elems.append((k, f))
            if f == 0:
                labels.append('e' if k == 0 else ('r' if k == 1 else f'r{_sup(k)}'))
            else:
                labels.append('s' if k == 0 else ('sr' if k == 1 else f'sr{_sup(k)}'))

    def mul(a, b):
        k = (a[0] + ((-b[0]) if a[1] else b[0])) % n
        f = a[1] ^ b[1]
        return (k, f)

    idx = {e: i for i, e in enumerate(elems)}
    m = len(elems)
    table = [[idx[mul(elems[i], elems[j])] for j in range(m)] for i in range(m)]
    return Group(labels, table, identity=idx[(0, 0)], generators=[idx[(1, 0)], idx[(0, 1)]])


def from_Sn(n):
    """Symmetric group S_n (all permutations of {0,...,n-1})."""
    from itertools import permutations as perm_iter
    perms = list(perm_iter(range(n)))
    idx = {p: i for i, p in enumerate(perms)}
    identity = tuple(range(n))

    def compose(p, q):
        return tuple(q[p[i]] for i in range(n))

    def perm_label(p):
        if p == identity:
            return 'e'
        visited = [False] * n
        cycles = []
        for i in range(n):
            if visited[i] or p[i] == i:
                continue
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(str(j))
                j = p[j]
            cycles.append('(' + ' '.join(cycle) + ')')
        return ''.join(cycles) or 'e'

    labels = [perm_label(p) for p in perms]
    m = len(perms)
    table = [[idx[compose(perms[i], perms[j])] for j in range(m)] for i in range(m)]
    
    gen_idx = []
    if n > 1:
        gen1 = tuple([1, 0] + list(range(2, n)))
        gen2 = tuple(list(range(1, n)) + [0])
        gen_idx.append(idx[gen1])
        if gen2 != gen1:
            gen_idx.append(idx[gen2])
            
    return Group(labels, table, identity=idx[identity], generators=gen_idx)


def from_table(table_2d):
    """Build a group from a raw 2D multiplication table (list of lists).
    Labels are just integers 0..n-1.
    """
    n = len(table_2d)
    labels = [str(i) for i in range(n)]
    return Group(labels, table_2d)


def from_permutation_generators(generators, n):
    """Build a group by closure from permutation generators.

    generators: list of tuples, each a permutation of {0,...,n-1}
    n: permutation degree
    Returns: ConcreteGroup
    """
    identity = tuple(range(n))
    elements = {identity}
    queue = [identity] + list(generators)
    elements.update(generators)

    while queue:
        current = queue.pop(0)
        for g in generators:
            for new in [_perm_compose(current, g, n), _perm_compose(g, current, n),
                        _perm_compose(current, _perm_inv(g, n), n),
                        _perm_compose(_perm_inv(g, n), current, n)]:
                if new not in elements:
                    elements.add(new)
                    queue.append(new)
                    if len(elements) > 1000:
                        raise ValueError(f"Group too large (>{len(elements)} elements). Aborting.")

    elements = sorted(elements)
    idx = {e: i for i, e in enumerate(elements)}

    def perm_label(p):
        if p == identity:
            return 'e'
        visited = [False] * n
        cycles = []
        for i in range(n):
            if visited[i] or p[i] == i:
                continue
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(str(j))
                j = p[j]
            cycles.append('(' + ' '.join(cycle) + ')')
        return ''.join(cycles) or 'e'

    labels = [perm_label(p) for p in elements]
    m = len(elements)
    table = [[idx[_perm_compose(elements[i], elements[j], n)] for j in range(m)] for i in range(m)]
    
    gen_indices = [idx[g] for g in generators if g in idx]
    return Group(labels, table, identity=idx[identity], generators=gen_indices)


def from_matrix_generators(generators, p):
    """Build a group by closure from matrix generators over Z_p.

    generators: list of 2D numpy arrays (square matrices)
    p: prime modulus
    Returns: ConcreteGroup
    """
    size = generators[0].shape[0]
    identity = np.eye(size, dtype=int)

    def mat_key(m):
        return tuple(m.flatten())

    def mat_mul(a, b):
        return (a @ b) % p

    def mat_inv(m):
        # Invert via Gauss-Jordan over Z_p
        n = m.shape[0]
        aug = np.hstack([m.copy(), np.eye(n, dtype=int)]) % p
        for i in range(n):
            # Find pivot
            pivot = -1
            for r in range(i, n):
                if aug[r, i] % p != 0:
                    pivot = r
                    break
            if pivot < 0:
                raise ValueError("Matrix not invertible")
            aug[[i, pivot]] = aug[[pivot, i]]
            inv_val = pow(int(aug[i, i]), p - 2, p)
            aug[i] = (aug[i] * inv_val) % p
            for r in range(n):
                if r != i and aug[r, i] != 0:
                    aug[r] = (aug[r] - aug[r, i] * aug[i]) % p
        return aug[:, n:] % p

    elements = {mat_key(identity): identity.copy()}
    queue = [identity.copy()]
    for g in generators:
        k = mat_key(g % p)
        if k not in elements:
            elements[k] = g.copy() % p
            queue.append(g.copy() % p)

    while queue:
        current = queue.pop(0)
        for g in generators:
            for new_mat in [mat_mul(current, g), mat_mul(g, current)]:
                k = mat_key(new_mat)
                if k not in elements:
                    elements[k] = new_mat
                    queue.append(new_mat)
                    if len(elements) > 500:
                        raise ValueError(f"Group too large (>{len(elements)} elements). Aborting.")

    elem_list = sorted(elements.keys())
    idx = {k: i for i, k in enumerate(elem_list)}
    mat_list = [elements[k] for k in elem_list]

    def mat_label(m):
        if np.array_equal(m, identity):
            return 'I'
        rows = [','.join(str(v) for v in row) for row in m]
        return '[' + '|'.join(rows) + ']'

    labels = [mat_label(m) for m in mat_list]
    m_count = len(elem_list)
    table = [[idx[mat_key(mat_mul(mat_list[i], mat_list[j]))] for j in range(m_count)] for i in range(m_count)]
    
    gen_indices = [idx[mat_key(g)] for g in generators if mat_key(g) in idx]
    return Group(labels, table, identity=idx[mat_key(identity)], generators=gen_indices)


# ── Helpers ──

def _perm_compose(p, q, n):
    return tuple(q[p[i]] for i in range(n))

def _perm_inv(p, n):
    inv = [0] * n
    for i, v in enumerate(p):
        inv[v] = i
    return tuple(inv)


# ────────────────────────────────────────────────────────────
# Catalog: named groups with descriptions
# ────────────────────────────────────────────────────────────

def from_presentation(generators, relations_str_list):
    import sympy
    from sympy.combinatorics.free_groups import free_group
    from sympy.combinatorics.fp_groups import FpGroup
    
    gen_str = ", ".join(generators)
    free_g, *gens = free_group(gen_str)
    if len(generators) == 1:
        gens = [gens[0]]
        
    gen_dict = {}
    for g in free_g.generators:
        gen_dict[str(g)] = g
        gen_dict[str(g).upper()] = g**-1
        
    def _parse_word(w):
        res = free_g.identity
        if w == "e" or w == "":
            return res
        for c in w:
            if c not in gen_dict:
                raise ValueError(f"Unknown generator character: {c}")
            res = res * gen_dict[c]
        return res

    sympy_rels = []
    for lhs, rhs in relations_str_list:
        w_lhs = _parse_word(lhs)
        w_rhs = _parse_word(rhs)
        rel = w_lhs * w_rhs**-1
        if not rel.is_identity:
            sympy_rels.append(rel)
            
    fp_group = FpGroup(free_g, sympy_rels)
    
    import threading
    ord_val = None
    err = None
    
    def check_order():
        nonlocal ord_val, err
        try:
            ord_val = fp_group.order()
        except Exception as e:
            err = e
            
    t = threading.Thread(target=check_order, daemon=True)
    t.start()
    t.join(timeout=2.0)
    
    if t.is_alive():
        raise ValueError("Group is infinite or too complex (Todd-Coxeter timeout).")
    if err:
        raise err
        
    if ord_val == sympy.oo:
        raise ValueError("The provided presentation defines an infinite group.")
    if ord_val > 1000:
        raise ValueError(f"Group is too large (order {ord_val}). Max allowed is 1000.")

    elements = list(fp_group.elements)
    
    def elem_to_str(e):
        if e.is_identity: return "e"
        letters = []
        for gen, power in e.array_form:
            g_str = str(gen)
            if power > 0:
                letters.append(g_str * power)
            elif power < 0:
                letters.append(g_str.upper() * (-power))
        return "".join(letters)

    labels = [elem_to_str(e) for e in elements]
    
    n = len(elements)
    table = [[0]*n for _ in range(n)]
    
    for i, a in enumerate(elements):
        for j, b in enumerate(elements):
            prod = fp_group.reduce(a * b)
            found = False
            for k, c in enumerate(elements):
                if fp_group.reduce(prod * c**-1).is_identity:
                    table[i][j] = k
                    found = True
                    break
            if not found:
                raise ValueError("Product not found in elements list!")
                
    # Identify the indices of the original generators
    gen_indices = []
    for g in free_g.generators:
        # Find which element is this generator
        for i, e in enumerate(elements):
            if fp_group.reduce(e * g**-1).is_identity:
                gen_indices.append(i)
                break
                
    return Group(labels, table, generators=gen_indices)


CATALOG = [
    ("Z_3", "ℤ₃ — cyclic, order 3, abelian", lambda: from_Zn(3)),
    ("Z_4", "ℤ₄ — cyclic, order 4, abelian", lambda: from_Zn(4)),
    ("Z_5", "ℤ₅ — cyclic, order 5, abelian", lambda: from_Zn(5)),
    ("Z_6", "ℤ₆ — cyclic, order 6, abelian", lambda: from_Zn(6)),
    ("Z_8", "ℤ₈ — cyclic, order 8, abelian", lambda: from_Zn(8)),
    ("U_5", "U(5) ≅ ℤ₄ — cyclic, order 4, abelian", lambda: from_Un(5)),
    ("U_7", "U(7) ≅ ℤ₆ — cyclic, order 6, abelian", lambda: from_Un(7)),
    ("U_8", "U(8) ≅ ℤ₂×ℤ₂ — not cyclic, order 4, abelian", lambda: from_Un(8)),
    ("U_12", "U(12) ≅ ℤ₂×ℤ₂ — not cyclic, order 4, abelian", lambda: from_Un(12)),
    ("D_3", "D₃ ≅ S₃ — dihedral, order 6, non-abelian", lambda: from_Dn(3)),
    ("D_4", "D₄ — dihedral, order 8, non-abelian", lambda: from_Dn(4)),
    ("D_5", "D₅ — dihedral, order 10, non-abelian", lambda: from_Dn(5)),
    ("D_6", "D₆ — dihedral, order 12, non-abelian", lambda: from_Dn(6)),
    ("S_3", "S₃ — symmetric, order 6, non-abelian", lambda: from_Sn(3)),
    ("S_4", "S₄ — symmetric, order 24, non-abelian", lambda: from_Sn(4)),
]
