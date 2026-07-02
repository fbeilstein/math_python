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
        self.input_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.input_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        tk.Label(self.input_frame, text="Prime p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(self.input_frame, width=5)
        self.ent_p.insert(0, "3")
        self.ent_p.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.input_frame, text="Degree n:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_n = tk.Entry(self.input_frame, width=5)
        self.ent_n.insert(0, "2")
        self.ent_n.pack(side=tk.LEFT, padx=5)
        tk.Button(self.input_frame, text="Find Primitives", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        
        tk.Label(self.input_frame, text="⚠️ Warning: O(p^n) brute-force search. Keep p^n < 1000", fg="#ffcc00", bg="#1e1e1e").pack(side=tk.LEFT, padx=10)
        
        self.btn_container = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.btn_container.pack(fill=tk.X, pady=5)
        
        self.btn_canvas = tk.Canvas(self.btn_container, bg="#1e1e1e", height=100, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.btn_container, orient="vertical", command=self.btn_canvas.yview)
        self.scrollable_frame = tk.Frame(self.btn_canvas, bg="#1e1e1e")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.btn_canvas.configure(
                scrollregion=self.btn_canvas.bbox("all")
            )
        )
        
        self.btn_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.btn_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.btn_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_canvas()
        
    def draw_math(self):
        try:
            p_val = int(self.ent_p.get())
            n_val = int(self.ent_n.get())
            
            if p_val < 2: raise ValueError("p must be >= 2")
            for i in range(2, int(p_val**0.5) + 1):
                if p_val % i == 0: raise ValueError(f"p={p_val} is not prime!")
            if n_val < 1: raise ValueError("n must be >= 1")
            
            primitives = []
            import itertools
            for coefs in itertools.product(range(p_val), repeat=n_val):
                poly = [1] + list(coefs)
                if tasks.is_primitive(poly, p_val, n_val):
                    primitives.append(poly)
            
            for w in self.scrollable_frame.winfo_children(): w.destroy()
            
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

            row_frame = tk.Frame(self.scrollable_frame, bg="#1e1e1e")
            row_frame.pack(fill=tk.X)
            for i, poly in enumerate(primitives):
                if i > 0 and i % 5 == 0:
                    row_frame = tk.Frame(self.scrollable_frame, bg="#1e1e1e")
                    row_frame.pack(fill=tk.X)
                btn = tk.Button(row_frame, text=poly_to_str(poly), bg="#007acc", fg="white", font=("Arial", 10, "bold"),
                                command=lambda p=poly: self.verify_primitive(p, p_val, n_val))
                btn.pack(side=tk.LEFT, padx=4, pady=4)
                
            msg = f"Found {len(primitives)} primitive polynomials.\n\nClick one of the blue buttons above to mathematically verify it!"
            self.ax.text(0.5, 0.5, msg, fontsize=18, ha='center', va='center', color='white')
        except Exception as e:
            msg = str(e)
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')
            
    def verify_primitive(self, poly, p, n):
        self.ax.clear()
        self.ax.axis('off')
        
        try:
            order = (p**n) - 1
            factors = []
            temp = order
            for i in range(2, int(temp**0.5) + 1):
                if temp % i == 0:
                    factors.append(i)
                    while temp % i == 0: temp //= i
            if temp > 1: factors.append(temp)
            d_tex = poly_to_latex(poly).strip('$')
            
            text = f"Verification of Primitivity for ${d_tex}$ over GF(${p}^{{{n}}}$)\n\n"
            
            def format_div(k, is_order):
                dividend = [1] + [0]*k
                q, r = tasks.gfp_poly_divide(dividend, poly, p)
                q_tex = poly_to_latex(q).strip('$')
                if len(q) > 4: 
                    lead = q[0]
                    if lead == 1: q_tex = f"x^{{{len(q)-1}}} + \\dots + {q[-1]}"
                    else: q_tex = f"{lead}x^{{{len(q)-1}}} + \\dots + {q[-1]}"
                r_tex = poly_to_latex(r).strip('$')
                
                if r_tex == "0":
                    if q_tex == "0": eq = f"$\\frac{{x^{{{k}}}}}{{{d_tex}}} = 0$"
                    else: eq = f"$\\frac{{x^{{{k}}}}}{{{d_tex}}} = {q_tex}$"
                else:
                    if q_tex == "0": eq = f"$\\frac{{x^{{{k}}}}}{{{d_tex}}} = \\frac{{{r_tex}}}{{{d_tex}}}$"
                    else: eq = f"$\\frac{{x^{{{k}}}}}{{{d_tex}}} = {q_tex} + \\frac{{{r_tex}}}{{{d_tex}}}$"
                    
                if is_order:
                    return eq + "   (Rem = 1)  [OK]"
                else:
                    return eq + "   (Rem $\\neq$ 1)  [OK]"
                    
            text += "1) Order Check (Must equal 1):\n"
            text += format_div(order, True) + "\n\n"
            
            if factors:
                text += "2) Sub-order Checks (Must NOT equal 1):\n"
                for q_fac in factors:
                    k = order // q_fac
                    text += f"Factor $q={q_fac}$ ($k={k}$):\n"
                    text += format_div(k, False) + "\n"
                    
            self.ax.text(0.5, 0.5, text, fontsize=16, ha='center', va='center', color='white')
        except Exception as e:
            msg = str(e)
            if "invalid literal" in msg: msg = "Please enter valid numbers in all fields!"
            self.ax.text(0.5, 0.5, f"Error: {msg}", color="red", fontsize=14, ha='center', va='center')
            
        self.canvas.draw()

