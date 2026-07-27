import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
import algebra_utils as utils

class TestLevel2(unittest.TestCase):
    def test_primitive_qr(self):
        poly = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1], 2)
        self.assertTrue(tasks.is_primitive(poly))

    def test_non_primitive(self):
        poly = utils.make_poly([1, 0, 0, 0, 0, 0, 0, 0, 1], 2)
        self.assertFalse(tasks.is_primitive(poly))

if __name__ == '__main__':
    unittest.main()
