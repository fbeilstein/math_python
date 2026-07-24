"""
Implementation tasks for the Group Theory Laboratory.

Phase 1 (L1–L3): Build the representations.
Phase 2 (L4–L7): Structural analysis.

Each function has a docstring specifying the expected behavior.
"""
import numpy as np
from group_engine import GroupElement, Group


# ════════════════════════════════════════════════════════════
# Level 1: Axiom Checker
# ════════════════════════════════════════════════════════════

def check_closure(elements):  #contains solution
    """Check if the set of elements is closed under multiplication.

    Args:
        elements: list or set of abstract GroupElement objects.
    Returns:
        bool: True if closed, False otherwise.
    """
    return all(a * b in elements for a in elements for b in elements)


def check_associativity(elements):  #contains solution
    """Check if the multiplication operation is associative.

    Args:
        elements: list or set of abstract GroupElement objects.
    Returns:
        bool: True if associative, False otherwise.
    """
    return all((a * b) * c == a * (b * c) for a in elements for b in elements for c in elements)


def find_identity(elements):  #contains solution
    """Find the identity element.

    Args:
        elements: list or set of abstract GroupElement objects.
    Returns:
        GroupElement or None: the identity element, or None if none exists.
    """
    return next((e for e in elements if all(e * a == a and a * e == a for a in elements)), None)


def check_inverses(elements, identity):  #contains solution
    """Check if every element has an inverse.

    Args:
        elements: list or set of abstract GroupElement objects.
        identity: the identity GroupElement.
    Returns:
        bool: True if every element has an inverse, False otherwise.
    """
    return all(any(a * b == identity and b * a == identity for b in elements) for a in elements)


class PermutationElement(GroupElement):
    """A permutation element that implements GroupElement abstract methods."""
    def __init__(self, mapping):
        """
        Args:
            mapping: iterable of length n, a permutation of {0,...,n-1}.
        """
        super().__init__(tuple(mapping))
        
    @property
    def mapping(self):
        return self._value
        
    def __mul__(self, other):  #contains solution
        """Compose self * other (apply other first, then self)."""
        n = len(self._value)
        return PermutationElement([self._value[other._value[i]] for i in range(n)])
        
    def __invert__(self):  #contains solution
        """Return the inverse permutation."""
        n = len(self._value)
        inv = [0] * n
        for i in range(n):
            inv[self._value[i]] = i
        return PermutationElement(inv)


def element_order(group, g):  #contains solution
    """Return the order of any abstract group element g.

    Args:
        group: an object of type Group.
        g: an abstract GroupElement inside the group.
    Returns:
        int: the order of the element.
    """
    identity = group.get_identity()
    current = g
    order = 1
    while current != identity:
        current = current * g
        order += 1
    return order


def generate_group(generators):  #contains solution
    """Generate all elements in ⟨generators⟩ by closure.

    Args:
        generators: list of abstract GroupElement objects.
    Returns:
        Group: the group object.
    """
    if not generators:
        return Group(elements=[])

    # We can get the identity by multiplying the first generator by its inverse
    identity = generators[0] * ~generators[0]
    
    group = Group(elements=[identity])
    queue = [g for g in generators]
    group.add_elements(queue)
    
    while queue:
        current = queue.pop(0)
        for g in list(group):
            for new in [current * g, g * current]:
                if new not in group:
                    group.add(new)
                    queue.append(new)
    return group


# ════════════════════════════════════════════════════════════
# Level 3: Cayley Graph (BFS)
# ════════════════════════════════════════════════════════════

def generate_cayley_graph(group, generators):  #contains solution
    """Generate the Cayley graph edges for a given set of generators.

    Args:
        group: abstract Group object forming G.
        generators: list of abstract GroupElement objects.
    Returns:
        tuple (nodes, edges) where nodes is a list of GroupElements and 
        edges is a list of tuples (source, generator, target).
    """
    visited = set()
    edges = []
    nodes = []

    # Iterate over all elements to ensure we find all connected components
    for start_node in group:
        if start_node in visited:
            continue
            
        queue = [start_node]
        visited.add(start_node)
        nodes.append(start_node)
        
        while queue:
            current = queue.pop(0)
            for g in generators:
                target = current * g
                edges.append((current, g, target))
                if target not in visited:
                    visited.add(target)
                    queue.append(target)
                    nodes.append(target)

    return nodes, edges


# ════════════════════════════════════════════════════════════
# Level 4: Subgroups & Lagrange
# ════════════════════════════════════════════════════════════




def find_all_subgroups(group):  #contains solution
    """Find all subgroups of the group using a mathematically rigorous lattice exploration.

    Args:
        group: abstract Group object.
    Returns:
        list of Group: each Group is a subgroup.
    """
    if not group: return []
    
    e = group.identity_element
    
    # Store Group objects to easily track unique subgroups
    # We can use Group directly because it has __hash__ and __eq__ implemented
    subgroup_sets = {Group(elements=[e])}
    queue = [Group(elements=[e])]
    
    # Breadth-first exploration of the subgroup lattice
    while queue:
        current_sg = queue.pop(0)
        
        for g in group:
            if g not in current_sg.elements:
                # Generate a new subgroup by adding g to the current subgroup
                new_group = generate_group(list(current_sg.elements) + [g])
                
                if new_group not in subgroup_sets:
                    subgroup_sets.add(new_group)
                    queue.append(new_group)
                    
    return list(subgroup_sets)


# ════════════════════════════════════════════════════════════
# Level 5: Cosets & Normality
# ════════════════════════════════════════════════════════════

