import numpy as np
from math import gcd
from itertools import product
from .core import Group

# ────────────────────────────────────────────────────────────
# Native Subclasses for Standard Groups
# ────────────────────────────────────────────────────────────

def _sup(k):
    """Unicode superscript for small integers."""
    s = '⁰¹²³⁴⁵⁶⁷⁸⁹'
    return ''.join(s[int(c)] for c in str(k))

class ZnGroup(Group):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self._elements = [self.Element(self, i) for i in range(n)]
        self.generators = [self._elements[1 if n > 1 else 0]]
        
    def multiply(self, left, right):
        return self._elements[(left.value + right.value) % self.n]
        
    def inverse(self, element):
        return self._elements[(-element.value) % self.n]

class UnGroup(Group):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.elems = [k for k in range(1, n) if gcd(k, n) == 1]
        self.idx = {e: i for i, e in enumerate(self.elems)}
        self._elements = [self.Element(self, e) for e in self.elems]
        
        gen_idx = []
        generated = {1}
        for e in self.elems:
            if len(generated) == len(self.elems): break
            if e not in generated:
                gen_idx.append(self.idx[e])
                new_gen = set(generated)
                q = list(new_gen)
                while q:
                    c = q.pop(0)
                    for g_idx in gen_idx:
                        nxt = (c * self.elems[g_idx]) % n
                        if nxt not in new_gen:
                            new_gen.add(nxt)
                            q.append(nxt)
                generated = new_gen
        self.generators = [self._elements[i] for i in gen_idx]
        
    def multiply(self, left, right):
        return self._elements[self.idx[(left.value * right.value) % self.n]]
        
    def inverse(self, element):
        # Python 3.8+ modular inverse
        return self._elements[self.idx[pow(element.value, -1, self.n)]]

class DnGroup(Group):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.elems = []
        for f in range(2):
            for k in range(n):
                self.elems.append((k, f))
                
        self.idx = {e: i for i, e in enumerate(self.elems)}
        
        def label(k, f):
            if f == 0:
                return 'e' if k == 0 else ('r' if k == 1 else f'r{_sup(k)}')
            else:
                return 's' if k == 0 else ('sr' if k == 1 else f'sr{_sup(k)}')
                
        self._elements = [self.Element(self, e, label=label(e[0], e[1])) for e in self.elems]
        self.generators = [self._elements[self.idx[(1, 0)]], self._elements[self.idx[(0, 1)]]]
        
    def multiply(self, left, right):
        a = left.value
        b = right.value
        k = (a[0] + ((-b[0]) if a[1] else b[0])) % self.n
        f = a[1] ^ b[1]
        return self._elements[self.idx[(k, f)]]
        
    def inverse(self, element):
        a = element.value
        if a[1] == 1:
            return element
        else:
            return self._elements[self.idx[((-a[0]) % self.n, 0)]]

class SnGroup(Group):
    def __init__(self, n):
        super().__init__()
        self.n = n
        from itertools import permutations as perm_iter
        self.perms = list(perm_iter(range(n)))
        self.idx = {p: i for i, p in enumerate(self.perms)}
        self.identity_tuple = tuple(range(n))
        
        def perm_label(p):
            if p == self.identity_tuple:
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
            
        self._elements = [self.Element(self, p, label=perm_label(p)) for p in self.perms]
        
        gen_idx = []
        if n > 1:
            gen1 = tuple([1, 0] + list(range(2, n)))
            gen2 = tuple(list(range(1, n)) + [0])
            gen_idx.append(self.idx[gen1])
            if gen2 != gen1:
                gen_idx.append(self.idx[gen2])
        self.generators = [self._elements[i] for i in gen_idx]
        
    def multiply(self, left, right):
        p = left.value
        q = right.value
        new_val = tuple(q[p[i]] for i in range(self.n))
        return self._elements[self.idx[new_val]]
        
    def inverse(self, element):
        p = element.value
        inv = [0] * self.n
        for i, v in enumerate(p):
            inv[v] = i
        return self._elements[self.idx[tuple(inv)]]

