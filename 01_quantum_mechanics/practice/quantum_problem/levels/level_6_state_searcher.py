import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import matplotlib.animation as animation
from scipy.ndimage import gaussian_filter1d
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks

class Level6StateSearcher:
    def __init__(self):
        self.fig = plt.figure(figsize=(11, 7))
        gs = self.fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.2)
        self.ax   = self.fig.add_subplot(gs[0])
        self.ax_E = self.fig.add_subplot(gs[1])
        
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 6 — The State Searcher Engine',
                          color='white', fontsize=13, fontweight='bold')
        self.fig.subplots_adjust(bottom=0.32)

        # Physics Setup
        self.L = 1.0
        self.N = 1024
        self.x = np.linspace(-self.L, 2*self.L, self.N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.dt = 0.0005
        
        # Deep finite well, SMOOTHED to prevent Trotter energy explosions
        raw_V = np.where((self.x < 0) | (self.x > self.L), 1000.0, 0.0)
        self.V = gaussian_filter1d(raw_V, sigma=10.0)
        
        self._init_state()
        self._setup_plots()

        # UI Controls - placed safely above the bottom crop
        ax_slider = plt.axes([0.15, 0.06, 0.70, 0.03])
        self.slider_E = widgets.Slider(ax_slider, 'Target Energy', 0.0, 200.0, valinit=50.0, color='#ba68c8')
        self.slider_E.label.set_color('white')
        self.slider_E.valtext.set_color('white')
        self.slider_E.on_changed(self.on_slider_change)
        
        ax_ground = plt.axes([0.15, 0.16, 0.20, 0.05])
        self.btn_ground = widgets.Button(ax_ground, 'Cool to Ground State', color='#444466', hovercolor='#5c5c8a')
        self.btn_ground.label.set_color('white')
        self.btn_ground.on_clicked(self.cool_ground)
        
        ax_next = plt.axes([0.40, 0.16, 0.20, 0.05])
        self.btn_next = widgets.Button(ax_next, 'Save & Find Next', color='#444466', hovercolor='#5c5c8a')
        self.btn_next.label.set_color('white')
        self.btn_next.on_clicked(self.find_next)
        


        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=30, blit=False, cache_frame_data=False)

    def disconnect_events(self):
        try:
            self.slider_E.disconnect_events()
        except: pass

    def _init_state(self):
        self.psi = tasks.gaussian_packet(self.N, self.dx, -self.L, self.L/2, self.L*0.1, 10.0)
        if self.psi is None: self.psi = np.zeros_like(self.x, dtype=complex)
        self.saved_states = []
        self.E_history = []
        self.t = 0.0
        self.is_updating_slider = False
        self.prev_E = 0.0
        self.cooldown_frames = 0

    def _setup_plots(self):
        for a in (self.ax, self.ax_E):
            a.set_facecolor('#16213e')
            a.tick_params(colors='#cccccc')
            for sp in a.spines.values(): sp.set_edgecolor('#444466')
            a.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        self.ax.set_xlim(-0.5, 1.5)
        self.ax.set_ylim(-2.0, 2.0)
        self.ax.set_ylabel('Wavefunction ψ(x)', color='#cccccc')
        
        self.ax.axvspan(-self.L, 0, color='#37474f', alpha=0.5)
        self.ax.axvspan(self.L, 2*self.L, color='#37474f', alpha=0.5)
        self.ax.axvline(0, color='white', lw=1.5)
        self.ax.axvline(self.L, color='white', lw=1.5)

        self.line_prob, = self.ax.plot(self.x, np.abs(self.psi)**2, color='#4fc3f7', lw=2.5, label='|ψ|²')
        self.line_real, = self.ax.plot(self.x, np.real(self.psi), color='#81c784', lw=1.5, alpha=0.7, label='Re[ψ]')
        self.ax.legend(loc='upper right', facecolor='#1a1a2e', labelcolor='white')
        
        self.text_energy = self.ax.text(0.02, 0.95, 'Current <E>: 0.0', transform=self.ax.transAxes,
                                         color='#ffcc80', fontsize=11, fontweight='bold', va='top',
                                         bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))
        self.text_states = self.ax.text(0.02, 0.85, 'Saved States: 0', transform=self.ax.transAxes,
                                         color='#81c784', fontsize=11, fontweight='bold', va='top',
                                         bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

        self.ax_E.set_xlim(0, 200)
        self.ax_E.set_ylim(0, 250)
        self.ax_E.set_ylabel('Total Energy <E>', color='#cccccc')
        self.ax_E.set_xlabel('Simulation Frame', color='#cccccc')
        self.line_E, = self.ax_E.plot([], [], color='#ffb74d', lw=2)

    
    def on_slider_change(self, val):
        if self.is_updating_slider:
            return
        target_E = self.slider_E.val
        try:
            current_E = tasks.calculate_energy(self.psi, self.V, self.dx)
            if target_E > current_E:
                self.psi = tasks.kick_to_energy(self.psi, target_E, self.V, self.dx)
            elif target_E < current_E:
                prev_E = current_E
                while current_E > target_E + 0.1:
                    self.psi = tasks.imaginary_time_step(self.psi, self.V, self.dx, 0.01)
                    for state in self.saved_states:
                        self.psi = tasks.project_out(self.psi, state, self.dx)
                    current_E = tasks.calculate_energy(self.psi, self.V, self.dx)
                    if np.abs(prev_E - current_E) < 1e-4:
                        break
                    prev_E = current_E
            
            # Snap slider to actual physically reached energy
            final_E = tasks.calculate_energy(self.psi, self.V, self.dx)
            self.is_updating_slider = True
            self.slider_E.set_val(final_E)
            self.is_updating_slider = False
        except Exception: pass

    def cool_ground(self, event):
        self.saved_states = []
        self.slider_E.set_val(0.0)

    def find_next(self, event):
        self.saved_states.append(self.psi.copy())
        noise = np.random.randn(self.N) + 1j * np.random.randn(self.N)
        noise = np.where((self.x > 0) & (self.x < self.L), noise, 0.0)
        self.psi = self.psi + noise * 0.5
        norm = np.sqrt(np.sum(np.abs(self.psi)**2) * self.dx)
        if norm > 1e-10: self.psi /= norm
        
        self.slider_E.set_val(0.0)


    def animate(self, frame):
        try:
            target_E = self.slider_E.val
            
            for _ in range(50): 
                current_E = tasks.calculate_energy(self.psi, self.V, self.dx)
                if current_E is None: break
                
                try:
                    self.psi = tasks.split_operator_step(self.psi, self.V, self.dx, self.dt)
                except Exception: pass
                    
                for state in self.saved_states:
                    try:
                        self.psi = tasks.project_out(self.psi, state, self.dx)
                    except Exception: pass

            self.t += 50 * self.dt
            
            self.line_prob.set_ydata(np.abs(self.psi)**2)
            self.line_real.set_ydata(np.real(self.psi))
            
            new_E = tasks.calculate_energy(self.psi, self.V, self.dx)
            self.text_energy.set_text(f'Current <E>: {new_E:.2f}')
            self.text_states.set_text(f'Saved States: {len(self.saved_states)}')
            
            self.E_history.append(new_E)
            if len(self.E_history) > self.ax_E.get_xlim()[1]:
                self.ax_E.set_xlim(0, len(self.E_history) + 50)
            
            max_e = max(100, max(self.E_history) * 1.1)
            self.ax_E.set_ylim(0, max_e)
            
            self.line_E.set_data(range(len(self.E_history)), self.E_history)
            
        except Exception as e:
            pass
            
if __name__ == '__main__':
    lvl = Level6StateSearcher()
    plt.show()
