import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import importlib

# Ensure implementation_tasks can be imported
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import implementation_tasks as tasks
import run_evaluation as eval_script

class WassersteinDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TDA Wasserstein Classifier Explorer")
        self.geometry("1400x800")
        self.configure(bg="#1e1e1e")

        self.setup_ui()
        self.base_shape = "circle"
        
        # Proper termination protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initial draw
        self.update_plots()

    def on_closing(self):
        self.quit()
        self.destroy()
        import sys
        sys.exit(0)

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg="#252526", width=250)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Shape Explorer", font=("Arial", 14, "bold"), 
                 bg="#252526", fg="white").pack(pady=20)
                 
        tk.Label(self.sidebar, text="Select Base Shape:", bg="#252526", fg="white").pack(pady=(10, 5))
        self.shape_var = tk.StringVar(value="circle")
        
        shapes = [("Circle", "circle"), ("Figure 8", "figure8"), ("Cluster", "cluster")]
        for text, val in shapes:
            tk.Radiobutton(self.sidebar, text=text, variable=self.shape_var, value=val, 
                           bg="#252526", fg="white", selectcolor="#3e3e42",
                           command=self.update_plots).pack(anchor="w", padx=20)

        tk.Label(self.sidebar, text="Noise Level:", bg="#252526", fg="white").pack(pady=(20, 5))
        self.noise_slider = tk.Scale(self.sidebar, from_=0.0, to=0.5, resolution=0.01, 
                                     orient="horizontal", bg="#252526", fg="white", 
                                     highlightthickness=0, command=lambda x: self.update_plots())
        self.noise_slider.set(0.15)
        self.noise_slider.pack(padx=20, fill="x")

        tk.Button(self.sidebar, text="Run ML Evaluation", bg="#007acc", fg="white", 
                  font=("Arial", 10, "bold"), command=self.run_ml).pack(pady=(40, 10), padx=20, fill="x")
                  
        self.progress = ttk.Progressbar(self.sidebar, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10, padx=20, fill="x")

        # Main Area
        self.main_area = tk.Frame(self, bg="#1e1e1e")
        self.main_area.pack(side="right", fill="both", expand=True)
        
        self.fig, self.axs = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.patch.set_facecolor('#1e1e1e')
        for ax in self.axs:
            ax.set_facecolor('#1e1e1e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_edgecolor('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_area)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    def generate_data(self, shape, noise):
        if shape == "circle":
            clean = eval_script.generate_circle(noise=0.0)
            noisy = eval_script.generate_circle(noise=noise)
        elif shape == "figure8":
            clean = eval_script.generate_figure8(noise=0.0)
            noisy = eval_script.generate_figure8(noise=noise)
        else:
            clean = eval_script.generate_cluster(noise=0.0)
            noisy = eval_script.generate_cluster(noise=noise)
        return clean, noisy

    def update_plots(self, *args):
        shape = self.shape_var.get()
        noise = float(self.noise_slider.get())
        
        # 1. Generate data
        clean_pts, noisy_pts = self.generate_data(shape, noise)
        
        # 2. Compute diagrams
        importlib.reload(tasks)
        max_edge = 5.0
        dgm_clean = tasks.compute_h1_diagram(clean_pts, max_edge_length=max_edge)
        dgm_noisy = tasks.compute_h1_diagram(noisy_pts, max_edge_length=max_edge)
        
        # 3. Plot Point Clouds
        self.axs[0].clear()
        self.axs[0].scatter(clean_pts[:,0], clean_pts[:,1], label="Clean Data", alpha=0.5, color="cyan")
        self.axs[0].scatter(noisy_pts[:,0], noisy_pts[:,1], label=f"Noisy (s={noise:.2f})", alpha=0.7, color="magenta")
        self.axs[0].set_aspect('equal')
        self.axs[0].legend(facecolor='#1e1e1e', labelcolor='white')
        self.axs[0].set_title(f"Point Cloud ({shape})", color='white')
        
        # 4. Plot Diagrams & Matching
        self.axs[1].clear()
        self.axs[1].plot([0, max_edge], [0, max_edge], color='gray', linestyle='--') # Diagonal
        
        if dgm_clean is None or dgm_noisy is None:
            self.axs[1].text(0.5, 0.5, "Implement compute_h1_diagram\nto see Wasserstein matching.", 
                             ha='center', va='center', color='yellow', fontsize=12, transform=self.axs[1].transAxes)
            self.axs[1].set_title("Waiting for implementation...", color='white')
            self.canvas.draw()
            return
            
        dist = 0
        if len(dgm_clean) > 0 or len(dgm_noisy) > 0:
            import gudhi
            dist, matching = gudhi.wasserstein.wasserstein_distance(
                dgm_clean if len(dgm_clean) > 0 else np.empty((0,2)), 
                dgm_noisy if len(dgm_noisy) > 0 else np.empty((0,2)),
                order=1, internal_p=2, matching=True
            )
            
            # Plot matching lines
            for i, j in matching:
                if i != -1 and j != -1:
                    p1 = dgm_clean[i]
                    p2 = dgm_noisy[j]
                    self.axs[1].plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', alpha=0.5)
                elif i != -1 and j == -1:
                    p1 = dgm_clean[i]
                    p2 = [(p1[0]+p1[1])/2, (p1[0]+p1[1])/2] # Projected to diagonal
                    self.axs[1].plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', alpha=0.5)
                elif i == -1 and j != -1:
                    p2 = dgm_noisy[j]
                    p1 = [(p2[0]+p2[1])/2, (p2[0]+p2[1])/2] # Projected to diagonal
                    self.axs[1].plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', alpha=0.5)
        
        # Plot points
        if len(dgm_clean) > 0:
            self.axs[1].scatter(dgm_clean[:,0], dgm_clean[:,1], marker='o', color='cyan', label='Clean H1')
        if len(dgm_noisy) > 0:
            self.axs[1].scatter(dgm_noisy[:,0], dgm_noisy[:,1], marker='s', color='magenta', label='Noisy H1')
            
        self.axs[1].set_title(f"Wasserstein Matching (W1 = {dist:.3f})", color='white')
        self.axs[1].set_xlim([0, 3.5])
        self.axs[1].set_ylim([0, 3.5])
        self.axs[1].legend(facecolor='#1e1e1e', labelcolor='white')
        
        self.canvas.draw()

    def run_ml(self):
        # Disable UI elements to prevent race conditions
        self.noise_slider.config(state='disabled')
        for child in self.sidebar.winfo_children():
            if isinstance(child, tk.Radiobutton) or isinstance(child, tk.Button):
                child.config(state='disabled')
                
        self.progress['value'] = 0
        self.sidebar.update_idletasks()
        
        def update_progress(current, total):
            # Update progress bar
            self.progress['value'] = (current / total) * 100
            self.sidebar.update_idletasks()
            
        import run_evaluation
        importlib.reload(run_evaluation)
        result = run_evaluation.run_ml_evaluation(progress_callback=update_progress)
        
        self.progress['value'] = 100
        
        # Re-enable UI elements
        self.noise_slider.config(state='normal')
        for child in self.sidebar.winfo_children():
            if isinstance(child, tk.Radiobutton) or isinstance(child, tk.Button):
                child.config(state='normal')
                
        self.sidebar.update_idletasks()
        
        if result:
            acc, cm, labels_list = result
            self.show_confusion_matrix(acc, cm, labels_list)

    def show_confusion_matrix(self, acc, cm, labels_list):
        from matplotlib.figure import Figure
        import seaborn as sns
        
        popup = tk.Toplevel(self)
        popup.title("ML Evaluation Results")
        popup.geometry("700x550")
        popup.configure(bg="#1e1e1e")
        
        fig = Figure(figsize=(7, 5))
        fig.patch.set_facecolor('#1e1e1e')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#1e1e1e')
        
        heatmap = sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=labels_list, yticklabels=labels_list, ax=ax)
                    
        # Update colorbar tick colors to white
        cbar = ax.collections[0].colorbar
        if cbar:
            cbar.ax.tick_params(colors='white')
                    
        ax.set_title(f"Wasserstein Classifier Confusion Matrix\nOverall Accuracy: {acc * 100:.1f}%", color='white')
        ax.set_ylabel('Actual Shape', color='white')
        ax.set_xlabel('Predicted Shape', color='white')
        ax.tick_params(colors='white')
        
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        canvas.draw()

if __name__ == "__main__":
    app = WassersteinDashboard()
    app.mainloop()
