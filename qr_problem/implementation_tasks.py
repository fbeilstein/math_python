import numpy as np

# =====================================================================
# STUDENT IMPLEMENTATION
# =====================================================================

def encode_text(text):
    """Convert human-readable string to an array of ASCII bytes."""
    return [ord(c) for c in text]

def decode_text(bytes_array):
    """Convert an array of ASCII bytes back to a string."""
    return "".join(chr(b) for b in bytes_array)

# ---------------------------------------------------------
# L1: GF(p) Polynomial Arithmetic
# ---------------------------------------------------------

def extended_gcd(a, b):
    if a == 0: return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1: raise Exception('modular inverse does not exist')
    return x % m

def gfp_poly_divide(dividend, divisor, p):
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
    
    inv_lead = mod_inverse(divisor[0], p)
    
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

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i: i += 1
        else:
            n //= i
            if i not in factors: factors.append(i)
    if n > 1 and n not in factors: factors.append(n)
    return factors

def gfp_poly_multiply(a, b, p):
    res = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            res[i+j] = (res[i+j] + a[i] * b[j]) % p
    return res

def is_primitive(poly, p, n):
    """
    L2: Prove a polynomial of degree n is primitive over GF(p).
    Check that x^(p^n - 1) == 1 mod poly, and x^k != 1 mod poly for all proper divisors k.
    """
    if len(poly) - 1 != n: return False
    
    order = (p ** n) - 1
    factors = prime_factors(order)
    
    def poly_pow_mod(base, exp, mod_poly):
        res = [1]
        base_pow = list(base)
        while exp > 0:
            if exp % 2 == 1:
                res = gfp_poly_multiply(res, base_pow, p)
                _, res = gfp_poly_divide(res, mod_poly, p)
            base_pow = gfp_poly_multiply(base_pow, base_pow, p)
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

def generate_gfpn_tables(p, n, primitive_poly):
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

def gfpn_add(a, b, p, n):
    res = 0; mult = 1
    for _ in range(n):
        res += ((a % p + b % p) % p) * mult
        mult *= p; a //= p; b //= p
    return res

def gfpn_sub(a, b, p, n):
    res = 0; mult = 1
    for _ in range(n):
        res += ((a % p - b % p) % p) * mult
        mult *= p; a //= p; b //= p
    return res

def gfpn_mul(a, b, log_table, exp_table, p, n):
    if a == 0 or b == 0: return 0
    return exp_table[(log_table[a] + log_table[b]) % (p**n - 1)]
    
def gfpn_div(a, b, log_table, exp_table, p, n):
    if b == 0: raise ZeroDivisionError()
    if a == 0: return 0
    return exp_table[(log_table[a] - log_table[b]) % (p**n - 1)]

