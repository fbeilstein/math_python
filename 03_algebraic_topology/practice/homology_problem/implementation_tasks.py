import numpy as np
import copy

# =====================================================================
# STUDENT IMPLEMENTATION (Homology)
# =====================================================================

# ---------------------------------------------------------
# L1: Integer Arithmetic (Extended GCD)
# ---------------------------------------------------------

def z_div(a, b): #contains solution
    """
    L1: Euclidean division. 
    Return (quotient, remainder) such that a = b * q + r.
    """
    return divmod(a, b)

def z_gcdex(a, b): #contains solution
    """
    L1: Extended Euclidean Algorithm for Integers.
    Given a, b, return (x, y, g) such that a*x + b*y = g = gcd(a, b).
    Note: gcd should always be >= 0.
    """
    if a == 0 and b == 0: return 0, 1, 0
    if a == 0: return 0, b // abs(b), abs(b)
    if b == 0: return a // abs(a), 0, abs(a)

    x_sign = -1 if a < 0 else 1
    y_sign = -1 if b < 0 else 1
    a, b = abs(a), abs(b)

    x, y, r, s = 1, 0, 0, 1
    while b != 0:
        c, q = a % b, a // b
        a, b, r, s, x, y = b, c, x - q * r, y - q * s, r, s
    return x * x_sign, y * y_sign, a


# ---------------------------------------------------------
# L2: Matrix Row/Col Operations
# ---------------------------------------------------------

def add_columns(m, i, j, a, b, c, d): #contains solution
    """
    L2: Elementary column operations.
    Updates matrix `m` IN-PLACE.
    For every row k:
      old_e = m[k][i]
      m[k][i] = a * old_e + b * m[k][j]
      m[k][j] = c * old_e + d * m[k][j]
    """
    for k in range(len(m)):
        e = m[k][i]
        m[k][i] = a * e + b * m[k][j]
        m[k][j] = c * e + d * m[k][j]

def add_rows(m, i, j, a, b, c, d): #contains solution
    """
    L2: Elementary row operations.
    Updates matrix `m` IN-PLACE.
    For every col k:
      old_e = m[i][k]
      m[i][k] = a * old_e + b * m[j][k]
      m[j][k] = c * old_e + d * m[j][k]
    """
    for k in range(len(m[0])):
        e = m[i][k]
        m[i][k] = a * e + b * m[j][k]
        m[j][k] = c * e + d * m[j][k]

def clear_column(m): #contains solution
    """
    L2: Zero out the first column of `m` (except m[0][0]) using row operations.
    Returns the modified matrix `m`.
    """
    if m[0][0] == 0: return m
    pivot = m[0][0]
    for j in range(1, len(m)):
        if m[j][0] == 0: continue
        q, r = z_div(m[j][0], pivot)
        if r == 0:
            add_rows(m, 0, j, 1, 0, -q, 1)
        else:
            a, b, g = z_gcdex(pivot, m[j][0])
            d_0 = z_div(m[j][0], g)[0]
            d_j = z_div(pivot, g)[0]
            add_rows(m, 0, j, a, b, d_0, -d_j)
            pivot = g
    return m

def clear_row(m): #contains solution
    """
    L2: Zero out the first row of `m` (except m[0][0]) using column operations.
    Returns the modified matrix `m`.
    """
    if m[0][0] == 0: return m
    pivot = m[0][0]
    for j in range(1, len(m[0])):
        if m[0][j] == 0: continue
        q, r = z_div(m[0][j], pivot)
        if r == 0:
            add_columns(m, 0, j, 1, 0, -q, 1)
        else:
            a, b, g = z_gcdex(pivot, m[0][j])
            d_0 = z_div(m[0][j], g)[0]
            d_j = z_div(pivot, g)[0]
            add_columns(m, 0, j, a, b, d_0, -d_j)
            pivot = g
    return m


# ---------------------------------------------------------
# L3: Smith Normal Form
# ---------------------------------------------------------

