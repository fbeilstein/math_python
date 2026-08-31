from itertools import zip_longest
# =====================================================================
# STUDENT IMPLEMENTATION
# =====================================================================

# ---------------------------------------------------------
# L1: Prime Field Elements — GF(p) arithmetic
# ---------------------------------------------------------

class PrimeField:
    """A finite field of prime order p."""
    _instances = {}
    def __new__(cls, p):
        if p not in cls._instances:
            inst = super().__new__(cls)
            inst._initialize(p)
            cls._instances[p] = inst
        return cls._instances[p]

    def _initialize(self, p):
        """Initializes the prime field with prime number p."""
        self.modulus = p

    @property
    def p(self):
        """Returns the prime characteristic of the field."""
        return self.modulus

    @property
    def size(self):
        """Returns the total number of elements in the field."""
        return self.modulus

    @property
    def zero(self):
        """Returns the additive identity (0) of the field."""
        return GaloisFieldElement(0, self)

    @property
    def one(self):
        """Returns the multiplicative identity (1) of the field."""
        return GaloisFieldElement(1, self)
    
    def __call__(self, val):
        """Creates a field element from an integer value."""
        return GaloisFieldElement(val, self)


class GaloisFieldElement:
    """An element of a Galois Field."""
    def __init__(self, val, field):
        self.field = field
        self.val = val % field.modulus

    def __add__(self, other): #contains solution
        """Adds two field elements.

        Args:
            other (GaloisFieldElement): The element to add.

        Returns:
            GaloisFieldElement: The sum modulo p.
        """
        return GaloisFieldElement((self.val + other.val) % self.field.modulus, self.field)
    def __sub__(self, other): #contains solution
        """Subtracts one field element from another.

        Args:
            other (GaloisFieldElement): The element to subtract.

        Returns:
            GaloisFieldElement: The difference modulo p.
        """
        return GaloisFieldElement((self.val - other.val) % self.field.modulus, self.field)
    def __mul__(self, other): #contains solution
        """Multiplies two field elements.

        Args:
            other (GaloisFieldElement): The element to multiply by.

        Returns:
            GaloisFieldElement: The product modulo p.
        """
        return GaloisFieldElement((self.val * other.val) % self.field.modulus, self.field)
    def __truediv__(self, other): #contains solution
        """Divides this element by another using the multiplicative inverse.

        Args:
            other (GaloisFieldElement): The non-zero divisor element.

        Returns:
            GaloisFieldElement: The quotient modulo p.

        Raises:
            ZeroDivisionError: If the divisor is the zero element. (Hint: explicitly use `raise ZeroDivisionError()`)
        """
        if not other: raise ZeroDivisionError()
        return self * (other ** (self.field.size - 2))
    def __floordiv__(self, other):
        """Alias for division since finite field division is always exact."""
        return self.__truediv__(other)
    def __pow__(self, exponent): #contains solution
        """Raises the element to an integer power using binary exponentiation.

        Args:
            exponent (int): The power to raise the element to. Can be negative.

        Returns:
            GaloisFieldElement: The exponentiated result.
        """
        if exponent < 0:
            if self.val == self.field.zero.val:
                raise ZeroDivisionError("division by zero")
            exponent = (self.field.size - 2) * (- exponent) % (self.field.size - 1)
            
        if exponent == 0: return self.field.one
        result = self.field.one
        base = self
        while exponent > 0:
            if exponent % 2 == 1: result = result * base
            base = base * base
            exponent //= 2
        return result
    def __neg__(self):
        """Returns the additive inverse (-a)."""
        return self.field.zero - self
    def __bool__(self):
        """Returns True if the element is not zero."""
        return bool(self.val)
    def __eq__(self, other):
        """Checks equality between two field elements."""
        return isinstance(other, GaloisFieldElement) and self.field == other.field and self.val == other.val
    def __repr__(self): return str(self.val)
    def __hash__(self): return hash(self.val)

# ---------------------------------------------------------
# L2: The Universal Polynomial
# ---------------------------------------------------------

