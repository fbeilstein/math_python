import tkinter as tk
from tkinter import messagebox
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level2Matrix(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="Elementary Matrix Operations", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
        
        self.matrix_text = tk.Text(self, font=("Courier", 16), width=30, height=8, bg="#2d2d30", fg="white", insertbackground="white")
        self.matrix_text.pack(pady=10)
        
        # Default matrix
        self.matrix_text.insert(tk.END, "12  6  9\n 4  2  3\n 8  4  6")
        
        btn_frame = tk.Frame(self, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Load Matrix", font=("Arial", 12), command=self.load_matrix, bg="#3e3e42", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Column 0", font=("Arial", 12), command=self.do_clear_column, bg="#007acc", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Row 0", font=("Arial", 12), command=self.do_clear_row, bg="#007acc", fg="white").pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self, text="", font=("Arial", 16, "bold"), bg="#1e1e1e")
        self.status_label.pack(pady=10)

        self.current_matrix = None
        self.load_matrix()

    def parse_matrix(self):
        text = self.matrix_text.get("1.0", tk.END).strip()
        matrix = []
        for line in text.split('\n'):
            line = line.strip()
            if not line: continue
            row = [int(x) for x in line.split()]
            matrix.append(row)
        return matrix

    def display_matrix(self, matrix):
        self.matrix_text.delete("1.0", tk.END)
        for row in matrix:
            self.matrix_text.insert(tk.END, " ".join(f"{x:4}" for x in row) + "\n")

    def load_matrix(self):
        try:
            self.current_matrix = self.parse_matrix()
            self.display_matrix(self.current_matrix)
            self.status_label.config(text="Matrix loaded successfully", fg="#4ec9b0")
        except ValueError:
            self.status_label.config(text="✗ ERROR: Invalid integers in matrix", fg="#f44747")

    def do_clear_column(self):
        try:
            m = self.parse_matrix()
            m = tasks.clear_column(m)
            self.display_matrix(m)
            
            # Check if column 0 is cleared (except m[0][0])
            cleared = all(m[i][0] == 0 for i in range(1, len(m)))
            if cleared:
                self.status_label.config(text="✓ SUCCESS: Column 0 cleared!", fg="#4ec9b0")
            else:
                self.status_label.config(text="✗ FAILED: Column 0 not fully cleared", fg="#f44747")
        except Exception as e:
            self.status_label.config(text=f"✗ ERROR: {e}", fg="#f44747")

    def do_clear_row(self):
        try:
            m = self.parse_matrix()
            m = tasks.clear_row(m)
            self.display_matrix(m)
            
            # Check if row 0 is cleared (except m[0][0])
            cleared = all(m[0][j] == 0 for j in range(1, len(m[0])))
            if cleared:
                self.status_label.config(text="✓ SUCCESS: Row 0 cleared!", fg="#4ec9b0")
            else:
                self.status_label.config(text="✗ FAILED: Row 0 not fully cleared", fg="#f44747")
        except Exception as e:
            self.status_label.config(text=f"✗ ERROR: {e}", fg="#f44747")



if __name__ == '__main__':
    unittest.main()
