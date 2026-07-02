import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestSpectralGraph(unittest.TestCase):
    def setUp(self):
        self.num_nodes = 3
        # Triangle graph
        self.edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 0, 1.0)]

    def test_build_adjacency_matrix(self):
        A = tasks.build_adjacency_matrix(self.num_nodes, self.edges)
        self.assertEqual(A.shape, (3, 3))
        self.assertEqual(A[0, 1], 1.0)
        self.assertEqual(A[1, 0], 1.0)
        self.assertEqual(A[0, 0], 0.0)

    def test_build_laplacian(self):
        A = tasks.build_adjacency_matrix(self.num_nodes, self.edges)
        L = tasks.build_laplacian_matrix(A)
        self.assertEqual(L[0, 0], 2.0)
        self.assertEqual(L[1, 1], 2.0)
        self.assertEqual(L[0, 1], -1.0)
        
        # Row sums of Laplacian should be 0
        self.assertAlmostEqual(np.sum(L[0, :]), 0)

    def test_build_normalized_laplacian(self):
        A = tasks.build_adjacency_matrix(self.num_nodes, self.edges)
        L_norm = tasks.build_normalized_laplacian(A)
        # For a regular graph of degree 2, L_norm = I - (1/2)*A
        self.assertAlmostEqual(L_norm[0, 0], 1.0)
        self.assertAlmostEqual(L_norm[0, 1], -0.5)

    def test_compute_spectrum(self):
        A = tasks.build_adjacency_matrix(self.num_nodes, self.edges)
        L = tasks.build_laplacian_matrix(A)
        evals, evecs = tasks.compute_spectrum(L)
        
        # Eigenvalues of triangle graph Laplacian: 0, 3, 3
        self.assertAlmostEqual(evals[0], 0.0)
        self.assertAlmostEqual(evals[1], 3.0)
        self.assertAlmostEqual(evals[2], 3.0)

    def test_find_zero_eigenvectors(self):
        # Create a disconnected graph (2 components)
        edges = [(0, 1, 1.0), (2, 3, 1.0)]
        A = tasks.build_adjacency_matrix(4, edges)
        L = tasks.build_laplacian_matrix(A)
        zero_evecs = tasks.find_zero_eigenvectors(L)
        # Should have 2 zero eigenvalues -> 2 columns
        self.assertEqual(zero_evecs.shape[1], 2)

    def test_get_spectral_coordinates(self):
        A = tasks.build_adjacency_matrix(self.num_nodes, self.edges)
        L = tasks.build_laplacian_matrix(A)
        v2, v3 = tasks.get_spectral_coordinates(L)
        self.assertEqual(len(v2), 3)
        self.assertEqual(len(v3), 3)

    def test_get_fiedler_vector(self):
        A = tasks.build_adjacency_matrix(self.num_nodes, self.edges)
        L_norm = tasks.build_normalized_laplacian(A)
        fiedler = tasks.get_fiedler_vector(L_norm)
        self.assertEqual(len(fiedler), 3)

if __name__ == '__main__':
    unittest.main()
