import tkinter as tk
from tkinter import messagebox
import unittest
import importlib
import sys
import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
levels_dir = os.path.join(base_dir, 'levels')
if levels_dir not in sys.path:
    sys.path.insert(0, levels_dir)

class RSADebugger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RSA Cryptography Debugger")
        self.geometry("1400x900")
        self.configure(bg="#1e1e1e")

        self.current_handler = None
        self.current_lvl_num = None
        
        self.setup_sidebar()
        self.setup_main_area()
        
        self.refresh_tests()
        self.switch_sandbox(1)

    def setup_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#252526", highlightbackground="#333333", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        tk.Label(self.sidebar, text="Implementation Tasks", font=("Arial", 12, "bold"), 
                 bg="#252526", fg="white").pack(pady=15, padx=20)
        
        self.tasks = {
            1: ("Miller-Rabin Primes", "level_1_primes", "Level1Primes"),
            2: ("Key Generation", "level_2_keys", "Level2Keys"),
            3: ("Fast Exponentiation", "level_3_encrypt", "Level3Encrypt")
        }
        
        self.status_indicators = {}
        for num, (name, mod, cls) in self.tasks.items():
            frame = tk.Frame(self.sidebar, bg="#252526")
            frame.pack(fill="x", pady=4, padx=10)
            
            ind = tk.Canvas(frame, width=15, height=15, highlightthickness=0, bg="#252526")
            ind.pack(side="left", padx=5)
            light = ind.create_oval(2, 2, 13, 13, fill="gray")
            self.status_indicators[num] = (ind, light)
            
            tk.Button(frame, text=f"L{num} {name}", width=25, font=("Arial", 9),
                       command=lambda n=num: self.switch_sandbox(n)).pack(side="left")

        tk.Button(self.sidebar, text="🔄 Reload & Retest", bg="#3e3e42", fg="white",
                  command=self.reload_and_retest).pack(pady=(30, 10), padx=20, fill="x")
                  
        tk.Button(self.sidebar, text="🚀 Secure Chat Demo", bg="#007acc", fg="white", 
                  font=("Arial", 10, "bold"), command=self.run_main_simulation).pack(pady=(0, 20), padx=20, fill="x")

    def setup_main_area(self):
        self.main_container = tk.Frame(self, bg="#1e1e1e")
        self.main_container.pack(side="right", fill="both", expand=True)

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

    def reload_and_retest(self):
        if not self.force_reload_core():
            return
            
        for num, (name, mod_name, class_name) in self.tasks.items():
            if mod_name in sys.modules:
                importlib.reload(sys.modules[mod_name])
        
        if self.current_lvl_num:
            self.switch_sandbox(self.current_lvl_num)
        
        self.refresh_tests()

    def switch_sandbox(self, level_num):
        if not self.force_reload_core():
            return

        for widget in self.main_container.winfo_children():
            widget.destroy()

        if self.current_handler is not None and hasattr(self.current_handler, 'destroy'):
            self.current_handler.destroy()

        try:
            name, mod_name, class_name = self.tasks[level_num]
            module = importlib.import_module(mod_name)
            importlib.reload(module) 
            
            level_class = getattr(module, class_name)
            self.current_handler = level_class(parent=self.main_container)
            
            self.current_lvl_num = level_num
            self.refresh_tests([(level_num, self.tasks[level_num])]) 
            
        except Exception as e:
            messagebox.showerror("Module Error", f"Failed to load Level {level_num}:\n{e}")

    def refresh_tests(self, test_list=None):
        if not test_list:
            test_list = self.tasks.items()
        loader = unittest.TestLoader()
        
        print('===================================================')
        print('                   RESTART TESTS')
        print('===================================================')
        
        for num, (name, mod_name, class_name) in test_list:
            try:
                module = importlib.import_module(mod_name)
                suite = loader.loadTestsFromModule(module)
                
                print(f"\n--- Running Tests for L{num}: {name} ---")
                result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
                
                canvas, light = self.status_indicators[num]
                color = "#4ec9b0" if (result.wasSuccessful() and result.testsRun > 0) else "#f44747"
                canvas.itemconfig(light, fill=color)
                
            except Exception as e:
                print(f"\n--- FATAL ERROR loading L{num}: {name} ---")
                print(f"Error details: {e}")
                
                canvas, light = self.status_indicators[num]
                canvas.itemconfig(light, fill="#f44747")

    def run_main_simulation(self):
        try:
            subprocess.Popen([sys.executable, "secure_chat.py"])
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to launch secure_chat.py:\n{e}")

if __name__ == "__main__":
    app = RSADebugger()
    app.mainloop()
