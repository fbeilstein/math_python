import numpy as np
import math
import unittest

class Dual:
    """Dual number: a + b*eps where eps^2 = 0."""
    def __init__(self, real, dual):
        self.real = float(real)
        self.dual = float(dual)

    def __repr__(self):
        return f"Dual({self.real}, {self.dual})"

    def __add__(self, other): #contains solution
        if isinstance(other, Dual):
            return Dual(self.real + other.real, self.dual + other.dual)
        return Dual(self.real + other, self.dual)

    def __radd__(self, other): #contains solution
        return self.__add__(other)

    def __sub__(self, other): #contains solution
        if isinstance(other, Dual):
            return Dual(self.real - other.real, self.dual - other.dual)
        return Dual(self.real - other, self.dual)

    def __rsub__(self, other): #contains solution
        return Dual(other - self.real, -self.dual)

    def __mul__(self, other): #contains solution
        if isinstance(other, Dual):
            # (a + b e)(c + d e) = ac + (ad + bc)e + bd e^2 = ac + (ad + bc)e
            return Dual(self.real * other.real, self.real * other.dual + self.dual * other.real)
        return Dual(self.real * other, self.dual * other)

    def __rmul__(self, other): #contains solution
        return self.__mul__(other)

    def __truediv__(self, other): #contains solution
        if isinstance(other, Dual):
            # (a + be) / (c + de) = (a + be)(c - de) / c^2 = (ac + (bc - ad)e) / c^2
            c = other.real
            if c == 0:
                raise ZeroDivisionError("Division by zero in dual part")
            return Dual(self.real / c, (self.dual * c - self.real * other.dual) / (c * c))
        return Dual(self.real / other, self.dual / other)

    def __rtruediv__(self, other): #contains solution
        c = self.real
        if c == 0:
            raise ZeroDivisionError("Division by zero in dual part")
        return Dual(other / c, (-other * self.dual) / (c * c))
        
    def __pow__(self, power): #contains solution
        if isinstance(power, Dual):
            raise NotImplementedError("Dual to the power of Dual not implemented")
        return Dual(self.real ** power, power * (self.real ** (power - 1)) * self.dual)

# Transcendental functions
def sin(x): #contains solution
    if isinstance(x, Dual):
        return Dual(math.sin(x.real), math.cos(x.real) * x.dual)
    return math.sin(x)

def cos(x): #contains solution
    if isinstance(x, Dual):
        return Dual(math.cos(x.real), -math.sin(x.real) * x.dual)
    return math.cos(x)

def tan(x): #contains solution
    if isinstance(x, Dual):
        cos_val = math.cos(x.real)
        return Dual(math.tan(x.real), x.dual / (cos_val * cos_val))
    return math.tan(x)

def exp(x): #contains solution
    if isinstance(x, Dual):
        e_val = math.exp(x.real)
        return Dual(e_val, e_val * x.dual)
    return math.exp(x)

def log(x): #contains solution
    if isinstance(x, Dual):
        return Dual(math.log(x.real), x.dual / x.real)
    return math.log(x)

# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