def gfpn_poly_multiply(poly1, poly2, log_table, exp_table, p, n):
    """L4: Multiply polynomials over GF(p^n)."""
    res = [0] * (len(poly1) + len(poly2) - 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            val = gfpn_mul(poly1[i], poly2[j], log_table, exp_table, p, n)
            res[i+j] = gfpn_add(res[i+j], val, p, n)
    while len(res) > 0 and res[0] == 0: res.pop(0)
    return res if res else [0]

def gfpn_poly_remainder(dividend, divisor, log_table, exp_table, p, n):
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

def get_generator_poly(num_ec_bytes, log_table, exp_table, p, n):
    """L5: Calculate the Reed-Solomon Generator Polynomial."""
    gen = [1]
    for i in range(num_ec_bytes):
        root = gfpn_sub(0, exp_table[i], p, n)
        gen = gfpn_poly_multiply(gen, [1, root], log_table, exp_table, p, n)
    return gen

# ---------------------------------------------------------
# L6: RS Decoding I (Syndromes)
# ---------------------------------------------------------

def calculate_syndromes(message, num_ec, log_table, exp_table, p, n):
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
# L7: RS Decoding II (Berlekamp-Massey)
# ---------------------------------------------------------

def berlekamp_massey(syndromes, log_table, exp_table, p, n):
    """L7: Find the Error Locator Polynomial."""
    C = [1]
    B = [1]
    L = 0
    m = 1
    b = 1
    for i in range(len(syndromes)):
        d = syndromes[i]
        for j in range(1, L + 1):
            if j < len(C):
                term = gfpn_mul(C[j], syndromes[i - j], log_table, exp_table, p, n)
                d = gfpn_add(d, term, p, n)
        if d == 0:
            m += 1
        else:
            T = list(C)
            factor = gfpn_div(d, b, log_table, exp_table, p, n)
            scaled_B = [gfpn_mul(factor, coef, log_table, exp_table, p, n) for coef in B]
            shift_B = [0]*m + scaled_B
            max_len = max(len(C), len(shift_B))
            pad_C = C + [0]*(max_len - len(C))
            pad_B = shift_B + [0]*(max_len - len(shift_B))
            C_new = [gfpn_sub(pad_C[k], pad_B[k], p, n) for k in range(max_len)]
            while len(C_new) > 1 and C_new[-1] == 0: C_new.pop()
            C = C_new
            if 2 * L <= i:
                L = i + 1 - L
                B = T
                b = d
                m = 1
            else:
                m += 1
    return list(reversed(C))

# ---------------------------------------------------------
# L8: RS Decoding III (Chien & Forney)
# ---------------------------------------------------------

def chien_search(err_loc, msg_len, log_table, exp_table, p, n):
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

def forney_algorithm(syndromes, err_loc, err_pos, msg_len, log_table, exp_table, p, n):
    """L8.2: Calculate the magnitude of each error."""
    S_low = syndromes
    Lambda_low = list(reversed(err_loc))
    Omega_low = [0] * (len(S_low) + len(Lambda_low) - 1)
    for i in range(len(S_low)):
        for j in range(len(Lambda_low)):
            val = gfpn_mul(S_low[i], Lambda_low[j], log_table, exp_table, p, n)
            Omega_low[i+j] = gfpn_add(Omega_low[i+j], val, p, n)
    Omega_low = Omega_low[:len(syndromes)]
    Lambda_prime_low = [0] * max(1, len(Lambda_low) - 1)
    for i in range(1, len(Lambda_low)):
        c = 0
        for _ in range(i % p):
            c = gfpn_add(c, Lambda_low[i], p, n)
        Lambda_prime_low[i-1] = c
        
    mags = {}
    for pos in err_pos:
        j = msg_len - 1 - pos
        X_k = exp_table[j % (p**n - 1)]
        X_k_inv = exp_table[(p**n - 1 - j) % (p**n - 1)]
        num = 0
        for i in range(len(Omega_low) - 1, -1, -1):
            num = gfpn_mul(num, X_k_inv, log_table, exp_table, p, n)
            num = gfpn_add(num, Omega_low[i], p, n)
        den = 0
        for i in range(len(Lambda_prime_low) - 1, -1, -1):
            den = gfpn_mul(den, X_k_inv, log_table, exp_table, p, n)
            den = gfpn_add(den, Lambda_prime_low[i], p, n)
        if den == 0: continue
        neg_X_k = gfpn_sub(0, X_k, p, n)
        mag = gfpn_mul(neg_X_k, num, log_table, exp_table, p, n)
        mag = gfpn_div(mag, den, log_table, exp_table, p, n)
        mags[pos] = mag
    return mags

# ---------------------------------------------------------
# L9: QR Code Specialization (The Matrix)
# ---------------------------------------------------------

def build_qr_matrix(version, all_bits, get_format_string):
    """L9: Route the data into the physical QR matrix. (ISO formatting pre-applied)."""
    size = 4 * version + 17
    matrix = np.full((size, size), -1, dtype=int)
    
    def draw_finder(r_start, c_start):
        for r in range(7):
            for c in range(7):
                is_edge = (r == 0 or r == 6 or c == 0 or c == 6)
                is_center = (2 <= r <= 4 and 2 <= c <= 4)
                matrix[r_start + r][c_start + c] = 1 if (is_edge or is_center) else 0
        for i in range(8):
            if r_start + 7 < size and c_start + i < size: matrix[r_start + 7][c_start + i] = 0
            if r_start + i < size and c_start + 7 < size: matrix[r_start + i][c_start + 7] = 0
            if r_start - 1 >= 0 and c_start + i < size: matrix[r_start - 1][c_start + i] = 0
            if r_start + i < size and c_start - 1 >= 0: matrix[r_start + i][c_start - 1] = 0

    draw_finder(0, 0)
    draw_finder(0, size - 7)
    draw_finder(size - 7, 0)
    
    if version >= 2:
        c = size - 7 
        for r in range(-2, 3):
            for col in range(-2, 3):
                is_border = (r == -2 or r == 2 or col == -2 or col == 2)
                is_abs_center = (r == 0 and col == 0)
                matrix[c + r][c + col] = 1 if (is_border or is_abs_center) else 0
    
    for i in range(8, size - 8):
        matrix[6][i] = matrix[i][6] = (i % 2) == 0
        
    matrix[4 * version + 9][8] = 1
    
    fmt = get_format_string()
    tl_x = [0, 1, 2, 3, 4, 5, 7, 8, 8, 8, 8, 8, 8, 8, 8]
    tl_y = [8, 8, 8, 8, 8, 8, 8, 8, 7, 5, 4, 3, 2, 1, 0]
    for i in range(15): matrix[tl_y[i]][tl_x[i]] = int(fmt[i])
    for i in range(7): matrix[size - 1 - i][8] = int(fmt[i])
    for i in range(8): matrix[8][size - 8 + i] = int(fmt[7 + i])

    bit_idx = 0
    direction = -1 
    col = size - 1
    row = size - 1
    
    while col > 0:
        if col == 6: col -= 1 
        for _ in range(size):
            for c_offset in range(2):
                if matrix[row][col - c_offset] == -1: 
                    if bit_idx < len(all_bits):
                        pixel = all_bits[bit_idx]
                        bit_idx += 1
                    else:
                        pixel = 0 
                    
                    if (row + (col - c_offset)) % 2 == 0:
                        pixel ^= 1
                        
                    matrix[row][col - c_offset] = pixel
            row += direction
        row -= direction 
        direction *= -1  
        col -= 2         

    return matrix
