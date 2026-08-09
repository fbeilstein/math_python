import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import implementation_tasks as tasks
import matplotlib.colors as mcolors

# =============================================================================
# GUI ENGINE
# =============================================================================

class VectorizedLab:
    def __init__(self):
        self.tr, self.det = -1.0, 2.0
        self.limit = 5
        self.is_dragging = False
        
        self.label_colors = {}

        self.fig, (self.ax_map, self.ax_phase) = plt.subplots(1, 2, figsize=(14, 7))
        plt.subplots_adjust(bottom=0.2, left=0.08, right=0.95)

        seeds = []
        for r in [0.5, 1.5, 3.0, 4.5]:
            n_pts = int(r * 6) + 4
            angles = np.linspace(0, 2*np.pi, n_pts, endpoint=False)
            for ang in angles:
                seeds.append([r * np.cos(ang), r * np.sin(ang)])
        self.seeds = np.array(seeds).T
        self.n_seeds = self.seeds.shape[1]

        self.draw_map()
        self.marker, = self.ax_map.plot(self.tr, self.det, 'ro', markersize=12, zorder=10)
        
        # Text display for Lambdas
        self.txt_lambda = self.ax_phase.text(0.05, 0.95, '', transform=self.ax_phase.transAxes, 
                                             verticalalignment='top', family='monospace',
                                             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        self.traj_artist, = self.ax_phase.plot([], [], color='#2c3e50', alpha=0.3, lw=1)
        self.quiver = None
        
        self.draw_phase_portrait()

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def draw_phase_portrait(self):
        res = tasks.get_lambdas(self.tr, self.det)
        if res is not None and len(res) == 4:
            r1, i1, r2, i2 = res
            l1_str = f"λ1: {r1:5.2f} + {i1:5.2f}i"
            l2_str = f"λ2: {r2:5.2f} + {i2:5.2f}i"
            self.txt_lambda.set_text(f"{l1_str}\n{l2_str}")

        # Update Title
        label = tasks.classify_system(self.tr, self.det)
        if label:
            # Look up dynamic color, fallback to black if missing
            color = self.label_colors.get(label, "black")
            self.ax_phase.set_title(f"Type: {label}", color=color, fontsize=15, fontweight='bold')
        else:
            self.ax_phase.set_title("Observe Lambdas & Trajectories", color='gray')
        
        # Integration logic
        t_span, t_eval = (0, 3.0), np.linspace(0, 3.0, 35)
        y0_flat = self.seeds.flatten()

        def odefunc(t, y_flat):
            y_grid = y_flat.reshape(2, -1)
            dx, dy = tasks.get_derivatives(y_grid[0], y_grid[1], self.tr, self.det)
            return np.concatenate([dx, dy])

        res_check = tasks.get_derivatives(self.seeds[0], self.seeds[1], self.tr, self.det)
        if res_check is not None and not np.all(res_check[0] == 0):
            sol_f = solve_ivp(odefunc, t_span, y0_flat, t_eval=t_eval, method='RK23')
            sol_b = solve_ivp(odefunc, (0, -t_span[1]), y0_flat, t_eval=-t_eval, method='RK23')
            yf = sol_f.y.reshape(2, self.n_seeds, -1).transpose(1, 2, 0)
            yb = sol_b.y.reshape(2, self.n_seeds, -1).transpose(1, 2, 0)
            full_paths = np.concatenate([np.flip(yb, axis=1), yf], axis=1)
            nan_sep = np.full((self.n_seeds, 1, 2), np.nan)
            plot_data = np.concatenate([full_paths, nan_sep], axis=1)
            self.traj_artist.set_data(plot_data[:, :, 0].flatten(), plot_data[:, :, 1].flatten())
            
            if self.quiver: self.quiver.remove()
            vx, vy = res_check
            mag = np.sqrt(vx**2 + vy**2) + 1e-9
            self.quiver = self.ax_phase.quiver(self.seeds[0], self.seeds[1], vx/mag, vy/mag, 
                                              color='#2c3e50', scale=35, width=0.004, alpha=0.8)

        self.ax_phase.set_xlim(-self.limit, self.limit); self.ax_phase.set_ylim(-self.limit, self.limit)
        self.ax_phase.axhline(0, color='black', lw=0.5, alpha=0.2); self.ax_phase.axvline(0, color='black', lw=0.5, alpha=0.2)

    def draw_map(self):
        self.ax_map.clear()
        
        t_range = np.linspace(-4, 4, 150)
        d_range = np.linspace(-2, 6, 150)
        t_grid, d_grid = np.meshgrid(t_range, d_range)

        try:
            # 1. Vectorize over student function
            v_classify = np.vectorize(tasks.classify_system, otypes=[object])
            labels = v_classify(t_grid, d_grid)
            
            if labels[0,0] is None:
                raise ValueError("Not implemented")

            # 2. Extract unique labels and dynamically generate a color palette
            unique_labels = np.unique(labels)
            
            # Use a categorical colormap like 'Set1' or 'tab10'
            import matplotlib.cm as cm
            cmap_base = plt.get_cmap('tab10')
            self.label_colors = {label: mcolors.to_hex(cmap_base(i % 10)) for i, label in enumerate(unique_labels)}
            
            color_palette = [self.label_colors[label] for label in unique_labels]
            student_cmap = mcolors.ListedColormap(color_palette)
            
            label_to_id = {label: i for i, label in enumerate(unique_labels)}
            region_ids = np.vectorize(label_to_id.get)(labels)
            
            # 3. Draw map
            self.ax_map.imshow(region_ids, extent=[-4, 4, -2, 6], origin='lower', 
                               alpha=0.4, cmap=student_cmap, aspect='auto')
            
        except Exception as e:
            # print(e) # uncomment for debugging
            pass
        finally:
            # Draw reference boundaries and set limits
            t_vals = np.linspace(-4, 4, 100)
            self.ax_map.plot(t_vals, (t_vals**2)/4, 'k-', lw=1, alpha=0.5)
            self.ax_map.axhline(0, color='black', lw=1.2)
            self.ax_map.axvline(0, color='black', lw=1.2, ls='--')
            self.ax_map.set_xlim(-4, 4)
            self.ax_map.set_ylim(-2, 6)
            self.ax_map.set_xlabel(r"Trace ($\tau$)")
            self.ax_map.set_ylabel(r"Determinant ($\Delta$)")
            if hasattr(self, 'marker'): self.ax_map.add_artist(self.marker)

    def on_press(self, event):
        if event.inaxes == self.ax_map and np.hypot(event.xdata - self.tr, event.ydata - self.det) < 0.6:
            self.is_dragging = True

    def on_motion(self, event):
        if self.is_dragging and event.inaxes == self.ax_map:
            self.tr, self.det = event.xdata, event.ydata
            self.marker.set_data([self.tr], [self.det])
            self.draw_phase_portrait()
            self.fig.canvas.draw_idle()

    def on_release(self, event): self.is_dragging = False

if __name__ == "__main__":
    lab = VectorizedLab()
    plt.show()
