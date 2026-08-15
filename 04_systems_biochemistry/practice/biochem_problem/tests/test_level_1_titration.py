import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel1Titration(unittest.TestCase):
    def test_buffer_region(self):
        # Weak acid (pKa=4.76), 0.1M HA, 0.1M A-. Add 0.5L of 0.1M strong acid.
        # Initial moles: 0.1 HA, 0.1 A-.
        # Add H+: 0.5L * 0.1M = 0.05 moles H+.
        # Final moles: HA = 0.1 + 0.05 = 0.15. A- = 0.1 - 0.05 = 0.05.
        # pH = 4.76 + log10(0.05 / 0.15) = 4.76 - 0.4771 = 4.2829
        ph = tasks.calculate_pH(4.76, 0.1, 0.1, 0.5, 0.1, True)
        self.assertAlmostEqual(ph, 4.28288, places=4)

    def test_excess_acid(self):
        # Exceed buffer capacity: Add 1.5L of 0.1M strong acid
        # Moles H+ = 0.15. A- is 0.1, so all A- converted to HA. 
        # Excess H+ = 0.05 moles. Total volume = 2.5L.
        # [H+] = 0.05 / 2.5 = 0.02 M. pH = -log10(0.02) = 1.69897
        ph = tasks.calculate_pH(4.76, 0.1, 0.1, 1.5, 0.1, True)
        self.assertAlmostEqual(ph, 1.69897, places=4)
        
    def test_excess_base(self):
        # Exceed buffer capacity with strong base: add 2.0L of 0.1M base
        # Moles OH- = 0.2. HA is 0.1. All HA converted to A-.
        # Excess OH- = 0.1 moles. Total vol = 3.0L.
        # [OH-] = 0.1 / 3 = 0.0333 M. pOH = 1.477. pH = 12.5228
        ph = tasks.calculate_pH(4.76, 0.1, 0.1, 2.0, 0.1, False)
        self.assertAlmostEqual(ph, 12.52287, places=4)

if __name__ == '__main__':
    unittest.main()
