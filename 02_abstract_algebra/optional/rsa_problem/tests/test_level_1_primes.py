import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel1Primes(unittest.TestCase):
    
    def test_l1_small_primes(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97, 104729]
        for p in primes:
            self.assertTrue(tasks.miller_rabin(p), f"Failed on prime {p}")
            
    def test_l1_small_composites(self):
        composites = [4, 6, 8, 9, 10, 15, 21, 25, 100, 104727]
        for c in composites:
            self.assertFalse(tasks.miller_rabin(c), f"Failed on composite {c}")
            
    def test_l1_edge_cases(self):
        self.assertFalse(tasks.miller_rabin(0))
        self.assertFalse(tasks.miller_rabin(1))
        self.assertFalse(tasks.miller_rabin(-5))

    def test_l1_generate_prime_bits(self):
        p = tasks.generate_prime(64)
        self.assertTrue(tasks.miller_rabin(p))
        self.assertTrue((1 << 63) <= p < (1 << 64), "Generated prime has incorrect bit length")

if __name__ == '__main__':
    unittest.main()
