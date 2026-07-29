"""
Level 5 — Absorbing Boundary Conditions
==========================================
Student implements: absorbing_mask(N, gobble_frac)

Visual debugger: side-by-side comparison of the mask profile,
and how applying it to the wave packet eliminates wrap-around artifacts.
Run:
    python levels/level_7_absorber.py
    python levels/level_7_absorber.py --no-graphics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks


# ============================================================
# GRAPHICS
# ============================================================
class Level5Absorber:

    def __init__(self):
        import matplotlib.animation as animation
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 5 — Absorbing Boundary Mask (Gobbler)',
                          color='white', fontsize=12, fontweight='bold')
        self.fig.subplots_adjust(bottom=0.22)

        ax_frac = plt.axes([0.15, 0.07, 0.70, 0.04])
        self.sl_frac = widgets.Slider(ax_frac, 'Absorber fraction', 0.02, 0.3,
                                      valinit=0.10, color='#ce93d8')
        self.sl_frac.label.set_color('white')
        self.sl_frac.valtext.set_color('white')
        self.sl_frac.on_changed(self._redraw)

        self.ax.set_facecolor('#16213e')
        self.ax.tick_params(colors='#cccccc')
        for sp in self.ax.spines.values(): sp.set_edgecolor('#444466')
        self.ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        self.N = 512
        self.L = 40.0
        self.x = np.linspace(-self.L/2, self.L/2, self.N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.V = np.zeros(self.N)
        self.dt = 0.005
        
        self.ax.set_ylim(-0.05, 1.15)
        self.ax.set_xlabel('x', color='#cccccc')
        self.ax.set_ylabel('Amplitude', color='#cccccc')
        
        # Plot mask
        self.mask_line, = self.ax.plot(self.x, np.ones(self.N), color='#ce93d8', lw=2, ls='--', alpha=0.8, label='Mask profile M(x)')
        
        # Plot wave
        self.prob_line, = self.ax.plot(self.x, np.zeros(self.N), color='#4fc3f7', lw=2, label='|ψ|²')
        
        self.left_span = self.ax.axvspan(self.x[0], self.x[0], color='#ff7043', alpha=0.15, label='Absorbing zone')
        self.right_span = self.ax.axvspan(self.x[-1], self.x[-1], color='#ff7043', alpha=0.15)
        
        self.norm_text = self.ax.text(0.5, 0.95, '', transform=self.ax.transAxes, 
                                      color='white', fontsize=10, ha='center', va='top',
                                      bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))
        
        self.ax.legend(loc='upper right', fontsize=9, facecolor='#1a1a2e', labelcolor='white')

        self._init_wave()
        self.anim = animation.FuncAnimation(self.fig, self._animate, interval=30, blit=False, cache_frame_data=False)

    def _init_wave(self):
        self.psi = tasks.gaussian_packet(self.N, self.dx, self.x[0], -self.L * 0.25, 1.0, 10.0)
        self.mask = np.ones(self.N)
        gf = self.sl_frac.val
        try:
            self.mask = tasks.apply_absorbing_mask(np.ones(self.N), gf)
        except Exception:
            pass
            
        self.mask_line.set_ydata(self.mask)
        gw = max(1, int(gf * self.N))
        
        # Update spans
        self.left_span.remove()
        self.right_span.remove()
        self.left_span = self.ax.axvspan(self.x[0], self.x[gw], color='#ff7043', alpha=0.15)
        self.right_span = self.ax.axvspan(self.x[-gw], self.x[-1], color='#ff7043', alpha=0.15)

    def _redraw(self, val):
        self._init_wave()

    def _animate(self, frame):
        try:
            for _ in range(5):
                self.psi = tasks.split_operator_step(self.psi, self.V, self.dx, self.dt)
                if self.psi is None: self.psi = np.zeros_like(self.x, dtype=complex)
                self.psi = tasks.apply_absorbing_mask(self.psi, self.sl_frac.val)
        except Exception:
            pass
            
        prob = np.abs(self.psi)**2
        norm = np.sum(prob) * self.dx
        self.prob_line.set_ydata(prob)
        norm_color = '#81c784' if norm > 0.95 else '#ff6e6e'
        self.norm_text.set_text(f'norm = {norm:.4f}')
        self.norm_text.set_color(norm_color)



if __name__ == '__main__':
    lvl = Level5Absorber()
    plt.show()
