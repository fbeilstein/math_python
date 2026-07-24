"""
Implementation tasks for the Group Theory Laboratory.

Phase 1 (L1–L3): Build the representations.
Phase 2 (L4–L7): Structural analysis.

Each function has a docstring specifying the expected behavior.
"""
import numpy as np


# ════════════════════════════════════════════════════════════
# Level 1: Axiom Checker
# ════════════════════════════════════════════════════════════

def check_closure(table):  #contains solution
    """Check if all entries in the multiplication table are valid elements.

    Args:
        table: list of lists (n x n), entries are integers.
    Returns:
        bool: True if closed, False otherwise.
    """
    n = len(table)
    valid = set(range(n))
    for i in range(n):
        for j in range(n):
            if table[i][j] not in valid:
                return False
    return True


def check_associativity(table):  #contains solution
    """Check if the operation defined by the table is associative.

    Args:
        table: list of lists (n x n).
    Returns:
        bool: True if associative, False otherwise.
    """
    n = len(table)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if table[table[a][b]][c] != table[a][table[b][c]]:
                    return False
    return True


def find_identity(table):  #contains solution
    """Find the identity element in the multiplication table.

    Args:
        table: list of lists (n x n).
    Returns:
        int or None: index of the identity element, or None if none exists.
    """
    n = len(table)
    for e in range(n):
        is_id = True
        for i in range(n):
            if table[e][i] != i or table[i][e] != i:
                is_id = False
                break
        if is_id:
            return e
    return None


def check_inverses(table, identity):  #contains solution
    """Check if every element has an inverse.

    Args:
        table: list of lists (n x n).
        identity: int, index of the identity element.
    Returns:
        bool: True if every element has an inverse, False otherwise.
    """
    n = len(table)
    for a in range(n):
        found = False
        for b in range(n):
            if table[a][b] == identity and table[b][a] == identity:
                found = True
                break
        if not found:
            return False
    return True


# ════════════════════════════════════════════════════════════
# Level 2: Permutation Engine
# ════════════════════════════════════════════════════════════

def compose_permutations(p, q):  #contains solution
    """Compose two permutations: return p ∘ q (apply q first, then p).

    Args:
        p, q: lists of length n, each a permutation of {0,...,n-1}.
    Returns:
        list: the composition p(q(i)) for each i.
    """
    return [p[q[i]] for i in range(len(p))]


def inverse_permutation(p):  #contains solution
    """Return the inverse of permutation p.

    Args:
        p: list of length n, a permutation of {0,...,n-1}.
    Returns:
        list: p⁻¹ such that compose(p, p⁻¹) = identity.
    """
    n = len(p)
    inv = [0] * n
    for i in range(n):
        inv[p[i]] = i
    return inv


def permutation_order(p):  #contains solution
    """Return the order of permutation p (smallest k ≥ 1 with p^k = id).

    Args:
        p: list of length n, a permutation of {0,...,n-1}.
    Returns:
        int: the order.
    """
    identity = list(range(len(p)))
    current = list(p)
    for k in range(1, len(p) * len(p) + 2):
        if current == identity:
            return k
        current = compose_permutations(list(p), current)
    return -1


def one_line_to_cycles(perm):  #contains solution
    """Convert one-line notation to cycle notation.

    Args:
        perm: list of length n, a permutation of {0,...,n-1}.
    Returns:
        list of lists: e.g. [[0,2,1], [3,4]] for cycles (0 2 1)(3 4).
                       Fixed points are omitted.
                       Empty list [] means the identity.
    """
    n = len(perm)
    visited = [False] * n
    cycles = []
    for i in range(n):
        if visited[i] or perm[i] == i:
            continue
        cycle = []
        j = i
        while not visited[j]:
            visited[j] = True
            cycle.append(j)
            j = perm[j]
        cycles.append(cycle)
    return cycles


