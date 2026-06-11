import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class BaseLevel:
    def __init__(self, controls_parent, canvas_parent):
        self.controls_parent = controls_parent
        self.canvas_parent = canvas_parent
        
        self.left_panel = tk.Frame(controls_parent, bg="#1e1e1e")
        self.left_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.right_panel = tk.Frame(canvas_parent, bg="#2d2d30")
        self.right_panel.pack(fill=tk.BOTH, expand=True)
        
    def destroy(self):
        self.left_panel.destroy()
        self.right_panel.destroy()
        
    def setup_graph_ui(self, figsize=(6, 4)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.fig.patch.set_facecolor('#2d2d30')
        self.ax.set_facecolor('#2d2d30')
        
        # Default styling for axes
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.right_panel)
        self.toolbar.update()
        
    def add_warning(self):
        warning_frame = tk.Frame(self.left_panel, bg="#4a0000", bd=2, relief=tk.RAISED)
        warning_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(warning_frame, text="⚠️ EXCEPTION", font=("Arial", 10, "bold"), bg="#4a0000", fg="white").pack(pady=(2,0))
        self.warning_label = tk.Label(warning_frame, text="", font=("Arial", 8), bg="#4a0000", fg="#ffcccc", wraplength=200)
        self.warning_label.pack(pady=(0,2))
        warning_frame.pack_forget()
        self.warning_frame = warning_frame

    def show_warning(self, msg):
        self.warning_label.config(text=msg)
        self.warning_frame.pack(fill=tk.X, pady=5)
        
    def hide_warning(self):
        self.warning_frame.pack_forget()
        
    def build_matrix_ui(self, parent_frame, T_def="5", R_def="3", P_def="1", S_def="0"):
        tk.Label(parent_frame, text="Payoff Matrix (Points Earned)", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,2))
        tk.Label(parent_frame, text="( Player 1 pts, Player 2 pts )", bg="#1e1e1e", fg="#aaaaaa", font=("Arial", 9)).grid(row=1, column=0, columnspan=3, pady=(0,10))
        
        tk.Label(parent_frame, text="P1 \\ P2", bg="#1e1e1e", fg="gray").grid(row=2, column=0)
        tk.Label(parent_frame, text="Coop.", bg="#1e1e1e", fg="white").grid(row=2, column=1)
        tk.Label(parent_frame, text="Def.", bg="#1e1e1e", fg="white").grid(row=2, column=2)
        
        # Row C
        tk.Label(parent_frame, text="Coop.", bg="#1e1e1e", fg="white").grid(row=3, column=0)
        fR = tk.Frame(parent_frame, bg="#1e1e1e")
        fR.grid(row=3, column=1, padx=2, pady=2)
        tk.Label(fR, text="( ", bg="#1e1e1e", fg="#aaaaaa").pack(side=tk.LEFT)
        self.entry_R = tk.Entry(fR, width=4)
        self.entry_R.insert(0, R_def)
        self.entry_R.pack(side=tk.LEFT)
        self.lbl_R2 = tk.Label(fR, text=f", {R_def} )", bg="#1e1e1e", fg="#aaaaaa")
        self.lbl_R2.pack(side=tk.LEFT)
        
        fS = tk.Frame(parent_frame, bg="#1e1e1e")
        fS.grid(row=3, column=2, padx=2, pady=2)
        tk.Label(fS, text="( ", bg="#1e1e1e", fg="#aaaaaa").pack(side=tk.LEFT)
        self.entry_S = tk.Entry(fS, width=4)
        self.entry_S.insert(0, S_def)
        self.entry_S.pack(side=tk.LEFT)
        self.lbl_T2 = tk.Label(fS, text=f", {T_def} )", bg="#1e1e1e", fg="#aaaaaa")
        self.lbl_T2.pack(side=tk.LEFT)
        
        # Row D
        tk.Label(parent_frame, text="Def.", bg="#1e1e1e", fg="white").grid(row=4, column=0)
        fT = tk.Frame(parent_frame, bg="#1e1e1e")
        fT.grid(row=4, column=1, padx=2, pady=2)
        tk.Label(fT, text="( ", bg="#1e1e1e", fg="#aaaaaa").pack(side=tk.LEFT)
        self.entry_T = tk.Entry(fT, width=4)
        self.entry_T.insert(0, T_def)
        self.entry_T.pack(side=tk.LEFT)
        self.lbl_S2 = tk.Label(fT, text=f", {S_def} )", bg="#1e1e1e", fg="#aaaaaa")
        self.lbl_S2.pack(side=tk.LEFT)
        
        fP = tk.Frame(parent_frame, bg="#1e1e1e")
        fP.grid(row=4, column=2, padx=2, pady=2)
        tk.Label(fP, text="( ", bg="#1e1e1e", fg="#aaaaaa").pack(side=tk.LEFT)
        self.entry_P = tk.Entry(fP, width=4)
        self.entry_P.insert(0, P_def)
        self.entry_P.pack(side=tk.LEFT)
        self.lbl_P2 = tk.Label(fP, text=f", {P_def} )", bg="#1e1e1e", fg="#aaaaaa")
        self.lbl_P2.pack(side=tk.LEFT)

        def update_labels(*args):
            self.lbl_R2.config(text=f", {self.entry_R.get()} )")
            self.lbl_T2.config(text=f", {self.entry_T.get()} )")
            self.lbl_S2.config(text=f", {self.entry_S.get()} )")
            self.lbl_P2.config(text=f", {self.entry_P.get()} )")
            
        self.entry_R.bind("<KeyRelease>", update_labels)
        self.entry_T.bind("<KeyRelease>", update_labels)
        self.entry_S.bind("<KeyRelease>", update_labels)
        self.entry_P.bind("<KeyRelease>", update_labels)
