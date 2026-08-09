import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button


class BaseLevel:
    """Shared interaction utilities for the Systems Biochemistry laboratory."""

    def __init__(self, fig=None):
        self.handles = {}
        self.dragging = None
        self.cids = []
        self.anim = None
        self._is_playing = False
        self._buttons = []
        self._play_buttons = []
        self._widgets = []

        if fig is None:
            self.fig, self.ax = plt.subplots(figsize=(9, 6))
        else:
            self.fig = fig
            self.fig.clear()
            self.ax = self.fig.add_subplot(111)
        self.axes = [self.ax]
        self.connect_events()

    def _style_ax(self, ax, title='', xlabel='', ylabel=''):
        ax.set_facecolor('#16213e')
        ax.set_title(title, color='white', fontsize=10, pad=8)
        ax.set_xlabel(xlabel, color='#d8dee9', fontsize=9)
        ax.set_ylabel(ylabel, color='#d8dee9', fontsize=9)
        ax.tick_params(colors='#d8dee9', labelsize=8)
        for spine in ax.spines.values():
            spine.set_color('#4c566a')
        ax.grid(True, color='#34405c', linestyle='--', alpha=0.55)

    # ----- reusable visual helpers -----

    def draw_trail(self, ax, trajectory, index, trail_length=40, cmap='plasma',
                   lw=2.6, alpha_max=0.85):
        """Render a fading comet-tail polyline behind the current dot."""
        start = max(0, index - trail_length)
        seg = trajectory[start:index + 1]
        if len(seg) < 2:
            return
        from matplotlib.collections import LineCollection
        points = seg.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        alphas = np.linspace(0.05, alpha_max, len(segments))
        import matplotlib.cm as mcm
        cm = mcm.get_cmap(cmap)
        colors = cm(np.linspace(0.25, 0.95, len(segments)))
        colors[:, 3] = alphas
        lc = LineCollection(segments, colors=colors, linewidths=lw, zorder=3)
        ax.add_collection(lc)

    def draw_vector_field(self, ax, rhs_func, xlim, ylim, nx=16, ny=16,
                          t=0.0, color='#8899bb', alpha=0.45, scale=None,
                          **rhs_kwargs):
        """Auto-generate a quiver plot with normalized arrows from any 2D RHS."""
        xs = np.linspace(xlim[0], xlim[1], nx)
        ys = np.linspace(ylim[0], ylim[1], ny)
        X, Y = np.meshgrid(xs, ys)
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        for i in range(ny):
            for j in range(nx):
                deriv = rhs_func([X[i, j], Y[i, j]], t, **rhs_kwargs)
                U[i, j], V[i, j] = deriv[0], deriv[1]
        mag = np.sqrt(U**2 + V**2) + 1e-12
        U, V = U / mag, V / mag
        ax.quiver(X, Y, U, V, mag, cmap='cool', alpha=alpha,
                  scale=scale or nx * 1.4, width=0.004, headwidth=3.5,
                  zorder=1)

    def draw_nullclines(self, ax, rhs_func, xlim, ylim, nx=200, ny=200,
                        t=0.0, colors=('#ff5f87', '#55d6ff'),
                        labels=('dx/dt = 0', 'dy/dt = 0'), lw=2.0,
                        **rhs_kwargs):
        """Draw dx/dt=0 and dy/dt=0 contours from any 2D RHS."""
        xs = np.linspace(xlim[0], ylim[1] if xlim[1] == ylim[1] else xlim[1], nx)
        ys = np.linspace(ylim[0], ylim[1], ny)
        xs = np.linspace(xlim[0], xlim[1], nx)
        X, Y = np.meshgrid(xs, ys)
        F = np.zeros_like(X)
        G = np.zeros_like(Y)
        for i in range(ny):
            for j in range(nx):
                d = rhs_func([X[i, j], Y[i, j]], t, **rhs_kwargs)
                F[i, j], G[i, j] = d[0], d[1]
        ax.contour(X, Y, F, levels=[0], colors=[colors[0]], linewidths=lw,
                   linestyles='--', zorder=2)
        ax.contour(X, Y, G, levels=[0], colors=[colors[1]], linewidths=lw,
                   linestyles='--', zorder=2)
        # legend proxies
        from matplotlib.lines import Line2D
        ax.legend(handles=[
            Line2D([], [], color=colors[0], ls='--', lw=lw, label=labels[0]),
            Line2D([], [], color=colors[1], ls='--', lw=lw, label=labels[1]),
        ], facecolor='#16213e', labelcolor='white', fontsize=7, loc='lower right')

    def draw_eigenvalue_badge(self, ax, jacobian_2x2, position=(0.97, 0.04),
                              fontsize=8):
        """Render a color-coded stability badge with Re(λ) values."""
        eigs = np.linalg.eigvals(jacobian_2x2)
        max_re = np.max(eigs.real)
        if max_re > 0.01:
            col, label = '#ff5f5f', 'UNSTABLE'
        elif max_re < -0.01:
            col, label = '#5fef7f', 'STABLE'
        else:
            col, label = '#ffcc66', 'MARGINAL'
        text = f'{label}\nλ = {eigs[0]:.3g}\nλ = {eigs[1]:.3g}'
        ax.text(position[0], position[1], text, transform=ax.transAxes,
                fontsize=fontsize, color=col, family='monospace',
                ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a2e',
                          edgecolor=col, alpha=0.9), zorder=10)

    def setup_axes(self, title='Sandbox', xlabel='x', ylabel='y'):
        self._style_ax(self.ax, title, xlabel, ylabel)

    def setup_dual_axes(self, title_left='', title_right='', xlabel_left='x', ylabel_left='y', xlabel_right='x', ylabel_right='y'):
        self.fig.clear()
        self.ax_left = self.fig.add_subplot(121)
        self.ax_right = self.fig.add_subplot(122)
        self.ax = self.ax_left
        self.axes = [self.ax_left, self.ax_right]
        self._style_ax(self.ax_left, title_left, xlabel_left, ylabel_left)
        self._style_ax(self.ax_right, title_right, xlabel_right, ylabel_right)

    def add_button(self, rect, label, callback, color='#2e86ab'):
        button_ax = self.fig.add_axes(rect)
        button = Button(button_ax, label, color=color, hovercolor='#4da3c7')
        button.label.set_color('white')
        button.on_clicked(callback)
        self._buttons.append(button)
        self._widgets.append(button)
        if label in {'Play / Pause', 'Play'}:
            self._play_buttons.append(button)
        return button

    def register_widget(self, widget):
        """Track a Matplotlib widget so it is safely disconnected on level changes."""
        self._widgets.append(widget)
        return widget

    def connect_events(self):
        self.cids.append(self.fig.canvas.mpl_connect('button_press_event', self.on_press))
        self.cids.append(self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion))
        self.cids.append(self.fig.canvas.mpl_connect('button_release_event', self.on_release))

    def disconnect_events(self):
        self.stop_animation()
        # Widgets keep their own canvas event connections and may retain a
        # mouse grab while a level is being switched. Release any capture first.
        grabber = self.fig.canvas.mouse_grabber
        if grabber is not None:
            self.fig.canvas.release_mouse(grabber)
        for widget in self._widgets:
            try:
                if self.fig.canvas.mouse_grabber == widget.ax:
                    self.fig.canvas.release_mouse(widget.ax)
                widget.disconnect_events()
            except (AttributeError, RuntimeError):
                pass
        self._widgets.clear()
        for cid in self.cids:
            self.fig.canvas.mpl_disconnect(cid)
        self.cids.clear()

    def on_press(self, event):
        if event.inaxes is None or event.xdata is None:
            return
        for name, pos in self.handles.items():
            handle_ax = getattr(self, '_handle_axes', {}).get(name, self.ax)
            if event.inaxes != handle_ax:
                continue
            xlim, ylim = handle_ax.get_xlim(), handle_ax.get_ylim()
            dx = (event.xdata - pos[0]) / (xlim[1] - xlim[0] + 1e-12)
            dy = (event.ydata - pos[1]) / (ylim[1] - ylim[0] + 1e-12)
            if np.hypot(dx, dy) < 0.05:
                self.dragging = name
                break

    def on_motion(self, event):
        if self.dragging and event.inaxes is not None and event.xdata is not None:
            handle_ax = getattr(self, '_handle_axes', {}).get(self.dragging, self.ax)
            if event.inaxes == handle_ax:
                self.handles[self.dragging] = np.array([event.xdata, event.ydata])
                self.redraw()

    def on_release(self, event):
        self.dragging = None

    def redraw(self):
        for ax in self.axes:
            ax.clear()
        self.draw()
        self.fig.canvas.draw_idle()

    def setup_animation(self, update_func, frames, interval=50):
        self._anim_update = update_func
        self._anim_frames = frames
        self._anim_interval = interval

    def _sync_play_labels(self):
        label = 'Pause' if self._is_playing else 'Play'
        for button in self._play_buttons:
            button.label.set_text(label)
        self.fig.canvas.draw_idle()

    def start_animation(self):
        if self.anim is None:
            update = getattr(self, '_anim_update', None)
            if update is None:
                update = getattr(self, '_update_frame', None)
            if update is None:
                raise RuntimeError('This level has no animation update function')
            frames = getattr(self, '_anim_frames', range(100000))
            interval = getattr(self, '_anim_interval', 45)
            self.anim = FuncAnimation(self.fig, update, frames=frames,
                                      interval=interval, repeat=True,
                                      blit=False, cache_frame_data=False)
        else:
            self.anim.event_source.start()
        self._is_playing = True
        self._sync_play_labels()

    def pause_animation(self):
        if self.anim is not None:
            self.anim.event_source.stop()
        self._is_playing = False
        self._sync_play_labels()

    def stop_animation(self):
        if self.anim is not None:
            self.anim.event_source.stop()
            # A stopped embedded animation may never receive a first GUI draw;
            # mark it as handled before releasing it to avoid a noisy warning.
            self.anim._draw_was_started = True
            self.anim = None
        self._is_playing = False
        self._sync_play_labels()

    def toggle_animation(self, _event=None):
        if self._is_playing:
            self.pause_animation()
        else:
            self.start_animation()

    def draw(self):
        raise NotImplementedError
