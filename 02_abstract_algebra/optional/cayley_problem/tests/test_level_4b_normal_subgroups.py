import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4b(unittest.TestCase):
    def test_normal(self):
        nodes = {"e", "a", "b", "ba"}
        rels = [("aa", ""), ("bb", ""), ("ab", "ba")]
        sub = {"e", "a"}
        self.assertTrue(tasks.is_normal_subgroup(sub, nodes, rels))

if __name__ == '__main__':
    unittest.main()
