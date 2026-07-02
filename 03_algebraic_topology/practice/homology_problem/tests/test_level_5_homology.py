import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel5Homology(unittest.TestCase):
    
    def test_l5_sphere(self):
        # A tetrahedron (sphere surface) has 4 vertices, 6 edges, 4 faces.
        # It's H0=1, H1=0, H2=1.
        # Boundary matrix ranks: rank(d1) = 3, rank(d2) = 3
        h0, h1, h2, torsion = tasks.compute_homology(4, 6, 4, 3, 3, [])
        self.assertEqual(h0, 1)
        self.assertEqual(h1, 0)
        self.assertEqual(h2, 1)

    def test_l5_torus(self):
        # A standard torus mesh: 9 vertices, 27 edges, 18 faces
        # H0=1, H1=2, H2=1
        # rank(d1) = 8, rank(d2) = 17
        h0, h1, h2, torsion = tasks.compute_homology(9, 27, 18, 8, 17, [])
        self.assertEqual(h0, 1)
        self.assertEqual(h1, 2)
        self.assertEqual(h2, 1)

    def test_l5_klein_bottle(self):
        # Klein Bottle: H0=1, H1=1, torsion=Z_2, H2=0
        h0, h1, h2, torsion = tasks.compute_homology(9, 27, 18, 8, 18, [2])
        self.assertEqual(h0, 1)
        self.assertEqual(h1, 1)
        self.assertEqual(h2, 0)
        self.assertIn(2, torsion)

if __name__ == '__main__':
    unittest.main()
