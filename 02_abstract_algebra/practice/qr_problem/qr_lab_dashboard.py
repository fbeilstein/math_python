import tkinter as tk
import subprocess
import sys
import os
import importlib

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

class QRDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unified QR Code Algebra Lab")
        self.geometry("1400x900")
        self.configure(bg="#1e1e1e")
        
        self.levels_dir = os.path.join(base_dir, "levels")
        
        self.levels = [
            ("level_1_gfp_math", "L1: GF(p) Math"),
            ("level_2_primitive", "L2: Primitive Search"),
            ("level_3_tables", "L3: GF(p^n) Tables"),
            ("level_4_gfpn_math", "L4: GF(p^n) Math"),
            ("level_5_rs_encoding", "L5: RS Encoding"),
            ("level_6_linear_decoding", "L6: Linear Decoding (PGZ)")
        ]
        self.current_frame = None
        
        self.build_ui()
        self.launch_level("level_1_gfp_math")

    def build_ui(self):
        self.sidebar = tk.Frame(self, width=250, bg="#2d2d30")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(self.sidebar, text="Levels", fg="white", bg="#2d2d30", font=("Arial", 16, "bold")).pack(pady=10)
        
        for module_name, label_text in self.levels:
            row = tk.Frame(self.sidebar, bg="#2d2d30")
            row.pack(fill=tk.X, pady=2, padx=10)            
            btn = tk.Button(row, text=label_text, bg="#3e3e42", fg="white", width=20,
                            command=lambda m=module_name: self.launch_level(m))
            btn.pack(side=tk.LEFT, padx=5)
                  
        tk.Frame(self.sidebar, height=2, bg="gray").pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(self.sidebar, text="⭐ MAIN DEMO ⭐", font=("Arial", 12, "bold"), bg="#28a745", fg="white",
                  command=lambda: self.launch_level("main_demo")).pack(pady=5, fill=tk.X, padx=10)
                  
        self.main_area = tk.Frame(self, bg="#1e1e1e")
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    def launch_level(self, module_name):
        if self.current_frame:
            self.current_frame.destroy()
            
        try:
            mod = importlib.import_module(f"levels.{module_name}")
            importlib.reload(mod)
            
            # Each module must define a LevelUI class inheriting from BaseLevelUI
            ui_class = getattr(mod, "LevelUI")
            self.current_frame = ui_class(self.main_area)
            self.current_frame.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            err_lbl = tk.Label(self.main_area, text=f"Error loading {module_name}:\n{e}", fg="red", bg="#1e1e1e", font=("Arial", 14))
            err_lbl.pack(pady=50)
            self.current_frame = err_lbl

if __name__ == "__main__":
    app = QRDashboard()
    app.mainloop()
