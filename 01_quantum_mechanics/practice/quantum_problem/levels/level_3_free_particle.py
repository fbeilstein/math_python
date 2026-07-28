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
        if self.psi is None: self.psi = np.zeros_like(self.x, dtype=complex)
        if self.psi is None: self.psi = np.zeros_like(self.x, dtype=complex)
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
                res = tasks.evolve_free_particle(self.psi, self.k, self.dt)
                if res is None: raise NotImplementedError("evolve_free_particle returned None")
                self.psi = res
            self.t += 8 * self.dt
            prob = np.abs(self.psi)**2
        except Exception:
            return
        self.prob_line.set_ydata(prob)
        self.real_line.set_ydata(self.psi.real)
        norm = np.sum(prob) * self.dx
        self.norms.append(norm)
        self.norm_line.set_data(range(len(self.norms)), self.norms)
        if len(self.norms) > self.ax_norm.get_xlim()[1]:
            self.ax_norm.set_xlim(0, len(self.norms) + 50)
        self.time_text.set_text(f't = {self.t:.3f} | norm = {norm:.5f}')



if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level3FreeParticle()
        plt.show()
