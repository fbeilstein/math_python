from itertools import zip_longest
# =====================================================================
# STUDENT IMPLEMENTATION
# =====================================================================

# ---------------------------------------------------------
# L1: Prime Field Elements — GF(p) arithmetic
# ---------------------------------------------------------

class PrimeField:
    _instances = {}
    def __new__(cls, p):
        if p not in cls._instances:
            inst = super().__new__(cls)
            inst.p = p
            inst.size = p
            inst.modulus = p
            cls._instances[p] = inst
        return cls._instances[p]

    @property
    def zero(self): return GaloisFieldElement(0, self)

    @property
    def one(self): return GaloisFieldElement(1, self)
    
    def __call__(self, val):
        return GaloisFieldElement(val, self)


class GaloisFieldElement:
    def __init__(self, val, field):
        self.field = field
        self.val = val % field.modulus

    def __add__(self, other): #contains solution
        return GaloisFieldElement((self.val + other.val) % self.field.modulus, self.field)
    def __sub__(self, other): #contains solution
        return GaloisFieldElement((self.val - other.val) % self.field.modulus, self.field)
    def __mul__(self, other): #contains solution
        return GaloisFieldElement((self.val * other.val) % self.field.modulus, self.field)
    def __truediv__(self, other): #contains solution
        if not other: raise ZeroDivisionError()
        return self * (other ** (self.field.size - 2))
    def __pow__(self, exponent): #contains solution
        if exponent == 0: return self.field.one
        result = self.field.one
        base = self
        while exponent > 0:
            if exponent % 2 == 1: result = result * base
            base = base * base
            exponent //= 2
        return result
    def __neg__(self): return self.field.zero - self
    def __bool__(self): return bool(self.val)
    def __eq__(self, other): return isinstance(other, GaloisFieldElement) and self.val == other.val
    def __repr__(self): return str(self.val)
    def __hash__(self): return hash(self.val)

# ---------------------------------------------------------
# L2: The Universal Polynomial
# ---------------------------------------------------------

class Polynomial:
    def __init__(self, coeffs):
        if not coeffs:
            raise ValueError("Cannot initialize Polynomial with empty coefficients.")
        self.coeffs = list(coeffs)
        self._trim()

    @property
    def base_field(self):
        return self.coeffs[0].field

    def __bool__(self):
        return len(self.coeffs) > 1 or bool(self.coeffs[0])

    def _trim(self):
        while len(self.coeffs) > 1 and not self.coeffs[0]:
            self.coeffs.pop(0)
        if not self.coeffs:
            self.coeffs = [self.base_field.zero]

    def __add__(self, other): #contains solution
        res = [a + b for a, b in zip_longest(reversed(self.coeffs), reversed(other.coeffs), fillvalue=self.base_field.zero)]
        res.reverse()
        return Polynomial(res)

    def __sub__(self, other): #contains solution
        res = [a - b for a, b in zip_longest(reversed(self.coeffs), reversed(other.coeffs), fillvalue=self.base_field.zero)]
        res.reverse()
        return Polynomial(res)

    def __mul__(self, other): #contains solution
        res = [self.base_field.zero] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                res[i+j] = res[i+j] + a * b
        return Polynomial(res)

    def __divmod__(self, other): #contains solution
        if not other: raise ZeroDivisionError()
        dividend = list(self.coeffs)
        divisor = other.coeffs
        if len(dividend) < len(divisor):
            return Polynomial([self.base_field.zero]), self
        quotient = [self.base_field.zero] * (len(dividend) - len(divisor) + 1)
        for i in range(len(quotient)):
            if dividend[i]:
                coef = dividend[i] / divisor[0]
                quotient[i] = coef
                for j in range(len(divisor)):
                    dividend[i + j] = dividend[i + j] - coef * divisor[j]
        return Polynomial(quotient), Polynomial(dividend)

    def __mod__(self, other):
        _, rem = divmod(self, other)
        return rem

    def __pow__(self, exponent, mod_poly=None):
        res = Polynomial([self.base_field.one])
        base_pow = self
        while exponent > 0:
            if exponent % 2 == 1:
                res = res * base_pow
                if mod_poly: res = res % mod_poly
            base_pow = base_pow * base_pow
            if mod_poly: base_pow = base_pow % mod_poly
            exponent //= 2
        return res

    def __call__(self, x): #contains solution
        val = self.coeffs[0]
        for c in self.coeffs[1:]:
            val = val * x + c
        return val

    def __len__(self): return len(self.coeffs)
    def __getitem__(self, idx): return self.coeffs[idx]

    def __eq__(self, other):
        if isinstance(other, Polynomial): return self.coeffs == other.coeffs
        return False

    def __repr__(self): return f"Poly({self.coeffs})"
    def __hash__(self): return hash(tuple(self.coeffs))

