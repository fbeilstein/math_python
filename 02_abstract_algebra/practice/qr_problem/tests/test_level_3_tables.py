import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
import algebra_utils as utils

class TestLevel3(unittest.TestCase):
    def test_extension_field_gf4(self):
        """Verify that α generates all nonzero elements of GF(4)."""
        poly = utils.make_poly([1, 1, 1], 2)
        gf = tasks.ExtensionField(poly)
        # α^0 = 1, α^1 = α, α^2 = α+1 (since α^2+α+1=0 ⟹ α^2=α+1 in GF(2))
        vals = [utils.ext_to_int(gf.exp(i)) for i in range(3)]
        self.assertEqual(vals, [1, 2, 3])
        # α^3 = 1 (cyclic)
        self.assertEqual(utils.ext_to_int(gf.exp(3)), 1)

if __name__ == '__main__':
    unittest.main()
