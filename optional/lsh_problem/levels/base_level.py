import tkinter as tk
import sys
import importlib
import hashlib

def make_hash_func(seed):
    def hash_func(shingle):
        h = hashlib.md5(f"{seed}_{shingle}".encode('utf8'))
        return int(h.hexdigest(), 16)
    return hash_func

class BaseView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.bg_color)
        self.app = app
        
    def get_tasks(self):
        if 'implementation_tasks' in sys.modules:
            importlib.reload(sys.modules['implementation_tasks'])
        import implementation_tasks as tasks
        return tasks
