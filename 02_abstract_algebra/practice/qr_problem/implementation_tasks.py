import numpy as np

# =====================================================================
# STUDENT IMPLEMENTATION
# =====================================================================

# ---------------------------------------------------------
# L1: GF(p) Polynomial Arithmetic
# ---------------------------------------------------------

def gfp_poly_divide(dividend, divisor, p): #contains solution
    """
    L1: Polynomial long division over GF(p).
    Both polynomials are lists of integer coefficients from highest degree to lowest.
    Example: 2x^2 + 1 -> [2, 0, 1]
    Return (quotient, remainder).
    """
    dividend = [c % p for c in dividend]
    divisor = [c % p for c in divisor]
    while len(dividend) > 0 and dividend[0] == 0: dividend.pop(0)
    while len(divisor) > 0 and divisor[0] == 0: divisor.pop(0)
    
    if not divisor: raise ZeroDivisionError("Polynomial division by zero")
    if len(dividend) < len(divisor): return [0], dividend
        
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    remainder = list(dividend)
    
    inv_lead = pow(divisor[0], p - 2, p)
    
    for i in range(len(quotient)):
        if remainder[i] != 0:
            coef = (remainder[i] * inv_lead) % p
            quotient[i] = coef
            for j in range(len(divisor)):
                remainder[i + j] = (remainder[i + j] - coef * divisor[j]) % p
                
    while len(remainder) > 0 and remainder[0] == 0: remainder.pop(0)
    if not remainder: remainder = [0]
    return quotient, remainder


# ---------------------------------------------------------
# L2: General Primitive Polynomial Search
# ---------------------------------------------------------

