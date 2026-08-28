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
        dividend_poly = tasks.Polynomial([tasks.PrimeField(p)(c) for c in reversed(dividend)])
        divisor_poly = tasks.Polynomial([tasks.PrimeField(p)(c) for c in reversed(divisor)])
        
        q, r = divmod(dividend_poly, divisor_poly)
        self.assertEqual([r[i].val for i in range(r.degree() + 1)], [1, 0, 1, 1, 1])

    def test_division_gf3(self):
        p = 3
        zero = tasks.PrimeField(p).zero
        dividend = tasks.Polynomial([tasks.PrimeField(p)(c) for c in reversed([2, 0, 1])])
        divisor = tasks.Polynomial([tasks.PrimeField(p)(c) for c in reversed([1, 2])])
        
        q, r = divmod(dividend, divisor)
        self.assertEqual([q[i].val for i in range(q.degree() + 1)], [2, 2])
        self.assertEqual([r[i].val for i in range(r.degree() + 1)], [0])

if __name__ == '__main__':
    unittest.main()
