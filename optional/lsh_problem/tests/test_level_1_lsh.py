import unittest
import sys, os
import math

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLSH(unittest.TestCase):
    def test_get_shingles(self):
        text = "apple banana cherry date"
        s = tasks.get_shingles(text, 2)
        self.assertEqual(len(s), 3)
        self.assertIn(("apple", "banana"), s)
        
    def test_jaccard_similarity(self):
        s1 = {1, 2, 3}
        s2 = {2, 3, 4}
        # Intersection = {2, 3} (2)
        # Union = {1, 2, 3, 4} (4)
        j = tasks.jaccard_similarity(s1, s2)
        self.assertAlmostEqual(j, 0.5)

    def test_create_signature(self):
        s = {1, 2, 3}
        hf1 = lambda x: x + 10
        hf2 = lambda x: -x
        sig = tasks.create_signature(s, [hf1, hf2])
        # Min of x+10 for {1,2,3} is 11
        # Min of -x for {1,2,3} is -3
        self.assertEqual(sig, (11, -3))

    def test_minhash_similarity(self):
        sig1 = (1, 2, 3, 4)
        sig2 = (1, 2, 9, 4)
        sim = tasks.minhash_similarity(sig1, sig2)
        self.assertAlmostEqual(sim, 0.75)

    def test_lsh_bloom_filter(self):
        signatures = [
            (1, 2, 3, 4),
            (1, 2, 9, 9),
            (0, 0, 3, 4)
        ]
        # num_bands = 2 (so rows_per_band = 2)
        # B0: D0=(1,2), D1=(1,2), D2=(0,0) -> collision for D0, D1
        # B1: D0=(3,4), D1=(9,9), D2=(3,4) -> collision for D0, D2
        buckets = tasks.lsh_bloom_filter(signatures, 2)
        self.assertIn(0, buckets[(0, (1, 2))])
        self.assertIn(1, buckets[(0, (1, 2))])
        self.assertIn(0, buckets[(1, (3, 4))])
        self.assertIn(2, buckets[(1, (3, 4))])

    def test_bloom_false_positive(self):
        # n=1000, m=10000, k=7
        p = tasks.bloom_false_positive(1000, 10000, 7)
        expected = (1.0 - math.exp(-7 * 1000 / 10000))**7
        self.assertAlmostEqual(p, expected)

    def test_collision_probability(self):
        p = tasks.collision_probability(0.8, 20, 5)
        expected = 1.0 - (1.0 - 0.8**5)**20
        self.assertAlmostEqual(p, expected)

    def test_calculate_threshold(self):
        t = tasks.calculate_threshold(20, 5)
        expected = (1.0 - 0.5**(1/20.0))**(1/5.0)
        self.assertAlmostEqual(t, expected)

if __name__ == '__main__':
    unittest.main()
