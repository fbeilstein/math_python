import sys
import tkinter as tk
import matplotlib.pyplot as plt
from levels.level_1_vectorized_math import Level1Math
from levels.level_2_fractal_explorer import Level2Explorer
from levels.level_3_video_renderer import Level3Video

class LabDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab Dashboard: Hypercomplex Fractals")
        self.geometry("1400x800")
        self.configure(bg="#1e1e1e")
        
        # Top Navigation
        self.nav_frame = tk.Frame(self, bg="#2d2d30", height=50)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)
        self.nav_frame.pack_propagate(False)
        
        tk.Label(self.nav_frame, text="Select Level:", font=("Arial", 12, "bold"), bg="#2d2d30", fg="white").pack(side=tk.LEFT, padx=10, pady=10)
        
        self.level_var = tk.StringVar(value="L2: Fractal Explorer")
        levels = [
            "L1: Vectorized Math",
            "L2: Fractal Explorer",
            "L3: Dragon Video"
        ]
        
        for lvl in levels:
            tk.Radiobutton(self.nav_frame, text=lvl, variable=self.level_var, value=lvl, 
                           bg="#2d2d30", fg="white", selectcolor="#007acc", indicatoron=0, 
                           width=20, font=("Arial", 10, "bold"), command=self.load_level).pack(side=tk.LEFT, padx=5, pady=10)
                           
        # Main Content Area
        self.content_frame = tk.Frame(self, bg="#1e1e1e")
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.current_level = None
        self.load_level()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        plt.close('all')
        self.quit()
        self.destroy()
        sys.exit(0)
        
    def load_level(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        left = tk.Frame(self.content_frame, bg="#1e1e1e", width=300)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left.pack_propagate(False)
        
        right = tk.Frame(self.content_frame, bg="#2d2d30")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        lvl = self.level_var.get()
        if lvl == "L1: Vectorized Math":
            self.current_level = Level1Math(left, right)
        elif lvl == "L2: Fractal Explorer":
            self.current_level = Level2Explorer(left, right)
        elif lvl == "L3: Dragon Video":
            self.current_level = Level3Video(left, right)

if __name__ == "__main__":
    app = LabDashboard()
    app.mainloop()
