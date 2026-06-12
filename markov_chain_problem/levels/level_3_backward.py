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

class Level3Backward(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="L3: Backward Rhyming Engine", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
        
        tk.Label(self, text="Target Suffix (e.g. 'ing'):", font=("Arial", 14), bg="#1e1e1e", fg="white").pack()
        self.entry_suffix = tk.Entry(self, font=("Courier", 16), width=10)
        self.entry_suffix.pack(pady=5)
        self.entry_suffix.insert(0, "ing")
        
        tk.Label(self, text="Length of generated words:", font=("Arial", 14), bg="#1e1e1e", fg="white").pack()
        self.entry_length = tk.Entry(self, font=("Courier", 16), width=5)
        self.entry_length.pack(pady=5)
        self.entry_length.insert(0, "10")
        
        tk.Button(self, text="Generate Backward!", font=("Arial", 14, "bold"), bg="#007acc", fg="white", command=self.generate).pack(pady=15)
        
        self.output_text = tk.Text(self, font=("Courier", 14), bg="#2d2d30", fg="#d4d4d4", height=10, width=60, wrap=tk.WORD)
        self.output_text.pack(pady=10)

        # Load corpus
        try:
            with open(os.path.join(parent_dir, "corpus.txt"), "r", encoding="utf-8") as f:
                self.text = f.read()
            tk.Label(self, text="Loaded Poe Corpus", font=("Arial", 10), bg="#1e1e1e", fg="gray").pack()
        except FileNotFoundError:
            self.text = ""

    def generate(self):
        if not self.text: return
        suffix = self.entry_suffix.get()
        try:
            length = int(self.entry_length.get())
        except ValueError:
            return
            
        corpus_tokens = tasks.tokenize(self.text)
        rev_model = tasks.build_reversed_model(corpus_tokens)
        result = tasks.generate_rhyming_line(rev_model, suffix, length)
            
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel3Backward(unittest.TestCase):
    
    def test_l3_reversed_model(self):
        tokens = ["a", "b", "c"]
        # Reversed is "c", "b", "a"
        # Order 2 model of "cba": ("c", "b") -> ["a"]
        rev_model = tasks.build_reversed_model(tokens)
        self.assertEqual(rev_model, {("c", "b"): ["a"]})
        
    def test_l3_generate_rhyming(self):
        # We want suffix "ing"
        rev_model = {("boring", "is"): ["this"]}
        # Seed is length 2
        result = tasks.generate_rhyming_line(rev_model, "ing", 3)
        self.assertEqual(result, "This is boring")

if __name__ == '__main__':
    unittest.main()
