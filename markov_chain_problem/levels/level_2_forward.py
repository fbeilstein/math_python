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

class Level2Forward(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="L2: Forward Text Generation", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
        
        tk.Label(self, text="Seed words (must be 2 words, space-separated):", font=("Arial", 14), bg="#1e1e1e", fg="white").pack()
        self.entry_seed = tk.Entry(self, font=("Courier", 16), width=20)
        self.entry_seed.pack(pady=5)
        self.entry_seed.insert(0, "once upon")
        
        tk.Label(self, text="Length:", font=("Arial", 14), bg="#1e1e1e", fg="white").pack()
        self.entry_length = tk.Entry(self, font=("Courier", 16), width=5)
        self.entry_length.pack(pady=5)
        self.entry_length.insert(0, "100")
        
        tk.Button(self, text="Generate", font=("Arial", 14, "bold"), bg="#007acc", fg="white", command=self.generate).pack(pady=15)
        
        self.output_text = tk.Text(self, font=("Courier", 14), bg="#2d2d30", fg="#d4d4d4", height=10, width=60, wrap=tk.WORD)
        self.output_text.pack(pady=10)

        # Load corpus text
        try:
            with open(os.path.join(parent_dir, "corpus.txt"), "r", encoding="utf-8") as f:
                self.text = f.read()
            tk.Label(self, text="Loaded Poe Corpus", font=("Arial", 10), bg="#1e1e1e", fg="gray").pack()
        except FileNotFoundError:
            self.text = ""

    def generate(self):
        if not self.text: return
        seed = self.entry_seed.get()
        try:
            length = int(self.entry_length.get())
        except ValueError:
            return
            
        seed_tokens = tuple(tasks.tokenize(seed))
        if len(seed_tokens) != 2:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: Seed must contain exactly 2 tokens. Found {len(seed_tokens)}.")
            return
            
        corpus_tokens = tasks.tokenize(self.text)
        model = tasks.build_model(corpus_tokens)
        
        result_tokens = tasks.generate_forward(model, seed_tokens, length)
        result = tasks.format_tokens(result_tokens)
        
        if result_tokens == list(seed_tokens):
            result = f"Error: The seed '{seed}' was not found anywhere in the corpus!\nTry a different seed."
            
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel2Forward(unittest.TestCase):
    
    def test_l2_deterministic_gen(self):
        # A completely deterministic model
        model = {("a", "b"): ["c"], ("b", "c"): ["d"], ("c", "d"): ["e"]}
        result = tasks.generate_forward(model, ("a", "b"), 5)
        self.assertEqual(result, ["a", "b", "c", "d", "e"])
        
    def test_l2_early_stop(self):
        model = {("a", "b"): ["c"]}
        result = tasks.generate_forward(model, ("a", "b"), 10)
        # Should stop after generating "c" because ("b", "c") is not in model
        self.assertEqual(result, ["a", "b", "c"])

if __name__ == '__main__':
    unittest.main()
