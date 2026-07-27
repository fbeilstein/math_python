import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel1(unittest.TestCase):
    def test_division_gf2(self):
        dividend = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        divisor = [1, 0, 0, 0, 1, 1, 1, 0, 1]
        p = 2
        
        zero = tasks.PrimeField(p).zero
        dividend_poly = tasks.Polynomial([tasks.PrimeField(p)(c) for c in dividend])
        divisor_poly = tasks.Polynomial([tasks.PrimeField(p)(c) for c in divisor])
        
        q, r = divmod(dividend_poly, divisor_poly)
        self.assertEqual([c.val for c in r.coeffs], [1, 1, 1, 0, 1])

    def test_division_gf3(self):
        p = 3
        zero = tasks.PrimeField(p).zero
        dividend = tasks.Polynomial([tasks.PrimeField(p)(c) for c in [2, 0, 1]])
        divisor = tasks.Polynomial([tasks.PrimeField(p)(c) for c in [1, 2]])
        
        q, r = divmod(dividend, divisor)
        self.assertEqual([c.val for c in q.coeffs], [2, 2])
        self.assertEqual([c.val for c in r.coeffs], [0])

if __name__ == '__main__':
    unittest.main()
