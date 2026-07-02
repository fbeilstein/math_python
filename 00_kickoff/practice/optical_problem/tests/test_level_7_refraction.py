import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel7Refraction(unittest.TestCase):
    def test_l7_refraction(self):
        ray_dir = np.array([1.0, -1.0]) / np.sqrt(2) # 45 degrees
        normal = np.array([0.0, 1.0])
        new_dir = tasks.refract_vector(ray_dir, normal, 1.0, 1.5)
        self.assertIsNotNone(new_dir)
        self.assertAlmostEqual(np.linalg.norm(new_dir), 1.0)
        self.assertAlmostEqual(np.abs(new_dir[0]) / np.sin(np.pi/4), 1.0 / 1.5)

if __name__ == '__main__':
    unittest.main()
