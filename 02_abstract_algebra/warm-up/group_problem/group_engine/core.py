"""
Group engine: unified representation for finite groups.

All input methods (catalog, permutations, presentations, matrices)
produce a ConcreteGroup, which stores the full multiplication table
and exposes a uniform interface for structural analysis.
"""
import numpy as np
from math import gcd
from itertools import product


class GroupElement:
    """Base class for all group elements."""
    def __init__(self, value):
        self._value = value
        
    def __eq__(self, other):
        if not isinstance(other, GroupElement):
            return False
        return type(self) is type(other) and self._value == other._value
        
    def __hash__(self):
        return hash((type(self), self._value))
        
    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return str(self) < str(other)


class ConcreteGroupElement(GroupElement):
    """An element of a ConcreteGroup."""
    def __init__(self, group, idx):
        super().__init__((id(group), idx))
        self.group = group
        self.idx = idx
        
    def __mul__(self, other):
        if not isinstance(other, ConcreteGroupElement) or self.group is not other.group:
            raise ValueError("Can only multiply elements from the same group.")
        return ConcreteGroupElement(self.group, self.group.multiply(self.idx, other.idx))
        
    def __invert__(self):
        return ConcreteGroupElement(self.group, self.group.inverse(self.idx))
        
    def __str__(self):
        return self.group.label(self.idx)
        
    def __repr__(self):
        return str(self)


class Group:
    """A finite group. Can be backed by an explicit multiplication table or initialized directly from elements.

    Attributes:
        labels:   list[str]   — human-readable names for each element (if table-backed)
        order:    int         — number of elements (if table-backed)
        identity: int         — index of the identity element (if table-backed)
        table:    np.ndarray  — (order x order) multiplication table, table[i][j] = i*j (if table-backed)
    """
    def __init__(self, labels=None, table=None, identity=None, generators=None, elements=None):
        if elements is not None:
            self._elements = list(set(elements))
            self._identity = None
            self.generators = generators or []
            self.table = None
            return

        self.labels = list(labels)
        self.order = len(labels)
        self.table = np.array(table, dtype=int)
        assert self.table.shape == (self.order, self.order)

        if identity is not None:
            self.identity = identity
        else:
            # Find identity: row i equals [0,1,...,n-1]
            target = np.arange(self.order)
            for i in range(self.order):
                if np.array_equal(self.table[i], target) and np.array_equal(self.table[:, i], target):
                    self.identity = i
                    break
            else:
                raise ValueError("No identity element found in multiplication table")

        # Precompute inverse table
        self._inv = np.zeros(self.order, dtype=int)
        for i in range(self.order):
            for j in range(self.order):
                if self.table[i][j] == self.identity:
                    self._inv[i] = j
                    break
                    
        self._elements = [ConcreteGroupElement(self, i) for i in range(self.order)]
        self._identity = self._elements[self.identity]
        
        # Convert generator indices to elements
        if generators:
            self.generators = [self._elements[g] for g in generators if g is not None]
        else:
            self.generators = []

    @property
    def elements(self):
        """Return list of all abstract GroupElement objects."""
        return self._elements
        
    @property
    def identity_element(self):
        """Return the identity GroupElement."""
        return self.get_identity()
        
    def get_identity(self):
        """Return the identity GroupElement."""
        if self._identity is None:
            # find identity element if not already cached (for non-table-backed)
            for e in self._elements:
                if all(e * a == a and a * e == a for a in self._elements):
                    self._identity = e
                    break
        return self._identity
        
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

    def update(self, items):
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

    def multiply(self, a, b):
        """Return the index of the product a·b."""
        return int(self.table[a][b])

    def inverse(self, a):
        """Return the index of a⁻¹."""
        return int(self._inv[a])

    def element_order(self, a):
        """Return the smallest k ≥ 1 such that a^k = identity."""
        val = a
        for k in range(1, self.order + 1):
            if val == self.identity:
                return k
            val = self.multiply(val, a)
        return self.order  # fallback

    def label(self, i):
        """Human-readable label for element i."""
        return self.labels[i]

    def all_elements(self):
        """Return list of all element indices."""
        return list(range(self.order))