def invariant_factors(m): #contains solution
    """
    L3: Compute the Smith Normal Form invariants of matrix `m`.
    Returns a list of integers (the diagonal elements).
    Note: m is modified in place, but you may want to copy it first if necessary.
    """
    if len(m) == 0 or len(m[0]) == 0: return []
    
    # 1. Bring a non-zero element to m[0][0] if possible
    ind = [i for i in range(len(m)) if m[i][0] != 0]
    if len(ind) > 0 and ind[0] != 0:
        m[0], m[ind[0]] = m[ind[0]], m[0]
    else:
        ind_col = [j for j in range(len(m[0])) if m[0][j] != 0]
        if len(ind_col) > 0 and ind_col[0] != 0:
            for r in range(len(m)):
                m[r][0], m[r][ind_col[0]] = m[r][ind_col[0]], m[r][0]

    # 2. Iteratively clear row and column until both are zero
    while True:
        has_non_zero = False
        for i in range(1, len(m[0])):
            if m[0][i] != 0: has_non_zero = True
        for i in range(1, len(m)):
            if m[i][0] != 0: has_non_zero = True
            
        if not has_non_zero: break
        
        m = clear_column(m)
        m = clear_row(m)

    # 3. Recursion on the submatrix
    if len(m) == 1 or len(m[0]) == 1:
        invs = []
    else:
        lower_right = []
        for i in range(1, len(m)):
            lower_right.append(m[i][1:])
        invs = invariant_factors(lower_right)

    # 4. Ensure divisibility condition a_i | a_{i+1}
    result = []
    if m[0][0] != 0:
        result.append(m[0][0])
        result.extend(invs)
        for i in range(len(result) - 1):
            if result[i] != 0 and z_div(result[i+1], result[i])[1] != 0:
                g = z_gcdex(result[i+1], result[i])[2]
                result[i+1] = z_div(result[i], g)[0] * result[i+1]
                result[i] = g
            else:
                break
    else:
        invs.append(m[0][0])
        result = invs
        
    return result


# ---------------------------------------------------------
# L4: Boundary Matrices
# ---------------------------------------------------------

def get_complex(tt): #contains solution
    """
    L4: Given a list of triangles (each triangle is a string of 3 sorted characters, e.g., 'ABC'),
    return a sorted list of all unique simplices (vertices, edges, faces).
    """
    parts = set()
    for t in tt:
        # vertex
        parts.add(t[0])
        parts.add(t[1])
        parts.add(t[2])
        # edge
        parts.add("".join(sorted([t[0], t[1]])))
        parts.add("".join(sorted([t[1], t[2]])))
        parts.add("".join(sorted([t[0], t[2]])))
        # face
        parts.add(t)
    return sorted(list(parts))

def calculate_boundary(chain, all_simplices_lower_dim): #contains solution
    """
    L4: Compute the boundary matrix.
    `chain` is a list of k-simplices (e.g. ['AB', 'AC', 'BC']).
    `all_simplices_lower_dim` is a list of (k-1)-simplices (e.g. ['A', 'B', 'C']).
    
    Returns a dictionary containing:
    - 'm': The boundary matrix (list of lists)
    - 'dim': Number of columns (length of chain)
    - 'rank': Rank of the matrix
    - 'smith_invs': Smith Normal Form invariants
    - 'torsion': Torsion coefficients
    - 'v': Rows labels (the lower dim simplices)
    - 'k': Columns labels (the k-simplices)
    """
    n = len(chain)
    matrix_dict = {}
    
    k_labels = []
    for i in range(n):
        k_labels.append(chain[i])
        for j in range(len(chain[i])):
            # Remove the j-th vertex
            x = chain[i][:j] + chain[i][j+1:]
            if x == '': continue
            if x not in matrix_dict:
                matrix_dict[x] = [0] * n
            matrix_dict[x][i] += 1 if (j % 2) == 0 else -1

    # In JS, the `all_simplices_lower_dim` is gathered implicitly from `matrix_dict` keys.
    # We will iterate over `matrix_dict` to form the matrix.
    m = []
    v_labels = []
    new_m = []
    for key in sorted(matrix_dict.keys()):
        m.append(list(matrix_dict[key]))
        new_m.append(list(matrix_dict[key]))
        v_labels.append(key)
        
    m_dim = len(m)
    smith = invariant_factors(new_m)
    
    rank = 0
    torsion = []
    for f in smith:
        if f != 0:
            rank += 1
            if abs(f) != 1:
                torsion.append(f)
                
    return {
        "dim": m_dim, 
        "rank": rank, 
        "smith_invs": smith, 
        "torsion": torsion, 
        "m": m, 
        "v": v_labels, 
        "k": k_labels
    }


# ---------------------------------------------------------
# L5: Homology Computation
# ---------------------------------------------------------

def compute_homology(num_c0, num_c1, num_c2, rank_d1, rank_d2, torsion_d2): #contains solution
    """
    L5: Compute the Betti numbers and torsion coefficients.
    Returns (h0, h1, h2, torsion_d2).
    """
    h0 = num_c0 - rank_d1
    h1 = num_c1 - rank_d1 - rank_d2
    h2 = num_c2 - rank_d2
    return h0, h1, h2, torsion_d2


# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
