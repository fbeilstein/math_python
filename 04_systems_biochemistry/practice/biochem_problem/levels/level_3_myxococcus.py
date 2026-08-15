import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
import implementation_tasks

class Level3Myxococcus:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#1e1e1e')
        
        self.ax = self.fig.add_axes([0.1, 0.3, 0.8, 0.6])
        self.ax.set_facecolor('#252526')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.set_title("Live Oscillograph (Frz Pathway)", color='white')
        
        axcolor = '#3e3e42'
        self.ax_sig = self.fig.add_axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)
        self.s_sig = Slider(self.ax_sig, 'External Signal', 0.0, 1.0, valinit=0.0)
        self.s_sig.label.set_color('white')
        self.s_sig.valtext.set_color('white')
        
        self.line_frz, = self.ax.plot([], [], 'r-', label='Frz')
        self.line_frzcd, = self.ax.plot([], [], 'g-', label='FrzCD')
        self.line_frze, = self.ax.plot([], [], 'b-', label='FrzE')
        self.ax.legend(facecolor='#252526', edgecolor='white', labelcolor='white', loc='upper right')
        
        self.time_window = 100
        self.ax.set_xlim(0, self.time_window)
        self.ax.set_ylim(0, 1)
        
        self.state = [1.0, 1.0, 1.0]
        self.t_data = []
        self.y_data = [[], [], []]
        self.current_t = 0.0
        
        # Test student function
        self.student_func = None
        try:
            res = implementation_tasks.frz_pathway_rhs(self.state, 0.0, 0.0)
            if res is not None and len(res) == 3:
                self.student_func = implementation_tasks.frz_pathway_rhs
                self.dashboard.log("Successfully loaded student frz_pathway_rhs.")
            else:
                self.dashboard.log("frz_pathway_rhs returned None or incorrect length.", color="#f44747")
        except Exception as e:
            self.dashboard.log(f"Error calling frz_pathway_rhs: {e}", color="#f44747")
            
        self.anim = FuncAnimation(self.fig, self.update, interval=50, blit=False, cache_frame_data=False)

    def update(self, frame):
        dt = 0.5
        sig = self.s_sig.val
        
        func = self.student_func if self.student_func else implementation_tasks.frz_pathway_rhs
            
        t_span = np.linspace(self.current_t, self.current_t + dt, 2)
        try:
            sol = odeint(func, self.state, t_span, args=(sig,))
            self.state = sol[-1].tolist()
        except Exception as e:
            self.dashboard.log(f"Integration error: {e}", color="#f44747")
            return
            
        self.current_t += dt
        self.t_data.append(self.current_t)
        self.y_data[0].append(self.state[0])
        self.y_data[1].append(self.state[1])
        self.y_data[2].append(self.state[2])
        
        if len(self.t_data) > self.time_window / dt:
            self.t_data.pop(0)
            self.y_data[0].pop(0)
            self.y_data[1].pop(0)
            self.y_data[2].pop(0)
            
        self.line_frz.set_data(self.t_data, self.y_data[0])
        self.line_frzcd.set_data(self.t_data, self.y_data[1])
        self.line_frze.set_data(self.t_data, self.y_data[2])
        
        self.ax.set_xlim(max(0, self.current_t - self.time_window), max(self.time_window, self.current_t))

    def disconnect_events(self):
        if hasattr(self, 'anim') and self.anim:
            self.anim.event_source.stop()
