"""
Level 1 — Gaussian Wave Packet
================================
Student implements: gaussian_packet(x, x0, sigma, k0)

Visual debugger: interactive sliders for x0, sigma, k0.
Run:
    python levels/level_1_gaussian.py            # visual
    python levels/level_1_gaussian.py --no-graphics   # unit tests only
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks
from levels.base_level import BaseLevel


# ============================================================
# GRAPHICS & INTERACTION
# ============================================================
class Level1Gaussian(BaseLevel):

    def __init__(self):
        super().__init__()
        self.fig.suptitle('Level 1 — Gaussian Wave Packet', color='white', fontsize=13, fontweight='bold')
        self.fig.subplots_adjust(bottom=0.38)

        # Sliders
        ax_x0    = plt.axes([0.15, 0.24, 0.70, 0.03])
        ax_sigma = plt.axes([0.15, 0.16, 0.70, 0.03])
        ax_k0    = plt.axes([0.15, 0.08, 0.70, 0.03])

        self.sl_x0    = widgets.Slider(ax_x0,    'Center $x_0$',  1.0, 9.0, valinit=5.0, color='#4fc3f7')
        self.sl_x0.label.set_color('white')
        self.sl_x0.valtext.set_color('white')
        self.sl_sigma = widgets.Slider(ax_sigma,  'Width $\\sigma$', 0.2, 2.0, valinit=0.8, color='#81c784')
        self.sl_sigma.label.set_color('white')
        self.sl_sigma.valtext.set_color('white')
        self.sl_k0    = widgets.Slider(ax_k0,    'Momentum $k_0$', 1.0, 20.0, valinit=8.0, color='#ffb74d')
        self.sl_k0.label.set_color('white')
        self.sl_k0.valtext.set_color('white')

        for sl in (self.sl_x0, self.sl_sigma, self.sl_k0):
            sl.on_changed(self._on_slider_change)

        self.draw()

    def disconnect_events(self):
        for sl in (self.sl_x0, self.sl_sigma, self.sl_k0):
            sl.disconnect_events()

    def draw(self):
        self.style_axes(xlabel='x', ylabel='')
        L = 10.0
        N = 1024
        x = np.linspace(0, L, N, endpoint=False)
        dx = x[1] - x[0]
        x_start = x[0]

        try:
            psi = tasks.gaussian_packet(N, dx, x_start, self.sl_x0.val, self.sl_sigma.val, self.sl_k0.val)
            if psi is None: raise NotImplementedError("gaussian_packet returned None")
            prob = np.abs(psi)**2
            norm = np.sum(prob) * dx
        except Exception as e:
            self.ax.text(0.5, 0.5, f'Error:\n{e}', transform=self.ax.transAxes,
                         ha='center', va='center', color='#ff6e6e', fontsize=10)
            return

        self.ax.plot(x, prob,      color='#4fc3f7', lw=2,   label='|ψ|²')
        self.ax.plot(x, psi.real,  color='#81c784', lw=1,   alpha=0.6, label='Re[ψ]')
        self.ax.plot(x, psi.imag,  color='#ffb74d', lw=1,   alpha=0.4, label='Im[ψ]')
        self.ax.axhline(0, color='#555577', lw=0.8)
        self.ax.set_xlim(x[0], x[-1])

        # Norm indicator
        norm_color = '#81c784' if abs(norm - 1.0) < 0.01 else '#ff6e6e'
        self.ax.text(0.97, 0.95, f'∫|ψ|² dx = {norm:.4f}',
                     transform=self.ax.transAxes, ha='right', va='top',
                     color=norm_color, fontsize=10,
                     bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))
        self.ax.legend(loc='upper left', fontsize=9, facecolor='#1a1a2e', labelcolor='white')



# ============================================================
# STANDALONE EXECUTION
# ============================================================
if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level1Gaussian()
        plt.show()
