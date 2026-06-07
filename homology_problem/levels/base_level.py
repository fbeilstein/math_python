import tkinter as tk

class BaseLevel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        self.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        super().destroy()
