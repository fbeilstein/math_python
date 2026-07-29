"""
Quantum Wave Explorer
=======================
The grand finale demo application for the Wave Packet problem set.
Requires all functions in `implementation_tasks.py` to be completed to work.

Modes:
  --mode barrier       (Tunneling through rectangular barrier)
  --mode well          (Exact infinite square well bouncing)
  --mode finite_well   (Scattering/Bound states in a finite well)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.widgets as widgets
import sys
from scipy.ndimage import gaussian_filter1d

# Import student implementations (should fail if not done)
try:
    import implementation_tasks as tasks
    # natural units setup
    hbar, m = 1.0, 1.0
except ImportError as e:
    print(f"Error loading implementation_tasks.py: {e}")
    sys.exit(1)


def open_potential_editor(x_grid, current_V, callback, title="Potential Editor"):
    """Opens a dedicated Matplotlib window for potential editing."""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.tick_params(colors='#cccccc')
    for sp in ax.spines.values(): sp.set_edgecolor('#444466')
    ax.set_xlim(x_grid[0], x_grid[-1])
    ax.set_ylim(-50, 50)
    ax.set_xlabel("Position x", color='white')
    ax.set_ylabel("V(x)", color='white')
    ax.set_title(title, color='white')
    ax.axhline(y=0, color='#444466', linewidth=1)
    ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)
    
    plt.subplots_adjust(bottom=0.2)
    
    line, = ax.plot(x_grid, current_V, color='#ff7043', lw=3)
    
    V_state = current_V.copy()
    is_drawing = [False]
    drawing_mode = [False]
    last_point = [None]
    
    def update_plot():
        line.set_data(x_grid, V_state)
        fig.canvas.draw_idle()

    # Toolbar buttons
    ax_clear = plt.axes([0.05, 0.05, 0.1, 0.075])
    ax_barrier = plt.axes([0.16, 0.05, 0.12, 0.075])
    ax_f_well = plt.axes([0.29, 0.05, 0.12, 0.075])
    ax_i_well = plt.axes([0.42, 0.05, 0.12, 0.075])
    ax_draw = plt.axes([0.55, 0.05, 0.2, 0.075])
    ax_apply = plt.axes([0.76, 0.05, 0.15, 0.075])

    btn_clear = widgets.Button(ax_clear, 'Clear')
    btn_barrier = widgets.Button(ax_barrier, 'Barrier')
    btn_f_well = widgets.Button(ax_f_well, 'Finite Well')
    btn_i_well = widgets.Button(ax_i_well, 'Infinite Well')
    btn_draw = widgets.Button(ax_draw, 'Toggle Draw: OFF')
    btn_apply = widgets.Button(ax_apply, 'Apply & Close', color='#81c784', hovercolor='#66bb6a')

    def on_clear(val):
        V_state[:] = 0.0
        update_plot()
    
    def on_barrier(val):
        V_raw = np.where(np.abs(x_grid) < 0.5, 25.0, 0.0)
        V_state[:] = gaussian_filter1d(V_raw, sigma=1)
        update_plot()

    def on_f_well(val):
        V_raw = np.where(np.abs(x_grid) < 1.0, -25.0, 0.0)
        V_state[:] = gaussian_filter1d(V_raw, sigma=1)
        update_plot()
        
    def on_i_well(val):
        V_raw = np.where(np.abs(x_grid) < 15.0, 0.0, 250.0)
        V_state[:] = gaussian_filter1d(V_raw, sigma=2)
        update_plot()

    def on_draw(val):
        drawing_mode[0] = not drawing_mode[0]
        btn_draw.label.set_text(f"Toggle Draw: {'ON' if drawing_mode[0] else 'OFF'}")
        btn_draw.color = '#ffb74d' if drawing_mode[0] else '0.85'
        fig.canvas.draw_idle()

    def on_apply(val):
        callback(V_state.copy())
        plt.close(fig)

    btn_clear.on_clicked(on_clear)
    btn_barrier.on_clicked(on_barrier)
    btn_f_well.on_clicked(on_f_well)
    btn_i_well.on_clicked(on_i_well)
    btn_draw.on_clicked(on_draw)
    btn_apply.on_clicked(on_apply)

    # Keep a reference to buttons to prevent garbage collection
    fig._buttons = [btn_clear, btn_barrier, btn_f_well, btn_i_well, btn_draw, btn_apply]

    # Drawing event logic
    def on_press(event):
        if not drawing_mode[0] or event.inaxes != ax: return
        is_drawing[0] = True
        last_point[0] = (event.xdata, event.ydata)

    def on_motion(event):
        if not is_drawing[0] or event.inaxes != ax: return
        x1, y1 = last_point[0]
        x2, y2 = event.xdata, event.ydata
        
        if x1 == x2:
            idx = np.argmin(np.abs(x_grid - x1))
            V_state[idx] = y2
        else:
            xa, xb = (x1, x2) if x1 < x2 else (x2, x1)
            ya, yb = (y1, y2) if x1 < x2 else (y2, y1)
            
            mask = (x_grid >= xa) & (x_grid <= xb)
            if np.any(mask):
                V_state[mask] = ya + (yb - ya) * (x_grid[mask] - xa) / (xb - xa)
                
        last_point[0] = (event.xdata, event.ydata)
        line.set_data(x_grid, V_state)
        fig.canvas.draw_idle()

    def on_release(event):
        if not is_drawing[0]: return
        is_drawing[0] = False
        update_plot()

    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('button_release_event', on_release)

    plt.show(block=False)

def run_explorer():
    N = 1024
    sim_time = 0.0
    norms = []
    R_accumulated = 0.0
    T_accumulated = 0.0

    L = 40.0
    x = np.linspace(-L/2, L/2, N, endpoint=False)
    dx = x[1] - x[0]
    from numpy.fft import fftfreq
    k_grid = 2 * np.pi * fftfreq(N, d=dx)

    barrier_width = 0.5
    v0_init = 25.0
    x0, sigma_init, k0_init = -L * 0.25, 1.0, 10.0
    dt = 0.002
    n_steps_per_frame = 15
    
    title = "Quantum Scattering (Custom Potential)"
    V_custom = np.where(np.abs(x) < 0.5, 25.0, 0.0)

    # Build the initial wave packet
    try:
        psi = tasks.gaussian_packet(N, dx, x[0], x0, sigma_init, k0_init)
        if psi is None: raise NotImplementedError
    except Exception:
        psi = np.zeros(N, dtype=complex)

    # UI Layout
    fig = plt.figure(figsize=(12, 9))
    fig.patch.set_facecolor('#1a1a2e')
    gs = fig.add_gridspec(2, 1, height_ratios=[10, 3], hspace=0.2)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    fig.subplots_adjust(bottom=0.25)
    fig.suptitle(title, color='white', fontsize=14, fontweight='bold')

    for ax in (ax1, ax2):
        ax.set_facecolor('#16213e')
        ax.tick_params(colors='#cccccc')
        for sp in ax.spines.values(): sp.set_edgecolor('#444466')

    # Main plot
    prob_line, = ax1.plot(x, np.abs(psi)**2, color='#4fc3f7', lw=2, label='|ψ|²')
    real_line, = ax1.plot(x, psi.real, color='#81c784', lw=1, alpha=0.5, label='Re[ψ]')
    y_max = max(np.max(np.abs(psi)**2) * 2.5, 0.1)
    # Give a symmetric plot so that real wave part clipping does not happen
    ax1.set_ylim(-y_max, y_max)
    ax1.set_ylabel('|ψ(x)|²', color='#cccccc')
    ax1.grid(True, color='#2a2a4a', ls='--', alpha=0.6)
    ax1.legend(loc='upper right', fontsize=9, facecolor='#1a1a2e', labelcolor='white')

    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, color='#ffcc80',
                         fontsize=11, fontfamily='monospace', va='top',
                         bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

    V_display_span = None
    V_display_fill = None
    V = V_custom
    # Scale V for display: map max(V) to y_max
    v_max = max(np.max(V), 1e-5)
    V_display = V * (y_max * 0.8) / v_max
    V_display_fill = ax1.fill_between(x, 0, V_display, color='#ff7043', alpha=0.3)
    
    # Absorbing zones visual cue on main plot
    gw = int(0.1 * N)
    ax1.axvspan(x[0], x[gw], color='#e91e63', alpha=0.1)
    ax1.axvspan(x[-gw], x[-1], color='#e91e63', alpha=0.1)

    # Norm Plot
    norm_line, = ax2.plot([], [], color='#ce93d8', lw=1.5)
    ax2.set_xlim(0, 400)
    ax2.set_ylim(0.0, 1.1)
    ax2.set_xlabel('Calculation Frames', color='#cccccc')
    ax2.set_ylabel('On-screen ∫|ψ|² dx', color='#cccccc')
    ax2.axhline(1.0, color='gray', ls='--', alpha=0.5)
    ax2.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

    # UI Controls
    ax_k0    = plt.axes([0.15, 0.16, 0.65, 0.03])
    ax_sigma = plt.axes([0.15, 0.11, 0.65, 0.03])
    slider_k0    = widgets.Slider(ax_k0, 'Momentum $k_0$', 2.0, 20.0, valinit=k0_init, color='#ffb74d')
    slider_sigma = widgets.Slider(ax_sigma, 'Width $\\sigma$', 0.5, 2.0, valinit=sigma_init, color='#81c784')

    # Colorize slider text
    for s in [slider_k0, slider_sigma]:
        if s:
            s.label.set_color('white')
            s.valtext.set_color('white')

    ax_btn = plt.axes([0.85, 0.06, 0.1, 0.05])
    btn_fire = widgets.Button(ax_btn, 'Fire Packet', color='#81c784', hovercolor='#66bb6a')
    
    ax_btn_pot = plt.axes([0.72, 0.06, 0.12, 0.05])
    btn_pot = widgets.Button(ax_btn_pot, 'Edit Potential', color='#ffb74d', hovercolor='#ffa726')

    def reset_sim(event=None):
        nonlocal psi, sim_time, norms, V, V_display_span, V_display_fill, barrier_width, R_accumulated, T_accumulated
        sim_time = 0.0
        norms.clear()
        R_accumulated = 0.0
        T_accumulated = 0.0
        try:
            psi = tasks.gaussian_packet(N, dx, x[0], x0, slider_sigma.val, slider_k0.val)
            if psi is None: raise NotImplementedError
        except Exception:
            psi = np.zeros(len(x), dtype=complex)
        
        V = V_custom.copy()
        if V_display_fill:
            V_display_fill.remove()
        v_max = max(np.max(np.abs(V)), 1e-5)
        V_display = V * (y_max * 0.8) / v_max
        V_display_fill = ax1.fill_between(x, 0, V_display, color='#ff7043', alpha=0.3)

    slider_k0.on_changed(reset_sim)
    slider_sigma.on_changed(reset_sim)
    btn_fire.on_clicked(reset_sim)
    
    def apply_new_potential(new_V):
        nonlocal V_custom
        V_custom = new_V
        reset_sim()

    def open_editor_wrapper(event):
        open_potential_editor(x, V_custom, apply_new_potential)

    btn_pot.on_clicked(open_editor_wrapper)

    def animate(frame):
        nonlocal psi, sim_time, R_accumulated, T_accumulated
        try:
            for _ in range(n_steps_per_frame):
                new_psi = tasks.split_operator_step(psi, V, dx, dt)
                if new_psi is None: raise NotImplementedError
                
                prob_before = np.abs(new_psi)**2
                try:
                    psi = tasks.apply_absorbing_mask(new_psi, 0.1)
                except Exception:
                    psi = new_psi
                prob_after = np.abs(psi)**2
                
                loss = prob_before - prob_after
                gw = int(0.1 * N)
                R_accumulated += np.sum(loss[:gw]) * dx
                T_accumulated += np.sum(loss[-gw:]) * dx
                    
            sim_time += n_steps_per_frame * dt
        except Exception:
            return prob_line, real_line, norm_line, time_text
            
        prob = np.abs(psi)**2
        prob_line.set_ydata(prob)
        real_line.set_ydata(psi.real)
        norm = np.sum(prob) * dx
        
        norm_total = norm
            
        norms.append(norm_total)

        if len(norms) > ax2.get_xlim()[1]:
            ax2.set_xlim(0, len(norms) + 100)
        norm_line.set_data(range(len(norms)), norms)

        R = R_accumulated
        T = T_accumulated
        status = f't={sim_time:.2f} | R:{R*100:04.1f}% | T:{T*100:04.1f}%'

        time_text.set_text(status)
        return prob_line, real_line, norm_line, time_text

    anim = animation.FuncAnimation(fig, animate, interval=30, blit=False, cache_frame_data=False)
    plt.show()


if __name__ == '__main__':
    print("Launching Wave Explorer in Custom Scattering mode...")
    run_explorer()
