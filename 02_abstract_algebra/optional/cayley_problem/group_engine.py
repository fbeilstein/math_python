import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup

class GroupElement:
    def __init__(self, group, val):
        self.group = group
        self.val = val  # SymPy FreeGroupElement
        
    def __mul__(self, other):
        if not isinstance(other, GroupElement):
            raise TypeError("Can only multiply GroupElement by GroupElement")
        # Automatically reduce upon multiplication
        reduced_val = self.group.fp_group.reduce(self.val * other.val)
        return GroupElement(self.group, reduced_val)
        
    def inv(self):
        reduced_val = self.group.fp_group.reduce(self.val**-1)
        return GroupElement(self.group, reduced_val)
        
    def __eq__(self, other):
        if not isinstance(other, GroupElement):
            return False
        # To test equality, check if a * b^-1 is the identity in the FpGroup
        diff = self.group.fp_group.reduce(self.val * other.val**-1)
        return diff.is_identity
        
    def __hash__(self):
        return hash(str(self))
        
    def __str__(self):
        if hasattr(self, '_canonical_str'):
            return self._canonical_str
            
        if self.val.is_identity:
            self._canonical_str = "e"
            return "e"
            
        # Find canonical match in group elements
        if self.group._elements is not None:
            for elem in self.group._elements:
                # To prevent infinite recursion, check if elem has _canonical_str
                if hasattr(elem, '_canonical_str'):
                    if self == elem:
                        self._canonical_str = elem._canonical_str
                        return self._canonical_str
                        
        # Fallback raw string formatting
        letters = []
        for gen, power in self.val.array_form:
            g_str = str(gen)
            if power > 0:
                letters.append(g_str * power)
            elif power < 0:
                letters.append(g_str.upper() * (-power))
        raw_str = "".join(letters)
        self._canonical_str = raw_str
        return raw_str

    def __repr__(self):
        return f"GroupElement({str(self)})"

class Group:
    def __init__(self, generators, relations_str_list):
        """
        generators: list of strings e.g. ['a', 'b']
        relations_str_list: list of tuples (lhs, rhs) e.g. [('aaaa', ''), ('bb', ''), ('abab', '')]
        """
        gen_str = ", ".join(generators)
        self.free_g, *gens = free_group(gen_str)
        if len(generators) == 1:
            gens = [gens[0]]  # free_group returns (F, a) or (F, a, b). if 1 gen, it's (F, a) wait no, F, a = free_group('a') works.
            # wait, actually free_group returns a tuple where first is the group.
            
        # Re-fetch robustly
        self.gen_dict = {}
        for g in self.free_g.generators:
            self.gen_dict[str(g)] = g
            self.gen_dict[str(g).upper()] = g**-1
            
        sympy_rels = []
        for lhs, rhs in relations_str_list:
            w_lhs = self._parse_word(lhs)
            w_rhs = self._parse_word(rhs)
            rel = w_lhs * w_rhs**-1
            if not rel.is_identity:
                sympy_rels.append(rel)
                
        self.fp_group = FpGroup(self.free_g, sympy_rels)
        
        # Verify finite order with a timeout using multiprocessing or threading
        import threading
        
        ord_val = None
        err = None
        
        def check_order():
            nonlocal ord_val, err
            try:
                ord_val = self.fp_group.order()
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
            
        # Cache elements
        self._elements = None
        self.get_elements()
        
    def _parse_word(self, w):
        res = self.free_g.identity
        if w == "e" or w == "":
            return res
        for c in w:
            if c not in self.gen_dict:
                raise ValueError(f"Unknown generator character: {c}")
            res = res * self.gen_dict[c]
        return res
        
    def get_elements(self):
        if self._elements is None:
            # First pass: wrap elements without canonicalizing
            raw_elements = [GroupElement(self, e) for e in self.fp_group.elements]
            # Force canonical string generation natively
            for elem in raw_elements:
                elem._canonical_str = GroupElement.__str__(elem) # Using the fallback
            self._elements = raw_elements
        return self._elements
        
    def identity(self):
        return GroupElement(self, self.free_g.identity)
        
    def parse(self, w):
        val = self.fp_group.reduce(self._parse_word(w))
        return GroupElement(self, val)
