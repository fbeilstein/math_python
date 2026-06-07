import tkinter as tk
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel, BaseLevelUI, poly_to_latex

class Level4(BaseLevel):
    def test_gfpn_math(self):
        p, n = 2, 8
        poly = [1, 0, 0, 0, 1, 1, 1, 0, 1]
        exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
        
        a = [2, 3] 
        b = [4]
        res = tasks.gfpn_poly_multiply(a, b, log_table, exp_table, p, n)
        self.assertEqual(res, [8, 12])

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        f1 = tk.Frame(self.top_frame, bg="#1e1e1e")
        f1.pack(fill=tk.X, pady=2)
        
        tk.Label(f1, text="p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(f1, width=3)
        self.ent_p.insert(0, "2")
        self.ent_p.pack(side=tk.LEFT, padx=2)
        
        tk.Label(f1, text="n:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_n = tk.Entry(f1, width=3)
        self.ent_n.insert(0, "8")
        self.ent_n.pack(side=tk.LEFT, padx=2)
        
        tk.Label(f1, text="Primitive Poly:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_poly = tk.Entry(f1, width=15)
        self.ent_poly.insert(0, "1,0,0,0,1,1,1,0,1")
        self.ent_poly.pack(side=tk.LEFT, padx=2)
        
        f2 = tk.Frame(self.top_frame, bg="#1e1e1e")
        f2.pack(fill=tk.X, pady=2)
        
        tk.Label(f2, text="Poly A:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_a = tk.Entry(f2, width=15)
        self.ent_a.insert(0, "2, 3")
        self.ent_a.pack(side=tk.LEFT, padx=5)
        
        tk.Label(f2, text="Poly B:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_b = tk.Entry(f2, width=15)
        self.ent_b.insert(0, "4")
        self.ent_b.pack(side=tk.LEFT, padx=5)
        
        tk.Button(f2, text="Calculate", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        
        self.update_canvas()
        
    def update_canvas(self):
        self.ax.clear()
        self.ax.axis('off')
        self.draw_math()
        self.canvas.draw()
        
    def draw_math(self):
        try:
            p = int(self.ent_p.get())
            n = int(self.ent_n.get())
            poly = [int(x.strip()) for x in self.ent_poly.get().replace(",", " ").split()]
            exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
            
            a = [int(x.strip()) for x in self.ent_a.get().replace(",", " ").split()]
            b = [int(x.strip()) for x in self.ent_b.get().replace(",", " ").split()]
            
            a_tex = poly_to_latex(a).strip('$')
            b_tex = poly_to_latex(b).strip('$')
            
            mul_res = tasks.gfpn_poly_multiply(a, b, log_table, exp_table, p, n)
            mul_tex = poly_to_latex(mul_res).strip('$')
            
            try:
                rem_res = tasks.gfpn_poly_remainder(a, b, log_table, exp_table, p, n)
                rem_tex = poly_to_latex(rem_res).strip('$')
            except ZeroDivisionError:
                rem_tex = "\\text{undefined}"
            
            def wrap(t):
                if '+' in t or '-' in t or '\\dots' in t: return f"({t})"
                return t
                
            a_str = wrap(a_tex)
            b_str = wrap(b_tex)
            
            text = f"GF(${p}^{{{n}}}$) Polynomial Arithmetic\n\n"
            text += f"${a_str} \\cdot {b_str} = {mul_tex}$\n\n"
            text += f"${a_str} \\text{{ mod }} {b_str} = {rem_tex}$\n"
            
            self.ax.text(0.5, 0.5, text, fontsize=18, ha='center', va='center', color='white')
        except Exception as e:
            msg = str(e)
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            if "list index out of range" in msg: msg = "Polynomial cannot be empty!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--no-graphics':
        import unittest
        unittest.main(argv=['first-arg-is-ignored'])
