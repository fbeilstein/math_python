import tkinter as tk
from tkinter import ttk, messagebox
import sys
import importlib

try:
    from sklearn.datasets import fetch_20newsgroups
except ImportError:
    messagebox.showerror("Dependency Error", "Please install scikit-learn: pip install scikit-learn")
    sys.exit(1)

from levels.level_4_minhash import Level4MinHash
from levels.level_5_bloom_sim import Level5BloomSim
from levels.level_6_bloom_curve import Level6BloomCurve
from levels.level_7_doc_matcher import Level7DocMatcher
from levels.level_8_lsh_curve import Level8LSHCurve

class LSHDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Probabilistic Document Similarity Dashboard")
        self.geometry("1200x800")
        
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"
        self.accent_color = "#007acc"
        self.list_bg = "#252526"
        self.text_bg = "#1e1e1e"
        self.configure(bg=self.bg_color)
        
        self.docs = []
        
        self.tasks = {
            4: ("MinHash Sandbox", Level4MinHash),
            5: ("Bloom Simulator", Level5BloomSim),
            6: ("Bloom Probability", Level6BloomCurve),
            7: ("Document Matcher", Level7DocMatcher),
            8: ("LSH Probability", Level8LSHCurve)
        }
        
        self.setup_ui()
        self.after(100, self.load_data)

    def setup_ui(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.bg_color, bd=0, sashwidth=4)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.sidebar = tk.Frame(self.paned_window, bg=self.list_bg, width=250, bd=1, relief=tk.SUNKEN)
        self.paned_window.add(self.sidebar, minsize=200)
        
        tk.Label(self.sidebar, text="Subproblems", bg=self.list_bg, fg=self.fg_color, font=("Arial", 12, "bold")).pack(pady=10)
        
        self.buttons = {}
        for num, (name, cls) in self.tasks.items():
            btn = tk.Button(self.sidebar, text=f"L{num}: {name}", bg=self.text_bg, fg=self.fg_color, 
                            font=("Arial", 10), anchor="w", padx=10, pady=5,
                            command=lambda n=num: self.switch_view(n))
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.buttons[num] = btn
            
        # Standard Reload button
        btn_reload = tk.Button(self.sidebar, text="🔄 Reload Code", bg=self.accent_color, fg="white", 
                               font=("Arial", 10, "bold"), anchor="center", padx=10, pady=5,
                               command=self.reload_code)
        btn_reload.pack(fill=tk.X, padx=5, pady=20)
            
        self.status_lbl = tk.Label(self.sidebar, text="Waiting...", bg=self.list_bg, fg="#cca700", font=("Arial", 9))
        self.status_lbl.pack(side=tk.BOTTOM, pady=10)
        
        self.main_area = tk.Frame(self.paned_window, bg=self.bg_color)
        self.paned_window.add(self.main_area)
        
        self.current_view_num = 4
        self.current_view = None
        self.switch_view(4)

    def reload_code(self):
        if 'implementation_tasks' in sys.modules:
            importlib.reload(sys.modules['implementation_tasks'])
        # Re-render the current view
        self.switch_view(self.current_view_num)

    def switch_view(self, num):
        if self.current_view is not None:
            self.current_view.destroy()
            
        for n, btn in self.buttons.items():
            btn.config(bg=self.text_bg, fg=self.fg_color)
        self.buttons[num].config(bg=self.accent_color, fg="white")
        
        self.current_view_num = num
        _, view_cls = self.tasks[num]
        self.current_view = view_cls(self.main_area, self)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        self.status_lbl.config(text="Downloading 20newsgroups...", fg="#cca700")
        self.update()
        try:
            newsgroups = fetch_20newsgroups(subset='train', categories=['sci.space'], remove=('headers', 'footers', 'quotes'))
            self.docs = newsgroups.data[:300]
            self.status_lbl.config(text=f"Loaded {len(self.docs)} docs", fg="#4ec9b0")
        except Exception as e:
            self.status_lbl.config(text="Error loading data", fg="#f44747")
            messagebox.showerror("Data Error", str(e))

if __name__ == "__main__":
    app = LSHDashboard()
    app.mainloop()