def cycles_to_one_line(cycles, n):  #contains solution
    """Convert cycle notation to one-line notation.

    Args:
        cycles: list of lists, e.g. [[0,2,1], [3,4]].
        n: total number of elements.
    Returns:
        list: one-line notation as a list of length n.
    """
    perm = list(range(n))
    for cycle in cycles:
        for i in range(len(cycle)):
            perm[cycle[i]] = cycle[(i + 1) % len(cycle)]
    return perm


def generate_permutation_group(generators, n):  #contains solution
    """Generate all permutations in ⟨generators⟩ by closure.

    Args:
        generators: list of lists, each a permutation of {0,...,n-1}.
        n: number of elements being permuted.
    Returns:
        list of lists: all permutations in the generated group,
                       including the identity.
    """
    identity = list(range(n))
    group = {tuple(identity)}
    queue = [tuple(g) for g in generators]
    group.update(queue)
    while queue:
        current = queue.pop(0)
        for g in list(group):
            for new in [compose_permutations(list(current), list(g)),
                        compose_permutations(list(g), list(current))]:
                t = tuple(new)
                if t not in group:
                    group.add(t)
                    queue.append(t)
    return [list(p) for p in group]


def is_even_permutation(p):  #contains solution
    """Determine if a permutation is even (True) or odd (False).

    Args:
        p: list of length n, a permutation of {0,...,n-1}.
    Returns:
        bool: True if even, False if odd.
    """
    cycles = one_line_to_cycles(p)
    transpositions = sum(len(c) - 1 for c in cycles)
    return transpositions % 2 == 0


# ════════════════════════════════════════════════════════════
# Level 3: Cayley Graph (BFS)
# ════════════════════════════════════════════════════════════

def generate_cayley_graph(group, generator_indices):  #contains solution
    """Build the Cayley graph of a group via BFS, finding all connected components.

    Args:
        group: a ConcreteGroup instance.
        generator_indices: list of int, indices of the generators.
    Returns:
        (nodes, edges):
            nodes: list of int (all element indices in BFS discovery order)
            edges: list of (from_idx, gen_idx, to_idx) for the full graph
    """
    nodes = []
    edges = []
    visited = set()

    for start_node in range(group.order):
        if start_node in visited:
            continue
            
        queue = [start_node]
        visited.add(start_node)
        nodes.append(start_node)
        
        while queue:
            current = queue.pop(0)
            for g in generator_indices:
                target = group.multiply(current, g)
                edges.append((current, g, target))
                if target not in visited:
                    visited.add(target)
                    queue.append(target)
                    nodes.append(target)

    return nodes, edges


# ════════════════════════════════════════════════════════════
# Level 4: Subgroups & Lagrange
# ════════════════════════════════════════════════════════════

def generate_subgroup(group, generator_indices):  #contains solution
    """Generate the subgroup ⟨generators⟩ by closure.

    Args:
        group: a ConcreteGroup instance.
        generator_indices: list of int, indices of the generators.
    Returns:
        set of int: the element indices forming the subgroup.
    """
    subgroup = {group.identity}
    queue = list(generator_indices)
    subgroup.update(generator_indices)

    while queue:
        current = queue.pop(0)
        for g in list(subgroup):
            for new in [group.multiply(current, g), group.multiply(g, current)]:
                if new not in subgroup:
                    subgroup.add(new)
                    queue.append(new)
    return subgroup


def find_all_subgroups(group):  #contains solution
    """Find all subgroups of the group.

    Args:
        group: a ConcreteGroup instance.
    Returns:
        list of frozenset: each frozenset is a subgroup (set of element indices).
    """
    subgroups = set()
    # The trivial subgroup and the full group
    subgroups.add(frozenset([group.identity]))
    subgroups.add(frozenset(range(group.order)))

    # Generate subgroup from each element
    for i in range(group.order):
        sg = generate_subgroup(group, [i])
        subgroups.add(frozenset(sg))

    # Generate from each pair of elements
    for i in range(group.order):
        for j in range(i + 1, group.order):
            sg = generate_subgroup(group, [i, j])
            subgroups.add(frozenset(sg))

    return sorted(subgroups, key=lambda s: (len(s), sorted(s)))


