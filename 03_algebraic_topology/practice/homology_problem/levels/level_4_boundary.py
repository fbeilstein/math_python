import tkinter as tk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.homology_base import MeshEditorLevel

class Level4Boundary(MeshEditorLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self.right_frame, text="L4: Boundary Matrices", font=("Arial", 16, "bold"), bg="#e0e0e0").pack(pady=10)
        
        self.output_text = tk.Text(self.right_frame, font=("Courier", 12), bg="#e0e0e0", wrap=tk.NONE)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if hasattr(self, 'mpl_canvas'):
            self.mpl_canvas.get_tk_widget().pack_forget()

        self.recalculate_math()

    def format_matrix(self, m, v, k):
        if not m or not m[0]: return "0\n"
        row_labels = [f"k_{x}" for x in v]
        col_labels = "       " + " ".join([f"{x:>4}" for x in k]) + "\n"
        s = col_labels
        s += "-------" + "-" * (5 * len(k)) + "\n"
        for i in range(len(m)):
            row_str = " ".join([f"{val:>4}" for val in m[i]])
            s += f"{row_labels[i]:<5} | {row_str}\n"
        return s + "\n"

    def recalculate_math(self):
        if not hasattr(self, 'output_text'): return
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        
        tt = ["".join(sorted([v.label for v in t.vertices])) for t in self.triangles]
        if not tt:
            self.output_text.insert(tk.END, "Draw some triangles to construct Boundary Matrices!")
            self.output_text.config(state=tk.DISABLED)
            return

        simplices = tasks.get_complex(tt)
        ch0 = [s for s in simplices if len(s) == 1]
        ch1 = [s for s in simplices if len(s) == 2]
        ch2 = [s for s in simplices if len(s) == 3]
        
        b1 = tasks.calculate_boundary(ch1, ch0)
        b2 = tasks.calculate_boundary(ch2, ch1)
        
        out = f"0-Chains (C0): {', '.join(ch0)}\n\n"
        out += f"1-Chains (C1): {', '.join(ch1)}\n\n"
        out += f"2-Chains (C2): {', '.join(ch2)}\n\n"
        
        out += "=== ∂1 BOUNDARY MATRIX ===\n"
        out += self.format_matrix(b1['m'], b1['v'], b1['k']) + "\n"
        
        out += "=== ∂2 BOUNDARY MATRIX ===\n"
        out += self.format_matrix(b2['m'], b2['v'], b2['k'])
        
        self.output_text.insert(tk.END, out)
        self.output_text.config(state=tk.DISABLED)


if __name__ == '__main__':
    unittest.main()
