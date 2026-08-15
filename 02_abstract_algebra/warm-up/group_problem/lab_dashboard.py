import tkinter as tk
from tkinter import ttk
import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from levels.level_1_axioms import Level1Axioms
from levels.level_2_permutations import Level2Permutations
from levels.level_3_cayley import Level3Cayley
from levels.level_4_subgroups import Level4Subgroups
from levels.level_5_cosets import Level5Cosets
from levels.level_6_center import Level6Center
from levels.level_7_homomorphisms import Level7Homomorphisms


class LabDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Group Theory Laboratory")
        self.geometry("1100x750")
        self.configure(bg="#1e1e1e")

        tk.Label(self, text="Group Theory Laboratory", font=("Arial", 16, "bold"),
                 bg="#1e1e1e", fg="#007acc").pack(pady=5)

        self.global_left = tk.Frame(self, bg="#1e1e1e", width=350)
        self.global_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.global_left.pack_propagate(False)

        self.nav_frame = tk.Frame(self.global_left, bg="#2d2d30", bd=2, relief=tk.RAISED)
        self.nav_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(self.nav_frame, text="Navigation", font=("Arial", 9, "bold"),
                 bg="#2d2d30", fg="#7ee787").pack(pady=(4, 4))

        self.controls_frame = tk.Frame(self.global_left, bg="#1e1e1e")
        self.controls_frame.pack(fill=tk.BOTH, expand=True)

        self.global_right = tk.Frame(self, bg="#2d2d30")
        self.global_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.current_level = None

        levels = [
            (Level1Axioms, "L1: Axiom Checker"),
            (Level2Permutations, "L2: Permutations"),
            (Level3Cayley, "L3: Cayley Graph"),
            (Level4Subgroups, "L4: Subgroups"),
            (Level5Cosets, "L5: Cosets & Normality"),
            (Level6Center, "L6: Center & Conjugacy"),
            (Level7Homomorphisms, "L7: Kernels & Images"),
        ]

        for cls, name in levels:
            tk.Button(self.nav_frame, text=name, bg="#3e3e42", fg="white",
                      font=("Arial", 9), anchor=tk.W,
                      command=lambda c=cls: self.load_level(c)).pack(fill=tk.X, padx=2, pady=1)

        tk.Button(self.nav_frame, text="🔄 Reload Code", bg="#d32f2f", fg="white",
                  font=("Arial", 9, "bold"),
                  command=self.reload_code).pack(fill=tk.X, padx=2, pady=(10, 2))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_level(Level1Axioms)

    def reload_code(self):
        import importlib
        try:
            if 'implementation_tasks' in sys.modules:
                importlib.reload(sys.modules['implementation_tasks'])
            else:
                import implementation_tasks
                
            if self.current_level:
                cls = self.current_level.__class__
                self.load_level(cls)
        except Exception as e:
            import tkinter.messagebox as mb
            mb.showerror("Reload Error", f"Error reloading code:\n{e}")

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
