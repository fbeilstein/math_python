"""
Level 6 — Infinite Well via DST
==================================
Student implements: dst_energy_levels(N, L)

Visual debugger: wave packet bouncing perfectly in an infinite well.
The DST propagator is exact — norm is conserved to machine precision.
Run:
    python levels/level_6_infinite_well.py
    python levels/level_6_infinite_well.py --no-graphics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks
from scipy.fft import dst, idst


# ============================================================
# GRAPHICS
# ============================================================
class Level6InfiniteWell:

    def _dst_step(self, psi, E_k, dt):
        psi_k = dst(psi, type=1, norm='ortho')
        psi_k = psi_k * np.exp(-1j * E_k * dt)
        return idst(psi_k, type=1, norm='ortho')

    def __init__(self):
        self.fig, (self.ax, self.ax_norm) = plt.subplots(2, 1, figsize=(10, 6),
                                                          gridspec_kw={'height_ratios': [3, 1]})
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 6 — Infinite Well (DST — Exact Propagator)',
                          color='white', fontsize=12, fontweight='bold')
        self.fig.subplots_adjust(hspace=0.4)

        L  = 20.0
        N  = 1024
        self.x  = np.linspace(0, L, N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.L  = L
        self.dt = 0.005

        try:
            self.E_k = tasks.dst_energy_levels(N, L)
        except Exception:
            self.E_k = None

        self.psi   = tasks.gaussian_packet(self.x, L * 0.3, L * 0.05, 15.0)
        self.norms = []
        self.t     = 0.0

        for ax in (self.ax, self.ax_norm):
            ax.set_facecolor('#16213e')
            ax.tick_params(colors='#cccccc')
            for sp in ax.spines.values(): sp.set_edgecolor('#444466')
            ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        y_max = np.max(np.abs(self.psi)**2) * 2.5
        self.ax.set_ylim(-y_max * 0.2, y_max)
        self.ax.set_xlim(self.x[0] - L*0.05, self.x[-1] + L*0.05)
        self.ax.set_ylabel('|ψ|²', color='#cccccc')
        # Infinite walls
        self.ax.axvline(0, color='white', lw=4)
        self.ax.axvline(L, color='white', lw=4)
        self.ax.axvspan(self.x[0]-L*0.05, 0, color='#37474f', alpha=0.4)
        self.ax.axvspan(L, self.x[-1]+L*0.05, color='#37474f', alpha=0.4)
        self.ax.text(-L*0.025, y_max*0.7, 'V=∞', color='white', fontsize=14, fontweight='bold', ha='center')
        self.ax.text( L*1.025, y_max*0.7, 'V=∞', color='white', fontsize=14, fontweight='bold', ha='center')

        self.prob_line, = self.ax.plot(self.x, np.abs(self.psi)**2, color='#4fc3f7', lw=2, label='|ψ|²')
        self.real_line, = self.ax.plot(self.x, self.psi.real, color='#81c784', lw=1, alpha=0.5, label='Re[ψ]')
        self.ax.legend(loc='upper right', fontsize=9, facecolor='#1a1a2e', labelcolor='white')
        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes,
                                      color='#ffcc80', fontsize=10, va='top',
                                      bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

        self.norm_line, = self.ax_norm.plot([], [], color='#4db6ac', lw=1.5)
        self.ax_norm.set_xlim(0, 400)
        self.ax_norm.set_ylim(0.9999, 1.0001)
        self.ax_norm.axhline(1.0, color='gray', ls='--', alpha=0.5)
        self.ax_norm.set_xlabel('Frame', color='#cccccc')
        self.ax_norm.set_ylabel('∫|ψ|²dx', color='#cccccc')

        self.anim = animation.FuncAnimation(
            self.fig, self._animate, interval=30, blit=False, cache_frame_data=False)

    def _animate(self, frame):
        if self.E_k is None:
            return
        try:
            for _ in range(10):
                self.psi = self._dst_step(self.psi, self.E_k, self.dt)
            self.t += 10 * self.dt
        except Exception:
            return
        prob = np.abs(self.psi)**2
        self.prob_line.set_ydata(prob)
        self.real_line.set_ydata(self.psi.real)
        norm = np.sum(prob) * self.dx
        self.norms.append(norm)
        if len(self.norms) > self.ax_norm.get_xlim()[1]:
            self.ax_norm.set_xlim(0, len(self.norms) + 50)
        self.norm_line.set_data(range(len(self.norms)), self.norms)
        self.time_text.set_text(f't = {self.t:.3f} | norm = {norm:.8f}')


# ============================================================
# UNIT TESTS
# ============================================================
class TestLevel6InfiniteWell(unittest.TestCase):

    def setUp(self):
        self.N = 512
        self.L = 10.0

    def test_returns_array(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        self.assertIsInstance(E_k, np.ndarray)
        self.assertEqual(len(E_k), self.N)

    def test_ground_state_energy(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        E1_expected = (np.pi / self.L)**2 / 2   # hbar=m=1
        self.assertAlmostEqual(E_k[0], E1_expected, places=6,
                               msg='Ground state energy E1 = (pi/L)^2/2 must match.')

    def test_quadratic_scaling(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        # E_n should scale as n^2: E_k[1] / E_k[0] ≈ 4
        ratio = E_k[1] / E_k[0]
        self.assertAlmostEqual(ratio, 4.0, places=4,
                               msg='Energies must scale as n² (E2/E1 = 4).')

    def test_monotone_increasing(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        self.assertTrue(np.all(np.diff(E_k) > 0),
                        msg='Energy levels must be strictly increasing.')


# ============================================================
# STANDALONE
# ============================================================
if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level6InfiniteWell()
        plt.show()
