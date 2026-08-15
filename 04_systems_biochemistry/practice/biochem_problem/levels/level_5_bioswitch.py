import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import implementation_tasks

# True Goldbeter-Koshland Parameters
K_R0, K_R1 = 0.22, 0.001
K_E0, K_E1 = 0.8, 0.01
K_M0, K_M1 = 0.01, 0.01
E_TOT = 0.5

def _rhs(state, t, S_val):
    R, E = state
    E = max(0.0, min(E, 0.4999))
    R = max(0.0, R)
    Ep = E_TOT - E
    dR = K_R0 * Ep + S_val - K_R1 * R
    dE = K_E0 * Ep / (Ep + K_M0) - K_E1 * R * E / (E + K_M1)
    return [dR, dE]

class Level5Bioswitch:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.fig = plt.figure(figsize=(12, 6))
        self.fig.patch.set_facecolor('#1e1e1e')

        self.ax = self.fig.add_axes([0.1, 0.15, 0.8, 0.75])
        self.ax.set_facecolor('#252526')
        self.ax.tick_params(colors='white')
        self.ax.set_xlabel("Time, t, sec", color='white', fontsize=12)
        self.ax.set_ylabel("Concentration", color='white', fontsize=12)
        self.ax.set_title("Interactive Pulse Experiment (Drag the orange dot)", color='white', fontsize=14)
        
        self.ax.set_xlim(0, 60000)
        self.ax.set_ylim(0, 250)

        # Lines
        self.line_R, = self.ax.plot([], [], color='#1f77b4', lw=2.5, label='[R]')
        self.line_S, = self.ax.plot([], [], color='#ff7f0e', lw=2.5, label='1000 × [S]')
        self.scatter_peak, = self.ax.plot([], [], 'o', color='#d62728', markersize=10, zorder=5)
        
        self.ax.legend(facecolor='#252526', edgecolor='white', labelcolor='white', loc='upper right')

        # Background vector field to hint at bistability
        # Based on parameters, OFF=0, Saddle~85, ON~103
        self.ax.axhline(103.0, color='white', linestyle='--', alpha=0.2, zorder=1)
        self.ax.axhline(85.0, color='red', linestyle=':', alpha=0.2, zorder=1)
        
        for t_bg in np.linspace(2000, 58000, 12):
            for r_bg in np.arange(15, 240, 15):
                if r_bg < 85:
                    dy = -12
                elif r_bg < 103:
                    dy = 8
                else:
                    dy = -12
                
                # Faint arrows pointing towards attractors
                self.ax.annotate('', xy=(t_bg, r_bg + dy), xytext=(t_bg, r_bg),
                                 arrowprops=dict(arrowstyle="->", color="white", alpha=0.15, lw=1.5),
                                 zorder=1)

        self.current_center = 30000
        self.current_intensity = 0.1
        
        self.is_dragging = False

        # Load Student Function
        self.student_func = None
        try:
            res = implementation_tasks.bioswitch_rhs([0.0, 0.5], 0.0, 0.0)
            if res is not None and len(res) == 2:
                self.student_func = implementation_tasks.bioswitch_rhs
                self.dashboard.log("Successfully loaded student bioswitch_rhs.")
        except Exception as e:
            self.dashboard.log(f"Error calling bioswitch_rhs: {e}", color="#f44747")

        # Events
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        # Initial draw
        self.update_plot()

    def _gaussian(self, t):
        return self.current_intensity * np.exp(-((t - self.current_center)**2) / 2000000.0)

    def update_plot(self, fast=False):
        # Update S curve
        t_S = np.linspace(0, 60000, 300)
        S_vals = self.current_intensity * np.exp(-((t_S - self.current_center)**2) / 2000000.0)
        self.line_S.set_data(t_S, S_vals * 1000)
        self.scatter_peak.set_data([self.current_center], [self.current_intensity * 1000])
        
        if not fast:
            # Integrate ODE
            t_R = np.linspace(0, 60000, 600)
            
            func = self.student_func if self.student_func else _rhs
            
            def wrapper(state, t):
                S_t = self._gaussian(t)
                return func(state, t, S_t)
                
            try:
                sol = odeint(wrapper, [0.0, 0.5], t_R, rtol=1e-6, atol=1e-8)
                self.line_R.set_data(t_R, sol[:, 0])
            except Exception as e:
                self.dashboard.log(f"Integration error: {e}", color="#f44747")
                
        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax: return
        
        # Normalize distance relative to axes limits
        dx = (event.xdata - self.current_center) / 60000.0
        dy = (event.ydata - self.current_intensity * 1000.0) / 250.0
        
        if np.sqrt(dx**2 + dy**2) < 0.05:
            self.is_dragging = True

    def on_motion(self, event):
        if not self.is_dragging or event.inaxes != self.ax:
            return
        
        self.current_center = np.clip(event.xdata, 0, 60000)
        self.current_intensity = np.clip(event.ydata / 1000.0, 0, 0.25)
        
        self.update_plot(fast=True)

    def on_release(self, event):
        if self.is_dragging:
            self.is_dragging = False
            self.update_plot(fast=False)
