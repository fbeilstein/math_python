import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level2Tournament(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        self.cumulative_scores_i = None
        self.cumulative_scores_j = None
        self.match_states = None
        self.total_matches = 0
        
        self.setup_graph_ui()
        self.add_warning()
        
        self.strategies = {cls.__name__: cls for cls in tasks.BaseStrategy.__subclasses__()}
        
        tk.Label(self.left_panel, text="Round-Robin Tournament", bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        matrix_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        matrix_frame.pack(fill=tk.X, pady=10)
        
        self.build_matrix_ui(matrix_frame, T_def="5", R_def="3", P_def="1", S_def="0")
        
        tk.Button(self.left_panel, text="Run Tournament", command=self.generate).pack(fill=tk.X, pady=(20, 5))
        tk.Button(self.left_panel, text="Reset Scores", command=self.reset_scores).pack(fill=tk.X, pady=5)
        
    def reset_scores(self):
        self.cumulative_scores_i = None
        self.cumulative_scores_j = None
        self.match_states = None
        self.total_matches = 0
        self.fig.clear()
        self.canvas.draw()
        
    def generate(self):
        self.hide_warning()
        try:
            T = float(self.entry_T.get())
            R = float(self.entry_R.get())
            P = float(self.entry_P.get())
            S = float(self.entry_S.get())
            rounds = 1
            
            matrix = {
                'C': {'C': R, 'D': S},
                'D': {'C': T, 'D': P}
            }
            
            import numpy as np
            
            # Re-fetch in case student added more
            self.strategies = {cls.__name__: cls for cls in tasks.BaseStrategy.__subclasses__()}
            strat_names = list(self.strategies.keys())
            N = len(strat_names)
            if N == 0:
                raise ValueError("No strategies defined in implementation_tasks.py")
                
            if self.cumulative_scores_i is None or self.cumulative_scores_i.shape != (N, N):
                self.cumulative_scores_i = np.zeros((N, N))
                self.cumulative_scores_j = np.zeros((N, N))
                self.match_states = [[None for _ in range(N)] for _ in range(N)]
                self.total_matches = 0
                
            self.total_matches += 1
            
            percent_results = np.zeros((N, N))
            percent_results_opp = np.zeros((N, N))
            
            for i in range(N):
                for j in range(N):
                    if self.match_states[i][j] is None:
                        s1 = self.strategies[strat_names[i]]()
                        s2 = self.strategies[strat_names[j]]()
                        hist_A = []
                        hist_B = []
                        s1.reset()
                        s2.reset()
                        self.match_states[i][j] = (s1, s2, hist_A, hist_B)
                    else:
                        s1, s2, hist_A, hist_B = self.match_states[i][j]
                        
                    sc1 = 0
                    sc2 = 0
                    for _ in range(rounds):
                        action_A = s1.get_action(hist_A, hist_B)
                        action_B = s2.get_action(hist_B, hist_A)
                        
                        sc1 += matrix[action_A][action_B]
                        sc2 += matrix[action_B][action_A]
                        
                        hist_A.append(action_A)
                        hist_B.append(action_B)
                    
                    self.cumulative_scores_i[i, j] += sc1
                    self.cumulative_scores_j[i, j] += sc2
                    
                    tot_i = self.cumulative_scores_i[i, j]
                    tot_j = self.cumulative_scores_j[i, j]
                    
                    total = tot_i + tot_j
                    if total > 0:
                        percent_results[i, j] = (tot_i / total) * 100
                        percent_results_opp[i, j] = (tot_j / total) * 100
                    else:
                        percent_results[i, j] = 50.0
                        percent_results_opp[i, j] = 50.0
            
            self.fig.clear()
            self.ax = self.fig.add_subplot(111)
            
            # Reapply dark theme styling that gets wiped by add_subplot
            self.ax.set_facecolor('#2d2d30')
            self.ax.tick_params(colors='white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
            for spine in self.ax.spines.values():
                spine.set_edgecolor('white')
                
            cax = self.ax.imshow(percent_results, cmap='RdYlGn', vmin=0, vmax=100)
            
            for i in range(N):
                for j in range(N):
                    pct_i = percent_results[i, j]
                    raw_i = self.cumulative_scores_i[i, j]
                    name_i = strat_names[i]
                    
                    pct_j = percent_results_opp[i, j]
                    raw_j = self.cumulative_scores_j[i, j]
                    name_j = strat_names[j]
                    
                    # RdYlGn is light in the middle (~50%), dark at the edges
                    text_color = "black" if 30 < pct_i < 70 else "white"
                    text = f"{name_i} - {pct_i:.1f}% ({raw_i:.1f})\n{name_j} - {pct_j:.1f}% ({raw_j:.1f})"
                    self.ax.text(j, i, text, ha="center", va="center", color=text_color, fontsize=9)
            
            self.ax.set_title(f"Tournament Match Outcomes (Row vs Col)")
            
            self.ax.set_xticks(range(N))
            self.ax.set_yticks(range(N))
            self.ax.set_xticklabels(strat_names, rotation=45, ha='right')
            self.ax.set_yticklabels(strat_names)
            
            self.cbar = self.fig.colorbar(cax, ax=self.ax)
            
            self.fig.tight_layout()
            
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
    app = Level2Tournament(controls, canvas)
    root.mainloop()
