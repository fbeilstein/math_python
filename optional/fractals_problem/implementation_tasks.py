import numpy as np

class VectorizedDual:
    """Vectorized Dual number: a + b*eps where eps^2 = 0. Wraps numpy arrays."""
    def __init__(self, real, dual):
        # #contains solution
        self.real = np.asarray(real, dtype=np.float64)
        self.dual = np.asarray(dual, dtype=np.float64)
        # #end solution

    def __add__(self, other):
        # #contains solution
        if isinstance(other, VectorizedDual):
            return VectorizedDual(self.real + other.real, self.dual + other.dual)
        return VectorizedDual(self.real + other, self.dual)
        # #end solution

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        # #contains solution
        if isinstance(other, VectorizedDual):
            return VectorizedDual(self.real - other.real, self.dual - other.dual)
        return VectorizedDual(self.real - other, self.dual)
        # #end solution
        
    def __rsub__(self, other):
        return VectorizedDual(other - self.real, -self.dual)

    def __mul__(self, other):
        # #contains solution
        if isinstance(other, VectorizedDual):
            return VectorizedDual(
                self.real * other.real,
                self.real * other.dual + self.dual * other.real
            )
        return VectorizedDual(self.real * other, self.dual * other)
        # #end solution

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power):
        # #contains solution
        if isinstance(power, int) or isinstance(power, float):
            return VectorizedDual(
                self.real ** power,
                power * (self.real ** (power - 1)) * self.dual
            )
        raise NotImplementedError("Power to another hypercomplex number not supported")
        # #end solution

    def __getitem__(self, mask):
        # #contains solution
        return VectorizedDual(self.real[mask], self.dual[mask])
        # #end solution

    def __setitem__(self, mask, val):
        # #contains solution
        if isinstance(val, VectorizedDual):
            self.real[mask] = val.real
            self.dual[mask] = val.dual
        else:
            self.real[mask] = val
            self.dual[mask] = 0
        # #end solution
        
    def copy(self):
        return VectorizedDual(self.real.copy(), self.dual.copy())

    def abs(self):
        """Returns the magnitude for escape condition"""
        return np.abs(self.real)


class VectorizedSplit:
    """Vectorized Split-complex number: a + b*j where j^2 = 1. Wraps numpy arrays."""
    def __init__(self, real, j):
        # #contains solution
        self.real = np.asarray(real, dtype=np.float64)
        self.j = np.asarray(j, dtype=np.float64)
        # #end solution

    def __add__(self, other):
        # #contains solution
        if isinstance(other, VectorizedSplit):
            return VectorizedSplit(self.real + other.real, self.j + other.j)
        return VectorizedSplit(self.real + other, self.j)
        # #end solution

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        # #contains solution
        if isinstance(other, VectorizedSplit):
            return VectorizedSplit(self.real - other.real, self.j - other.j)
        return VectorizedSplit(self.real - other, self.j)
        # #end solution
        
    def __rsub__(self, other):
        return VectorizedSplit(other - self.real, -self.j)

    def __mul__(self, other):
        # #contains solution
        if isinstance(other, VectorizedSplit):
            return VectorizedSplit(
                self.real * other.real + self.j * other.j,
                self.real * other.j + self.j * other.real
            )
        return VectorizedSplit(self.real * other, self.j * other)
        # #end solution

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power):
        # #contains solution
        if power == 2:
            return self * self
        elif power == 3:
            return self * self * self
        else:
            # General power requires full hyperbolic expansion
            raise NotImplementedError("Arbitrary power not implemented for Split-Complex, use integer powers <= 3")
        # #end solution

    def __getitem__(self, mask):
        # #contains solution
        return VectorizedSplit(self.real[mask], self.j[mask])
        # #end solution

    def __setitem__(self, mask, val):
        # #contains solution
        if isinstance(val, VectorizedSplit):
            self.real[mask] = val.real
            self.j[mask] = val.j
        else:
            self.real[mask] = val
            self.j[mask] = 0
        # #end solution
        
    def copy(self):
        return VectorizedSplit(self.real.copy(), self.j.copy())

    def abs(self):
        """Returns the magnitude for escape condition"""
        return np.abs(self.real)


def render_fractal(algebra, fractal_type, formula_str, c_val=None, width=400, height=400, max_iter=30):
    """
    Renders the fractal grid.
    algebra: 'Complex (i^2 = -1)', 'Dual (e^2 = 0)', 'Split-Complex (j^2 = 1)'
    fractal_type: 'Mandelbrot' or 'Julia'
    formula_str: Arbitrary python math string, e.g., 'z**2 + c'
    c_val: Complex value for Julia sets
    """
    # #contains solution
    x, y = np.meshgrid(np.linspace(-2, 2, width), np.linspace(-2, 2, height))
    
    if algebra == "Complex (i^2 = -1)":
        c = x + 1j * y
        if fractal_type == "Mandelbrot":
            z = np.zeros_like(c)
        else:
            z = c.copy()
            c = np.full_like(z, c_val)
            
        def get_abs(v): return np.abs(v)
            
    elif algebra == "Dual (e^2 = 0)":
        c = VectorizedDual(x, y)
        if fractal_type == "Mandelbrot":
            z = VectorizedDual(np.zeros_like(x), np.zeros_like(y))
        else:
            z = c.copy()
            c = VectorizedDual(np.full_like(x, c_val.real), np.full_like(y, c_val.imag))
            
        def get_abs(v): return v.abs()
            
    elif algebra == "Split-Complex (j^2 = 1)":
        c = VectorizedSplit(x, y)
        if fractal_type == "Mandelbrot":
            z = VectorizedSplit(np.zeros_like(x), np.zeros_like(y))
        else:
            z = c.copy()
            c = VectorizedSplit(np.full_like(x, c_val.real), np.full_like(y, c_val.imag))
            
        def get_abs(v): return v.abs()
        
    img = np.zeros(x.shape, dtype=int)
    active = np.ones(x.shape, dtype=bool)
    
    # We ignore warnings for overflow during eval
    with np.errstate(all='ignore'):
        for i in range(max_iter):
            # Use eval to allow arbitrary dynamic formulas
            z_new = eval(formula_str, {"z": z[active], "c": c[active], "np": np})
            z[active] = z_new
            escaped = get_abs(z) > 2
            
            newly_escaped = escaped & active
            img[newly_escaped] = i
            active &= ~newly_escaped
            if not active.any():
                break
                
    img[active] = max_iter
    return img
    # #end solution

# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