class Polynomial:
    """A polynomial over a field. The internal representation is entirely up to you."""
    def __init__(self, coeffs): #contains solution
        """Initializes the polynomial with a list of coefficients.

        Args:
            coeffs (list[GaloisFieldElement]): Coefficients in Low-to-High order (c_0, c_1, ..., c_n).
                So coeffs[i] is the coefficient for x^i. (Note: This internal Low-to-High order 
                is chosen because array index `i` naturally matches the polynomial degree `x^i`, 
                making algorithms easier to write. The UI and ISO QR standards use High-to-Low.)
            
        Raises:
            ValueError: If coeffs is empty. (Hint: explicitly use `raise ValueError()`)
        """
        if not coeffs:
            raise ValueError("Cannot initialize Polynomial with empty coefficients.")
        self._internal_coeffs = list(coeffs)
        while len(self._internal_coeffs) > 1 and not self._internal_coeffs[-1]:
            self._internal_coeffs.pop()
        if not self._internal_coeffs:
            self._internal_coeffs = [coeffs[0].field.zero]

    def degree(self): #contains solution
        """Calculates the mathematical degree of the polynomial.

        Returns:
            int: The highest power of x with a non-zero coefficient. Returns 0 for the constant polynomials.
        """
        return len(self._internal_coeffs) - 1

    def __getitem__(self, power): #contains solution
        """Retrieves the coefficient for a specific power of x.

        Args:
            power (int): The power of x.

        Returns:
            GaloisFieldElement: The coefficient of x^power, or zero if power exceeds the degree.
            
        Raises:
            IndexError: If the power is negative. (Hint: explicitly use `raise IndexError()`)
        """
        if power < 0: raise IndexError("Negative powers not supported.")
        if power > self.degree():
            return self._internal_coeffs[0].field.zero
        return self._internal_coeffs[power]

    def __add__(self, other): #contains solution
        """Adds two polynomials.

        Args:
            other (Polynomial): The polynomial to add.

        Returns:
            Polynomial: A new polynomial representing the sum.
        """
        max_deg = max(self.degree(), other.degree())
        res = [self[i] + other[i] for i in range(max_deg + 1)]
        return Polynomial(res)

    def __sub__(self, other): #contains solution
        """Subtracts one polynomial from another.

        Args:
            other (Polynomial): The polynomial to subtract.

        Returns:
            Polynomial: A new polynomial representing the difference.
        """
        max_deg = max(self.degree(), other.degree())
        res = [self[i] - other[i] for i in range(max_deg + 1)]
        return Polynomial(res)

    def __mul__(self, other): #contains solution
        """Multiplies two polynomials using cross-multiplication.

        Args:
            other (Polynomial): The polynomial to multiply by.

        Returns:
            Polynomial: A new polynomial representing the product.
        """
        res = [self[0].field.zero] * (self.degree() + other.degree() + 1)
        for i in range(self.degree() + 1):
            for j in range(other.degree() + 1):
                res[i+j] = res[i+j] + self[i] * other[j]
        return Polynomial(res)

    def __divmod__(self, other): #contains solution
        """Performs polynomial long division.

        Args:
            other (Polynomial): The divisor polynomial.

        Returns:
            tuple[Polynomial, Polynomial]: A tuple containing (quotient, remainder).

        Raises:
            ZeroDivisionError: If the divisor is the zero polynomial. (Hint: explicitly use `raise ZeroDivisionError()`)
        """
        if not other: raise ZeroDivisionError()
        dividend = [self[i] for i in range(self.degree() + 1)]
        divisor = [other[i] for i in range(other.degree() + 1)]
        
        if len(dividend) < len(divisor):
            return Polynomial([self[0].field.zero]), self
            
        quotient = [self[0].field.zero] * (len(dividend) - len(divisor) + 1)
        for i in range(len(quotient) - 1, -1, -1):
            if dividend[i + len(divisor) - 1]:
                coef = dividend[i + len(divisor) - 1] / divisor[-1]
                quotient[i] = coef
                for j in range(len(divisor)):
                    dividend[i + j] = dividend[i + j] - coef * divisor[j]
        return Polynomial(quotient), Polynomial(dividend)

    def __call__(self, x): #contains solution
        """Evaluates the polynomial at a given value using Horner's method.

        Args:
            x (GaloisFieldElement): The value to substitute for x.

        Returns:
            GaloisFieldElement: The evaluated result.
        """
        val = self[self.degree()]
        for i in range(self.degree() - 1, -1, -1):
            val = val * x + self[i]
        return val

    # --- API-driven boilerplate functions ---
    
    @property
    def base_field(self):
        """Returns the underlying field of the coefficients."""
        return self[0].field

    def __bool__(self):
        """Returns True if the polynomial is not the zero polynomial."""
        return self.degree() > 0 or bool(self[0])

    def __mod__(self, other):
        """Returns the remainder of polynomial division."""
        _, rem = divmod(self, other)
        return rem

    def __floordiv__(self, other):
        """Returns the quotient of polynomial division."""
        q, _ = divmod(self, other)
        return q

    def __pow__(self, exponent, mod_poly=None):
        """Raises the polynomial to an integer power using binary exponentiation."""
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

    def __eq__(self, other):
        """Checks if two polynomials are mathematically equal."""
        if not isinstance(other, Polynomial): return False
        if self.degree() != other.degree(): return False
        return all(self[i] == other[i] for i in range(self.degree() + 1))

    def __repr__(self): 
        """Returns a string representation of the polynomial coefficients."""
        return f"Poly({[self[i] for i in range(self.degree() + 1)]})"
        
    def __hash__(self): 
        """Computes a hash based on the polynomial coefficients."""
        return hash(tuple(self[i] for i in range(self.degree() + 1)))

