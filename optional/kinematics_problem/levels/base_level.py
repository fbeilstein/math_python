import tkinter as tk

class BaseLevel:
    def __init__(self, controls_parent, canvas_parent):
        self.controls_parent = controls_parent
        self.canvas_parent = canvas_parent
        
        self.left_panel = tk.Frame(controls_parent, bg="#1e1e1e")
        self.left_panel.pack(fill=tk.BOTH, expand=True)
        
        self.right_panel = tk.Frame(canvas_parent, bg="#2d2d30")
        self.right_panel.pack(fill=tk.BOTH, expand=True)
        
    def destroy(self):
        self.left_panel.destroy()
        self.right_panel.destroy()
