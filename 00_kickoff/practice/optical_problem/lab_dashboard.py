import tkinter as tk
from tkinter import messagebox

import importlib
import sys
import os
import subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ensure directories are in path for robust importing
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
levels_dir = os.path.join(base_dir, 'levels')
if levels_dir not in sys.path:
    sys.path.insert(0, levels_dir)

class OpticsDebugger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optics Engine Debugger Pro")
        self.geometry("1150x850")
        self.configure(bg="#1e1e1e")

        self.current_handler = None
        self.current_lvl_num = None
        
        self.setup_sidebar()
        self.setup_main_area()
        
        # Start with Level 1
        self.switch_sandbox(1)
        

    def setup_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#252526", highlightbackground="#333333", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        tk.Label(self.sidebar, text="Implementation Tasks", font=("Arial", 12, "bold"), 
                 bg="#252526", fg="white").pack(pady=15, padx=20)
        
        self.tasks = {
            1: ("Infinite Line", "level_1_line", "Level1Line"),
            2: ("Segment Bounds", "level_2_segment", "Level2Segment"),
            3: ("Circle Math", "level_3_circle", "Level3Circle"),
            4: ("Arc Sector", "level_4_arc", "Level4Arc"),
            5: ("Line Normals", "level_5_segment_normal", "Level5SegmentNormal"),
            6: ("Arc Normals", "level_6_arc_normal", "Level6ArcNormal"),
            7: ("Refraction", "level_7_refraction", "Level7Refraction")
        }
        
        for num, (name, mod, cls) in self.tasks.items():
            frame = tk.Frame(self.sidebar, bg="#252526")
            frame.pack(fill="x", pady=4, padx=10)
            
            tk.Button(frame, text=f"L{num} {name}", width=20, font=("Arial", 9),
                       command=lambda n=num: self.switch_sandbox(n)).pack(side="left")

        # Utility Buttons (Wired to the new aggressive reload)
        tk.Button(self.sidebar, text="🔄 Reload Code", bg="#3e3e42", fg="white",
                  command=self.reload_code).pack(pady=(30, 10), padx=20, fill="x")
                  
        tk.Button(self.sidebar, text="🚀 Run Main Simulation", bg="#007acc", fg="white", 
                  font=("Arial", 10, "bold"), command=self.run_main_simulation).pack(pady=(0, 20), padx=20, fill="x")

    def setup_main_area(self):
        self.main_container = tk.Frame(self, bg="#1e1e1e")
        self.main_container.pack(side="right", fill="both", expand=True)

        self.fig = Figure(figsize=(7, 7), facecolor="#252526")
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def force_reload_core(self):
        try:
            if 'implementation_tasks' in sys.modules:
                importlib.reload(sys.modules['implementation_tasks'])
            else:
                import implementation_tasks
            return True
        except Exception as e:
            messagebox.showerror("Compilation Error", f"Your implementation_tasks.py has an error:\n\n{e}")
            return False

    def reload_code(self):
        # 1. Stop and alert if the core tasks file is broken
        if not self.force_reload_core():
            return
            
        # 2. Force reload all level modules so tests update
        for num, (name, mod_name, class_name) in self.tasks.items():
            if mod_name in sys.modules:
                importlib.reload(sys.modules[mod_name])
        
        # 3. Re-instantiate the sandbox to trigger a clean draw
        if self.current_lvl_num:
            self.switch_sandbox(self.current_lvl_num)

    def switch_sandbox(self, level_num):
        if not self.force_reload_core():
            return

        if self.current_handler is not None:
            self.current_handler.disconnect_events()

        try:
            name, mod_name, class_name = self.tasks[level_num]
            module = importlib.import_module(mod_name)
            importlib.reload(module) 
            
            level_class = getattr(module, class_name)
            
            self.ax.clear()
            self.current_handler = level_class(ax=self.ax)
            self.current_handler.draw()
            self.canvas.draw()
            
            self.current_lvl_num = level_num 
            
        except Exception as e:
            messagebox.showerror("Module Error", f"Failed to load Level {level_num}:\n{e}")


                

    def run_main_simulation(self):
        """Launches the main optic_bench.py script as an independent process."""
        try:
            subprocess.Popen([sys.executable, "optic_bench.py"])
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to launch optic_bench.py:\n{e}")

if __name__ == "__main__":
    app = OpticsDebugger()
    app.mainloop()