def compute_left_cosets(group, subgroup):  #contains solution
    """Compute the left cosets gH of a subgroup H.

    Args:
        group: abstract Group object forming G.
        subgroup: abstract Group object forming H.
    Returns:
        list of set: the distinct left cosets.
    """
    cosets = []
    covered = set()
    for g in group:
        if g in covered:
            continue
        coset = set(g * h for h in subgroup)
        cosets.append(coset)
        covered.update(coset)
    return cosets


def compute_right_cosets(group, subgroup):  #contains solution
    """Compute the right cosets Hg of a subgroup H.

    Args:
        group: abstract Group object forming G.
        subgroup: abstract Group object forming H.
    Returns:
        list of set: the distinct right cosets.
    """
    cosets = []
    covered = set()
    for g in group:
        if g in covered:
            continue
        coset = set(h * g for h in subgroup)
        cosets.append(coset)
        covered.update(coset)
    return cosets


def is_normal(group, subgroup):  #contains solution
    """Check if a subgroup is normal (gH = Hg for all g).

    Args:
        group: abstract Group object forming G.
        subgroup: abstract Group object forming H.
    Returns:
        bool: True if H is normal in G.
    """
    # Compare left and right cosets
    left_cosets = compute_left_cosets(group, subgroup)
    right_cosets = compute_right_cosets(group, subgroup)
    
    # Sort them for list comparison since sets of sets are tricky
    sort_key = lambda c: sorted([str(x) for x in c])
    return sorted(left_cosets, key=sort_key) == sorted(right_cosets, key=sort_key)


# ════════════════════════════════════════════════════════════
# Level 6: Center, Commutator, Conjugacy
# ════════════════════════════════════════════════════════════

def compute_center(group):  #contains solution
    """Compute the center of the group Z(G).

    Args:
        group: abstract Group object forming G.
    Returns:
        set of GroupElement: elements that commute with all other elements.
    """
    center = set()
    for z in group:
        if all(z * g == g * z for g in group):
            center.add(z)
    return center


def compute_commutator_subgroup(group):  #contains solution
    """Compute the commutator subgroup [G, G].

    Args:
        group: abstract Group object forming G.
    Returns:
        Group: the commutator subgroup.
    """
    commutators = set()
    for a in group:
        for b in group:
            comm = a * b * ~a * ~b
            commutators.add(comm)
    return generate_group(list(commutators))


def compute_conjugacy_classes(group):  #contains solution
    """Partition G into conjugacy classes.

    Args:
        group: abstract Group object forming G.
    Returns:
        list of set: each set is a conjugacy class.
    """
    assigned = set()
    classes = []
    for a in group:
        if a in assigned:
            continue
        cls = set()
        for g in group:
            conj = g * a * ~g
            cls.add(conj)
        assigned.update(cls)
        classes.append(cls)
    return classes


# ════════════════════════════════════════════════════════════
# Level 7: Homomorphisms & Kernels
# ════════════════════════════════════════════════════════════

def deduce_homomorphism(group_G, group_H, partial_phi):
    """Deduce a homomorphism by BFS closure of φ(ab) = φ(a)·φ(b).

    Structurally identical to generate_group, operating on (key, value) pairs.

    Args:
        group_G, group_H: Group instances.
        partial_phi: dict {GroupElement: GroupElement}, the known arrows.

    Returns:
        dict or None: the (possibly partial) completed mapping, or None on contradiction.
    """
    e_G, e_H = group_G.identity_element, group_H.identity_element
    if e_G in partial_phi and partial_phi[e_G] != e_H:
        return None

    poss = {}
    for g in group_G:
        if g in partial_phi:
            poss[g] = {partial_phi[g]}
        else:
            poss[g] = set(group_H)
            
    # Enforce identity mapping
    poss[e_G] = {e_H}
    
    changed = True
    while changed:
        changed = False
        
        for a in group_G:
            for b in group_G:
                ab = a * b
                
                # Check valid assignments for unique elements among a, b, ab
                elements = list(set([a, b, ab]))
                valid_assignments = []
                
                def search(idx, current_assignment):
                    if idx == len(elements):
                        h_a = current_assignment[a]
                        h_b = current_assignment[b]
                        h_ab = current_assignment[ab]
                        if h_a * h_b == h_ab:
                            valid_assignments.append(current_assignment.copy())
                        return
                    elem = elements[idx]
                    for h in poss[elem]:
                        current_assignment[elem] = h
                        search(idx + 1, current_assignment)
                        del current_assignment[elem]
                        
                search(0, {})
                
                if not valid_assignments:
                    return None
                    
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
            return None
            
    return result_phi


def is_homomorphism(group_G, phi):  #contains solution
    """Check if phi: G -> H is a group homomorphism.

    Args:
        group_G: abstract Group object forming G.
        phi: dict where phi[g] is the image of element g.
    Returns:
        bool: True if phi is a homomorphism, False otherwise.
    """
    for a in group_G:
        for b in group_G:
            # Also gracefully handle incomplete maps if phi is a dict
            if a not in phi or b not in phi or (a * b) not in phi:
                return False
            if phi[a * b] != phi[a] * phi[b]:
                return False
    return True


def compute_kernel(group_G, group_H, phi):  #contains solution
    """Compute the kernel of a homomorphism phi: G -> H.

    Args:
        group_G: abstract Group object forming G.
        group_H: abstract Group object forming H.
        phi: dict, the homomorphism.
    Returns:
        set of GroupElement: elements in G that map to the identity of H.
    """
    e_H = group_H.identity_element
    return {g for g in group_G if g in phi and phi[g] == e_H}


def compute_image(group_G, group_H, phi):  #contains solution
    """Compute the image of a homomorphism phi: G -> H.

    Args:
        group_G: abstract Group object forming G.
        group_H: abstract Group object forming H.
        phi: dict, the homomorphism.
    Returns:
        set of GroupElement: elements in H that are in the image.
    """
    return {phi[g] for g in group_G if g in phi}