# ════════════════════════════════════════════════════════════
# Level 5: Cosets & Normality
# ════════════════════════════════════════════════════════════

def compute_left_cosets(group, subgroup):  #contains solution
    """Compute the left cosets gH of a subgroup H.

    Args:
        group: a ConcreteGroup instance.
        subgroup: set of int (element indices forming H).
    Returns:
        list of frozenset: the distinct left cosets.
    """
    cosets = []
    covered = set()
    for g in range(group.order):
        if g in covered:
            continue
        coset = frozenset(group.multiply(g, h) for h in subgroup)
        cosets.append(coset)
        covered.update(coset)
    return cosets


def compute_right_cosets(group, subgroup):  #contains solution
    """Compute the right cosets Hg of a subgroup H.

    Args:
        group: a ConcreteGroup instance.
        subgroup: set of int (element indices forming H).
    Returns:
        list of frozenset: the distinct right cosets.
    """
    cosets = []
    covered = set()
    for g in range(group.order):
        if g in covered:
            continue
        coset = frozenset(group.multiply(h, g) for h in subgroup)
        cosets.append(coset)
        covered.update(coset)
    return cosets


def is_normal(group, subgroup):  #contains solution
    """Check if a subgroup is normal (left cosets == right cosets).

    Args:
        group: a ConcreteGroup instance.
        subgroup: set of int (element indices forming H).
    Returns:
        bool: True if H is normal in G.
    """
    left = set(frozenset(group.multiply(g, h) for h in subgroup) for g in range(group.order))
    right = set(frozenset(group.multiply(h, g) for h in subgroup) for g in range(group.order))
    return left == right


# ════════════════════════════════════════════════════════════
# Level 6: Center, Commutator, Conjugacy
# ════════════════════════════════════════════════════════════

def compute_center(group):  #contains solution
    """Compute the center Z(G) = {z : zg = gz for all g}.

    Args:
        group: a ConcreteGroup instance.
    Returns:
        set of int: element indices forming the center.
    """
    center = set()
    for z in range(group.order):
        if all(group.multiply(z, g) == group.multiply(g, z) for g in range(group.order)):
            center.add(z)
    return center


def compute_commutator_subgroup(group):  #contains solution
    """Compute the commutator subgroup [G,G] = ⟨aba⁻¹b⁻¹⟩.

    Args:
        group: a ConcreteGroup instance.
    Returns:
        set of int: element indices forming [G,G].
    """
    commutators = set()
    for a in range(group.order):
        for b in range(group.order):
            # aba⁻¹b⁻¹
            ab = group.multiply(a, b)
            a_inv = group.inverse(a)
            b_inv = group.inverse(b)
            comm = group.multiply(group.multiply(ab, a_inv), b_inv)
            commutators.add(comm)
    # Close under multiplication
    return generate_subgroup(group, list(commutators))


def compute_conjugacy_classes(group):  #contains solution
    """Partition G into conjugacy classes.

    Args:
        group: a ConcreteGroup instance.
    Returns:
        list of frozenset: each frozenset is a conjugacy class.
    """
    assigned = [False] * group.order
    classes = []
    for a in range(group.order):
        if assigned[a]:
            continue
        cls = set()
        for g in range(group.order):
            # gag⁻¹
            conj = group.multiply(group.multiply(g, a), group.inverse(g))
            cls.add(conj)
        for c in cls:
            assigned[c] = True
        classes.append(frozenset(cls))
    return classes


# ════════════════════════════════════════════════════════════
# Level 7: Homomorphisms & Kernels
# ════════════════════════════════════════════════════════════

