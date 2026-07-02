import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4Hack(unittest.TestCase):
    
    def test_l4_factorize(self):
        # 15 = 3 * 5
        res = tasks.factorize(15)
        self.assertIsNotNone(res)
        self.assertEqual(set(res), {3, 5})
        
        # Test a slightly larger number (p=101, q=103)
        res = tasks.factorize(10403)
        self.assertIsNotNone(res)
        self.assertEqual(set(res), {101, 103})

    def test_l4_hack_rsa(self):
        pub, priv = tasks.generate_keypair(32)
        m = 42069
        c = tasks.encrypt(m, pub)
        
        # Now hack it!
        m_hacked = tasks.hack_rsa(pub, c)
        self.assertEqual(m, m_hacked)

if __name__ == '__main__':
    unittest.main()
