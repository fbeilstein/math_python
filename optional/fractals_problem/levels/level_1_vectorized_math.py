import tkinter as tk
import numpy as np
from levels.base_level import BaseLevel
from implementation_tasks import VectorizedDual, VectorizedSplit

class Level1Math(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L1: Vectorized Math Debugger", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Z input
        row_z = tk.Frame(input_frame, bg="#1e1e1e")
        row_z.pack(fill=tk.X, pady=2)
        tk.Label(row_z, text="z = ", bg="#1e1e1e", fg="white", width=5).pack(side=tk.LEFT)
        self.entry_z_real = tk.Entry(row_z, width=5)
        self.entry_z_real.pack(side=tk.LEFT)
        self.entry_z_real.insert(0, "0.5")
        tk.Label(row_z, text=" + ", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_z_img = tk.Entry(row_z, width=5)
        self.entry_z_img.pack(side=tk.LEFT)
        self.entry_z_img.insert(0, "0.5")
        tk.Label(row_z, text="X", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        
        # C input
        row_c = tk.Frame(input_frame, bg="#1e1e1e")
        row_c.pack(fill=tk.X, pady=2)
        tk.Label(row_c, text="c = ", bg="#1e1e1e", fg="white", width=5).pack(side=tk.LEFT)
        self.entry_c_real = tk.Entry(row_c, width=5)
        self.entry_c_real.pack(side=tk.LEFT)
        self.entry_c_real.insert(0, "0.1")
        tk.Label(row_c, text=" + ", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_c_img = tk.Entry(row_c, width=5)
        self.entry_c_img.pack(side=tk.LEFT)
        self.entry_c_img.insert(0, "-0.2")
        tk.Label(row_c, text="X", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        
        # Formula
        tk.Label(input_frame, text="Formula:", bg="#1e1e1e", fg="white").pack(anchor=tk.W, pady=(10,0))
        self.entry_formula = tk.Entry(input_frame, width=25)
        self.entry_formula.pack(fill=tk.X, pady=2)
        self.entry_formula.insert(0, "z**2 + c")
        
        tk.Button(self.left_panel, text="Evaluate", bg="#007acc", fg="white", font=("Arial", 10, "bold"), command=self.calculate).pack(fill=tk.X, pady=10)
        
        self.output_text = tk.Text(self.right_panel, bg="#1e1e1e", fg="white", font=("Courier", 14), state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.calculate()
        
    def calculate(self):
        try:
            zr = float(self.entry_z_real.get())
            zi = float(self.entry_z_img.get())
            cr = float(self.entry_c_real.get())
            ci = float(self.entry_c_img.get())
            formula = self.entry_formula.get()
        except ValueError:
            return
            
        results = []
        
        # Evaluate Complex
        try:
            z_c = zr + 1j * zi
            c_c = cr + 1j * ci
            res_c = eval(formula, {"z": z_c, "c": c_c, "np": np})
            results.append(f"Complex (i²=-1):\nResult = {res_c.real:.4f} + {res_c.imag:.4f}i\n")
        except Exception as e:
            results.append(f"Complex (i²=-1):\nError: {e}\n")
            
        # Evaluate Dual
        try:
            z_d = VectorizedDual(zr, zi)
            c_d = VectorizedDual(cr, ci)
            res_d = eval(formula, {"z": z_d, "c": c_d, "np": np})
            results.append(f"Dual (ε²=0):\nResult = {float(res_d.real):.4f} + {float(res_d.dual):.4f}ε\n")
        except Exception as e:
            results.append(f"Dual (ε²=0):\nError: {e}\n")
            
        # Evaluate Split-Complex
        try:
            z_s = VectorizedSplit(zr, zi)
            c_s = VectorizedSplit(cr, ci)
            res_s = eval(formula, {"z": z_s, "c": c_s, "np": np})
            results.append(f"Split-Complex (j²=1):\nResult = {float(res_s.real):.4f} + {float(res_s.j):.4f}j\n")
        except Exception as e:
            results.append(f"Split-Complex (j²=1):\nError: {e}\n")
            
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "=== Vectorized Math Evaluation ===\n\n")
        self.output_text.insert(tk.END, "\n".join(results))
        self.output_text.config(state=tk.DISABLED)
