import tkinter as tk
from tkinter import ttk
import sys
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import implementation_tasks as tasks
from source_manager import SourceManager

class Level4Segmentation:
    def __init__(self, controls_parent, canvas_parent):
        self.controls_parent = controls_parent
        self.canvas_parent = canvas_parent
        
        self.left_panel = tk.Frame(controls_parent, bg="#1e1e1e")
        self.left_panel.pack(fill=tk.BOTH, expand=True)
        
        self.source = SourceManager()
        
        tk.Label(self.left_panel, text="L4: Image Segmentation", bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.left_panel, text="Input Source:", bg="#1e1e1e", fg="white").pack(anchor="w")
        self.source_var = tk.StringVar(value="grid")
        self.source_combo = ttk.Combobox(self.left_panel, textvariable=self.source_var, values=["grid", "camera", "image"], state="readonly")
        self.source_combo.pack(fill=tk.X, pady=5)
        self.source_combo.bind("<<ComboboxSelected>>", self.change_source)
        
        tk.Label(self.left_panel, text="Color Similarity (Sigma I):", bg="#1e1e1e", fg="white").pack(anchor="w", pady=(10,0))
        self.sigma_I_var = tk.DoubleVar(value=0.1)
        tk.Scale(self.left_panel, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, variable=self.sigma_I_var, bg="#1e1e1e", fg="white").pack(fill=tk.X)
        
        tk.Label(self.left_panel, text="Spatial Proximity (Sigma X):", bg="#1e1e1e", fg="white").pack(anchor="w", pady=(10,0))
        self.sigma_X_var = tk.DoubleVar(value=5.0)
        tk.Scale(self.left_panel, from_=1.0, to=20.0, resolution=0.5, orient=tk.HORIZONTAL, variable=self.sigma_X_var, bg="#1e1e1e", fg="white").pack(fill=tk.X)
        
        tk.Label(self.left_panel, text="Fiedler Threshold:", bg="#1e1e1e", fg="white").pack(anchor="w", pady=(10,0))
        self.thresh_var = tk.DoubleVar(value=0.0)
        tk.Scale(self.left_panel, from_=-0.1, to=0.1, resolution=0.001, orient=tk.HORIZONTAL, variable=self.thresh_var, bg="#1e1e1e", fg="white").pack(fill=tk.X)
        
        self.play_btn = tk.Button(self.left_panel, text="Play / Segment", command=self.toggle_play, bg="#2e5c2e", fg="white")
        self.play_btn.pack(fill=tk.X, pady=(20, 5))
        
        self.warning_label = tk.Label(self.left_panel, text="", bg="#1e1e1e", fg="red", wraplength=200, justify="left")
        self.warning_label.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        
        self.is_playing = False
        self.setup_graph_ui()
        self.update_frame()
        
    def setup_graph_ui(self):
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.fig.patch.set_facecolor('#2d2d30')
        
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.set_facecolor('#2d2d30')
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_edgecolor('white')
                
        self.ax1.set_title("Original Image", color='white')
        self.ax2.set_title("Fiedler Vector (Math)", color='white')
        self.ax3.set_title("Component A", color='white')
        self.ax4.set_title("Component B", color='white')
        
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_parent)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def change_source(self, event=None):
        mode = self.source_var.get()
        if mode == "image":
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
            if file_path:
                self.source.set_mode("image", file_path)
            else:
                self.source_var.set("grid")
                self.source.set_mode("grid")
        else:
            self.source.set_mode(mode)
            
        if not self.is_playing:
            self.update_frame()
            
    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_btn.config(text="Pause", bg="#8c2e2e")
            self.auto_step()
        else:
            self.play_btn.config(text="Play / Segment", bg="#2e5c2e")
            
    def auto_step(self):
        if self.is_playing:
            self.update_frame()
            self.controls_parent.after(50, self.auto_step)
            
    def update_frame(self):
        self.warning_label.config(text="")
        try:
            frame = self.source.get_frame()
            if frame is None: return
            
            # To run eigen decomposition interactively, we must heavily downsample
            # eigh on 1024x1024 takes ~0.1s. 32x32 image -> 1024 pixels.
            W, H = 32, 32
            small_frame = cv2.resize(frame, (W, H))
            
            pixels = small_frame.reshape(-1, 3).astype(float) / 255.0
            
            # Spatial coordinates
            x_coords, y_coords = np.meshgrid(np.arange(W), np.arange(H))
            positions = np.stack([x_coords.ravel(), y_coords.ravel()], axis=1).astype(float)
            
            # Vectorized pairwise distance calculation
            dist_I = np.sum((pixels[:, None, :] - pixels[None, :, :])**2, axis=2)
            dist_X = np.sum((positions[:, None, :] - positions[None, :, :])**2, axis=2)
            
            sI = self.sigma_I_var.get()
            sX = self.sigma_X_var.get()
            
            # Construct adjacency
            A = np.exp(-dist_I / (sI**2)) * np.exp(-dist_X / (sX**2))
            # Remove self loops
            np.fill_diagonal(A, 0)
            
            # Use student's code
            L = tasks.build_normalized_laplacian(A)
            fiedler = tasks.get_fiedler_vector(L)
            
            # Enforce deterministic sign convention to prevent component flipping
            if fiedler[0] < 0:
                fiedler = -fiedler
            
            # Reshape Fiedler vector to 2D heatmap
            heatmap_small = fiedler.reshape((H, W))
            
            # Upsample heatmap back to full camera resolution
            orig_H, orig_W = frame.shape[:2]
            heatmap = cv2.resize(heatmap_small, (orig_W, orig_H), interpolation=cv2.INTER_CUBIC)
            
            # Threshold to binary mask
            thresh = self.thresh_var.get()
            mask_A = (heatmap > thresh).astype(np.uint8)
            mask_B = (heatmap <= thresh).astype(np.uint8)
            
            # Create Component A (mask B is blacked out)
            comp_A = frame.copy()
            comp_A[mask_A == 0] = [0, 0, 0]
            
            # Create Component B (mask A is blacked out)
            comp_B = frame.copy()
            comp_B[mask_B == 0] = [0, 0, 0]
            
            self.ax1.clear()
            self.ax2.clear()
            self.ax3.clear()
            self.ax4.clear()
            
            self.ax1.set_title("Original", color='white')
            self.ax2.set_title("Fiedler Heatmap", color='white')
            self.ax3.set_title("Component A", color='white')
            self.ax4.set_title("Component B", color='white')
            
            # Convert BGR to RGB for matplotlib
            orig_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            comp_A_rgb = cv2.cvtColor(comp_A, cv2.COLOR_BGR2RGB)
            comp_B_rgb = cv2.cvtColor(comp_B, cv2.COLOR_BGR2RGB)
            
            self.ax1.imshow(orig_rgb)
            self.ax2.imshow(heatmap, cmap='RdBu')
            self.ax3.imshow(comp_A_rgb)
            self.ax4.imshow(comp_B_rgb)
            
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.set_xticks([])
                ax.set_yticks([])
            
            self.canvas.draw()
            
        except Exception as e:
            self.warning_label.config(text=f"Error: {e}")
            self.is_playing = False
            self.play_btn.config(text="Play / Segment", bg="#2e5c2e")
            
    def destroy(self):
        self.is_playing = False
        self.source.release()
        self.left_panel.destroy()
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
