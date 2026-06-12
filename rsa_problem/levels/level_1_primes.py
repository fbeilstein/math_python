import tkinter as tk
import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level1Primes(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="L1: Miller-Rabin Primality Test", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
        
        # Test specific number
        frame_test = tk.Frame(self, bg="#1e1e1e")
        frame_test.pack(pady=10)
        
        tk.Label(frame_test, text="Test Number:", font=("Arial", 14), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=5)
        self.entry_test = tk.Entry(frame_test, font=("Courier", 14), width=25)
        self.entry_test.pack(side=tk.LEFT, padx=5)
        self.entry_test.insert(0, "104729") # the 10000th prime
        
        tk.Button(frame_test, text="Is Prime?", font=("Arial", 12, "bold"), bg="#007acc", fg="white", command=self.test_prime).pack(side=tk.LEFT, padx=10)
        
        self.lbl_test_res = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#1e1e1e")
        self.lbl_test_res.pack(pady=5)
        
        # Generate random prime
        frame_gen = tk.Frame(self, bg="#1e1e1e")
        frame_gen.pack(pady=30)
        
        tk.Label(frame_gen, text="Generate Prime (Bits):", font=("Arial", 14), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=5)
        self.entry_bits = tk.Entry(frame_gen, font=("Courier", 14), width=5)
        self.entry_bits.pack(side=tk.LEFT, padx=5)
        self.entry_bits.insert(0, "512")
        
        tk.Button(frame_gen, text="Generate", font=("Arial", 12, "bold"), bg="#007acc", fg="white", command=self.gen_prime).pack(side=tk.LEFT, padx=10)
        
        self.output_gen = tk.Text(self, font=("Courier", 12), bg="#2d2d30", fg="#4ec9b0", height=8, width=70, wrap=tk.CHAR)
        self.output_gen.pack(pady=10)

    def test_prime(self):
        try:
            n = int(self.entry_test.get())
        except ValueError:
            self.lbl_test_res.config(text="Invalid integer", fg="#f44747")
            return
            
        is_p = tasks.miller_rabin(n)
        if is_p:
            self.lbl_test_res.config(text=f"{n} is PROBABLY PRIME ✓", fg="#4ec9b0")
        else:
            self.lbl_test_res.config(text=f"{n} is COMPOSITE ✗", fg="#f44747")

    def gen_prime(self):
        try:
            bits = int(self.entry_bits.get())
        except ValueError:
            return
            
        p = tasks.generate_prime(bits)
        self.output_gen.delete("1.0", tk.END)
        self.output_gen.insert(tk.END, str(p))

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel1Primes(unittest.TestCase):
    
    def test_l1_small_primes(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97, 104729]
        for p in primes:
            self.assertTrue(tasks.miller_rabin(p), f"Failed on prime {p}")
            
    def test_l1_small_composites(self):
        composites = [4, 6, 8, 9, 10, 15, 21, 25, 100, 104727]
        for c in composites:
            self.assertFalse(tasks.miller_rabin(c), f"Failed on composite {c}")
            
    def test_l1_edge_cases(self):
        self.assertFalse(tasks.miller_rabin(0))
        self.assertFalse(tasks.miller_rabin(1))
        self.assertFalse(tasks.miller_rabin(-5))

    def test_l1_generate_prime_bits(self):
        p = tasks.generate_prime(64)
        self.assertTrue(tasks.miller_rabin(p))
        self.assertTrue((1 << 63) <= p < (1 << 64), "Generated prime has incorrect bit length")

if __name__ == '__main__':
    unittest.main()
