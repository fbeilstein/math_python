import tkinter as tk
import unittest
import sys
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level1NGrams(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="L1: N-Gram Extractor", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
        
        input_frame = tk.Frame(self, bg="#1e1e1e")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Sample Text:", font=("Arial", 14), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=5)
        self.entry_text = tk.Entry(input_frame, font=("Courier", 14), width=40)
        self.entry_text.pack(side=tk.LEFT, padx=5)
        self.entry_text.insert(0, "to be or not to be")
        
        tk.Button(input_frame, text="Extract", font=("Arial", 12, "bold"), bg="#007acc", fg="white", command=self.extract).pack(side=tk.LEFT, padx=15)
        
        self.output_text = tk.Text(self, font=("Courier", 14), bg="#2d2d30", fg="#d4d4d4", height=20, width=60)
        self.output_text.pack(pady=20)

    def extract(self):
        text = self.entry_text.get()
        if not text: return
            
        tokens = tasks.tokenize(text)
        model = tasks.build_model(tokens)
        
        # Format the model nicely (convert tuple keys to strings for JSON)
        json_model = {str(k): v for k, v in model.items()}
        formatted = json.dumps(json_model, indent=4, ensure_ascii=False)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, formatted)

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel1NGrams(unittest.TestCase):
    
    def test_l1_tokenize(self):
        tokens = tasks.tokenize("Hello, world! It's a test.")
        self.assertEqual(tokens, ["hello", ",", "world", "!", "it's", "a", "test", "."])
    
    def test_l1_basic_model(self):
        tokens = ["to", "be", "or", "not", "to", "be"]
        model = tasks.build_model(tokens)
        self.assertEqual(model[("to", "be")], ["or"])
        self.assertEqual(model[("or", "not")], ["to"])
        
if __name__ == '__main__':
    unittest.main()
