import string

# =====================================================================
# STUDENT IMPLEMENTATION (Group Theory & Cayley Graphs)
# =====================================================================

# ---------------------------------------------------------
# L1: Word Reduction
# ---------------------------------------------------------

_reduce_cache = {}
_compiled_rels = {}

def get_all_rels(relations):
    rel_key = tuple(relations)
    if rel_key in _compiled_rels: return _compiled_rels[rel_key]
    
    def inv_w(w):
        return "".join(c.lower() if c.isupper() else c.upper() for c in reversed(w))
        
    all_rels = list(relations)
    for lhs, rhs in relations:
        inv_lhs = inv_w(lhs)
        inv_rhs = inv_w(rhs)
        if (inv_lhs, inv_rhs) not in all_rels:
            all_rels.append((inv_lhs, inv_rhs))
            
    trivial_rels = []
    # Just pre-populate the whole alphabet a-z to be safe and avoid missing letters
    for c in "abcdefghijklmnopqrstuvwxyz":
        trivial_rels.append((c + c.upper(), ""))
        trivial_rels.append((c.upper() + c, ""))
        
    res = trivial_rels + all_rels
    _compiled_rels[rel_key] = res
    return res

def reduce_word(word, relations):
    rel_key = tuple(relations)
    cache_key = (word, rel_key)
    if cache_key in _reduce_cache:
        return _reduce_cache[cache_key]
        
    original_word = word

    """
    L1: Reduce a word in a finitely presented group.
    `word`: A string like 'aabA'. (Uppercase implies inverse: A = a^-1).
    `relations`: A list of tuples (lhs, rhs), e.g., [("aaaa", ""), ("bb", ""), ("abab", "")].
    
    You must iteratively apply:
    1. Trivial cancellations (e.g., 'aA' -> '', 'Aa' -> '', 'bB' -> '', 'Bb' -> '')
    2. The group relations (replace lhs with rhs).
    Stop when the word cannot be reduced any further.
    To prevent infinite loops on crazy groups, limit to 1000 iterations.
    Return the reduced word. If it reduces to the empty string, return 'e'.
    """
    """
    L1: Reduce a word in a finitely presented group.
    """
    # BEGIN_SOLUTION
    all_rels = get_all_rels(relations)
    
    for _ in range(1000):
        changed = False
        for lhs, rhs in all_rels:
            if lhs in word:
                word = word.replace(lhs, rhs)
                changed = True
        if not changed:
            break
            
    res = word if word else "e"
    _reduce_cache[cache_key] = res
    return res
    # END_SOLUTION

# ---------------------------------------------------------
# L2: Cayley Graph Generation (BFS)
# ---------------------------------------------------------

def generate_cayley_graph(generators, relations, max_depth=10): #contains solution
    """
    L2: Generate the Cayley Graph using Breadth-First Search.
    Start at 'e' (the identity).
    Multiply the current word by each generator on the right.
    Reduce the new word.
    Record the node and the directed edge (current_word, generator, new_word).
    Return (nodes, edges) where:
    - nodes is a set of unique reduced words.
    - edges is a list of tuples: (source, generator, target).
    """
    # BEGIN_SOLUTION
    nodes = set(["e"])
    edges = []
    
    queue = [("e", 0)] # (word, depth)
    visited = set(["e"])
    
    while queue:
        current_word, depth = queue.pop(0)
        
        if depth >= max_depth:
            continue
            
        for g in generators:
            # Multiply on the right
            if current_word == "e":
                new_word_raw = g
            else:
                new_word_raw = current_word + g
                
            new_word = reduce_word(new_word_raw, relations)
            
            # Record edge
            edges.append((current_word, g, new_word))
            
            if new_word not in visited:
                visited.add(new_word)
                nodes.add(new_word)
                queue.append((new_word, depth + 1))
                
    return nodes, edges
    # END_SOLUTION

# ---------------------------------------------------------
# L3: Subgroups and Cosets
# ---------------------------------------------------------

def invert_word(w):
    if w == "e": return "e"
    return "".join(c.lower() if c.isupper() else c.upper() for c in reversed(w))

_canon_cache = {}

