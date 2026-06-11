import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from levels.level_1_laplacian import Level1Laplacian
from levels.level_2_components import Level2Components
from levels.level_3_layout import Level3Layout
from levels.level_4_segmentation import Level4Segmentation

class LabDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Spectral Graph Theory Lab")
        self.root.geometry("1100x750")
        self.root.configure(bg="#2d2d30")
        
        self.menu_frame = tk.Frame(root, bg="#1e1e1e", width=250)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.menu_frame.pack_propagate(False)
        
        self.content_frame = tk.Frame(root, bg="#2d2d30")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.controls_frame = tk.Frame(self.content_frame, bg="#1e1e1e", width=250)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.controls_frame.pack_propagate(False)
        
        self.canvas_frame = tk.Frame(self.content_frame, bg="#2d2d30")
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.current_level = None
        
        self.setup_menu()
        
    def setup_menu(self):
        tk.Label(self.menu_frame, text="Laboratory Levels", bg="#1e1e1e", fg="white", font=("Arial", 14, "bold")).pack(pady=20)
        
        levels = [
            ("L1: Matrix Construction", Level1Laplacian),
            ("L2: Null Space", Level2Components),
            ("L3: Spectral Layout", Level3Layout),
            ("L4: Image Segmentation", Level4Segmentation)
        ]
        
        for name, cls in levels:
            btn = tk.Button(self.menu_frame, text=name, bg="#3d3d40", fg="white", 
                            relief=tk.FLAT, command=lambda c=cls: self.load_level(c))
            btn.pack(fill=tk.X, padx=10, pady=5)
            
        tk.Button(self.menu_frame, text="Reload Module", bg="#550000", fg="white", 
                  relief=tk.FLAT, command=self.reload_module).pack(fill=tk.X, padx=10, pady=20)
                  
    def reload_module(self):
        import importlib
        import implementation_tasks as tasks
        importlib.reload(tasks)
        if self.current_level:
            self.load_level(self.current_level.__class__)
            
    def load_level(self, level_class):
        if self.current_level:
            self.current_level.destroy()
            
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        self.current_level = level_class(self.controls_frame, self.canvas_frame)

if __name__ == "__main__":
    root = tk.Tk()
    
    def on_closing():
        if hasattr(app, 'current_level') and app.current_level:
            app.current_level.destroy()
        root.quit()
        root.destroy()
        sys.exit(0)
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = LabDashboard(root)
    root.mainloop()
