import itertools

def make_poly(coeffs, p):
    """Convert a list of integers into a Polynomial of GaloisFieldElements."""
    import implementation_tasks as tasks
    return tasks.Polynomial([tasks.PrimeField(p)(c) for c in coeffs])

def find_primitives(p, n):
    """L3: Brute force find all primitive polynomials of degree n over GF(p)."""
    import implementation_tasks as tasks
    primitives = []
    for coefs in itertools.product(range(p), repeat=n):
        poly = list(coefs) + [1]
        poly_obj = make_poly(poly, p)
        if tasks.is_primitive(poly_obj):
            primitives.append(poly)
    return primitives

def int_to_ext(val, field):
    """Convert an integer to an ExtFieldElement."""
    import implementation_tasks as tasks
    cs = []
    temp = val
    for _ in range(field.n):
        cs.append(tasks.GaloisFieldElement(temp % field.p, tasks.PrimeField(field.p)))
        temp //= field.p
    return tasks.GaloisFieldElement(tasks.Polynomial(cs), field)

def ext_to_int(element):
    """Convert an ExtFieldElement to an integer."""
    val = 0
    p = element.field.p
    for i in range(element.val.degree() + 1):
        val += element.val[i].val * (p ** i)
    return val


def solve_linear(A, b):
    """L7.1: Solve a linear system Ax = b using Gaussian Elimination.
    
    Raises:
        ValueError: If the matrix A is singular (no unique solution).
    """
    A = [list(row) for row in A]
    b = list(b)
    size = len(b)

    for i in range(size):
        pivot_row = i
        while pivot_row < size and not A[pivot_row][i]:
            pivot_row += 1
        if pivot_row == size:
            raise ValueError("Singular matrix")

        A[i], A[pivot_row] = A[pivot_row], A[i]
        b[i], b[pivot_row] = b[pivot_row], b[i]

        pivot_val = A[i][i]
        for j in range(i, size):
            A[i][j] = A[i][j] / pivot_val
        b[i] = b[i] / pivot_val

        for k in range(i + 1, size):
            factor = A[k][i]
            if factor:
                for j in range(i, size):
                    A[k][j] = A[k][j] - factor * A[i][j]
                b[k] = b[k] - factor * b[i]

    x = [None] * size
    for i in range(size - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, size):
            x[i] = x[i] - A[i][j] * x[j]

    return x
