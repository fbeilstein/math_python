import tkinter as tk
from tkinter import messagebox
import importlib
import sys
import os

# Ensure directories are in path for robust importing
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks
from levels.level_1_ngram import Level1NGram
from levels.level_2_statistics import Level2Statistics
from levels.level_3_smoothing import Level3Smoothing
from levels.level_4_experts import Level4Experts
from levels.level_5_pi import Level5Pi

class MarkovLabDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Markov Chain & Statistics Lab")
        self.geometry("1100x850")
        self.configure(bg="#1e1e1e")

        self.levels = {
            1: ("L1 Basic N-Gram", Level1NGram),
            2: ("L2 Statistics", Level2Statistics),
            3: ("L3 Smoothing", Level3Smoothing),
            4: ("L4 Mixture of Experts", Level4Experts),
            5: ("L5 The Pi Simulator", Level5Pi)
        }
        
        self.current_level = None
        
        self.setup_sidebar()
        self.setup_main_area()
        
        # Start at Level 1
        self.switch_level(1)

    def setup_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#252526", highlightbackground="#333333", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="Laboratory Levels", font=("Arial", 12, "bold"), 
                 bg="#252526", fg="white").pack(pady=15, padx=20)
        
        self.level_buttons = {}
        for num, (name, _) in self.levels.items():
            btn = tk.Button(self.sidebar, text=name, width=22, font=("Arial", 10),
                            bg="#3e3e42", fg="white",
                            command=lambda n=num: self.switch_level(n))
            btn.pack(pady=4, padx=10)
            self.level_buttons[num] = btn

        tk.Button(self.sidebar, text="🔄 Reload Code", bg="#007acc", fg="white", font=("Arial", 10, "bold"),
                  command=self.reload_code).pack(pady=(40, 10), padx=20, fill="x")
                  
        tk.Label(self.sidebar, text="Instructions:", font=("Arial", 10, "bold", "underline"), bg="#252526", fg="white").pack(pady=(20, 5))
        tk.Label(self.sidebar, text="Press '1' or '2' on\nyour keyboard to\ntest the predictor.", 
                 bg="#252526", fg="gray", font=("Arial", 10)).pack()

    def setup_main_area(self):
        self.main_container = tk.Frame(self, bg="#1e1e1e")
        self.main_container.pack(side="right", fill="both", expand=True)

    def reload_code(self):
        try:
            importlib.reload(implementation_tasks)
            # Re-init current level to pick up new code
            self.switch_level(self.current_level_num)
        except Exception as e:
            messagebox.showerror("Compilation Error", f"Error in implementation_tasks.py:\n\n{e}")

    def switch_level(self, level_num):
        self.current_level_num = level_num
        for num, btn in self.level_buttons.items():
            btn.configure(bg="#3e3e42")
        self.level_buttons[level_num].configure(bg="#007acc")
        
        # Destroy current level
        if self.current_level is not None:
            self.current_level.destroy()
            
        # Create new level
        LevelClass = self.levels[level_num][1]
        self.current_level = LevelClass(self.main_container)
        self.current_level.pack(fill="both", expand=True)
        
        # Ensure keyboard events go to the level
        self.current_level.focus_set()

    def on_closing(self):
        if self.current_level is not None:
            self.current_level.destroy()
        self.destroy()

if __name__ == "__main__":
    app = MarkovLabDashboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
