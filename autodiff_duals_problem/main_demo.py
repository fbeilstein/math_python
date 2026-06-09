import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# Ensure we can import math_engine and BaseLevel
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from levels.base_level import BaseLevel
from implementation_tasks import Dual, sin, cos, tan, exp, log

class MainDemo(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L4: The AutoDiff Engine", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=200).pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="Define 'def f(x):' (Python code):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2)
        
        self.text_code = tk.Text(input_frame, font=("Courier", 10), height=12, width=25)
        self.text_code.pack(fill=tk.X, pady=2, padx=2)
        default_code = """def f(x):
    res = x
    for _ in range(3):
        res = sin(res) * 2.0
    return res"""
        self.text_code.insert("1.0", default_code)
        
        row_x = tk.Frame(input_frame, bg="#1e1e1e")
        row_x.pack(fill=tk.X, pady=5)
        
        tk.Label(row_x, text="x min:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=2)
        self.entry_xmin = tk.Entry(row_x, font=("Courier", 10), width=5)
        self.entry_xmin.pack(side=tk.LEFT, padx=2)
        self.entry_xmin.insert(0, "-3")
        
        tk.Label(row_x, text="x max:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=2)
        self.entry_xmax = tk.Entry(row_x, font=("Courier", 10), width=5)
        self.entry_xmax.pack(side=tk.LEFT, padx=2)
        self.entry_xmax.insert(0, "3")
        
        tk.Button(self.left_panel, text="Compile & Plot", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.calculate).pack(fill=tk.X, pady=10, padx=2)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.calculate()

    def calculate(self):
        code_str = self.text_code.get("1.0", tk.END).strip()
        try:
            xmin = float(self.entry_xmin.get())
            xmax = float(self.entry_xmax.get())
        except ValueError:
            return
            
        # Create execution environment with math functions
        safe_dict = {
            'sin': sin,
            'cos': cos,
            'tan': tan,
            'exp': exp,
            'log': log,
            'Dual': Dual
        }
        
        try:
            # Execute the user's code to define f(x)
            exec(code_str, safe_dict)
            if 'f' not in safe_dict:
                print("Error: Code must define a function named 'f'")
                return
            user_func = safe_dict['f']
        except Exception as e:
            print("Compile error:", e)
            return

        x_vals = np.linspace(xmin, xmax, 400)
        y_vals = []
        dy_vals = []
        
        for xv in x_vals:
            d_x = Dual(xv, 1.0)
            try:
                res = user_func(d_x)
                if isinstance(res, Dual):
                    y_vals.append(res.real)
                    dy_vals.append(res.dual)
                else:
                    y_vals.append(float(res))
                    dy_vals.append(0.0)
            except Exception as e:
                print("Evaluation error:", e)
                return
                
        self.ax.clear()
        self.ax.plot(x_vals, y_vals, label="f(x)", color="blue", linewidth=2)
        self.ax.plot(x_vals, dy_vals, label="f'(x) [AutoDiff]", color="red", linestyle="--", linewidth=2)
        
        self.ax.set_title("Automatic Differentiation via Dual Numbers")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = tk.Tk()
    app.title("AutoDiff Main Demo (Standalone)")
    app.geometry("1000x600")
    app.configure(bg="#1e1e1e")
    
    left = tk.Frame(app, bg="#1e1e1e", width=250)
    left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    left.pack_propagate(False)
    
    right = tk.Frame(app, bg="#2d2d30")
    right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    demo = MainDemo(left, right)
    
    app.mainloop()
