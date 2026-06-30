import tkinter as tk
from levels.base_level import BaseLevel
from implementation_tasks import Dual

class Level1Arithmetic(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L1: Arithmetic", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(pady=2, fill=tk.X)
        
        tk.Label(input_frame, text="Dual X (a + bε):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        rowx = tk.Frame(input_frame, bg="#1e1e1e")
        rowx.pack(fill=tk.X, padx=2)
        self.entry_x_a = tk.Entry(rowx, font=("Courier", 10), width=6)
        self.entry_x_a.pack(side=tk.LEFT, padx=1)
        self.entry_x_a.insert(0, "3.0")
        tk.Label(rowx, text="+", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_x_b = tk.Entry(rowx, font=("Courier", 10), width=6)
        self.entry_x_b.pack(side=tk.LEFT, padx=1)
        self.entry_x_b.insert(0, "2.0")
        tk.Label(rowx, text="ε", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        
        tk.Label(input_frame, text="Dual Y (c + dε):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=(10, 1))
        rowy = tk.Frame(input_frame, bg="#1e1e1e")
        rowy.pack(fill=tk.X, padx=2)
        self.entry_y_c = tk.Entry(rowy, font=("Courier", 10), width=6)
        self.entry_y_c.pack(side=tk.LEFT, padx=1)
        self.entry_y_c.insert(0, "1.0")
        tk.Label(rowy, text="+", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_y_d = tk.Entry(rowy, font=("Courier", 10), width=6)
        self.entry_y_d.pack(side=tk.LEFT, padx=1)
        self.entry_y_d.insert(0, "4.0")
        tk.Label(rowy, text="ε", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        
        tk.Label(input_frame, text="Operation:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=(10,1))
        self.op_var = tk.StringVar(value="X * Y")
        for op in ["X + Y", "X - Y", "X * Y", "X / Y"]:
            tk.Radiobutton(input_frame, text=op, variable=self.op_var, value=op, bg="#1e1e1e", fg="white", selectcolor="#2d2d30").pack(anchor=tk.W, padx=10)
        
        tk.Button(self.left_panel, text="Calculate", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.calculate).pack(pady=10, fill=tk.X, padx=2)
        
        # Output Text
        tk.Label(self.right_panel, text="Arithmetic Breakdown", font=("Arial", 18, "bold"), bg="#2d2d30", fg="#007acc").pack(pady=(20,10))
        self.out_text = tk.Text(self.right_panel, font=("Courier", 14), bg="#1e1e1e", fg="#5ce65c")
        self.out_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.calculate()
        
    def calculate(self):
        try:
            a, b = float(self.entry_x_a.get()), float(self.entry_x_b.get())
            c, d = float(self.entry_y_c.get()), float(self.entry_y_d.get())
        except ValueError:
            return
            
        X = Dual(a, b)
        Y = Dual(c, d)
        op = self.op_var.get()
        
        out = f"X = {a} + {b}ε\n"
        out += f"Y = {c} + {d}ε\n"
        out += "-"*40 + "\n\n"
        
        try:
            if op == "X + Y":
                res = X + Y
                out += f"X + Y = ({a} + {c}) + ({b} + {d})ε\n"
            elif op == "X - Y":
                res = X - Y
                out += f"X - Y = ({a} - {c}) + ({b} - {d})ε\n"
            elif op == "X * Y":
                res = X * Y
                out += f"X * Y = ({a} + {b}ε)({c} + {d}ε)\n"
                out += f"      = ({a}*{c}) + ({a}*{d} + {b}*{c})ε + ({b}*{d})ε²\n"
                out += f"      = {a*c} + {a*d + b*c}ε + 0  (since ε²=0)\n"
            elif op == "X / Y":
                res = X / Y
                out += f"X / Y = ({a} + {b}ε) / ({c} + {d}ε)\n"
                out += f"Multiply top and bottom by conjugate ({c} - {d}ε):\n"
                out += f"      = ({a} + {b}ε)({c} - {d}ε) / c²\n"
                out += f"      = ({a*c}) + ({b*c} - {a*d})ε / {c*c}\n"
                
            out += "-"*40 + "\n\n"
            out += f"Result: {res.real} + {res.dual}ε\n"
        except Exception as e:
            out += f"Error: {str(e)}"
            
        self.out_text.delete("1.0", tk.END)
        self.out_text.insert(tk.END, out)
