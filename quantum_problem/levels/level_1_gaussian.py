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
import unittest
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
        self.sl_sigma = widgets.Slider(ax_sigma,  'Width $\\sigma$', 0.2, 2.0, valinit=0.8, color='#81c784')
        self.sl_k0    = widgets.Slider(ax_k0,    'Momentum $k_0$', 1.0, 20.0, valinit=8.0, color='#ffb74d')

        for sl in (self.sl_x0, self.sl_sigma, self.sl_k0):
            sl.on_changed(self._on_slider_change)

        self.draw()

    def disconnect_events(self):
        for sl in (self.sl_x0, self.sl_sigma, self.sl_k0):
            sl.disconnect_events()

    def draw(self):
        self.style_axes(xlabel='x', ylabel='')
        L = 10.0
        x = np.linspace(0, L, 1024, endpoint=False)

        try:
            psi = tasks.gaussian_packet(x, self.sl_x0.val, self.sl_sigma.val, self.sl_k0.val)
        except Exception as e:
            self.ax.text(0.5, 0.5, f'Error:\n{e}', transform=self.ax.transAxes,
                         ha='center', va='center', color='#ff6e6e', fontsize=10)
            return

        dx = x[1] - x[0]
        prob = np.abs(psi)**2
        norm = np.sum(prob) * dx

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
# UNIT TESTS
# ============================================================
class TestLevel1Gaussian(unittest.TestCase):

    def setUp(self):
        self.L  = 10.0
        self.x  = np.linspace(0, self.L, 2048, endpoint=False)
        self.dx = self.x[1] - self.x[0]

    def test_returns_complex_array(self):
        psi = tasks.gaussian_packet(self.x, 5.0, 0.8, 5.0)
        self.assertIsInstance(psi, np.ndarray, "Return value must be a numpy array.")
        self.assertEqual(psi.dtype.kind, 'c', "Array must be complex.")

    def test_normalization(self):
        psi = tasks.gaussian_packet(self.x, 5.0, 0.8, 5.0)
        norm = np.sum(np.abs(psi)**2) * self.dx
        self.assertAlmostEqual(norm, 1.0, places=4, msg="Wavefunction must be normalized to 1.")

    def test_peak_at_x0(self):
        x0 = 4.0
        psi = tasks.gaussian_packet(self.x, x0, 0.5, 5.0)
        peak_idx = np.argmax(np.abs(psi)**2)
        self.assertAlmostEqual(self.x[peak_idx], x0, delta=0.1, msg="Probability peak must be at x0.")

    def test_momentum_phase(self):
        k0 = 6.0
        psi = tasks.gaussian_packet(self.x, 5.0, 0.8, k0)
        # The phase winding rate should equal k0
        phase = np.angle(psi)
        # finite diff of phase near center
        center = len(self.x) // 2
        dphi = np.diff(phase[center-5:center+5])
        dphi = (dphi + np.pi) % (2*np.pi) - np.pi  # unwrap locally
        k_measured = np.mean(dphi) / self.dx
        self.assertAlmostEqual(k_measured, k0, delta=0.3, msg="Phase gradient must equal k0.")


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
