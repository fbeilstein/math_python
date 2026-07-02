import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel5(unittest.TestCase):
    def test_rs_encoding(self):
        text = "Hello"
        bytes_arr = [ord(c) for c in text]
        self.assertEqual(bytes_arr, [72, 101, 108, 108, 111])

if __name__ == '__main__':
    unittest.main()
