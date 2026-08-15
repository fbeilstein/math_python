import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import implementation_tasks

class Level6Cusp:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.history = {'w': [], 'cyc': [], 'c': []}
        self.current_c = 0.0
        self.is_pressed = False
        
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#1e1e1e')
        
        # 3D Axis
        self.ax3d = self.fig.add_axes([0.05, 0.2, 0.45, 0.7], projection='3d')
        self.ax3d.set_facecolor('#1e1e1e')
        self.ax3d.tick_params(colors='white')
        self.ax3d.set_xlabel('Wee1 (w)', color='white')
        self.ax3d.set_ylabel('Cyclin (cyc)', color='white')
        self.ax3d.set_zlabel('Cdc2 (C)', color='white')
        self.ax3d.set_title("3D State Manifold", color='white')
        
        # 2D Axis
        self.ax2d = self.fig.add_axes([0.55, 0.2, 0.4, 0.7])
        self.ax2d.set_facecolor('#252526')
        self.ax2d.tick_params(colors='white')
        self.ax2d.set_xlabel('Wee1 (w)', color='white')
        self.ax2d.set_ylabel('Cyclin (cyc)', color='white')
        self.ax2d.set_title("Control Plane (Click & Drag)", color='white')
        self.ax2d.grid(True, linestyle='--', alpha=0.5)
        
        self.student_func = None
        try:
            # test the student function
            if hasattr(implementation_tasks, 'cell_cycle_steady_state'):
                res = implementation_tasks.cell_cycle_steady_state(0.0, 2.0, 0.0)
                self.student_func = implementation_tasks.cell_cycle_steady_state
                self.dashboard.log("Successfully loaded student cell_cycle_steady_state.")
        except Exception as e:
            self.dashboard.log(f"Error calling cell_cycle_steady_state: {e}", color="#f44747")

        self.generate_3d_manifold()
        self.generate_2d_bifurcation()
        self.setup_interactions()
        self.update_system(2.0, 0.0)
        
    def generate_3d_manifold(self):
        import matplotlib.tri as mtri
        
        c_vals = np.linspace(-3, 3, 50)
        w_vals = np.linspace(0, 5, 50)
        W, C = np.meshgrid(w_vals, c_vals)
        CYC = C**3 - W * C
        
        w_flat, cyc_flat, c_flat = W.flatten(), CYC.flatten(), C.flatten()
        valid = (cyc_flat >= -5) & (cyc_flat <= 5)
        
        w_clean = w_flat[valid]
        cyc_clean = cyc_flat[valid]
        c_clean = c_flat[valid]
        
        tri = mtri.Triangulation(w_clean, c_clean)
        self.ax3d.plot_trisurf(w_clean, cyc_clean, c_clean, triangles=tri.triangles, cmap='coolwarm', alpha=0.8, edgecolor='none')
        
        self.ax3d.set_xlim(0, 5)
        self.ax3d.set_ylim(-5, 5)
        self.ax3d.set_zlim(-3, 3)
        self.ax3d.view_init(elev=20, azim=135)
        
    def generate_2d_bifurcation(self):
        w_bif = np.linspace(0, 5, 200)
        cyc_pos = np.sqrt( (4.0/27.0) * w_bif**3 )
        cyc_neg = -np.sqrt( (4.0/27.0) * w_bif**3 )
        
        self.ax2d.plot(w_bif, cyc_pos, 'k-', linewidth=2, label="Fold Line")
        self.ax2d.plot(w_bif, cyc_neg, 'k-', linewidth=2)
        self.ax2d.fill_between(w_bif, cyc_neg, cyc_pos, color='#FF4B4B', alpha=0.15, label="Bistable Region")
        
        self.ax2d.set_xlim(0, 5)
        self.ax2d.set_ylim(-5, 5)
        self.ax2d.legend(facecolor='#252526', edgecolor='white', labelcolor='white', loc='lower right')
        
    def setup_interactions(self):
        self.marker_2d, = self.ax2d.plot([0], [0], 'wo', markersize=8, markeredgecolor='black')
        self.trajectory_2d, = self.ax2d.plot([], [], 'w:', linewidth=2, alpha=0.8)
        
        self.marker_3d, = self.ax3d.plot([0], [0], [0], 'wo', markersize=8, markeredgecolor='black', zorder=5)
        self.trajectory_3d, = self.ax3d.plot([], [], [], color='white', linewidth=2, linestyle=':', alpha=0.8)
        
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
    def update_system(self, w_val, cyc_val):
        self.marker_2d.set_data([w_val], [cyc_val])
        
        try:
            if self.student_func:
                self.current_c = self.student_func(cyc_val, w_val, self.current_c)
            else:
                # Fallback just in case
                roots = np.roots([1, 0, -w_val, -cyc_val])
                real_roots = np.real(roots[np.abs(np.imag(roots)) < 1e-5])
                self.current_c = real_roots[np.argmin(np.abs(real_roots - self.current_c))]
        except Exception as e:
            self.dashboard.log(f"Error in student code: {e}", color="#f44747")
            return
            
        self.history['w'].append(w_val)
        self.history['cyc'].append(cyc_val)
        self.history['c'].append(self.current_c)
        
        if len(self.history['w']) > 60:
            for key in self.history: self.history[key].pop(0)
            
        self.trajectory_2d.set_data(self.history['w'], self.history['cyc'])
        self.marker_3d.set_data_3d([w_val], [cyc_val], [self.current_c])
        self.trajectory_3d.set_data_3d(self.history['w'], self.history['cyc'], self.history['c'])
            
        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes == self.ax2d:
            self.is_pressed = True
            for key in self.history: self.history[key].clear()
            self.update_system(event.xdata, event.ydata)

    def on_release(self, event):
        self.is_pressed = False

    def on_motion(self, event):
        if self.is_pressed and event.inaxes == self.ax2d:
            self.update_system(event.xdata, event.ydata)
