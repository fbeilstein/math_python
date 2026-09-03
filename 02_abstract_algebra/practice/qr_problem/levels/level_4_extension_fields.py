import tkinter as tk
from tkinter import ttk
import sys
import os
import numpy as np
import ast

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
import algebra_utils as utils
from levels.base_level import BaseLevelUI, poly_to_latex

def poly_to_str(poly):
    if not poly or (len(poly) == 1 and poly[0] == 0): return "0"
    terms = []
    deg = len(poly) - 1
    for i, c in enumerate(poly):
        if c == 0: continue
        power = deg - i
        term = ""
        if c != 1 or power == 0: term += str(c)
        if power > 0:
            term += "x"
            if power > 1: term += f"^{power}"
        terms.append(term)
    return " + ".join(terms)

class GFTransformer(ast.NodeTransformer):
    def visit_List(self, node):
        return ast.Call(
            func=ast.Name(id='GF', ctx=ast.Load()),
            args=[node],
            keywords=[]
        )
    def visit_Tuple(self, node):
        return ast.Call(
            func=ast.Name(id='GF', ctx=ast.Load()),
            args=[ast.List(elts=node.elts, ctx=ast.Load())],
            keywords=[]
        )
    def visit_Constant(self, node):
        if isinstance(node.value, int):
            return ast.Call(
                func=ast.Name(id='GF', ctx=ast.Load()),
                args=[ast.List(elts=[ast.Constant(value=node.value)], ctx=ast.Load())],
                keywords=[]
            )
        return node
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        if isinstance(node.op, ast.Pow):
            right = node.right
        else:
            right = self.visit(node.right)
        return ast.BinOp(left=left, op=node.op, right=right)

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        self.dyn_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.dyn_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.mode_var = tk.StringVar(value="Calculator")
        modes = ["Calculator", "Cayley Tables", "Inverse Mappings"]
        for m in modes:
            tk.Radiobutton(self.dyn_frame, text=m, variable=self.mode_var, value=m, 
                           command=self.build_dynamic_inputs, bg="#1e1e1e", fg="white", 
                           selectcolor="#3e3e42").pack(side=tk.LEFT, padx=5)
                           
        tk.Label(self.dyn_frame, text=" | p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(self.dyn_frame, width=3)
        self.ent_p.insert(0, "2")
        self.ent_p.pack(side=tk.LEFT, padx=3)
        self.ent_p.bind("<Return>", lambda e: self.update_primitives())
        
        tk.Label(self.dyn_frame, text="n:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_n = tk.Entry(self.dyn_frame, width=3)
        self.ent_n.insert(0, "3")
        self.ent_n.pack(side=tk.LEFT, padx=3)
        self.ent_n.bind("<Return>", lambda e: self.update_primitives())

        tk.Label(self.dyn_frame, text="Poly:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.poly_combo = ttk.Combobox(self.dyn_frame, state="readonly", width=12)
        self.poly_combo.pack(side=tk.LEFT, padx=5)
        self.poly_combo.bind("<<ComboboxSelected>>", lambda e: self.update_canvas())

        self.input_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.primitives_list = []
        self.update_primitives()

    def build_dynamic_inputs(self, *args):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
            
        mode = self.mode_var.get()
        
        if mode == "Calculator":
            tk.Label(self.input_frame, text="Expr:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
            self.ent_expr = tk.Entry(self.input_frame, width=30)
            self.ent_expr.insert(0, "(1, 1) * [1, 0] + (0, 1)**-1")
            self.ent_expr.pack(side=tk.LEFT, padx=3)
            self.ent_expr.bind("<Return>", lambda e: self.update_canvas())
            
        tk.Button(self.input_frame, text="Calculate", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()

    def update_primitives(self):
        try:
            p = int(self.ent_p.get())
            n = int(self.ent_n.get())
            if p < 2 or n < 1: return
            for i in range(2, int(p**0.5) + 1):
                if p % i == 0: return
                
            primitives = utils.find_primitives(p, n)
            self.primitives_list = primitives
            str_list = [poly_to_str(poly[::-1]) for poly in primitives]
            self.poly_combo['values'] = str_list
            if str_list:
                self.poly_combo.current(0)
            else:
                self.poly_combo.set('')
                
            self.build_dynamic_inputs()
        except:
            pass

    def draw_math(self):
        try:
            p = int(self.ent_p.get())
            n = int(self.ent_n.get())
            
            idx = self.poly_combo.current()
            if idx < 0 or not self.primitives_list:
                raise ValueError("No primitive polynomial selected!")
                
            poly = self.primitives_list[idx]
            poly_obj = utils.make_poly(poly, p)
            gf = tasks.ExtensionField(poly_obj)
            
            def make_ext_elem(val):
                cs = [tasks.PrimeField(p)(v) for v in reversed(val)]
                return tasks.GaloisFieldElement(tasks.Polynomial(cs), gf)

            mode = self.mode_var.get()
            
            if mode == "Calculator":
                expr_str = self.ent_expr.get().strip()
                try:
                    tree = ast.parse(expr_str, mode='eval')
                    tree = GFTransformer().visit(tree)
                    ast.fix_missing_locations(tree)
                    code = compile(tree, '<string>', 'eval')
                    res = eval(code, {}, {'GF': make_ext_elem})
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
                expr_tex = re.sub(r'\*\*(-?\d+)', r'^{\1}', expr_tex)
                expr_tex = expr_tex.replace('%', '\\%').replace('*', '\\cdot ')
                
                res_coeffs = [res.val[i].val for i in range(res.val.degree() + 1)]
                res_tex = poly_to_latex(res_coeffs[::-1]).strip('$')
                
                text = f"GF(${p}^{{{n}}}$) Arithmetic\n\n"
                text += f"${expr_tex}$\n"
                text += f"$= {res_tex}$"
                    
                self.ax.text(0.5, 0.5, text, fontsize=24, ha='center', va='center', color='white')
                
            elif mode == "Cayley Tables":
                if p**n > 16: raise ValueError("Field too large for nice tables (p^n <= 16)")
                
                alpha_list = [gf.zero]
                alpha_str_map = {0: "$0$"}
                for i in range((p**n) - 1):
                    elem = gf.alpha ** i
                    alpha_list.append(elem)
                    val = utils.ext_to_int(elem)
                    alpha_str_map[val] = f"$\\alpha^{{{i}}}$" if i > 1 else ("$\\alpha$" if i == 1 else "$1$")
                
                add_data = [[alpha_str_map[utils.ext_to_int(a + b)] for b in alpha_list] for a in alpha_list]
                
                self.ax.set_xlim(-2, p**n + 6)
                self.ax.set_ylim(-1, p**n + 2)
                self.ax.axis('off')
                
                self.ax.text((p**n)/2, p**n + 1, "Addition (+) Zech's Logarithms", color="white", fontsize=16, ha='center')
                
                for i, a in enumerate(alpha_list):
                    header = alpha_str_map[utils.ext_to_int(a)]
                    self.ax.text(i, -1, header, color="#00ffff", ha="center", va="center", fontsize=12)
                    self.ax.text(-1, p**n - 1 - i, header, color="#00ffff", ha="center", va="center", fontsize=12)
                
                for i in range(p**n):
                    for j in range(p**n):
                        self.ax.text(j, p**n - 1 - i, add_data[i][j], ha="center", va="center", color="w", fontsize=10)
                        
                self.ax.text(p**n + 3, p**n + 1, "Exponential Cycle", color="white", fontsize=16, ha='center')
                for i in range((p**n) - 1):
                    val = utils.ext_to_int(gf.alpha ** i)
                    c = []
                    if val == 0: c = [0]
                    else:
                        temp = val
                        while temp > 0:
                            c.insert(0, temp % p)
                            temp //= p
                    sym = alpha_str_map[val]
                    self.ax.text(p**n + 2, p**n - 1 - i, f"{sym} = {poly_to_latex(c)}", color="white", ha="left", va="center", fontsize=12)

            elif mode == "Inverse Mappings":
                if p**n > 16: raise ValueError("Field too large for nice mappings (p^n <= 16)")
                
                elems = []
                for val in range(p**n):
                    c = []
                    if val == 0: c = [0]
                    else:
                        temp = val
                        while temp > 0:
                            c.insert(0, temp % p)
                            temp //= p
                    
                    poly_elem = make_ext_elem(c)
                    str_rep = poly_to_latex(c)
                    elems.append((val, poly_elem, str_rep))
                
                self.ax.set_xlim(-1, 8)
                self.ax.set_ylim(-1, p**n + 1)
                self.ax.axis('off')
                
                self.ax.text(0.5, p**n, "Additive Inverses", color="white", fontsize=16, ha='center')
                self.ax.text(6.5, p**n, "Multiplicative Inverses", color="white", fontsize=16, ha='center')
                
                for val, poly_elem, str_rep in elems:
                    add_inv = -poly_elem
                    add_inv_val = utils.ext_to_int(add_inv)
                    add_inv_str = elems[add_inv_val][2]
                    
                    y1 = p**n - 1 - val
                    y2 = p**n - 1 - add_inv_val
                    
                    self.ax.text(0, y1, str_rep, color="white", fontsize=12, ha='right', va='center')
                    self.ax.text(1.5, y2, add_inv_str, color="white", fontsize=12, ha='left', va='center')
                    self.ax.annotate("", xy=(1.3, y2), xytext=(0.2, y1),
                                     arrowprops=dict(arrowstyle="->", color="#ffc107", lw=1, alpha=0.6))
                                     
                    if val != 0:
                        mul_inv = gf.one / poly_elem
                        mul_inv_val = utils.ext_to_int(mul_inv)
                        mul_inv_str = elems[mul_inv_val][2]
                        
                        y1_m = p**n - 1 - val
                        y2_m = p**n - 1 - mul_inv_val
                        
                        self.ax.text(6, y1_m, str_rep, color="white", fontsize=12, ha='right', va='center')
                        self.ax.text(7.5, y2_m, mul_inv_str, color="white", fontsize=12, ha='left', va='center')
                        self.ax.annotate("", xy=(7.3, y2_m), xytext=(6.2, y1_m),
                                         arrowprops=dict(arrowstyle="->", color="#00ffff", lw=1, alpha=0.6))
                
        except Exception as e:
            msg = str(e)
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            if "list index out of range" in msg: msg = "Polynomial cannot be empty!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')

if __name__ == '__main__':
    lvl = LevelUI()
    lvl.draw()
    tk.mainloop()
