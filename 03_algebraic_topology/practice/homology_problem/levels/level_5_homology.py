import tkinter as tk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.homology_base import MeshEditorLevel

class Level5Homology(MeshEditorLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self.right_frame, text="L5: Homology Computation", font=("Arial", 16, "bold"), bg="#e0e0e0").pack(pady=5)
        
        # We KEEP the mpl_canvas provided by MeshEditorLevel for this one!
        self.recalculate_math()

    def recalculate_math(self):
        self.ax.clear()
        self.ax.axis("off")
        
        tt = ["".join(sorted([v.label for v in t.vertices])) for t in self.triangles]
        if not tt:
            self.ax.text(0.1, 0.9, "Draw a surface to compute homology!", color="blue", fontsize=14)
            self.mpl_canvas.draw()
            return
            
        if len(set(tt)) != len(tt):
            self.ax.text(0.1, 0.9, f"Duplicate triangle detected: {max(set(tt), key=tt.count)}", color="red", fontsize=14)
            self.mpl_canvas.draw()
            return

        simplices = tasks.get_complex(tt)
        ch0 = [s for s in simplices if len(s) == 1]
        ch1 = [s for s in simplices if len(s) == 2]
        ch2 = [s for s in simplices if len(s) == 3]
        
        b1 = tasks.calculate_boundary(ch1, ch0)
        b2 = tasks.calculate_boundary(ch2, ch1)
        
        h0, h1, h2, torsion = tasks.compute_homology(len(ch0), len(ch1), len(ch2), b1['rank'], b2['rank'], b2['torsion'])
        
        out_txt = "Homology Groups:\n"
        out_txt += f"$H_0(K) \\cong \\mathbb{{Z}}^{h0}$\n"
        out_txt += f"$H_1(K) \\cong \\mathbb{{Z}}^{h1}$"
        if torsion:
            for t in torsion: out_txt += f"$\\oplus \\mathbb{{Z}}_{{{abs(t)}}}$"
        out_txt += "\n"
        out_txt += f"$H_2(K) \\cong \\mathbb{{Z}}^{h2}$\n\n"
        out_txt += f"Connected Components: {h0}\n"
        out_txt += f"Holes: {h1}\n"
        out_txt += f"Voids: {h2}\n"
        
        self.ax.text(0.05, 0.9, out_txt, fontsize=14, va="top", wrap=True)
        
        ch_str = (
            r"$\underset{\mathrm{dim}=0}{\emptyset} "
            r"\underset{\mathrm{rank}=0}{\overset{\partial_3}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=" + str(len(ch2)) + r"}{C_2} "
            r"\underset{\mathrm{rank}=" + str(b2['rank']) + r"}{\overset{\partial_2}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=" + str(len(ch1)) + r"}{C_1} "
            r"\underset{\mathrm{rank}=" + str(b1['rank']) + r"}{\overset{\partial_1}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=" + str(len(ch0)) + r"}{C_0} "
            r"\underset{\mathrm{rank}=0}{\overset{\partial_0}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=0}{\{0\}}$"
        )
        self.ax.text(0.05, 0.3, ch_str, fontsize=14, va="top")
        
        self.mpl_canvas.draw()


if __name__ == '__main__':
    unittest.main()
