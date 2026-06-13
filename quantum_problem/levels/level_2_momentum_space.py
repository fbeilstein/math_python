"""
Level 2 — Momentum Space
==========================
Student implements: momentum_wavefunction(psi, dx)

Visual debugger: two-panel view — position space and momentum space.
Demonstrates the Fourier-limit: narrow in x → broad in k, and vice versa.
Run:
    python levels/level_2_momentum_space.py
    python levels/level_2_momentum_space.py --no-graphics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks


# ============================================================
# GRAPHICS & INTERACTION
# ============================================================
class Level2MomentumSpace:

    def __init__(self):
        self.fig, (self.ax_x, self.ax_k) = plt.subplots(1, 2, figsize=(12, 4))
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 2 — Momentum Space (Fourier Duality)', color='white',
                          fontsize=13, fontweight='bold')
        self.fig.subplots_adjust(bottom=0.32)

        ax_sigma = plt.axes([0.15, 0.12, 0.70, 0.03])
        ax_k0    = plt.axes([0.15, 0.05, 0.70, 0.03])
        self.sl_sigma = widgets.Slider(ax_sigma, 'Width $\\sigma$', 0.1, 3.0, valinit=0.8, color='#81c784')
        self.sl_k0    = widgets.Slider(ax_k0,    'Momentum $k_0$', 0.0, 20.0, valinit=8.0, color='#ffb74d')
        self.sl_sigma.on_changed(self._redraw)
        self.sl_k0.on_changed(self._redraw)

        self._style(self.ax_x, '|ψ(x)|²', 'x')
        self._style(self.ax_k, '|φ(k)|²', 'k')
        self.draw()

    def disconnect_events(self):
        self.sl_sigma.disconnect_events()
        self.sl_k0.disconnect_events()

    def _style(self, ax, ylabel, xlabel):
        ax.set_facecolor('#16213e')
        ax.tick_params(colors='#cccccc')
        ax.set_xlabel(xlabel, color='#cccccc', fontsize=10)
        ax.set_ylabel(ylabel, color='#cccccc', fontsize=10)
        for sp in ax.spines.values():
            sp.set_edgecolor('#444466')
        ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

    def _redraw(self, val):
        self.ax_x.clear(); self.ax_k.clear()
        self._style(self.ax_x, '|ψ(x)|²', 'x')
        self._style(self.ax_k, '|φ(k)|²', 'k')
        self.draw()
        self.fig.canvas.draw_idle()

    def draw(self):
        L  = 10.0
        x  = np.linspace(0, L, 1024, endpoint=False)
        dx = x[1] - x[0]

        try:
            psi = tasks.gaussian_packet(x, L / 2, self.sl_sigma.val, self.sl_k0.val)
        except Exception:
            return

        try:
            k, phi = tasks.momentum_wavefunction(psi, dx)
        except Exception as e:
            self.ax_k.text(0.5, 0.5, f'Error:\n{e}', transform=self.ax_k.transAxes,
                           ha='center', va='center', color='#ff6e6e', fontsize=9)
            return

        # Position space
        self.ax_x.plot(x, np.abs(psi)**2, color='#4fc3f7', lw=2)
        self.ax_x.set_xlim(x[0], x[-1])
        self.ax_x.axhline(0, color='#555577', lw=0.8)

        # Momentum space (sort so plot is contiguous)
        idx = np.argsort(k)
        k_s = k[idx]
        prob_k = np.abs(phi[idx])**2
        dk = k_s[1] - k_s[0]
        norm_k = np.sum(prob_k) * dk

        self.ax_k.plot(k_s, prob_k, color='#ce93d8', lw=2)
        self.ax_k.axvline(self.sl_k0.val, color='#ffb74d', lw=1.2, ls='--', label=f'k₀={self.sl_k0.val:.1f}')
        k_max_plot = max(self.sl_k0.val * 2, 20.0)
        self.ax_k.set_xlim(-0.5 * k_max_plot, k_max_plot * 1.5)
        self.ax_k.axhline(0, color='#555577', lw=0.8)

        norm_color = '#81c784' if abs(norm_k - 1.0) < 0.05 else '#ff6e6e'
        self.ax_k.text(0.97, 0.95, f'∫|φ|² dk = {norm_k:.4f}',
                       transform=self.ax_k.transAxes, ha='right', va='top',
                       color=norm_color, fontsize=10,
                       bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))
        self.ax_k.legend(loc='upper left', fontsize=9, facecolor='#1a1a2e', labelcolor='white')


# ============================================================
# UNIT TESTS
# ============================================================
class TestLevel2MomentumSpace(unittest.TestCase):

    def setUp(self):
        L  = 10.0
        self.x  = np.linspace(0, L, 2048, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.k0 = 5.0
        psi = tasks.gaussian_packet(self.x, L / 2, 0.8, self.k0)
        self.k, self.phi = tasks.momentum_wavefunction(psi, self.dx)

    def test_returns_two_arrays(self):
        self.assertIsInstance(self.k,   np.ndarray, "First return value must be k (numpy array).")
        self.assertIsInstance(self.phi, np.ndarray, "Second return value must be phi (numpy array).")

    def test_same_length(self):
        self.assertEqual(len(self.k), len(self.phi), "k and phi must have the same length.")

    def test_normalization(self):
        idx = np.argsort(self.k)
        dk = self.k[idx][1] - self.k[idx][0]
        norm = np.sum(np.abs(self.phi)**2) * dk
        self.assertAlmostEqual(norm, 1.0, delta=0.05,
                               msg="Momentum wavefunction must be normalized.")

    def test_peak_at_k0(self):
        peak_k = self.k[np.argmax(np.abs(self.phi)**2)]
        self.assertAlmostEqual(peak_k, self.k0, delta=0.5,
                               msg="Momentum-space peak must be near k0.")


# ============================================================
# STANDALONE
# ============================================================
if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level2MomentumSpace()
        plt.show()
