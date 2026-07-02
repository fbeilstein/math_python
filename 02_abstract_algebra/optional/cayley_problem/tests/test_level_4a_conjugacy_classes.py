import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4a(unittest.TestCase):
    def test_conjugacy(self):
        nodes = {"e", "a", "b", "ba"} # K4
        rels = [("aa", ""), ("bb", ""), ("ab", "ba")]
        # In abelian group, conjugacy class of a is just {a}
        c_class = tasks.compute_conjugacy_class("a", nodes, rels)
        self.assertEqual(c_class, {"a"})

if __name__ == '__main__':
    unittest.main()
