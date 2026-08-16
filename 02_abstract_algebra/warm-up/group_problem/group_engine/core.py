"""
Group engine: unified representation for finite groups.

All input methods (catalog, permutations, presentations, matrices)
produce a Group subclass, which exposes a uniform interface for structural analysis.
"""

class Group:
    """Base class for all groups."""
    
    class Element:
        """A generic element that proxies operations to its parent group."""
        def __init__(self, group, value, label=None):
            self.group = group
            self.value = tuple(value) if isinstance(value, list) else value
            self.label = label if label is not None else str(self.value)
            
        def __mul__(self, other):
            if not isinstance(other, type(self)) or self.group is not other.group:
                raise ValueError("Cannot multiply elements from different groups.")
            return self.group.multiply(self, other)
            
        def __invert__(self):
            return self.group.inverse(self)
            
        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.group is other.group and self.value == other.value
            
        def __hash__(self):
            # Tuples are immutable and hashable
            # Sometimes value might be an unhashable array, we convert to tuple if needed
            try:
                v_hash = hash(self.value)
            except TypeError:
                v_hash = hash(tuple(self.value)) if isinstance(self.value, list) else hash(str(self.value))
            return hash((id(self.group), v_hash))
            
        def __repr__(self):
            return self.label
            
        def __str__(self):
            return self.label
            
        def __lt__(self, other):
            if not isinstance(other, type(self)):
                return NotImplemented
            return str(self) < str(other)

    def __init__(self, elements=None):
        self._elements = elements if elements is not None else []
        self._identity = None
        self.generators = []

    # --- Abstract Methods ---
    def multiply(self, left, right):
        raise NotImplementedError

    def inverse(self, element):
        raise NotImplementedError

    # --- Container Methods ---
    @property
    def order(self):
        """Return the number of elements in the group."""
        return len(self._elements)

    @property
    def elements(self):
        """Return list of all Element objects."""
        return self._elements
        
    @property
    def identity_element(self):
        """Return the identity Element, utilizing student code."""
        if self._identity is None:
            import implementation_tasks
            # Directly call the student's logic. If it fails, let it crash!
            candidate = implementation_tasks.find_identity(self._elements)
            
            # Minimal mathematical verification
            if candidate is None:
                raise ValueError("Your find_identity() function returned None!")
            if not all(candidate * a == a and a * candidate == a for a in self._elements):
                raise ValueError(f"Your find_identity() returned {candidate}, but it does not act as an identity!")
                
            self._identity = candidate
        return self._identity
        
    def get_identity(self):
        return self.identity_element
        
    def __len__(self):
        return len(self._elements)
        
    def __iter__(self):
        return iter(self._elements)

    def __contains__(self, item):
        return item in self._elements

    def add(self, item):
        if item not in self._elements:
            self._elements.append(item)
            self._identity = None # invalidate cache

    def add_elements(self, items):
        for item in items:
            self.add(item)

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False
        return set(self._elements) == set(other._elements)

    def __hash__(self):
        return hash(frozenset(self._elements))

    def __lt__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return set(self._elements) < set(other._elements)

    def __le__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return set(self._elements) <= set(other._elements)

# Alias for backwards compatibility with type hints in implementation_tasks.py
GroupElement = Group.Element