def deduce_homomorphism(group_G, group_H, partial_phi):
    """Attempt to deduce the rest of a homomorphism mapping.
    
    Args:
        group_G, group_H: ConcreteGroup instances.
        partial_phi: dict of {g_idx: h_idx} representing manually drawn arrows.
        
    Returns:
        (completed_phi: dict, error: str|None)
    """
    # Homomorphisms always map identity to identity
    if group_G.identity in partial_phi:
        if partial_phi[group_G.identity] != group_H.identity:
            return partial_phi, f"Contradiction: Identity of G must map to identity of H."

    poss = {}
    for g in range(group_G.order):
        if g in partial_phi:
            poss[g] = {partial_phi[g]}
        else:
            poss[g] = set(range(group_H.order))
            
    # Enforce identity mapping
    poss[group_G.identity] = {group_H.identity}
    
    changed = True
    while changed:
        changed = False
        
        for a in range(group_G.order):
            for b in range(group_G.order):
                ab = group_G.multiply(a, b)
                
                # Check valid assignments for unique elements among a, b, ab
                elements = list(set([a, b, ab]))
                valid_assignments = []
                
                def search(idx, current_assignment):
                    if idx == len(elements):
                        h_a = current_assignment[a]
                        h_b = current_assignment[b]
                        h_ab = current_assignment[ab]
                        if group_H.multiply(h_a, h_b) == h_ab:
                            valid_assignments.append(current_assignment.copy())
                        return
                    elem = elements[idx]
                    for h in poss[elem]:
                        current_assignment[elem] = h
                        search(idx + 1, current_assignment)
                        del current_assignment[elem]
                        
                search(0, {})
                
                if not valid_assignments:
                    return partial_phi, f"Contradiction detected at φ({group_G.label(a)}·{group_G.label(b)})"
                    
                # Rebuild poss
                new_poss = {e: set() for e in elements}
                for asgn in valid_assignments:
                    for e in elements:
                        new_poss[e].add(asgn[e])
                        
                for e in elements:
                    if len(new_poss[e]) < len(poss[e]):
                        poss[e] = new_poss[e]
                        changed = True

    # Reconstruct deduced phi
    result_phi = {}
    for g, p in poss.items():
        if len(p) == 1:
            result_phi[g] = list(p)[0]
        elif len(p) == 0:
            return partial_phi, f"Contradiction: No valid mapping for {group_G.label(g)}"
            
    return result_phi, None


def is_homomorphism(group_G, group_H, phi):  #contains solution
    """Check if phi: G -> H is a group homomorphism.

    Args:
        group_G, group_H: ConcreteGroup instances.
        phi: dict or list where phi[i] is the image of element i of G in H.
    Returns:
        bool: True if phi is a homomorphism, False otherwise.
    """
    for a in range(group_G.order):
        for b in range(group_G.order):
            # Also gracefully handle incomplete maps if phi is a dict
            if isinstance(phi, dict):
                if a not in phi or b not in phi or group_G.multiply(a, b) not in phi:
                    return False
            if phi[group_G.multiply(a, b)] != group_H.multiply(phi[a], phi[b]):
                return False
    return True


def compute_kernel(group_G, group_H, phi):  #contains solution
    """Compute the kernel of a homomorphism phi: G -> H.

    Args:
        group_G, group_H: ConcreteGroup instances.
        phi: dict or list, the homomorphism.
    Returns:
        set of int: element indices in G that map to the identity of H.
    """
    if isinstance(phi, dict):
        return {g for g in range(group_G.order) if g in phi and phi[g] == group_H.identity}
    return {g for g in range(group_G.order) if phi[g] == group_H.identity}


def compute_image(group_G, group_H, phi):  #contains solution
    """Compute the image of a homomorphism phi: G -> H.

    Args:
        group_G, group_H: ConcreteGroup instances.
        phi: dict or list, the homomorphism.
    Returns:
        set of int: element indices in H that are in the image.
    """
    if isinstance(phi, dict):
        return {phi[g] for g in range(group_G.order) if g in phi}
    return {phi[g] for g in range(group_G.order)}