def graph_multiply(start_node, word, all_elements, edges):
    """
    Multiply a node by a word using the precomputed Cayley Graph edges.
    This is O(len(word)) and completely avoids string reduction.
    Returns the resulting node, or None if it falls off the graph boundary.
    """
    if word == "e" or not word: return start_node
    
    # Build fast adjacency lookups
    # forward: (node, gen) -> target
    # backward: (node, gen) -> source
    # We can cache this on the graph object or rebuild it quickly.
    # To be extremely fast, we assume edges is accessible.
    forward = {}
    backward = {}
    for u, g, v in edges:
        forward[(u, g)] = v
        backward[(v, g)] = u
        
    current = start_node
    for c in word:
        if current is None: return None
        if c.islower():
            current = forward.get((current, c))
        else:
            current = backward.get((current, c.lower()))
    return current

def canonicalize(word, all_elements, relations, edges=None):
    """
    Helper: Find which node in all_elements this word corresponds to.
    """
    if word in all_elements: return word
    
    # If we have edges, try fast graph traversal first!
    if edges is not None:
        res = graph_multiply("e", word, all_elements, edges)
        if res is not None: return res

    rel_key = tuple(relations)
    cache_key = (word, frozenset(all_elements), rel_key)
    if cache_key in _canon_cache:
        return _canon_cache[cache_key]
        
    red_word = reduce_word(word, relations)
    if red_word in all_elements:
        _canon_cache[cache_key] = red_word
        return red_word
        
    for n in all_elements:
        raw = (red_word if red_word != "e" else "") + (invert_word(n) if n != "e" else "")
        if not raw: raw = "e"
        if reduce_word(raw, relations) == "e":
            _canon_cache[cache_key] = n
            return n
    
    _canon_cache[cache_key] = red_word
    return red_word

def generate_subgroup(subset, all_elements, relations, edges=None): #contains solution
    """
    L3a: Given a subset of elements (reduced words), compute the full 
    subgroup generated by them. This means closure under multiplication 
    and inversion.
    """
    # BEGIN_SOLUTION
    subgroup = set(["e"])
    queue = ["e"]
    
    gens = list(subset) + [invert_word(w) for w in subset]
    
    while queue:
        current = queue.pop(0)
        for g in gens:
            if edges is not None:
                new_w = graph_multiply(current, g, all_elements, edges)
                if new_w is None:
                    if current == "e": new_w_raw = g
                    elif g == "e": new_w_raw = current
                    else: new_w_raw = current + g
                    new_w = canonicalize(new_w_raw, all_elements, relations, edges)
            else:
                if current == "e": new_w_raw = g
                elif g == "e": new_w_raw = current
                else: new_w_raw = current + g
                new_w = canonicalize(new_w_raw, all_elements, relations, edges)
                
            if new_w in all_elements and new_w not in subgroup:
                subgroup.add(new_w)
                queue.append(new_w)
                
    return subgroup
    # END_SOLUTION

def compute_left_cosets(subgroup, all_elements, relations, edges=None): #contains solution
    """
    L3b: Generate all Left Cosets of a subgroup.
    Return a list of sets, where each set is a coset (gH).
    """
    # BEGIN_SOLUTION
    cosets = []
    covered = set()
    
    for g in sorted(list(all_elements), key=lambda x: (len(x), x)):
        if g in covered:
            continue
            
        coset = set()
        for h in subgroup:
            if edges is not None:
                val = graph_multiply(g, h, all_elements, edges)
                if val is None:
                    raw = h if g == "e" else (g if h == "e" else g + h)
                    val = canonicalize(raw, all_elements, relations, edges)
            else:
                raw = h if g == "e" else (g if h == "e" else g + h)
                val = canonicalize(raw, all_elements, relations, edges)
                
            if val in all_elements:
                coset.add(val)
                covered.add(val)
            
        cosets.append(coset)
        
    return cosets
    # END_SOLUTION

# ---------------------------------------------------------
# L4: Normality and Conjugacy
# ---------------------------------------------------------