# ---------------------------------------------------------
# L3: Primitive Polynomial Search
# ---------------------------------------------------------

def is_primitive(poly): #contains solution
    n = poly.degree()
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
    x = Polynomial([zero, PrimeField(p).one]) # Low-to-High: 0 + 1x
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
        """Singleton pattern"""
        if mod_poly not in cls._instances:
            inst = super().__new__(cls)
            inst._initialize(mod_poly)
            cls._instances[mod_poly] = inst
        return cls._instances[mod_poly]

    def _initialize(self, mod_poly): #contains solution
        """Initializes the extension field with a modulus polynomial.

        Args:
            mod_poly (Polynomial): The irreducible modulus polynomial generating the field.
        """
        self.modulus = mod_poly

    @property
    def p(self): #contains solution
        """Returns the characteristic of the base prime field.

        Returns:
            int: The prime number p.
        """
        return self.modulus[0].field.p

    @property
    def n(self): #contains solution
        """Returns the degree of the extension.

        Returns:
            int: The degree n of the modulus polynomial.
        """
        return self.modulus.degree()

    @property
    def size(self): #contains solution
        """Returns the total number of elements in the extension field.

        Returns:
            int: The size of the field (p^n).
        """
        return self.p ** self.n

    @property
    def zero(self): #contains solution
        """Returns the additive identity (zero) of the extension field.

        Returns:
            GaloisFieldElement: The zero element.
        """
        base_field = self.modulus[0].field
        return GaloisFieldElement(Polynomial([base_field.zero]), self)

    @property
    def one(self): #contains solution
        """Returns the multiplicative identity (one) of the extension field.

        Returns:
            GaloisFieldElement: The one element.
        """
        base_field = self.modulus[0].field
        return GaloisFieldElement(Polynomial([base_field.one]), self)
        
    @property
    def alpha(self): #contains solution
        """Returns the generator element x of the extension field."""
        base_field = self.modulus[0].field
        return GaloisFieldElement(Polynomial([base_field.zero, base_field.one]), self)
        
    def __call__(self, val):
        return GaloisFieldElement(val, self)




# ---------------------------------------------------------
# L5: RS Encoding
# ---------------------------------------------------------

def get_generator_poly(num_ec_bytes, field): #contains solution
    gen = Polynomial([field.one])
    for i in range(num_ec_bytes):
        root = -(field.alpha ** i)
        term = Polynomial([root, field.one]) # Low-to-High: root + 1x
        gen = gen * term
    return gen

# ---------------------------------------------------------
# L6: RS Decoding I (Syndromes)
# ---------------------------------------------------------

def calculate_syndromes(message_poly, num_ec, field): #contains solution
    return [message_poly(field.alpha ** i) for i in range(num_ec)]

# ---------------------------------------------------------
# L7: RS Decoding II (Linear Algebra / PGZ Algorithm)
# ---------------------------------------------------------

from algebra_utils import solve_linear
# solve_linear(A, b) performs Gaussian Elimination over a field.
# Use it to solve G * x = y for x over GF(p^n).
# Note: It explicitly raises ValueError("Singular matrix") if the matrix is singular.


def pgz_error_locator(syndromes, field): #contains solution
    max_t = len(syndromes) // 2
    for t in range(max_t, 0, -1):
        A = []
        b = []
        for i in range(t):
            A.append(syndromes[i : i + t])
            b.append(-syndromes[i + t])
        try:
            x = solve_linear(A, b)
            return Polynomial([field.one] + list(reversed(x))) # Low-to-High: 1 + x_0 x + ... + x_{t-1} x^t
        except ValueError:
            continue

    return Polynomial([field.one])

# ---------------------------------------------------------
# L8: RS Decoding III (Chien Search & Error Magnitudes)
# ---------------------------------------------------------

def chien_search(err_loc, msg_len, field): #contains solution
    err_pos = []
    for i in range(msg_len):
        root = field.alpha ** ((field.size - 1 - i) % (field.size - 1))
        if not err_loc(root):
            err_pos.append(i)
    return err_pos

def linear_error_magnitudes(syndromes, err_pos, msg_len, field): #contains solution
    t = len(err_pos)
    if t == 0: return {}

    X = [field.alpha ** pos for pos in err_pos]

    A = []
    b = []
    for k in range(t):
        row = []
        for i in range(t):
            row.append(X[i] ** k)
        A.append(row)
        b.append(syndromes[k])

    Y = solve_linear(A, b)

    return {pos: Y[i] for i, pos in enumerate(err_pos)}
