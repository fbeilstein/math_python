import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel5(unittest.TestCase):
    def test_center(self):
        nodes = {"e", "a", "b", "ba"} # K4 is abelian
        rels = [("aa", ""), ("bb", ""), ("ab", "ba")]
        center = tasks.compute_center(nodes, rels)
        self.assertEqual(center, nodes)
        
    def test_commutator(self):
        nodes = {"e", "a", "b", "ba"} # K4 is abelian
        rels = [("aa", ""), ("bb", ""), ("ab", "ba")]
        commutator = tasks.compute_commutator_subgroup(nodes, rels)
        self.assertEqual(commutator, {"e"})

if __name__ == '__main__':
    unittest.main()
