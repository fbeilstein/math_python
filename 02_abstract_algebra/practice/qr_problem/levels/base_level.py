import sys
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def poly_to_latex(poly):
    """
    Convert a polynomial list [c_k, ..., c_1, c_0] to a LaTeX string.
    """
    if not poly or all(c == 0 for c in poly):
        return "$0$"
    
    terms = []
    deg = len(poly) - 1
    for i, c in enumerate(poly):
        if c == 0:
            continue
        power = deg - i
        term = ""
        
        # Format the coefficient
        if c != 1 or power == 0:
            term += str(c)
            
        # Format the variable
        if power > 0:
            term += "x"
            if power > 1:
                term += f"^{{{power}}}"
                
        terms.append(term)
        
    return "$" + " + ".join(terms) + "$"

class BaseLevelUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        
        # Subclasses can use self.top_frame for inputs
        self.top_frame = tk.Frame(self, bg="#1e1e1e")
        self.top_frame.pack(fill=tk.X, pady=10)
        
        # And self.canvas_frame for matplotlib
        self.canvas_frame = tk.Frame(self, bg="#1e1e1e")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1e1e1e')
        self.ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.setup_inputs()
        
    def setup_inputs(self):
        pass
        
    def update_canvas(self):
        self.ax.clear()
        self.ax.axis('off')
        self.draw_math()
        self.canvas.draw()
        
    def draw_math(self):
        pass


