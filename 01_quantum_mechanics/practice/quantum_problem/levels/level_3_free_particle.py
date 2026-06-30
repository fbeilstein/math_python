"""
Level 3 — Free Particle Propagation
======================================
Student implements: evolve_free_particle(psi, k, dt)

Visual debugger: animated wave packet that spreads due to dispersion.
Press any key to pause/resume.
Run:
    python levels/level_3_free_particle.py
    python levels/level_3_free_particle.py --no-graphics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks


# ============================================================
# GRAPHICS & INTERACTION
# ============================================================
class Level3FreeParticle:

    def __init__(self):
        self.fig, (self.ax, self.ax_norm) = plt.subplots(2, 1, figsize=(10, 6),
                                                          gridspec_kw={'height_ratios': [3, 1]})
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 3 — Free Particle Propagation (wave packet spreading)',
                          color='white', fontsize=12, fontweight='bold')
        self.fig.subplots_adjust(hspace=0.4)

        # Grid
        L  = 20.0
        N  = 1024
        self.x  = np.linspace(0, L, N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        from numpy.fft import fftfreq
        self.k  = 2 * np.pi * fftfreq(N, d=self.dx)
        self.dt = 0.005

        self.psi = tasks.gaussian_packet(self.x, L * 0.3, 0.6, 8.0)
        self.norms = []

        for ax in (self.ax, self.ax_norm):
            ax.set_facecolor('#16213e')
            ax.tick_params(colors='#cccccc')
            for sp in ax.spines.values(): sp.set_edgecolor('#444466')
            ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        self.prob_line, = self.ax.plot(self.x, np.abs(self.psi)**2, color='#4fc3f7', lw=2, label='|ψ|²')
        self.real_line, = self.ax.plot(self.x, self.psi.real, color='#81c784', lw=1, alpha=0.5, label='Re[ψ]')
        self.ax.set_xlim(self.x[0], self.x[-1])
        y_max = np.max(np.abs(self.psi)**2) * 2.5
        self.ax.set_ylim(-y_max * 0.3, y_max)
        self.ax.set_ylabel('|ψ(x)|²', color='#cccccc')
        self.ax.legend(loc='upper right', fontsize=9, facecolor='#1a1a2e', labelcolor='white')
        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes,
                                      color='#ffcc80', fontsize=10, va='top',
                                      bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

        self.norm_line, = self.ax_norm.plot([], [], color='#ce93d8', lw=1.5)
        self.ax_norm.set_xlim(0, 300)
        self.ax_norm.set_ylim(0.0, 1.2)
        self.ax_norm.axhline(1.0, color='gray', ls='--', alpha=0.5)
        self.ax_norm.set_xlabel('Frame', color='#cccccc')
        self.ax_norm.set_ylabel('∫|ψ|² dx', color='#cccccc')

        self.t = 0.0
        self.anim = animation.FuncAnimation(
            self.fig, self._animate, interval=30, blit=False, cache_frame_data=False)

    def _animate(self, frame):
        try:
            for _ in range(8):
                self.psi = tasks.evolve_free_particle(self.psi, self.k, self.dt)
            self.t += 8 * self.dt
        except Exception:
            return

        prob = np.abs(self.psi)**2
        self.prob_line.set_ydata(prob)
        self.real_line.set_ydata(self.psi.real)
        norm = np.sum(prob) * self.dx
        self.norms.append(norm)
        self.norm_line.set_data(range(len(self.norms)), self.norms)
        if len(self.norms) > self.ax_norm.get_xlim()[1]:
            self.ax_norm.set_xlim(0, len(self.norms) + 50)
        self.time_text.set_text(f't = {self.t:.3f} | norm = {norm:.5f}')


# ============================================================
# UNIT TESTS
# ============================================================
class TestLevel3FreeParticle(unittest.TestCase):

    def setUp(self):
        from numpy.fft import fftfreq
        L  = 20.0
        N  = 1024
        self.x  = np.linspace(0, L, N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.k  = 2 * np.pi * fftfreq(N, d=self.dx)
        self.dt = 0.01
        self.k0 = 5.0
        self.psi0 = tasks.gaussian_packet(self.x, L / 2, 0.8, self.k0)

    def test_returns_array(self):
        psi_new = tasks.evolve_free_particle(self.psi0, self.k, self.dt)
        self.assertIsInstance(psi_new, np.ndarray)

    def test_norm_conserved(self):
        psi = self.psi0.copy()
        for _ in range(100):
            psi = tasks.evolve_free_particle(psi, self.k, self.dt)
        norm = np.sum(np.abs(psi)**2) * self.dx
        self.assertAlmostEqual(norm, 1.0, delta=1e-4,
                               msg="Free evolution must conserve norm (unitary).")

    def test_group_velocity(self):
        # After time T the peak should shift by v_g * T = (k0/m) * T
        T   = 1.0
        n_steps = int(T / self.dt)
        psi = self.psi0.copy()
        for _ in range(n_steps):
            psi = tasks.evolve_free_particle(psi, self.k, self.dt)
        peak_x = self.x[np.argmax(np.abs(psi)**2)]
        expected = self.x[np.argmax(np.abs(self.psi0)**2)] + self.k0 * T   # v_g = k0 in natural units
        self.assertAlmostEqual(peak_x, expected, delta=0.5,
                               msg="Wave packet group velocity should equal k0.")


# ============================================================
# STANDALONE
# ============================================================
if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level3FreeParticle()
        plt.show()
