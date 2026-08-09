import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint
import implementation_tasks as tasks
from base_level import BaseLevel


class Level4Glycolysis(BaseLevel):
    """Glycolytic oscillator with nullclines, vector field, eigenvalue panel and click-to-launch."""

    def __init__(self, fig=None):
        super().__init__(fig)

    def draw(self):
        self.fig.clear(); self.fig.patch.set_facecolor('#0f172a')
        grid = self.fig.add_gridspec(2, 3, hspace=.48, wspace=.40,
                                      width_ratios=[1, 1, 0.7])
        self.ax_time = self.fig.add_subplot(grid[0, 0])
        self.ax_phase = self.fig.add_subplot(grid[1, 0])
        self.ax_bif = self.fig.add_subplot(grid[:, 1])
        self.ax_eig = self.fig.add_subplot(grid[:, 2])
        self.axes = [self.ax_time, self.ax_phase, self.ax_bif, self.ax_eig]
        self._style_ax(self.ax_time, 'Concentrations', 'time', 'concentration')
        self._style_ax(self.ax_phase, 'Phase portrait  (click to launch)', 'glucose $G$', 'ATP')
        self._style_ax(self.ax_bif, 'Bifurcation diagram', '$K_m$', 'glucose $G$')
        self._style_ax(self.ax_eig, 'Eigenvalues', 'Re(λ)', 'Im(λ)')
        self.fig.subplots_adjust(bottom=.18, top=.92, left=.06, right=.97)

        self.Km, self.frame = 14., 0
        self.G0, self.A0 = 10.0, 5.0

        # Time series
        self.g_line, = self.ax_time.plot([], [], color='#ffcc66', lw=2, label='$G$')
        self.a_line, = self.ax_time.plot([], [], color='#55d6ff', lw=2, label='ATP')
        self.ax_time.legend(facecolor='#16213e', labelcolor='white', fontsize=8)

        # Phase portrait
        (self.phase_line,) = self.ax_phase.plot([], [], color='#a3ffb0', lw=1.3, alpha=0.35)
        self.phase_dot = self.ax_phase.scatter([], [], s=60, color='#ff5f87',
                                                edgecolors='white', zorder=8)
        self.fp_dot = self.ax_phase.scatter([], [], s=80, marker='x', color='#5fef7f',
                                             linewidths=2, zorder=9)

        # Bifurcation diagram
        self.max_line, = self.ax_bif.plot([], [], color='#ffcc66', lw=2, label='$G_{max/min}$')
        self.min_line, = self.ax_bif.plot([], [], color='#ffcc66', lw=2)
        self.fixed_line, = self.ax_bif.plot([], [], '--', color='#55d6ff', lw=1.7, label='$G^*$')
        self.km_marker = self.ax_bif.axvline(self.Km, color='#ff5f87', lw=2)
        self.ax_bif.legend(facecolor='#16213e', labelcolor='white', fontsize=7)

        # Eigenvalue panel
        self.eig_dots = self.ax_eig.scatter([], [], s=90, color='#c792ea',
                                             edgecolors='white', zorder=5)
        self.ax_eig.axvline(0, color='#ff5f87', lw=1, ls='--', alpha=0.6)
        self.ax_eig.axhline(0, color='#4c566a', lw=0.8, alpha=0.4)

        self.status = self.ax_bif.text(.03, .96, '', transform=self.ax_bif.transAxes,
                                        va='top', color='white', fontsize=8,
                                        bbox=dict(boxstyle='round,pad=.35', facecolor='#26354f',
                                                  edgecolor='none'))

        # Slider & buttons
        s_ax = self.fig.add_axes([.16, .065, .46, .028], facecolor='#26354f')
        self.slider = Slider(s_ax, '$K_m$', 10., 25., valinit=self.Km, color='#55d6ff')
        self.register_widget(self.slider)
        self.slider.on_changed(self._set_km)
        self.add_button([.74, .045, .16, .07], 'Play / Pause', self.toggle_animation)

        # Click-to-launch
        self.cids.append(self.fig.canvas.mpl_connect('button_press_event', self._launch))

        self._build_bifurcation()
        self._recompute()

    def _launch(self, event):
        if event.inaxes == self.ax_phase and event.xdata is not None:
            self.G0 = max(0.1, event.xdata)
            self.A0 = max(0.1, event.ydata)
            self._recompute()

    def _build_bifurcation(self):
        self.k_grid = np.linspace(10, 25, 28)
        span = np.linspace(0, 600, 1500)
        gmax, gmin, gfixed = tasks.bifurcation_sweep_km(self.k_grid, t_span=span)
        self.max_line.set_data(self.k_grid, gmax)
        self.min_line.set_data(self.k_grid, gmin)
        self.fixed_line.set_data(self.k_grid, gfixed)
        self.ax_bif.relim(); self.ax_bif.autoscale_view()

    def _set_km(self, value):
        self.Km = float(value); self._recompute()

    def _recompute(self):
        self.t = np.linspace(0, 500, 1600)
        self.sol = odeint(tasks.glycolysis_rhs, [self.G0, self.A0], self.t,
                          args=(self.Km, .36, .02, 6.))

        # Time series
        self.g_line.set_data(self.t, self.sol[:, 0])
        self.a_line.set_data(self.t, self.sol[:, 1])
        self.ax_time.relim(); self.ax_time.autoscale_view()

        # Phase portrait: rebuild with vector field + nullclines
        self.phase_line.set_data(self.sol[:, 0], self.sol[:, 1])
        for c in list(self.ax_phase.collections): c.remove()

        G_range = (0.1, max(40, np.max(self.sol[:, 0]) * 1.15))
        A_range = (0.1, max(15, np.max(self.sol[:, 1]) * 1.15))

        self.draw_vector_field(self.ax_phase, tasks.glycolysis_rhs,
                               G_range, A_range, nx=14, ny=12,
                               Km=self.Km, Vin=.36, k1=.02, kp=6.)
        self.draw_nullclines(self.ax_phase, tasks.glycolysis_rhs,
                             G_range, A_range, nx=250, ny=250,
                             Km=self.Km, Vin=.36, k1=.02, kp=6.,
                             labels=(r'$\dot{G}=0$', r'$\dot{A}=0$'))

        self.ax_phase.set_xlim(*G_range)
        self.ax_phase.set_ylim(*A_range)

        # Fixed point & eigenvalues
        try:
            G_star, A_star = tasks.glycolysis_fixed_point(self.Km)
            self.fp_dot.set_offsets([[G_star, A_star]])
            J = tasks.glycolysis_jacobian([G_star, A_star], self.Km)
            eig = np.linalg.eigvals(J)
            self.eig_dots.set_offsets(np.column_stack([eig.real, eig.imag]))
            max_re = np.max(eig.real)
            # Color eigenvalue dots
            col = '#ff5f5f' if max_re > 0.01 else '#5fef7f'
            self.eig_dots.set_facecolor(col)
            self.eig_dots.set_edgecolor('white')
            # Eigenvalue panel limits
            re_ext = max(0.05, abs(eig.real).max() * 1.5)
            im_ext = max(0.5, abs(eig.imag).max() * 1.3)
            self.ax_eig.set_xlim(-re_ext, re_ext)
            self.ax_eig.set_ylim(-im_ext, im_ext)
            self.draw_eigenvalue_badge(self.ax_eig, J)
            self.status.set_text(f'$K_m$ = {self.Km:.1f}\n'
                                 f'max Re(λ) = {max_re:.3g}')
        except ValueError:
            self.status.set_text(f'$K_m$ = {self.Km:.1f}\nno positive equilibrium')

        self.km_marker.set_xdata([self.Km, self.Km])
        self._update_frame(0)
        self.fig.canvas.draw_idle()

    def _update_frame(self, frame):
        i = int(frame) % len(self.t)
        self.phase_dot.set_offsets([self.sol[i]])

        # Ghost trail
        traj = self.sol[:, :2]
        self.draw_trail(self.ax_phase, traj, i, trail_length=80, cmap='spring')
        return self.phase_dot,


if __name__ == '__main__':
    level = Level4Glycolysis(); plt.show()
