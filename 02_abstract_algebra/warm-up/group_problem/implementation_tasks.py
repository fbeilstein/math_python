"""
Implementation tasks for the Group Theory Laboratory.

Phase 1 (L1–L3): Build the representations.
Phase 2 (L4–L7): Structural analysis.

Each function has a docstring specifying the expected behavior.
"""
import numpy as np
from itertools import product
from group_engine import Group


# ════════════════════════════════════════════════════════════
# Level 1: Axiom Checker
# ════════════════════════════════════════════════════════════

def check_closure(elements):  #contains solution
    """Check if the set of elements is closed under multiplication.

    Args:
        elements (list[Group.Element] | set[Group.Element]): A collection of group elements to test.
    Returns:
        bool: True if closed, False otherwise.
    """
    return all(a * b in elements for a in elements for b in elements)


def check_associativity(elements):  #contains solution
    """Check if the multiplication operation is associative.

    Args:
        elements (list[Group.Element] | set[Group.Element]): A collection of group elements to test.
    Returns:
        bool: True if associative, False otherwise.
    """
    return all((a * b) * c == a * (b * c) for a in elements for b in elements for c in elements)


def find_identity(elements):  #contains solution
    """Find the identity element.

    Args:
        elements (list[Group.Element] | set[Group.Element]): A collection of group elements to test.
    Returns:
        Group.Element or None: the identity element, or None if none exists.
    """
    return next((e for e in elements if all(e * a == a and a * e == a for a in elements)), None)


def check_inverses(elements, identity):  #contains solution
    """Check if every element has an inverse.

    Args:
        elements (list[Group.Element] | set[Group.Element]): A collection of group elements to test.
        identity (Group.Element): the identity element.
    Returns:
        bool: True if every element has an inverse, False otherwise.
    """
    return all(any(a * b == identity and b * a == identity for b in elements) for a in elements)


# ════════════════════════════════════════════════════════════
# Level 2: Permutation Group
# ════════════════════════════════════════════════════════════

class PermutationGroup(Group):
    """Level 2 Task: Implement permutation multiplication and inversion."""
    
    def multiply(self, left, right):  #contains solution
        """Compose two permutations.
        
        Args:
            left (Group.Element): The first permutation element. 
                `left.value` is a tuple representing its one-line notation.
            right (Group.Element): The second permutation element.
                `right.value` is a tuple representing its one-line notation.
        Returns:
            Group.Element: A new Element that belongs to this group.
            Note: Use `self.Element(self, new_value)` to construct and return it.
        """
        n = len(left.value)
        new_mapping = [left.value[right.value[i]] for i in range(n)]
        return self.Element(self, new_mapping)
        
    def inverse(self, element):  #contains solution
        """Find the inverse permutation.
        
        Args:
            element (Group.Element): The permutation to invert. 
                `element.value` is a tuple representing its one-line notation.
        Returns:
            Group.Element: A new Element that belongs to this group.
            Note: Use `self.Element(self, new_value)` to construct and return it.
        """
        n = len(element.value)
        inv = [0] * n
        for i in range(n):
            inv[element.value[i]] = i
        return self.Element(self, inv)


def element_order(group, g):  #contains solution
    """Return the order of any abstract group element g.

    Args:
        group (Group): an object of type Group.
        g (Group.Element): an abstract element inside the group.
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
        generators: list of abstract Group.Element objects.
    Returns:
        Group: the group object.
        
    Note: To create a new generic subgroup from scratch, use `Group(elements=[...])`.
    You can then use `group.add(element)` to add newly generated elements to it.
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
# Level 3: Cayley Graph
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

def deduce_homomorphism(group_G, group_H, partial_phi):  #contains solution
    """
    Deduce mappings using Constraint Satisfaction.
    Evaluates both local element orders and global algebraic structure.
    """
    # 1. Local Constraint: Seed domains using the Order Theorem
    poss = {
        g: {partial_phi[g]} if g in partial_phi else 
           {h for h in group_H if element_order(group_G, g) % element_order(group_H, h) == 0}
        for g in group_G
    }
    
    for g in poss:
        if not poss[g]: return {}

    # 2. Global Constraint: Iteratively enforce φ(a)·φ(b) = φ(ab)
    # We use full Arc-Consistency, propagating constraints both forward and backward.
    changed = True
    while changed:
        changed = False
        for a in group_G:
            for b in group_G:
                c = a * b
                
                if a == b:
                    # Forward: tighten c = a^2
                    valid_c = {ha * ha for ha in poss[a]}
                    new_poss_c = poss[c] & valid_c
                    if not new_poss_c: return {}
                    if len(new_poss_c) < len(poss[c]):
                        poss[c] = new_poss_c
                        changed = True
                        
                    # Backward: tighten a based on c
                    valid_a = {ha for ha in poss[a] if (ha * ha) in poss[c]}
                    if not valid_a: return {}
                    if len(valid_a) < len(poss[a]):
                        poss[a] = valid_a
                        changed = True
                else:
                    # Forward: tighten c = a * b
                    valid_c = {ha * hb for ha in poss[a] for hb in poss[b]}
                    new_poss_c = poss[c] & valid_c
                    if not new_poss_c: return {}
                    if len(new_poss_c) < len(poss[c]):
                        poss[c] = new_poss_c
                        changed = True
                        
                    # Backward: tighten a = c * b^-1
                    valid_a = {hc * (~hb) for hc in poss[c] for hb in poss[b]}
                    new_poss_a = poss[a] & valid_a
                    if not new_poss_a: return {}
                    if len(new_poss_a) < len(poss[a]):
                        poss[a] = new_poss_a
                        changed = True
                        
                    # Backward: tighten b = a^-1 * c
                    valid_b = {(~ha) * hc for hc in poss[c] for ha in poss[a]}
                    new_poss_b = poss[b] & valid_b
                    if not new_poss_b: return {}
                    if len(new_poss_b) < len(poss[b]):
                        poss[b] = new_poss_b
                        changed = True

    # 3. Return the mappings that are mathematically forced (domain size 1)
    return {g: list(p)[0] for g, p in poss.items() if len(p) == 1}


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
