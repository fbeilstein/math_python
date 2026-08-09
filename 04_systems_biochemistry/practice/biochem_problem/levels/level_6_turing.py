import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp
import implementation_tasks as tasks
from base_level import BaseLevel


class Level6Turing(BaseLevel):
    """2D Turing pattern formation with dispersion relation panel."""

    def __init__(self, fig=None):
        super().__init__(fig)

    def draw(self):
        self.fig.clear(); self.fig.patch.set_facecolor('#0f172a')
        grid = self.fig.add_gridspec(1, 2, width_ratios=[1.3, 1], wspace=.35)
        self.ax_space = self.fig.add_subplot(grid[0, 0])
        self.ax_spectrum = self.fig.add_subplot(grid[0, 1])
        self.axes = [self.ax_space, self.ax_spectrum]

        self._style_ax(self.ax_space, '2D Turing Pattern (Activator $u$)', 'x', 'y')
        self._style_ax(self.ax_spectrum, 'Dispersion Relation', 'wavenumber $k$', 'max Re(λ)')
        self.fig.subplots_adjust(bottom=.18, top=.90, left=.06, right=.97)

        # PDE parameters
        self.Nx, self.Ny = 30, 30
        self.Dv = 20.
        self.a, self.b, self.Du, self.dx = 0.1, 0.9, 1.0, 1.0
        self.seed = 42

        # 2D Heatmap
        self.image = self.ax_space.imshow(np.zeros((self.Nx, self.Ny)), aspect='equal',
                                          cmap='viridis', origin='lower',
                                          extent=[0, self.Nx, 0, self.Ny])
        self.fig.colorbar(self.image, ax=self.ax_space, fraction=0.046, pad=0.04)

        # Dispersion relation panel
        self.disp_line, = self.ax_spectrum.plot([], [], color='#ffcc66', lw=2.4)
        self.ax_spectrum.axhline(0, color='#ff5f87', lw=1, ls='--', alpha=0.8)
        self.k_marker = self.ax_spectrum.scatter([], [], s=80, color='#5fef7f',
                                                  edgecolors='white', zorder=5)

        self.status = self.ax_space.text(.02, .96, '', transform=self.ax_space.transAxes,
                                          va='top', color='white', fontsize=8,
                                          bbox=dict(boxstyle='round,pad=.35', facecolor='#26354f',
                                                    edgecolor='none'))

        # Slider & buttons
        s_ax = self.fig.add_axes([.15, .065, .35, .028], facecolor='#26354f')
        self.slider = Slider(s_ax, '$D_v/D_u$', 2., 40., valinit=self.Dv, color='#55d6ff')
        self.register_widget(self.slider)
        self.slider.on_changed(self._set_diffusion)
        self.add_button([.60, .045, .14, .07], 'New noise', self._new_noise, '#6c5ce7')
        self.add_button([.77, .045, .16, .07], 'Play / Pause', self.toggle_animation)

        self._simulate()

    def _set_diffusion(self, value):
        self.Dv = float(value); self._simulate()

    def _new_noise(self, _event=None):
        self.seed += 1; self._simulate()

    def _simulate(self):
        rng = np.random.default_rng(self.seed)
        u0_hom = self.a + self.b
        v0_hom = self.b / (u0_hom**2)

        N = self.Nx * self.Ny
        u0 = u0_hom + 0.05 * rng.standard_normal(N)
        v0 = v0_hom + 0.05 * rng.standard_normal(N)
        flat_init = np.concatenate([u0, v0])

        self.t_eval = np.linspace(0, 100, 150)
        # Using solve_ivp with explicit RK45 for the PDE (fast enough for 30x30 demo)
        res = solve_ivp(tasks.schnakenberg_2d_pde_rhs_flat,
                        (0, 100), flat_init, t_eval=self.t_eval,
                        args=(self.a, self.b, self.Du, self.Dv, self.dx, self.Nx, self.Ny),
                        method='RK45')
        self.sol = res.y[:N, :].T  # Only keep u (activator) for display

        # Dispersion relation
        k_max = np.pi  # max wavenumber on lattice
        self.k_array = np.linspace(0, k_max, 200)
        self.sigma = tasks.turing_dispersion_relation(self.k_array, self.a, self.b, self.Du, self.Dv)
        self.disp_line.set_data(self.k_array, self.sigma)

        # Find most unstable mode
        max_idx = np.argmax(self.sigma)
        self.dominant_k = self.k_array[max_idx]
        self.max_sigma = self.sigma[max_idx]

        self.k_marker.set_offsets([[self.dominant_k, self.max_sigma]])

        self.ax_spectrum.set_xlim(0, k_max)
        self.ax_spectrum.set_ylim(min(-0.2, np.min(self.sigma) * 1.1),
                                  max(0.1, self.max_sigma * 1.3))

        self.image.set_clim(np.min(self.sol), np.max(self.sol))

        self._update_frame(1)
        self.fig.canvas.draw_idle()

    def _update_frame(self, frame):
        i = max(0, int(frame) % len(self.t_eval))
        u_grid = self.sol[i].reshape(self.Nx, self.Ny)
        self.image.set_data(u_grid)

        t_val = self.t_eval[i]
        self.status.set_text(f'$D_v/D_u$ = {self.Dv:.1f}\nt = {t_val:.1f}\n'
                             f'dominant k = {self.dominant_k:.2f}')
        return self.image,


if __name__ == '__main__':
    level = Level6Turing(); plt.show()
