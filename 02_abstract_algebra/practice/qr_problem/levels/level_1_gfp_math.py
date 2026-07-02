import tkinter as tk
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevelUI, poly_to_latex

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        tk.Label(self.top_frame, text="Dividend:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_div = tk.Entry(self.top_frame, width=20)
        self.ent_div.insert(0, "1,0,0,0,0,0,0,0,0")
        self.ent_div.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.top_frame, text="Divisor:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_dsr = tk.Entry(self.top_frame, width=20)
        self.ent_dsr.insert(0, "1,0,0,0,1,1,1,0,1")
        self.ent_dsr.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.top_frame, text="Prime p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(self.top_frame, width=5)
        self.ent_p.insert(0, "2")
        self.ent_p.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.top_frame, text="Calculate", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()
        
    def draw_math(self):
        try:
            p = int(self.ent_p.get())
            if p < 2: raise ValueError("p must be >= 2")
            for i in range(2, int(p**0.5) + 1):
                if p % i == 0: raise ValueError(f"p={p} is not prime!")
                
            dividend = [int(x.strip()) % p for x in self.ent_div.get().replace(",", " ").split()]
            divisor = [int(x.strip()) % p for x in self.ent_dsr.get().replace(",", " ").split()]
            
            # strip leading zeros for rendering
            while len(dividend) > 1 and dividend[0] == 0: dividend.pop(0)
            while len(divisor) > 1 and divisor[0] == 0: divisor.pop(0)
            
            if len(divisor) == 1 and divisor[0] == 0:
                raise ValueError("Cannot divide by zero polynomial!")
            
            q, r = tasks.gfp_poly_divide(dividend, divisor, p)
            
            p_tex = poly_to_latex(dividend).strip('$')
            d_tex = poly_to_latex(divisor).strip('$')
            q_tex = poly_to_latex(q).strip('$')
            r_tex = poly_to_latex(r).strip('$')
            
            text = f"GF(${p}$) Polynomial Division\n\n"
            
            if r_tex == "0":
                if q_tex == "0": eq = f"$\\frac{{{p_tex}}}{{{d_tex}}} = 0$"
                else: eq = f"$\\frac{{{p_tex}}}{{{d_tex}}} = {q_tex}$"
            else:
                if q_tex == "0": eq = f"$\\frac{{{p_tex}}}{{{d_tex}}} = \\frac{{{r_tex}}}{{{d_tex}}}$"
                else: eq = f"$\\frac{{{p_tex}}}{{{d_tex}}} = {q_tex} + \\frac{{{r_tex}}}{{{d_tex}}}$"
                
            text += eq
            
            self.ax.text(0.5, 0.5, text, fontsize=22, ha='center', va='center', color='white')
        except Exception as e:
            msg = str(e)
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            if "list index out of range" in msg: msg = "Polynomial cannot be empty!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')

