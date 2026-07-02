import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel1Line(unittest.TestCase):
    
    def test_l1_infinite_hit(self):
        """Checks if the math finds the intersection point."""
        origin, rd = np.array([0.0, 0.0]), np.array([1.0, 0.0])
        p1, p2 = np.array([5.0, -5.0]), np.array([5.0, 5.0])
        result = tasks.intersect_line_infinite(origin, rd, p1, p2)
        
        self.assertIsInstance(result, np.ndarray, "Expected output to be a numpy array.")
        np.testing.assert_allclose(result, [5.0, 0.0], atol=1e-7, err_msg="Intersection coordinates do not match.")

    def test_l1_parallel(self):
        """Parallel lines should return None."""
        origin, rd = np.array([0.0, 0.0]), np.array([1.0, 0.0])
        p1, p2 = np.array([0.0, 5.0]), np.array([10.0, 5.0])
        result = tasks.intersect_line_infinite(origin, rd, p1, p2)
        self.assertIsNone(result, "Expected None for parallel lines.")

if __name__ == '__main__':
    unittest.main()
