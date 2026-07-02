import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestEvolutionaryGame(unittest.TestCase):
    def setUp(self):
        self.matrix = {
            'C': {'C': 3, 'D': 0},
            'D': {'C': 5, 'D': 1}
        }

    def test_strategies(self):
        ac = tasks.AlwaysCooperate()
        ad = tasks.AlwaysDefect()
        tft = tasks.TitForTat()
        gt = tasks.GrimTrigger()
        
        self.assertEqual(ac.get_action([], []), 'C')
        self.assertEqual(ad.get_action([], []), 'D')
        self.assertEqual(tft.get_action([], []), 'C')
        self.assertEqual(tft.get_action(['C'], ['D']), 'D')
        self.assertEqual(gt.get_action(['C'], ['C']), 'C')
        self.assertEqual(gt.get_action(['C'], ['D']), 'D')
        self.assertEqual(gt.get_action(['D', 'C'], ['D', 'C']), 'D')

    def test_play_match(self):
        ac = tasks.AlwaysCooperate()
        ad = tasks.AlwaysDefect()
        
        score_ac, score_ad = tasks.play_match(ac, ad, self.matrix, 5)
        # AC gets 0 against AD, AD gets 5 against AC
        self.assertEqual(score_ac, 0)
        self.assertEqual(score_ad, 25)
        
        tft = tasks.TitForTat()
        score_tft, score_ad2 = tasks.play_match(tft, ad, self.matrix, 5)
        # TFT cooperates first (0), AD defects (5). Then TFT defects (1) and AD defects (1) for 4 rounds.
        # TFT: 0 + 4*1 = 4
        # AD: 5 + 4*1 = 9
        self.assertEqual(score_tft, 4)
        self.assertEqual(score_ad2, 9)

    def test_neighborhood_fitness(self):
        grid = np.array([
            [tasks.AlwaysCooperate(), tasks.AlwaysDefect(), tasks.AlwaysCooperate()],
            [tasks.AlwaysDefect(), tasks.AlwaysCooperate(), tasks.AlwaysDefect()],
            [tasks.AlwaysCooperate(), tasks.AlwaysDefect(), tasks.AlwaysCooperate()]
        ], dtype=object)
        
        # Center is AC, surrounded by 4 ADs and 4 ACs + itself (AC)
        # 5 ACs, 4 ADs.
        # Against AC: 3. Against AD: 0.
        # Self gets 5 * 3 = 15.
        fitness = tasks.compute_neighborhood_fitness(grid, 1, 1, self.matrix, rounds=1)
        self.assertEqual(fitness, 15)

    def test_update_grid_deterministic(self):
        grid = np.array([
            [tasks.AlwaysCooperate(), tasks.AlwaysCooperate()],
            [tasks.AlwaysCooperate(), tasks.AlwaysDefect()]
        ], dtype=object)
        
        new_grid = tasks.update_grid_deterministic(grid, self.matrix, rounds=1)
        
        # In a 2x2, AD is against 3 ACs + itself (AD). 
        # AD fitness: 5 * 3 + 1 = 16
        # An AC is against 2 ACs, 1 AD, 1 self. 
        # AC fitness: 3 * 3 + 0 = 9
        # Everyone should copy AD.
        for r in range(2):
            for c in range(2):
                self.assertIsInstance(new_grid[r, c], tasks.AlwaysDefect)

if __name__ == '__main__':
    unittest.main()
