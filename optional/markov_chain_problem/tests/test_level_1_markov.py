import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestMarkovChain(unittest.TestCase):
    def test_update_markov_counts(self):
        counts = {}
        history = "121"
        tasks.update_markov_counts(history, "2", 2, counts)
        self.assertIn("21", counts)
        self.assertEqual(counts["21"]["2"], 1)
        self.assertEqual(counts["21"]["1"], 0)

    def test_predict_fixed_order(self):
        counts = {"11": {"1": 10, "2": 2}}
        pred = tasks.predict_fixed_order("0011", 2, counts)
        self.assertEqual(pred, "1")
        
        counts_tied = {"11": {"1": 5, "2": 5}}
        pred_tied = tasks.predict_fixed_order("0011", 2, counts_tied)
        self.assertIn(pred_tied, ["1", "2"])

    def test_calculate_p_value(self):
        # 100 trials, 60 correct. Null p=0.5, mu=50, sigma=5
        # z = 2.0. p-value for sf(60) is ~0.0227
        pval = tasks.calculate_p_value(60, 100)
        self.assertTrue(0.02 < pval < 0.03)

    def test_predict_with_fallback(self):
        counts = {
            "111": {"1": 5, "2": 5}, # Tied at order 3
            "11": {"1": 2, "2": 10}, # Clear winner at order 2
            "1": {"1": 100, "2": 0}  # Ignored because order 2 succeeded
        }
        pred = tasks.predict_with_fallback("0111", 3, counts)
        self.assertEqual(pred, "2")

    def test_mixture_of_experts(self):
        scores = [1.0, 1.0]
        preds = ["1", "2"]
        # Expert 1 gets it right, expert 2 wrong. Decay 0.9.
        updated = tasks.update_expert_scores(scores, preds, "1", 0.9)
        self.assertAlmostEqual(updated[0], 1.9)
        self.assertAlmostEqual(updated[1], 0.9)
        
        best = tasks.get_best_expert(updated)
        self.assertEqual(best, 0)

    def test_pi_generator(self):
        pi_bits = tasks.generate_pi_binary_digits(10)
        self.assertEqual(len(pi_bits), 10)
        # pi is 3.14159...
        # fraction is 0.14159265...
        # In binary: 0.0010010000111111...
        self.assertTrue(pi_bits.startswith("0010"))

if __name__ == '__main__':
    unittest.main()
