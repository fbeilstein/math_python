import random

# =====================================================================
# STUDENT IMPLEMENTATION (RSA Cryptography)
# =====================================================================

def fast_mod_exp(base, exp, mod): #contains solution
    """
    L3: Compute (base^exp) % mod efficiently using square-and-multiply.
    """
    # BEGIN_SOLUTION
    res = 1
    base = base % mod
    while exp > 0:
        if (exp % 2) == 1:
            res = (res * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return res
    # END_SOLUTION

def miller_rabin(n, k=40): #contains solution
    """
    L1: Miller-Rabin primality test. Return True if probable prime, False if composite.
    - Handle edge cases: n <= 1, n == 2, n == 3, n even.
    - Write n-1 as 2^r * d.
    - Test k random bases 'a' in [2, n-2].
    """
    # BEGIN_SOLUTION
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = fast_mod_exp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = fast_mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
            
    return True
    # END_SOLUTION

def generate_prime(bits): #contains solution
    """
    L1: Generate a random odd integer of 'bits' length that passes Miller-Rabin.
    """
    # BEGIN_SOLUTION
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1 # Ensure it's exactly 'bits' long and odd
        if miller_rabin(p):
            return p
    # END_SOLUTION

def extended_gcd(a, b): #contains solution
    """
    L2: Extended Euclidean Algorithm. Return (x, y, g) such that a*x + b*y = g = gcd(a, b).
    """
    # BEGIN_SOLUTION
    if a == 0:
        return (0, 1, b)
    x1, y1, g = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (x, y, g)
    # END_SOLUTION

def mod_inverse(e, phi): #contains solution
    """
    L2: Compute the modular inverse 'd' such that (e * d) % phi == 1.
    If e and phi are not coprime, raise ValueError.
    """
    # BEGIN_SOLUTION
    x, y, g = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("e and phi are not coprime!")
    return x % phi
    # END_SOLUTION

def generate_keypair(bits=512): #contains solution
    """
    L2: Generate an RSA keypair.
    1. Generate two primes p, q of length `bits // 2`
    2. Compute n = p * q
    3. Compute phi = (p-1)*(q-1)
    4. Choose a valid e (usually 65537, or a random valid prime)
    5. Compute d
    Returns ((e, n), (d, n))
    """
    # BEGIN_SOLUTION
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    # Ensure e is coprime to phi
    if phi % e == 0:
        # Fallback to finding a random coprime e if 65537 fails
        while True:
            e = random.randrange(3, phi, 2)
            if extended_gcd(e, phi)[2] == 1:
                break
                
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))
    # END_SOLUTION

def encrypt(m_int, pub_key): #contains solution
    """
    L3: Textbook RSA Encryption -> c = m^e (mod n)
    """
    # BEGIN_SOLUTION
    e, n = pub_key
    return fast_mod_exp(m_int, e, n)
    # END_SOLUTION

def decrypt(c_int, priv_key): #contains solution
    """
    L3: Textbook RSA Decryption -> m = c^d (mod n)
    """
    # BEGIN_SOLUTION
    d, n = priv_key
    return fast_mod_exp(c_int, d, n)
    # END_SOLUTION