def compute_conjugacy_class(element, all_elements, relations, edges=None): #contains solution
    """
    L4a: Compute the conjugacy class of an element x: {g * x * g^-1 for all g in G}.
    """
    # BEGIN_SOLUTION
    conj_class = set()
        
    for g in all_elements:
        g_inv = invert_word(g)
        
        if edges is not None:
            v1 = graph_multiply(g, element, all_elements, edges)
            if v1 is not None:
                val = graph_multiply(v1, g_inv, all_elements, edges)
                if val is not None and val in all_elements:
                    conj_class.add(val)
                    continue
        
        # Fallback
        parts = []
        if g != "e": parts.append(g)
        if element != "e": parts.append(element)
        if g_inv != "e": parts.append(g_inv)
        
        if not parts:
            conj_class.add("e")
        else:
            raw = "".join(parts)
            val = canonicalize(raw, all_elements, relations, edges)
            if val in all_elements:
                conj_class.add(val)
            
    return conj_class
    # END_SOLUTION

def is_normal_subgroup(subgroup, all_elements, relations, edges=None): #contains solution
    """
    L4b: Check if a subgroup is normal (gH = Hg for all g).
    A subgroup is normal iff it is a union of conjugacy classes,
    meaning for any h in H and g in G, ghg^-1 is in H.
    """
    # BEGIN_SOLUTION
    for h in subgroup:
        for g in all_elements:
            g_inv = invert_word(g)
            
            if edges is not None:
                v1 = graph_multiply(g, h, all_elements, edges)
                if v1 is not None:
                    val = graph_multiply(v1, g_inv, all_elements, edges)
                    if val is not None:
                        if val not in subgroup: return False
                        continue
                        
            parts = []
            if g != "e": parts.append(g)
            if h != "e": parts.append(h)
            if g_inv != "e": parts.append(g_inv)
            
            raw = "".join(parts) if parts else "e"
            val = canonicalize(raw, all_elements, relations, edges)
            if val not in subgroup:
                return False
    return True
    # END_SOLUTION

# ---------------------------------------------------------
# L5: Center and Commutator Subgroup
# ---------------------------------------------------------

def compute_center(all_elements, relations, edges=None): #contains solution
    """
    L5a: Compute the Center Z(G) (elements that commute with ALL elements).
    """
    # BEGIN_SOLUTION
    center = set()
    for z in all_elements:
        commutes_with_all = True
        for g in all_elements:
            if edges is not None:
                val1 = graph_multiply(z, g, all_elements, edges)
                val2 = graph_multiply(g, z, all_elements, edges)
                if val1 is not None and val2 is not None:
                    if val1 != val2:
                        commutes_with_all = False
                        break
                    continue
                    
            # Check if z*g == g*z
            raw1 = (z if z != "e" else "") + (g if g != "e" else "")
            raw2 = (g if g != "e" else "") + (z if z != "e" else "")
            
            val1 = canonicalize(raw1, all_elements, relations, edges) if raw1 else "e"
            val2 = canonicalize(raw2, all_elements, relations, edges) if raw2 else "e"
            
            if val1 != val2:
                commutes_with_all = False
                break
        if commutes_with_all:
            center.add(z)
    return center
    # END_SOLUTION

def compute_commutator_subgroup(all_elements, relations, edges=None): #contains solution
    """
    L5b: Compute the Commutator Subgroup [G, G].
    It is generated by all commutators [a, b] = a * b * a^-1 * b^-1.
    """
    # BEGIN_SOLUTION
    commutators = set()
    for a in all_elements:
        for b in all_elements:
            a_inv = invert_word(a)
            b_inv = invert_word(b)
            
            if edges is not None:
                v1 = graph_multiply(a, b, all_elements, edges)
                if v1 is not None:
                    v2 = graph_multiply(v1, a_inv, all_elements, edges)
                    if v2 is not None:
                        v3 = graph_multiply(v2, b_inv, all_elements, edges)
                        if v3 is not None and v3 in all_elements:
                            commutators.add(v3)
                            continue
            
            parts = []
            if a != "e": parts.append(a)
            if b != "e": parts.append(b)
            if a_inv != "e": parts.append(a_inv)
            if b_inv != "e": parts.append(b_inv)
            
            raw = "".join(parts) if parts else "e"
            val = canonicalize(raw, all_elements, relations, edges)
            if val in all_elements:
                commutators.add(val)
            
    # The commutator subgroup is GENERATED BY the commutators
    return generate_subgroup(commutators, all_elements, relations, edges)
    # END_SOLUTION
