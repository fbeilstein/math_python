import tkinter as tk
import sys
import os
import numpy as np
import ast

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevelUI

class GFTransformer(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, int):
            return ast.Call(
                func=ast.Name(id='GF', ctx=ast.Load()),
                args=[ast.Constant(value=node.value)],
                keywords=[]
            )
        return node
        
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        if isinstance(node.op, ast.Pow):
            right = node.right # Do not wrap exponent in GF
        else:
            right = self.visit(node.right)
        return ast.BinOp(left=left, op=node.op, right=right)

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        self.dyn_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.dyn_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.mode_var = tk.StringVar(value="Calculator")
        modes = ["Calculator", "Cayley Tables", "Inverse Mappings", "Power Orbits"]
        for m in modes:
            tk.Radiobutton(self.dyn_frame, text=m, variable=self.mode_var, value=m, 
                           command=self.build_dynamic_inputs, bg="#1e1e1e", fg="white", 
                           selectcolor="#3e3e42").pack(side=tk.LEFT, padx=5)
                           
        tk.Label(self.dyn_frame, text=" | p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(self.dyn_frame, width=5)
        self.ent_p.insert(0, "7")
        self.ent_p.pack(side=tk.LEFT, padx=3)
        self.ent_p.bind("<KeyRelease>", lambda e: self.update_canvas())

        self.input_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.build_dynamic_inputs()

    def build_dynamic_inputs(self, *args):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
            
        mode = self.mode_var.get()
        
        if mode == "Calculator":
            tk.Label(self.input_frame, text="Expression:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
            self.ent_expr = tk.Entry(self.input_frame, width=25)
            self.ent_expr.insert(0, "-2 * (3 + 5**-1)")
            self.ent_expr.pack(side=tk.LEFT, padx=3)
            self.ent_expr.bind("<Return>", lambda e: self.update_canvas())
            
        elif mode == "Power Orbits":
            tk.Label(self.input_frame, text="Base a:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
            self.ent_a = tk.Entry(self.input_frame, width=5)
            self.ent_a.insert(0, "2")
            self.ent_a.pack(side=tk.LEFT, padx=3)
            self.ent_a.bind("<KeyRelease>", lambda e: self.update_canvas())
            
        tk.Button(self.input_frame, text="Calculate", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()

    def draw_math(self):
        try:
            p = int(self.ent_p.get())
            if p < 2: raise ValueError("p must be >= 2")
            for i in range(2, int(p**0.5) + 1):
                if p % i == 0: raise ValueError(f"p={p} is not prime!")
                
            field = tasks.PrimeField(p)
            mode = self.mode_var.get()
            
            if mode == "Calculator":
                expr_str = self.ent_expr.get().strip()
                try:
                    tree = ast.parse(expr_str, mode='eval')
                    tree = GFTransformer().visit(tree)
                    ast.fix_missing_locations(tree)
                    code = compile(tree, '<string>', 'eval')
                    res = eval(code, {}, {'GF': field})
                except Exception as e:
                    raise ValueError(f"Invalid expression: {e}")
                
                expr_tex = expr_str.replace('%', '\\%')    
                text = f"GF(${p}$) Arithmetic\n\n"
                text += f"${expr_tex} \\ (\\mathrm{{mod}}\\ {p})$\n"
                text += f"$= {res.val}$"
                    
                self.ax.text(0.5, 0.5, text, fontsize=24, ha='center', va='center', color='white')
                
            elif mode == "Cayley Tables":
                if p > 13: raise ValueError("Prime too large for nice tables (p <= 13)")
                
                add_data = [[(field(i) + field(j)).val for j in range(p)] for i in range(p)]
                mul_data = [[(field(i) * field(j)).val for j in range(p)] for i in range(p)]
                
                spacer = [[-1]*2 for _ in range(p)]
                combined = np.hstack([add_data, spacer, mul_data])
                masked = np.ma.masked_where(combined == -1, combined)
                
                self.ax.imshow(masked, cmap='viridis')
                for i in range(p):
                    for j in range(p):
                        self.ax.text(j, i, add_data[i][j], ha="center", va="center", color="w" if add_data[i][j] < p/2 else "k")
                        self.ax.text(j + p + 2, i, mul_data[i][j], ha="center", va="center", color="w" if mul_data[i][j] < p/2 else "k")
                        
                self.ax.set_title(f"Addition (+) mod {p}                     Multiplication (*) mod {p}", color="white", fontsize=16, pad=20)
                
            elif mode == "Inverse Mappings":
                if p > 23: raise ValueError("Prime too large for nice mappings (p <= 23)")
                
                self.ax.set_xlim(-1, 7)
                self.ax.set_ylim(-1, p)
                self.ax.axis('off')
                
                self.ax.text(0.5, p, "Additive Inverses", color="white", fontsize=16, ha='center')
                self.ax.text(5.5, p, "Multiplicative Inverses", color="white", fontsize=16, ha='center')
                
                for i in range(p):
                    add_inv = (-field(i)).val
                    y1 = p - 1 - i
                    y2 = p - 1 - add_inv
                    
                    self.ax.text(0, y1, str(i), color="white", fontsize=14, ha='right', va='center')
                    self.ax.text(1, y2, str(add_inv), color="white", fontsize=14, ha='left', va='center')
                    
                    self.ax.annotate("", xy=(0.8, y2), xytext=(0.2, y1),
                                     arrowprops=dict(arrowstyle="->", color="#ffc107", lw=1, alpha=0.6))
                                     
                    if i != 0:
                        mul_inv = (field(1) / field(i)).val
                        y1_m = p - 1 - i
                        y2_m = p - 1 - mul_inv
                        
                        self.ax.text(5, y1_m, str(i), color="white", fontsize=14, ha='right', va='center')
                        self.ax.text(6, y2_m, str(mul_inv), color="white", fontsize=14, ha='left', va='center')
                        
                        self.ax.annotate("", xy=(5.8, y2_m), xytext=(5.2, y1_m),
                                         arrowprops=dict(arrowstyle="->", color="#28a745", lw=1, alpha=0.6))

            elif mode == "Power Orbits":
                if p > 31: raise ValueError("Prime too large for orbits (p <= 31)")
                a_val = int(self.ent_a.get()) % p
                a = field(a_val)
                
                theta = np.linspace(0, 2*np.pi, p, endpoint=False)
                theta = np.pi/2 - theta
                
                x = np.cos(theta)
                y = np.sin(theta)
                
                self.ax.scatter(x, y, s=600, c='#28a745', zorder=2)
                for i in range(p):
                    self.ax.text(x[i], y[i], str(i), ha='center', va='center', color='white', fontweight='bold', zorder=3)
                    
                self.ax.set_aspect('equal')
                self.ax.set_xlim(-1.5, 1.5)
                self.ax.set_ylim(-1.5, 1.5)
                self.ax.set_title(f"Powers of {a.val} mod {p}", color="white", fontsize=18, pad=20)
                
                if a.val == 0:
                    self.ax.annotate("", xy=(x[0], y[0]), xytext=(x[1], y[1]),
                                     arrowprops=dict(arrowstyle="->", color="#ffc107", lw=2, shrinkA=15, shrinkB=15, connectionstyle="arc3,rad=-0.1"), zorder=1)
                    self.ax.annotate("", xy=(x[0]+0.01, y[0]+0.01), xytext=(x[0], y[0]),
                                     arrowprops=dict(arrowstyle="->", color="#ffc107", lw=2, shrinkA=15, shrinkB=15, connectionstyle="arc3,rad=3.0"), zorder=1)
                    return
                    
                visited = []
                curr = 1
                while True:
                    visited.append(curr)
                    nxt = (field(curr) * a).val
                    
                    self.ax.annotate("", xy=(x[nxt], y[nxt]), xytext=(x[curr], y[curr]),
                                     arrowprops=dict(arrowstyle="->", color="#ffc107", lw=2, shrinkA=15, shrinkB=15,
                                     connectionstyle="arc3,rad=-0.1"), zorder=1)
                    
                    curr = nxt
                    if curr == 1:
                        break
                        
        except Exception as e:
            msg = str(e)
            if "NoneType" in msg: msg = "Function not yet implemented!"
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')
