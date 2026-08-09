import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint
import implementation_tasks as tasks
from base_level import BaseLevel


class Level2Ultrasensitivity(BaseLevel):
    """Goldbeter-Koshland ultrasensitivity with Hill coefficient and cascade response."""

    def __init__(self, fig=None):
        super().__init__(fig)

    def draw(self):
        self.fig.clear(); self.fig.patch.set_facecolor('#0f172a')
        grid = self.fig.add_gridspec(2, 2, height_ratios=[1.2, 1], hspace=.48, wspace=.35)
        self.ax_switch = self.fig.add_subplot(grid[:, 0])
        self.ax_signal = self.fig.add_subplot(grid[0, 1])
        self.ax_cascade = self.fig.add_subplot(grid[1, 1])
        self.axes = [self.ax_switch, self.ax_signal, self.ax_cascade]
        self._style_ax(self.ax_switch, 'Goldbeter–Koshland switch', r'$v_1/v_2$', 'modified fraction $y$')
        self._style_ax(self.ax_signal, 'Input pulse', 'time', 'signal boost')
        self._style_ax(self.ax_cascade, 'Frz cascade response', 'time', 'fraction')
        self.fig.subplots_adjust(bottom=.18, top=.90, left=.08, right=.96)
        self.K, self.boost, self.frame = .03, .14, 0
        self.ratio = np.linspace(.05, 2., 300)

        # Ghost comparison curves: store previous K values
        self._ghost_K_values = [0.5, 0.1, 0.01]

        # Main switch curve
        (self.switch_line,) = self.ax_switch.plot([], [], lw=2.6, color='#55d6ff',
                                                   label='current $K$')
        self.switch_dot = self.ax_switch.scatter([], [], s=60, color='#ffcc66', zorder=5)

        # Ghost comparison curves (drawn once)
        self._ghost_lines = []
        for gK in self._ghost_K_values:
            y_ghost = np.array([tasks.goldbeter_koshland(v, 1., gK, gK) for v in self.ratio])
            gl, = self.ax_switch.plot(self.ratio, y_ghost, lw=1.2, alpha=0.3,
                                      color='#aabbcc', ls=':', label=f'$K$={gK}')
            self._ghost_lines.append(gl)

        # Hill coefficient badge
        self.hill_text = self.ax_switch.text(.97, .55, '', transform=self.ax_switch.transAxes,
                                              ha='right', va='top', color='#ffcc66', fontsize=11,
                                              family='monospace',
                                              bbox=dict(boxstyle='round,pad=0.4',
                                                        facecolor='#1a1a2e', edgecolor='#ffcc66',
                                                        alpha=0.9))

        # Signal panel
        (self.signal_line,) = self.ax_signal.plot([], [], color='#ff5f87', lw=2)
        self.signal_dot = self.ax_signal.scatter([], [], s=40, color='#ffcc66', zorder=5)

        # Cascade panel
        cascade_colors = ['#55d6ff', '#a3ffb0', '#c792ea']
        self.cascade_lines = []
        for i, (name, col) in enumerate(zip(('Frz', 'FrzCD', 'FrzE'), cascade_colors)):
            ln, = self.ax_cascade.plot([], [], lw=2, label=name, color=col)
            self.cascade_lines.append(ln)
        self.cascade_dot = self.ax_cascade.scatter([], [], s=45, color='white', zorder=5)
        self.ax_cascade.legend(facecolor='#16213e', labelcolor='white', fontsize=8)

        self.status = self.ax_switch.text(.03, .96, '', transform=self.ax_switch.transAxes,
                                           va='top', color='white', fontsize=8,
                                           bbox=dict(boxstyle='round,pad=.35', facecolor='#26354f',
                                                     edgecolor='none'))

        self.ax_switch.legend(facecolor='#16213e', labelcolor='white', fontsize=7,
                               loc='lower right')

        # Sliders
        k_ax = self.fig.add_axes([.13, .065, .32, .028], facecolor='#26354f')
        b_ax = self.fig.add_axes([.55, .065, .20, .028], facecolor='#26354f')
        self.k_slider = Slider(k_ax, '$K$', .001, .5, valinit=self.K, color='#55d6ff')
        self.b_slider = Slider(b_ax, 'pulse', 0., .3, valinit=self.boost, color='#ff5f87')
        self.register_widget(self.k_slider); self.register_widget(self.b_slider)
        self.k_slider.on_changed(self._set_params)
        self.b_slider.on_changed(self._set_params)
        self.add_button([.79, .045, .15, .07], 'Play / Pause', self.toggle_animation)
        self._recompute()

    def _compute_hill_coefficient(self, K):
        """Estimate effective Hill coefficient from the GK curve slope at midpoint."""
        delta = 0.005
        y_plus = tasks.goldbeter_koshland(1.0 + delta, 1., K, K)
        y_minus = tasks.goldbeter_koshland(1.0 - delta, 1., K, K)
        slope = (y_plus - y_minus) / (2.0 * delta)
        # Hill coefficient: n_H ≈ 4 * slope (at midpoint where y=0.5, v1/v2=1)
        return max(1.0, 4.0 * slope)

    def _set_params(self, _value):
        self.K, self.boost = float(self.k_slider.val), float(self.b_slider.val)
        self._recompute()

    def _recompute(self):
        self.y = np.array([tasks.goldbeter_koshland(v, 1., self.K, self.K)
                           for v in self.ratio])
        self.t = np.linspace(0, 70, 350)
        self.signal = np.where(self.t > 30, self.boost, 0.)
        self.sol = odeint(tasks.frz_pathway_rhs, [.1, .1, .1], self.t,
                          args=([.2] * 3, [.1] * 3, [self.K] * 3, [self.K] * 3, self.boost))

        self.switch_line.set_data(self.ratio, self.y)
        self.signal_line.set_data(self.t, self.signal)
        for line, values in zip(self.cascade_lines, self.sol.T):
            line.set_data(self.t, values)

        # Hill coefficient
        nH = self._compute_hill_coefficient(self.K)
        self.hill_text.set_text(f'$n_H$ ≈ {nH:.1f}')

        self.ax_switch.set(xlim=(.05, 2), ylim=(-.03, 1.05))
        self.ax_signal.set(xlim=(0, 70), ylim=(-.02, max(.05, self.boost * 1.25)))
        self.ax_cascade.set(xlim=(0, 70), ylim=(-.05, 1.05))
        self.frame = 0
        self._update_frame(0)
        self.fig.canvas.draw_idle()

    def _update_frame(self, frame):
        i = int(frame) % len(self.t)
        ratio_now = .2 + 1.6 * i / (len(self.t) - 1)
        y_now = tasks.goldbeter_koshland(ratio_now, 1., self.K, self.K)
        self.switch_dot.set_offsets([[ratio_now, y_now]])
        self.signal_dot.set_offsets([[self.t[i], self.signal[i]]])
        self.cascade_dot.set_offsets([[self.t[i], self.sol[i, 2]]])
        slope = (tasks.goldbeter_koshland(1.01, 1., self.K, self.K) -
                 tasks.goldbeter_koshland(.99, 1., self.K, self.K)) / .02
        self.status.set_text(f'K = {self.K:.3f}\nlocal slope at 1 = {slope:.1f}')
        return self.switch_dot, self.signal_dot, self.cascade_dot


if __name__ == '__main__':
    level = Level2Ultrasensitivity(); plt.show()
