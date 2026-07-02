import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel3Encrypt(unittest.TestCase):
    
    def test_l3_fast_mod_exp(self):
        # 5^3 mod 13 = 125 mod 13 = 8
        self.assertEqual(tasks.fast_mod_exp(5, 3, 13), 8)
        # 4^13 mod 497 = 445
        self.assertEqual(tasks.fast_mod_exp(4, 13, 497), 445)

    def test_l3_encryption_cycle(self):
        # We'll generate a small key and test
        pub, priv = tasks.generate_keypair(64)
        m = 12345
        c = tasks.encrypt(m, pub)
        m_dec = tasks.decrypt(c, priv)
        self.assertEqual(m, m_dec)

if __name__ == '__main__':
    unittest.main()
