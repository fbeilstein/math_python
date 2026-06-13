import tkinter as tk
from tkinter import messagebox
import unittest
import importlib
import sys
import os
import subprocess
import io
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ensure directories are in path for robust importing
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
levels_dir = os.path.join(base_dir, 'levels')
if levels_dir not in sys.path:
    sys.path.insert(0, levels_dir)

class QuantumDebugger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quantum Wave Packet Dashboard")
        self.geometry("1100x750")
        self.configure(bg="#1e1e1e")

        self.current_handler = None
        self.current_lvl_num = None

        self.setup_sidebar()
        self.setup_main_area()
        self.refresh_tests()

    def setup_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#252526", highlightbackground="#333333", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        tk.Label(self.sidebar, text="Wave Packet Tasks", font=("Arial", 12, "bold"), 
                 bg="#252526", fg="white").pack(pady=15, padx=20)
        
        self.tasks = {
            1: ("Gaussian Packet", "level_1_gaussian", "Level1Gaussian", "levels/level_1_gaussian.py"),
            2: ("Momentum Space", "level_2_momentum_space", "Level2MomentumSpace", "levels/level_2_momentum_space.py"),
            3: ("Free Particle", "level_3_free_particle", "Level3FreeParticle", "levels/level_3_free_particle.py"),
            4: ("Eigenfunctions", "level_4_eigenfunctions", "Level4Eigenfunctions", "levels/level_4_eigenfunctions.py"),
            5: ("Split-Operator", "level_5_split_operator", "Level5SplitOperator", "levels/level_5_split_operator.py"),
            6: ("Infinite Well", "level_6_infinite_well", "Level6InfiniteWell", "levels/level_6_infinite_well.py"),
            7: ("Absorbing Mask", "level_7_absorber", "Level7Absorber", "levels/level_7_absorber.py")
        }
        
        self.status_indicators = {}
        for num, (name, mod, cls, path) in self.tasks.items():
            frame = tk.Frame(self.sidebar, bg="#252526")
            frame.pack(fill="x", pady=4, padx=10)
            
            ind = tk.Canvas(frame, width=15, height=15, highlightthickness=0, bg="#252526")
            ind.pack(side="left", padx=5)
            light = ind.create_oval(2, 2, 13, 13, fill="gray")
            self.status_indicators[num] = (ind, light)
            
            tk.Button(frame, text=f"L{num} {name}", width=20, font=("Arial", 9),
                       command=lambda n=num: self.switch_sandbox(n)).pack(side="left")

        # Utility Buttons
        tk.Button(self.sidebar, text="🔄 Reload & Retest", bg="#3e3e42", fg="white",
                  command=self.reload_and_retest).pack(pady=(30, 10), padx=20, fill="x")
                  
        tk.Button(self.sidebar, text="🚀 Run Wave Explorer", bg="#007acc", fg="white", 
                  font=("Arial", 10, "bold"), command=self.run_main_simulation).pack(pady=(0, 20), padx=20, fill="x")

        # Test output area appended inside the sidebar
        self.log_area = tk.Text(self.sidebar, bg="#2d2d30", fg="#d4d4d4", font=("Consolas", 9),
                                state=tk.DISABLED, wrap="word", padx=5, pady=5, height=20, width=35)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)


    def setup_main_area(self):
        self.main_container = tk.Frame(self, bg="#1e1e1e")
        self.main_container.pack(side="right", fill="both", expand=True)

        self.fig = Figure(figsize=(8, 7), facecolor="#1e1e1e")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def log(self, text, color="#d4d4d4"):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.config(state=tk.DISABLED)
        self.log_area.see(tk.END)

    def clear_log(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)

    def force_reload_core(self):
        try:
            if 'implementation_tasks' in sys.modules:
                importlib.reload(sys.modules['implementation_tasks'])
            else:
                import implementation_tasks
            return True
        except Exception as e:
            self.log(f"CRITICAL ERROR:\n{str(e)}", color="#f44747")
            return False

    def reload_and_retest(self):
        if not self.force_reload_core():
            return
            
        for num, (name, mod_name, class_name, _) in self.tasks.items():
            if mod_name in sys.modules:
                importlib.reload(sys.modules[mod_name])
        
        if self.current_lvl_num:
            self.switch_sandbox(self.current_lvl_num)
        
        self.refresh_tests()

    def switch_sandbox(self, level_num):
        if not self.force_reload_core():
            return

        # Stop previous animations to avoid ghost loops
        if self.current_handler is not None:
            if hasattr(self.current_handler, 'anim') and self.current_handler.anim:
                try:
                    self.current_handler.anim.event_source.stop()
                except Exception:
                    pass
            # disconnect events if applicable
            if hasattr(self.current_handler, 'disconnect_events'):
                self.current_handler.disconnect_events()

        try:
            name, mod_name, class_name, _ = self.tasks[level_num]
            module = importlib.import_module(mod_name)
            importlib.reload(module) 
            level_class = getattr(module, class_name)
            
            # Reattach the pyplot backend to tkinter figure using magic
            plt.close('all')
            self.fig.clear()
            plt.figure = lambda *args, **kwargs: self.fig
            
            self.current_handler = level_class()
            self.canvas.draw()
            self.current_lvl_num = level_num
            self.refresh_tests([(level_num, self.tasks[level_num])]) 
            
        except Exception as e:
            messagebox.showerror("Module Error", f"Failed to load Level {level_num}:\n{e}")

    def refresh_tests(self, test_list=None):
        if not test_list:
            self.clear_log()
            test_list = self.tasks.items()
        
        if not self.force_reload_core():
            for num in self.tasks:
                canvas, light = self.status_indicators[num]
                canvas.itemconfig(light, fill="#f44747")
            return

        loader = unittest.TestLoader()

        for num, task in test_list:
            if len(task) == 4:
                name, mod_name, class_name, _ = task
            else:
                name, mod_name, class_name = task[0], task[1], task[2]
                
            if mod_name in sys.modules:
                importlib.reload(sys.modules[mod_name])
                
            try:
                module = importlib.import_module(mod_name)
                suite = loader.loadTestsFromModule(module)
                
                # Capture unittest output
                stream = io.StringIO()
                runner = unittest.TextTestRunner(stream=stream, verbosity=1)
                result = runner.run(suite)
                
                output = stream.getvalue()
                if not 'OK' in output:
                    self.log(f"L{num}: {name} -- FAILED")
                
                canvas, light = self.status_indicators[num]
                if result.wasSuccessful() and result.testsRun > 0:
                    canvas.itemconfig(light, fill="#4ec9b0")
                else:
                    canvas.itemconfig(light, fill="#f44747")
                    
            except Exception as e:
                self.log(f"FATAL ERROR L{num}: {str(e)}")
                canvas, light = self.status_indicators[num]
                canvas.itemconfig(light, fill="#f44747")

    def run_main_simulation(self):
        """Launches the main wave_explorer.py script."""
        try:
            subprocess.Popen([sys.executable, "wave_explorer.py", "--mode", "scattering"], cwd=base_dir)
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to launch wave_explorer.py:\n{e}")

if __name__ == "__main__":
    app = QuantumDebugger()
    app.mainloop()
