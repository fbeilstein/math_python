import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel2Keys(unittest.TestCase):
    
    def test_l2_extended_gcd(self):
        x, y, g = tasks.extended_gcd(42, 30)
        self.assertEqual(g, 6)
        self.assertEqual(42*x + 30*y, g)

    def test_l2_mod_inverse(self):
        # 3 * d = 1 mod 11 -> d = 4 (since 12 = 1 mod 11)
        d = tasks.mod_inverse(3, 11)
        self.assertEqual(d, 4)
        
    def test_l2_mod_inverse_fail(self):
        with self.assertRaises(ValueError):
            tasks.mod_inverse(2, 4) # not coprime

    def test_l2_generate_keypair(self):
        pub, priv = tasks.generate_keypair(64)
        e, n = pub
        d, n_priv = priv
        self.assertEqual(n, n_priv)
        self.assertTrue(n > 0)
        self.assertTrue(d > 0)
        # We can't directly check (e*d)%phi without phi, but we can verify it doesn't crash

if __name__ == '__main__':
    unittest.main()