class TableGroup(Group):
    """Reserved for dynamically generated tables (matrices, presentations, UI experiments)."""
    def __init__(self, labels, table, generators=None):
        super().__init__()
        self.table = table
        self._elements = [self.Element(self, i, label=labels[i]) for i in range(len(labels))]
        if generators:
            self.generators = [self._elements[g] for g in generators if g is not None]

    def multiply(self, left, right):
        return self._elements[int(self.table[left.value][right.value])]
        
    def inverse(self, element):
        # Uses student's find_identity via identity_element
        ident = self.identity_element
        for e in self._elements:
            if self.multiply(element, e) == ident:
                return e
        raise ValueError("Inverse not found in table.")


# ────────────────────────────────────────────────────────────
# Factory methods
# ────────────────────────────────────────────────────────────

def from_Zn(n): return ZnGroup(n)
def from_Un(n): return UnGroup(n)
def from_Dn(n): return DnGroup(n)
def from_Sn(n): return SnGroup(n)

def from_table(table_2d):
    n = len(table_2d)
    return TableGroup([str(i) for i in range(n)], table_2d)

def from_permutation_generators(generators, n):
    def _perm_compose(p, q, n): return tuple(q[p[i]] for i in range(n))
    def _perm_inv(p, n):
        inv = [0] * n
        for i, v in enumerate(p): inv[v] = i
        return tuple(inv)

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
        if p == identity: return 'e'
        visited = [False] * n
        cycles = []
        for i in range(n):
            if visited[i] or p[i] == i: continue
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
    return TableGroup(labels, table, generators=gen_indices)

def from_matrix_generators(generators, p):
    size = generators[0].shape[0]
    identity = np.eye(size, dtype=int)

    def mat_key(m): return tuple(m.flatten())
    def mat_mul(a, b): return (a @ b) % p

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
        if np.array_equal(m, identity): return 'I'
        rows = [','.join(str(v) for v in row) for row in m]
        return '[' + '|'.join(rows) + ']'

    labels = [mat_label(m) for m in mat_list]
    m_count = len(elem_list)
    table = [[idx[mat_key(mat_mul(mat_list[i], mat_list[j]))] for j in range(m_count)] for i in range(m_count)]
    gen_indices = [idx[mat_key(g)] for g in generators if mat_key(g) in idx]
    return TableGroup(labels, table, generators=gen_indices)

def from_presentation(generators, relations_str_list):
    import sympy
    from sympy.combinatorics.free_groups import free_group
    from sympy.combinatorics.fp_groups import FpGroup
    
    gen_str = ", ".join(generators)
    free_g, *gens = free_group(gen_str)
    if len(generators) == 1: gens = [gens[0]]
        
    gen_dict = {}
    for g in free_g.generators:
        gen_dict[str(g)] = g
        gen_dict[str(g).upper()] = g**-1
        
    def _parse_word(w):
        res = free_g.identity
        if w == "e" or w == "": return res
        for c in w:
            if c not in gen_dict: raise ValueError(f"Unknown generator character: {c}")
            res = res * gen_dict[c]
        return res

    sympy_rels = []
    for lhs, rhs in relations_str_list:
        w_lhs = _parse_word(lhs)
        w_rhs = _parse_word(rhs)
        rel = w_lhs * w_rhs**-1
        if not rel.is_identity: sympy_rels.append(rel)
            
    fp_group = FpGroup(free_g, sympy_rels)
    
    import threading
    ord_val = None
    err = None
    
    def check_order():
        nonlocal ord_val, err
        try: ord_val = fp_group.order()
        except Exception as e: err = e
            
    t = threading.Thread(target=check_order, daemon=True)
    t.start()
    t.join(timeout=2.0)
    
    if t.is_alive(): raise ValueError("Group is infinite or too complex (Todd-Coxeter timeout).")
    if err: raise err
        
    if ord_val == sympy.oo: raise ValueError("The provided presentation defines an infinite group.")
    if ord_val > 1000: raise ValueError(f"Group is too large (order {ord_val}). Max allowed is 1000.")

    elements = list(fp_group.elements)
    
    def elem_to_str(e):
        if e.is_identity: return "e"
        letters = []
        for gen, power in e.array_form:
            g_str = str(gen)
            if power > 0: letters.append(g_str * power)
            elif power < 0: letters.append(g_str.upper() * (-power))
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
            if not found: raise ValueError("Product not found in elements list!")
                
    gen_indices = []
    for g in free_g.generators:
        for i, e in enumerate(elements):
            if fp_group.reduce(e * g**-1).is_identity:
                gen_indices.append(i)
                break
                
    return TableGroup(labels, table, generators=gen_indices)

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