# ---------------------------------------------------------
# L3: Primitive Polynomial Search
# ---------------------------------------------------------

def is_primitive(poly): #contains solution
    """L3: Prove a polynomial of degree n is primitive over GF(p)."""
    n = len(poly) - 1
    p = poly.base_field.p
    
    order = (p ** n) - 1

    factors = []
    temp = order
    for i in range(2, int(temp**0.5) + 1):
        if temp % i == 0:
            factors.append(i)
            while temp % i == 0: temp //= i
    if temp > 1: factors.append(temp)

    zero = poly.base_field.zero
    x = Polynomial([PrimeField(p).one, zero])
    one_poly = Polynomial([PrimeField(p).one])

    if pow(x, order, poly) != one_poly:
        return False

    for q in factors:
        if pow(x, order // q, poly) == one_poly:
            return False

    return True

# ---------------------------------------------------------
# L4: Extension Field — GF(p^n) as polynomials mod primitive
# ---------------------------------------------------------

class ExtensionField:
    _instances = {}
    def __new__(cls, mod_poly):
        if mod_poly not in cls._instances:
            inst = super().__new__(cls)
            inst.modulus = mod_poly
            inst.n = len(mod_poly) - 1
            inst.p = mod_poly.coeffs[0].field.p
            inst.size = inst.p ** inst.n
            inst._zero_gfp = mod_poly.coeffs[0].field.zero
            inst._one_gfp = mod_poly.coeffs[0].field.one
            inst.alpha = GaloisFieldElement(Polynomial([inst._one_gfp, inst._zero_gfp]), inst)
            cls._instances[mod_poly] = inst
        return cls._instances[mod_poly]

    @property
    def zero(self):
        return GaloisFieldElement(Polynomial([self._zero_gfp]), self)

    @property
    def one(self):
        return GaloisFieldElement(Polynomial([self._one_gfp]), self)
        
    def __call__(self, val):
        return GaloisFieldElement(val, self)

    def exp(self, i):
        """Compute α^i via binary exponentiation — no tables needed."""
        return self.alpha ** i



# ---------------------------------------------------------
# L5: RS Encoding
# ---------------------------------------------------------

def get_generator_poly(num_ec_bytes, field): #contains solution
    """L5: Calculate the Reed-Solomon Generator Polynomial."""
    gen = Polynomial([field.one])
    for i in range(num_ec_bytes):
        root = -field.exp(i)
        term = Polynomial([field.one, root])
        gen = gen * term
    return gen

# ---------------------------------------------------------
# L6: RS Decoding I (Syndromes)
# ---------------------------------------------------------

def calculate_syndromes(message_poly, num_ec, field): #contains solution
    """L6: Evaluate the message at the roots of the generator polynomial."""
    return [message_poly(field.exp(i)) for i in range(num_ec)]

# ---------------------------------------------------------
# L7: RS Decoding II (Linear Algebra / PGZ Algorithm)
# ---------------------------------------------------------

from algebra_utils import solve_linear
# solve_linear(A, b) performs Gaussian Elimination over a field.
# Use it to solve $G * x = y$ for $x$ over $GF(p^n)$. 


def pgz_error_locator(syndromes, field): #contains solution
    """L7.2: Find Error Locator Polynomial using PGZ algorithm."""
    max_t = len(syndromes) // 2
    for t in range(max_t, 0, -1):
        A = []
        b = []
        for i in range(t):
            A.append(syndromes[i : i + t])
            b.append(-syndromes[i + t])
        try:
            x = solve_linear(A, b)
            return Polynomial(list(x) + [field.one])
        except Exception:
            continue

    return Polynomial([field.one])

# ---------------------------------------------------------
# L8: RS Decoding III (Chien Search & Error Magnitudes)
# ---------------------------------------------------------

def chien_search(err_loc, msg_len, field): #contains solution
    """L8.1: Find the roots of the Error Locator Polynomial."""
    err_pos = []
    for i in range(msg_len):
        root = field.exp((field.size - 1 - i) % (field.size - 1))
        if not err_loc(root):
            err_pos.append(msg_len - 1 - i)
    return err_pos

def linear_error_magnitudes(syndromes, err_pos, msg_len, field): #contains solution
    """L8.2: Calculate the magnitude of each error using Linear Algebra."""
    t = len(err_pos)
    if t == 0: return {}

    X = [field.exp((msg_len - 1 - pos) % (field.size - 1)) for pos in err_pos]

    A = []
    b = []
    for k in range(t):
        row = []
        for i in range(t):
            row.append(X[i] ** k if X[i] != field.zero else (field.one if k == 0 else field.zero))
        A.append(row)
        b.append(syndromes[k])

    Y = solve_linear(A, b)

    return {pos: Y[i] for i, pos in enumerate(err_pos)}