def is_primitive(poly, p, n): #contains solution
    """
    L2: Prove a polynomial of degree n is primitive over GF(p).
    Check that x^(p^n - 1) == 1 mod poly, and x^k != 1 mod poly for all proper divisors k.
    """
    if len(poly) - 1 != n: return False
    
    order = (p ** n) - 1
    
    factors = []
    temp = order
    for i in range(2, int(temp**0.5) + 1):
        if temp % i == 0:
            factors.append(i)
            while temp % i == 0: temp //= i
    if temp > 1: factors.append(temp)
    
    def gfp_poly_mul(a, b):
        res = [0] * (len(a) + len(b) - 1)
        for i in range(len(a)):
            for j in range(len(b)):
                res[i+j] = (res[i+j] + a[i] * b[j]) % p
        return res
    
    def poly_pow_mod(base, exp, mod_poly):
        res = [1]
        base_pow = list(base)
        while exp > 0:
            if exp % 2 == 1:
                res = gfp_poly_mul(res, base_pow)
                _, res = gfp_poly_divide(res, mod_poly, p)
            base_pow = gfp_poly_mul(base_pow, base_pow)
            _, base_pow = gfp_poly_divide(base_pow, mod_poly, p)
            exp //= 2
        return res
        
    x = [1, 0]
    res = poly_pow_mod(x, order, poly)
    if res != [1]: return False
        
    for q in factors:
        res = poly_pow_mod(x, order // q, poly)
        if res == [1]: return False
            
    return True


# ---------------------------------------------------------
# L3: GF(p^n) Field Generation
# ---------------------------------------------------------

def generate_gfpn_tables(p, n, primitive_poly): #contains solution
    """
    L3: Construct the Exponential and Logarithmic lookup tables for GF(p^n).
    """
    field_size = p**n
    exp_table = [0] * field_size
    log_table = [0] * field_size
    
    def poly_to_int(poly):
        val = 0
        for c in poly: val = val * p + c
        return val

    current_poly = [1]
    for i in range(field_size - 1):
        val = poly_to_int(current_poly)
        exp_table[i] = val
        log_table[val] = i
        
        current_poly.append(0)
        _, current_poly = gfp_poly_divide(current_poly, primitive_poly, p)
        
    exp_table[field_size - 1] = exp_table[0]
    return exp_table, log_table


# ---------------------------------------------------------
# L4: GF(p^n) Polynomial Arithmetic
# ---------------------------------------------------------

def gfpn_add(a, b, p, n): #contains solution
    res = 0; mult = 1
    for _ in range(n):
        res += ((a % p + b % p) % p) * mult
        mult *= p; a //= p; b //= p
    return res

def gfpn_sub(a, b, p, n): #contains solution
    res = 0; mult = 1
    for _ in range(n):
        res += ((a % p - b % p) % p) * mult
        mult *= p; a //= p; b //= p
    return res

def gfpn_mul(a, b, log_table, exp_table, p, n): #contains solution
    if a == 0 or b == 0: return 0
    return exp_table[(log_table[a] + log_table[b]) % (p**n - 1)]
    
def gfpn_div(a, b, log_table, exp_table, p, n): #contains solution
    if b == 0: raise ZeroDivisionError()
    if a == 0: return 0
    return exp_table[(log_table[a] - log_table[b]) % (p**n - 1)]

def gfpn_poly_multiply(poly1, poly2, log_table, exp_table, p, n): #contains solution
    """L4: Multiply polynomials over GF(p^n)."""
    res = [0] * (len(poly1) + len(poly2) - 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            val = gfpn_mul(poly1[i], poly2[j], log_table, exp_table, p, n)
            res[i+j] = gfpn_add(res[i+j], val, p, n)
    while len(res) > 0 and res[0] == 0: res.pop(0)
    return res if res else [0]

def gfpn_poly_remainder(dividend, divisor, log_table, exp_table, p, n): #contains solution
    """L4: Find the remainder of polynomial division over GF(p^n)."""
    dividend = list(dividend)
    divisor = list(divisor)
    while len(dividend) > 0 and dividend[0] == 0: dividend.pop(0)
    while len(divisor) > 0 and divisor[0] == 0: divisor.pop(0)
    if not divisor: raise ZeroDivisionError()
    if len(dividend) < len(divisor): return dividend
        
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    remainder = list(dividend)
    
    for i in range(len(quotient)):
        if remainder[i] != 0:
            coef = gfpn_div(remainder[i], divisor[0], log_table, exp_table, p, n)
            quotient[i] = coef
            for j in range(len(divisor)):
                val = gfpn_mul(coef, divisor[j], log_table, exp_table, p, n)
                remainder[i + j] = gfpn_sub(remainder[i + j], val, p, n)
                
    while len(remainder) > 0 and remainder[0] == 0: remainder.pop(0)
    return remainder if remainder else [0]


# ---------------------------------------------------------
# L5: RS Encoding
# ---------------------------------------------------------

def get_generator_poly(num_ec_bytes, log_table, exp_table, p, n): #contains solution
    """L5: Calculate the Reed-Solomon Generator Polynomial."""
    gen = [1]
    for i in range(num_ec_bytes):
        root = gfpn_sub(0, exp_table[i], p, n)
        gen = gfpn_poly_multiply(gen, [1, root], log_table, exp_table, p, n)
    return gen

# ---------------------------------------------------------
# L6: RS Decoding I (Syndromes)
# ---------------------------------------------------------

def calculate_syndromes(message, num_ec, log_table, exp_table, p, n): #contains solution
    """L6: Evaluate the message at the roots of the generator polynomial."""
    syndromes = []
    for i in range(num_ec):
        val = 0
        root = exp_table[i]
        for coef in message:
            val = gfpn_mul(val, root, log_table, exp_table, p, n)
            val = gfpn_add(val, coef, p, n)
        syndromes.append(val)
    return syndromes

# ---------------------------------------------------------
# L7: RS Decoding II (Linear Algebra / PGZ Algorithm)
# ---------------------------------------------------------

def gfpn_solve_linear(A, b, log_table, exp_table, p, n): #contains solution
    """L7.1: Solve a linear system Ax = b over GF(p^n) using Gaussian Elimination."""
    A = [list(row) for row in A]
    b = list(b)
    size = len(b)
    
    # Forward elimination
    for i in range(size):
        # Find pivot
        pivot_row = i
        while pivot_row < size and A[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == size:
            raise Exception("Singular matrix")
            
        # Swap rows
        A[i], A[pivot_row] = A[pivot_row], A[i]
        b[i], b[pivot_row] = b[pivot_row], b[i]
        
        # Normalize pivot row
        pivot_val = A[i][i]
        for j in range(i, size):
            A[i][j] = gfpn_div(A[i][j], pivot_val, log_table, exp_table, p, n)
        b[i] = gfpn_div(b[i], pivot_val, log_table, exp_table, p, n)
        
        # Eliminate below
        for k in range(i + 1, size):
            factor = A[k][i]
            if factor != 0:
                for j in range(i, size):
                    val = gfpn_mul(factor, A[i][j], log_table, exp_table, p, n)
                    A[k][j] = gfpn_sub(A[k][j], val, p, n)
                val = gfpn_mul(factor, b[i], log_table, exp_table, p, n)
                b[k] = gfpn_sub(b[k], val, p, n)
                
    # Back substitution
    x = [0] * size
    for i in range(size - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, size):
            val = gfpn_mul(A[i][j], x[j], log_table, exp_table, p, n)
            x[i] = gfpn_sub(x[i], val, p, n)
            
    return x

def pgz_error_locator(syndromes, log_table, exp_table, p, n): #contains solution
    """L7.2: Find Error Locator Polynomial using Linear Algebra (PGZ algorithm)."""
    max_t = len(syndromes) // 2
    for t in range(max_t, 0, -1):
        A = []
        b = []
        for i in range(t):
            # Matrix A: row i is S[i], S[i+1], ..., S[i+t-1]
            A.append(syndromes[i : i + t])
            # Vector b: -S[i+t]
            b.append(gfpn_sub(0, syndromes[i + t], p, n))
            
        try:
            x = gfpn_solve_linear(A, b, log_table, exp_table, p, n)
            # x is [L_t, L_{t-1}, ..., L_1]. The error locator is L_t x^t + ... + L_1 x + 1.
            return list(x) + [1]
        except Exception:
            # Matrix was singular; there are fewer than t errors. Try t-1.
            continue
            
    return [1] # No errors


# ---------------------------------------------------------
# L8: RS Decoding III (Chien & Forney)
# ---------------------------------------------------------

def chien_search(err_loc, msg_len, log_table, exp_table, p, n): #contains solution
    """L8.1: Find the roots of the Error Locator Polynomial to pinpoint errors."""
    err_pos = []
    for i in range(msg_len):
        root = exp_table[(p**n - 1 - i) % (p**n - 1)]
        val = 0
        for coef in err_loc:
            val = gfpn_mul(val, root, log_table, exp_table, p, n)
            val = gfpn_add(val, coef, p, n)
        if val == 0:
            err_pos.append(msg_len - 1 - i)
    return err_pos

def linear_error_magnitudes(syndromes, err_pos, msg_len, log_table, exp_table, p, n): #contains solution
    """L8.2: Calculate the magnitude of each error using Linear Algebra."""
    t = len(err_pos)
    if t == 0: return {}
    
    X = []
    for pos in err_pos:
        j = msg_len - 1 - pos
        X.append(exp_table[j % (p**n - 1)])
        
    A = []
    b = []
    for k in range(t):
        row = []
        for i in range(t):
            if X[i] == 0:
                val = 1 if k == 0 else 0
            else:
                j = log_table[X[i]]
                val = exp_table[(j * k) % (p**n - 1)]
            row.append(val)
        A.append(row)
        b.append(syndromes[k])
        
    Y = gfpn_solve_linear(A, b, log_table, exp_table, p, n)
    
    mags = {}
    for i, pos in enumerate(err_pos):
        mags[pos] = Y[i]
        
    return mags


