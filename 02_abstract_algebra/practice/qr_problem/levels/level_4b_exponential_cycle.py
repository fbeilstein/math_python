import tkinter as tk
from tkinter import ttk
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
import algebra_utils as utils
from levels.base_level import BaseLevelUI, poly_to_latex
import itertools

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

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        tk.Label(self.top_frame, text="Prime p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(self.top_frame, width=5)
        self.ent_p.insert(0, "2")
        self.ent_p.pack(side=tk.LEFT, padx=5)
        self.ent_p.bind("<KeyRelease>", lambda e: self.update_primitives())
        
        tk.Label(self.top_frame, text="Degree n:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_n = tk.Entry(self.top_frame, width=5)
        self.ent_n.insert(0, "3")
        self.ent_n.pack(side=tk.LEFT, padx=5)
        self.ent_n.bind("<KeyRelease>", lambda e: self.update_primitives())
        
        tk.Label(self.top_frame, text="Primitive Poly:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        
        self.poly_combo = ttk.Combobox(self.top_frame, state="readonly", width=15)
        self.poly_combo.pack(side=tk.LEFT, padx=5)
        self.poly_combo.bind("<<ComboboxSelected>>", lambda e: self.update_canvas())
        
        self.primitives_list = []
        
        tk.Button(self.top_frame, text="Generate Exponential Cycle", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_primitives()
        
    def update_primitives(self):
        try:
            p = int(self.ent_p.get())
            n = int(self.ent_n.get())
            
            if p < 2 or n < 1: return
            for i in range(2, int(p**0.5) + 1):
                if p % i == 0: return
                
            primitives = utils.find_primitives(p, n)
            
            self.primitives_list = primitives
            str_list = [poly_to_str(p[::-1]) for p in primitives]
            self.poly_combo['values'] = str_list
            if str_list:
                self.poly_combo.current(0)
            else:
                self.poly_combo.set('')
                
            self.update_canvas()
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
            
            text = f"GF(${p}^{{{n}}}$) Exponential Cycle\n"
            text += f"Modulo Primitive: {poly_to_latex(poly[::-1])}\n\n"
            
            for i in range(min(15, (p**n) - 1)):
                val = utils.ext_to_int(gf.exp(i))
                c = []
                if val == 0: c = [0]
                else:
                    while val > 0:
                        c.insert(0, val % p)
                        val //= p
                text += f"$\\alpha^{{{i}}} = $ {poly_to_latex(c)}\n"
            if (p**n) - 1 > 15:
                text += "\n..."
                
            self.ax.text(0.5, 0.5, text, fontsize=18, ha='center', va='center', color='white')
        except Exception as e:
            msg = str(e)
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            if "list index out of range" in msg: msg = "Polynomial cannot be empty!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')

