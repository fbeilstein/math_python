import numpy as np

def get_derivatives(x, z, tr, det): #contains solution
    """
    Returns dx/dt and dz/dt for the system:
    [dx/dt, dz/dt]^T = A [x, z]^T
    where A has trace `tr` and determinant `det`.
    Using the standard companion matrix A = [[0, 1], [-det, tr]].
    """
    return z, -det*x + tr*z

def get_lambdas(tr, det): #contains solution
    """
    Calculates the eigenvalues (lambdas) of the 2x2 matrix with trace `tr` and determinant `det`.
    Returns an array of [Re(L1), Im(L1), Re(L2), Im(L2)].
    """
    disc = tr**2 - 4*det
    if disc >= 0:
        L1 = (tr + np.lib.scimath.sqrt(disc)) / 2
        L2 = (tr - np.lib.scimath.sqrt(disc)) / 2
        return [L1, 0, L2, 0]
    else:
        L_imag = np.sqrt(-disc) / 2
        L_real = tr / 2
        return np.array([L_real, L_imag, L_real, -L_imag])

def classify_system(tr, det): #contains solution
    """
    Classifies the fixed point based on the trace and determinant.
    Returns a string label (e.g., "Saddle", "Center", "Stable Node").
    """
    disc = tr**2 - 4*det
    if det < 0: return "Saddle"
    if disc < 0:
        if abs(tr) < 0.001: return "Center"
        return "Stable Spiral" if tr < 0 else "Unstable Spiral"
    return "Stable Node" if tr < 0 else "Unstable Node"

# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
