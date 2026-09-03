import tkinter as tk
import sys
import os
import ast

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevelUI, poly_to_latex

class PolyTransformer(ast.NodeTransformer):
    def __init__(self, p):
        self.p = p

    def visit_List(self, node):
        gf_args = []
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, int):
                gf_call = ast.Call(
                    func=ast.Name(id='GF', ctx=ast.Load()),
                    args=[ast.Constant(value=elt.value)],
                    keywords=[]
                )
                gf_args.append(gf_call)
            else:
                gf_args.append(self.visit(elt))
                
        # Reverse gf_args here because Polynomial constructor expects Low-to-High,
        # but the user provides High-to-Low lists in the UI (e.g. [2, 0, 1] for 2x^2 + 1)
        poly_call = ast.Call(
            func=ast.Name(id='Poly', ctx=ast.Load()),
            args=[ast.List(elts=list(reversed(gf_args)), ctx=ast.Load())],
            keywords=[]
        )
        return poly_call

    visit_Tuple = visit_List

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        tk.Label(self.top_frame, text="Expression:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_expr = tk.Entry(self.top_frame, width=35)
        self.ent_expr.insert(0, "divmod([2, 0, 1], [1, 2])")
        self.ent_expr.pack(side=tk.LEFT, padx=5)
        self.ent_expr.bind("<Return>", lambda e: self.update_canvas())
        
        tk.Label(self.top_frame, text="Prime p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(self.top_frame, width=5)
        self.ent_p.insert(0, "3")
        self.ent_p.pack(side=tk.LEFT, padx=5)
        self.ent_p.bind("<Return>", lambda e: self.update_canvas())
        
        tk.Button(self.top_frame, text="Calculate", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()
        
    def draw_math(self):
        try:
            p = int(self.ent_p.get())
            if p < 2: raise ValueError("p must be >= 2")
            for i in range(2, int(p**0.5) + 1):
                if p % i == 0: raise ValueError(f"p={p} is not prime!")
                
            expr_str = self.ent_expr.get().strip()
            field = tasks.PrimeField(p)
            
            try:
                tree = ast.parse(expr_str, mode='eval')
                tree = PolyTransformer(p).visit(tree)
                ast.fix_missing_locations(tree)
                code = compile(tree, '<string>', 'eval')
                
                def Poly(coeffs):
                    return tasks.Polynomial(coeffs)
                    
                env = {'GF': field, 'Poly': Poly, 'divmod': divmod}
                res = eval(code, {}, env)
            except Exception as e:
                raise ValueError(f"Invalid expression: {e}")
                
            import re
            def replace_array_with_poly(match):
                try:
                    val = ast.literal_eval(match.group(0))
                    if isinstance(val, (list, tuple)) and all(isinstance(x, int) for x in val):
                        tex = poly_to_latex(list(val)).strip('$')
                        if not tex: tex = "0"
                        return f"({tex})"
                except:
                    pass
                return match.group(0)
                
            expr_tex = re.sub(r'\[[\d\s,]+\]|\([\d\s,]+\)', replace_array_with_poly, expr_str)
            expr_tex = expr_tex.replace('%', '\\%').replace('*', '\\cdot ').replace('divmod', '\\mathrm{divmod}')
            text = f"GF(${p}$) Polynomial Arithmetic\n\n"
            text += f"${expr_tex} \\ (\\mathrm{{mod}}\\ {p})$\n"
            
            if isinstance(res, tuple):
                q, r = res
                q_vals = [q[i].val for i in range(q.degree() + 1)]
                r_vals = [r[i].val for i in range(r.degree() + 1)]
                q_tex = poly_to_latex(q_vals[::-1]).strip('$') 
                r_tex = poly_to_latex(r_vals[::-1]).strip('$')
                text += f"$= (\\mathrm{{Q:}}\\ {q_tex}, \\ \\mathrm{{R:}}\\ {r_tex})$"
            elif isinstance(res, tasks.Polynomial):
                res_vals = [res[i].val for i in range(res.degree() + 1)]
                res_tex = poly_to_latex(res_vals[::-1]).strip('$')
                text += f"$= {res_tex}$"
            else:
                text += f"$= {res}$"
                
            self.ax.text(0.5, 0.5, text, fontsize=22, ha='center', va='center', color='white')
        except Exception as e:
            msg = str(e)
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')
