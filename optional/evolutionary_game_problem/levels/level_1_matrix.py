import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level1Matrix(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.setup_graph_ui()
        self.add_warning()
        
        # Get strategies dynamically from the student's implementation
        self.strategies = {cls.__name__: cls for cls in tasks.BaseStrategy.__subclasses__()}
        strat_names = list(self.strategies.keys())
        
        # UI controls
        tk.Label(self.left_panel, text="Player 1 Strategy:", bg="#1e1e1e", fg="white").pack(anchor="w")
        self.strat1_var = tk.StringVar(value=strat_names[0] if strat_names else "")
        ttk.Combobox(self.left_panel, textvariable=self.strat1_var, values=strat_names, state="readonly").pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.left_panel, text="Player 2 Strategy:", bg="#1e1e1e", fg="white").pack(anchor="w")
        self.strat2_var = tk.StringVar(value=strat_names[1] if len(strat_names) > 1 else (strat_names[0] if strat_names else ""))
        ttk.Combobox(self.left_panel, textvariable=self.strat2_var, values=strat_names, state="readonly").pack(fill=tk.X, pady=(0, 10))
        
        matrix_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        matrix_frame.pack(fill=tk.X, pady=10)
        
        self.build_matrix_ui(matrix_frame, T_def="5", R_def="3", P_def="1", S_def="0")
        
        tk.Label(self.left_panel, text="Rounds:", bg="#1e1e1e", fg="white").pack(anchor="w", pady=(10,0))
        self.entry_rounds = tk.Entry(self.left_panel)
        self.entry_rounds.insert(0, "100")
        self.entry_rounds.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(self.left_panel, text="Play Match", command=self.generate).pack(fill=tk.X, pady=10)
        
    def generate(self):
        self.hide_warning()
        try:
            T = float(self.entry_T.get())
            R = float(self.entry_R.get())
            P = float(self.entry_P.get())
            S = float(self.entry_S.get())
            rounds = int(self.entry_rounds.get())
            
            matrix = {
                'C': {'C': R, 'D': S},
                'D': {'C': T, 'D': P}
            }
            
            s1_class = self.strategies.get(self.strat1_var.get())
            s2_class = self.strategies.get(self.strat2_var.get())
            
            if not s1_class or not s2_class:
                raise ValueError("Invalid strategy selected.")
                
            s1 = s1_class()
            s2 = s2_class()
            
            score_A, score_B = tasks.play_match(s1, s2, matrix, rounds)
            
            self.ax.clear()
            
            labels = [f"Player 1\n({s1_class.__name__})", f"Player 2\n({s2_class.__name__})"]
            scores = [score_A, score_B]
            colors = ['#1f77b4', '#ff7f0e']
            
            self.ax.bar(labels, scores, color=colors)
            self.ax.set_ylabel("Total Payoff")
            self.ax.set_title(f"1v1 Match Results ({rounds} rounds)")
            
            for i, v in enumerate(scores):
                self.ax.text(i, v, str(v), ha='center', va='bottom', color='white', fontweight='bold')
                
            self.canvas.draw()
            
        except Exception as e:
            self.show_warning(str(e))

if __name__ == "__main__":
    root = tk.Tk()
    
    def on_closing():
        root.quit()
        root.destroy()
        sys.exit(0)
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.geometry("800x600")
    controls = tk.Frame(root, width=200)
    controls.pack(side=tk.LEFT, fill=tk.Y)
    canvas = tk.Frame(root)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    app = Level1Matrix(controls, canvas)
    root.mainloop()
