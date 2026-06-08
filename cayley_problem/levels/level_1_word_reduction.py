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

class Level1WordReduction(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.add_warning()
        
        tk.Label(self.left_panel, text="L1: Word Reduction Engine", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Word:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_word = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_word.pack(fill=tk.X, padx=2, pady=1)
        self.entry_word.insert(0, "abABaaaa")
        
        tk.Label(input_frame, text="Relations (lhs=rhs):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_rels = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_rels.pack(fill=tk.X, padx=2, pady=1)
        self.entry_rels.insert(0, "aaaa=e, bb=e, abab=e")
        
        tk.Button(self.left_panel, text="Reduce Word!", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.reduce).pack(pady=10, fill=tk.X, padx=2)
        
        # Put the output into the big right panel
        tk.Label(self.right_panel, text="Reduction Result", font=("Arial", 16, "bold"), bg="#2d2d30", fg="#007acc").pack(pady=(20,5))
        self.output_text = tk.Text(self.right_panel, font=("Courier", 24), bg="#1e1e1e", fg="#5ce65c", height=5)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def parse_relations(self, rels_str):
        rels = []
        for part in rels_str.split(','):
            part = part.strip()
            if '=' in part:
                lhs, rhs = part.split('=', 1)
                lhs = lhs.strip()
                rhs = rhs.strip()
                if rhs == 'e': rhs = ''
                if lhs == 'e': lhs = ''
                rels.append((lhs, rhs))
        return rels

    def reduce(self):
        word = self.entry_word.get().strip()
        if word == 'e': word = ''
        rels_str = self.entry_rels.get()
        relations = self.parse_relations(rels_str)
        
        result = tasks.reduce_word(word, relations)
        
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Reduced form: {result}")

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel1(unittest.TestCase):
    def test_trivial_cancellations(self):
        self.assertEqual(tasks.reduce_word("aA", []), "e")
        self.assertEqual(tasks.reduce_word("bBa", []), "a")
        
    def test_relations(self):
        rels = [("aaaa", ""), ("bb", "")]
        self.assertEqual(tasks.reduce_word("aaaaa", rels), "a")
        self.assertEqual(tasks.reduce_word("aabaaaaa", rels), "aaba")

if __name__ == '__main__':
    unittest.main()
