import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
import algebra_utils as utils

class TestLevel4(unittest.TestCase):
    def test_gfpn_math(self):
        poly = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1], 2)
        gf = tasks.ExtensionField(poly)

        a = tasks.Polynomial([utils.int_to_ext(3, gf), utils.int_to_ext(2, gf)])
        b = tasks.Polynomial([utils.int_to_ext(4, gf)])
        res = a * b
        self.assertEqual([utils.ext_to_int(res[i]) for i in range(res.degree() + 1)], [12, 8])

if __name__ == '__main__':
    unittest.main()
