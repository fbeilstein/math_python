import numpy as np

def build_adjacency_matrix(num_nodes, edges): #contains solution
    """
    Construct a dense Adjacency Matrix from a list of edges.
    edges: list of tuples (node1, node2, weight)
    num_nodes: integer representing total number of nodes (0 to num_nodes-1)
    
    Return a numpy array A of shape (num_nodes, num_nodes).
    Remember that the graph is undirected, so A[i][j] = A[j][i].
    """
    A = np.zeros((num_nodes, num_nodes))
    for u, v, w in edges:
        A[u, v] = w
        A[v, u] = w
    return A

def build_laplacian_matrix(A): #contains solution
    """
    Construct the unnormalized Graph Laplacian L = D - A.
    A is the adjacency matrix.
    D is the degree matrix (a diagonal matrix where D[i, i] is the sum of row i in A).
    """
    D = np.diag(np.sum(A, axis=1))
    return D - A

def build_normalized_laplacian(A): #contains solution
    """
    Construct the normalized Graph Laplacian L_norm = I - D^{-1/2} A D^{-1/2}.
    If a node is isolated (degree 0), its D^{-1/2} entry should be 0.
    """
    d = np.sum(A, axis=1)
    d_inv_sqrt = np.zeros_like(d)
    d_inv_sqrt[d > 0] = 1.0 / np.sqrt(d[d > 0])
    D_inv_sqrt = np.diag(d_inv_sqrt)
    I = np.eye(A.shape[0])
    return I - D_inv_sqrt @ A @ D_inv_sqrt

def compute_spectrum(L): #contains solution
    """
    Compute the eigenvalues and eigenvectors of a symmetric matrix L.
    Use numpy.linalg.eigh (since L is symmetric).
    Return (eigenvalues, eigenvectors) sorted by eigenvalue in ascending order.
    """
    evals, evecs = np.linalg.eigh(L)
    idx = np.argsort(evals)
    return evals[idx], evecs[:, idx]

def find_zero_eigenvectors(L, tol=1e-5): #contains solution
    """
    Given a Graph Laplacian L, compute its spectrum and
    return a matrix whose columns are the eigenvectors corresponding 
    to eigenvalues that are approximately 0 (less than tol).
    """
    evals, evecs = compute_spectrum(L)
    zero_indices = np.where(evals < tol)[0]
    return evecs[:, zero_indices]

def get_spectral_coordinates(L): #contains solution
    """
    For Spectral Graph Drawing (Level 3).
    Given a Graph Laplacian L, compute its spectrum.
    Return the X and Y coordinates for each node using the 2nd and 3rd smallest eigenvectors.
    (Assuming the graph is fully connected, so the 1st eigenvector is the constant 0-eigenvector).
    
    Return a tuple: (x_coords, y_coords) where each is a 1D numpy array of size N.
    """
    evals, evecs = compute_spectrum(L)
    v2 = evecs[:, 1]
    v3 = evecs[:, 2]
    return v2, v3

def get_fiedler_vector(L): #contains solution
    """
    For Spectral Image Segmentation (Level 4).
    Given a Normalized Graph Laplacian L, compute its spectrum.
    Return the Fiedler vector (the eigenvector corresponding to the 2nd smallest eigenvalue).
    """
    evals, evecs = compute_spectrum(L)
    return evecs[:, 1]

# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
