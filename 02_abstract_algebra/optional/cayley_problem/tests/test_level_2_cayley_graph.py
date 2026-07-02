import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel2(unittest.TestCase):
    def test_cayley_graph_cyclic(self):
        nodes, edges = tasks.generate_cayley_graph(["a"], [("aaaa", "")])
        self.assertEqual(len(nodes), 4)
        
    def test_cayley_graph_klein4(self):
        nodes, edges = tasks.generate_cayley_graph(["a", "b"], [("aa", ""), ("bb", ""), ("ab", "ba")])
        self.assertEqual(len(nodes), 4)

if __name__ == '__main__':
    unittest.main()
