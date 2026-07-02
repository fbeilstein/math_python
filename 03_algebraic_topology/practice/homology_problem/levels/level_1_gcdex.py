import tkinter as tk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level1GCD(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # UI Setup
        tk.Label(self, text="Extended Euclidean Algorithm", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
        
        input_frame = tk.Frame(self, bg="#1e1e1e")
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="a =", font=("Arial", 16), bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_a = tk.Entry(input_frame, font=("Arial", 16), width=8)
        self.entry_a.pack(side=tk.LEFT, padx=10)
        self.entry_a.insert(0, "42")
        
        tk.Label(input_frame, text="b =", font=("Arial", 16), bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_b = tk.Entry(input_frame, font=("Arial", 16), width=8)
        self.entry_b.pack(side=tk.LEFT, padx=10)
        self.entry_b.insert(0, "30")
        
        tk.Button(self, text="Compute Bézout Identity", font=("Arial", 14), command=self.compute, bg="#007acc", fg="white").pack(pady=10)
        
        self.result_label = tk.Label(self, text="", font=("Courier", 18, "bold"), bg="#1e1e1e", fg="white")
        self.result_label.pack(pady=30)
        
        self.status_label = tk.Label(self, text="", font=("Arial", 16, "bold"), bg="#1e1e1e")
        self.status_label.pack(pady=10)

    def compute(self):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            
            x, y, g = tasks.z_gcdex(a, b)
            
            self.result_label.config(text=f"{a} * ({x}) + {b} * ({y}) = {g}")
            
            if a * x + b * y == g and g >= 0:
                self.status_label.config(text="✓ SUCCESS", fg="#4ec9b0")
            else:
                self.status_label.config(text="✗ FAILED: Math does not check out!", fg="#f44747")
                
        except ValueError:
            self.status_label.config(text="✗ ERROR: Invalid integer inputs", fg="#f44747")
            self.result_label.config(text="")
        except Exception as e:
            self.status_label.config(text=f"✗ ERROR: {e}", fg="#f44747")
            self.result_label.config(text="")


if __name__ == '__main__':
    unittest.main()
