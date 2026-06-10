import tkinter as tk
from tkinter import ttk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from levels.level_2_cayley_graph import Level2CayleyGraph
from levels.level_3_subgroups_cosets import Level3SubgroupsCosets
from levels.level_4a_conjugacy_classes import Level4aConjugacy
from levels.level_4b_normal_subgroups import Level4bNormality
from levels.level_5_center_commutator import Level5CenterCommutator

class LabDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Cayley Graph Pedagogical Laboratory")
        self.geometry("900x700")
        self.configure(bg="#1e1e1e")
        
        # Title Label
        tk.Label(self, text="Abstract Algebra Laboratory: Cayley Graphs", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#007acc").pack(pady=5)
        
        self.global_left = tk.Frame(self, bg="#1e1e1e", width=220)
        self.global_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.global_left.pack_propagate(False)
        
        self.nav_frame = tk.Frame(self.global_left, bg="#2d2d30", bd=2, relief=tk.RAISED)
        self.nav_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(self.nav_frame, text="Select Level:", font=("Arial", 10, "bold"), bg="#2d2d30", fg="white").pack(pady=2)
        
        self.controls_frame = tk.Frame(self.global_left, bg="#1e1e1e")
        self.controls_frame.pack(fill=tk.BOTH, expand=True)
        
        self.global_right = tk.Frame(self, bg="#2d2d30")
        self.global_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.current_level = None
        
        levels = [
            (Level2CayleyGraph, "L1: Cayley Graph"),
            (Level3SubgroupsCosets, "L2: Subgroups & Cosets"),
            (Level4aConjugacy, "L3a: Conjugacy Classes"),
            (Level4bNormality, "L3b: Normal Subgroups"),
            (Level5CenterCommutator, "L4: Center & Commutator")
        ]
        
        for cls, name in levels:
            tk.Button(self.nav_frame, text=name, bg="#3e3e42", fg="white", font=("Arial", 9), anchor=tk.W,
                      command=lambda c=cls: self.load_level(c)).pack(fill=tk.X, padx=2, pady=1)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_level(Level2CayleyGraph)

    def load_level(self, level_class):
        if self.current_level:
            self.current_level.destroy()
        self.current_level = level_class(self.controls_frame, self.global_right)

    def on_closing(self):
        import matplotlib.pyplot as plt
        plt.close('all')
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = LabDashboard()
    app.mainloop()
