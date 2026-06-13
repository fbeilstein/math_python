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
import argparse
import sys

# Import student implementations (should fail if not done)
try:
    import implementation_tasks as tasks
    # natural units setup
    hbar, m = 1.0, 1.0
except ImportError as e:
    print(f"Error loading implementation_tasks.py: {e}")
    sys.exit(1)


def run_explorer(mode='barrier'):
    N = 1024
    sim_time = 0.0
    norms = []

    if mode == 'well':
        L = 20.0
        x = np.linspace(0, L, N, endpoint=False)
        dx = x[1] - x[0]
        try:
            E_k = tasks.dst_energy_levels(N, L)
            if E_k is None: raise NotImplementedError
        except Exception:
            E_k = np.zeros(N)

        x0, sigma_init, k0_init = L * 0.3, L * 0.05, 15.0
        dt = 0.005
        n_steps_per_frame = 10
        title = "True Infinite Well ($V=\\infty$)"

    elif mode in ('barrier', 'finite_well', 'scattering'):
        L = 40.0
        x = np.linspace(-L/2, L/2, N, endpoint=False)
        dx = x[1] - x[0]
        from numpy.fft import fftfreq
        k_grid = 2 * np.pi * fftfreq(N, d=dx)
        
        try:
            mask = tasks.absorbing_mask(N, gobble_frac=0.1)
            if mask is None: raise NotImplementedError
        except Exception:
            mask = np.ones(N)

        barrier_width = 0.5
        v0_init = 25.0
        x0, sigma_init, k0_init = -L * 0.25, 1.0, 10.0
        dt = 0.002
        n_steps_per_frame = 15
        title = "Quantum Tunneling & Scattering"

    # Build the initial wave packet
    try:
        psi = tasks.gaussian_packet(x, x0, sigma_init, k0_init)
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
    if mode in ('barrier', 'finite_well', 'scattering'):
        V = np.where(np.abs(x) < barrier_width / 2, v0_init, 0.0)
        
        # Potential visual overlay directly on main plot
        v_color = '#ff7043' if v0_init > 0 else '#4fc3f7'
        V_display_span = ax1.axvspan(-barrier_width/2, barrier_width/2, color=v_color, alpha=0.2)
        
        # Absorbing zones visual cue on main plot
        gw = int(0.1 * N)
        ax1.axvspan(x[0], x[gw], color='#e91e63', alpha=0.1)
        ax1.axvspan(x[-gw], x[-1], color='#e91e63', alpha=0.1)
    elif mode == 'well':
        # Infinite walls
        ax1.axvline(x[0], color='white', lw=4)
        ax1.axvline(x[-1], color='white', lw=4)
        ax1.axvspan(x[0]-L*0.1, x[0], color='#37474f', alpha=0.5)
        ax1.axvspan(x[-1], x[-1]+L*0.1, color='#37474f', alpha=0.5)
        ax1.set_xlim(x[0]-L*0.1, x[-1]+L*0.1)

    # Norm Plot
    norm_line, = ax2.plot([], [], color='#ce93d8', lw=1.5)
    ax2.set_xlim(0, 400)
    ax2.set_ylim(0.0, 1.1)
    ax2.set_xlabel('Calculation Frames', color='#cccccc')
    ax2.set_ylabel('∫|ψ|² dx', color='#cccccc')
    ax2.axhline(1.0, color='gray', ls='--', alpha=0.5)
    ax2.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

    # UI Controls
    ax_k0    = plt.axes([0.15, 0.16, 0.65, 0.03])
    ax_sigma = plt.axes([0.15, 0.11, 0.65, 0.03])
    slider_k0    = widgets.Slider(ax_k0, 'Momentum $k_0$', 2.0, 30.0, valinit=k0_init, color='#ffb74d')
    slider_sigma = widgets.Slider(ax_sigma, 'Width $\\sigma$', 0.5, 3.0, valinit=sigma_init, color='#81c784')

    slider_v0 = slider_a = None
    if mode in ('barrier', 'finite_well', 'scattering'):
        ax_v0 = plt.axes([0.15, 0.06, 0.65, 0.03])
        ax_a  = plt.axes([0.15, 0.01, 0.65, 0.03])
        slider_v0 = widgets.Slider(ax_v0, 'Potential $V_0$', -50.0, 50.0, valinit=v0_init, color='#ff7043')
        slider_a  = widgets.Slider(ax_a, 'Width $a$', 0.1, 5.0, valinit=barrier_width, color='#ba68c8')

    # Colorize slider text
    for s in [slider_k0, slider_sigma, slider_v0, slider_a]:
        if s:
            s.label.set_color('white')
            s.valtext.set_color('white')

    ax_btn = plt.axes([0.85, 0.06, 0.1, 0.05])
    btn_fire = widgets.Button(ax_btn, 'Fire Packet', color='#81c784', hovercolor='#66bb6a')

    def reset_sim(event=None):
        nonlocal psi, sim_time, norms, V, V_display_span, barrier_width
        sim_time = 0.0
        norms.clear()
        try:
            psi = tasks.gaussian_packet(x, x0, slider_sigma.val, slider_k0.val)
            if psi is None: raise NotImplementedError
        except Exception:
            psi = np.zeros(len(x), dtype=complex)
        
        if mode in ('barrier', 'finite_well', 'scattering') and slider_v0 and slider_a:
            barrier_width = slider_a.val
            V = np.where(np.abs(x) < barrier_width / 2, slider_v0.val, 0.0)
            if V_display_span:
                V_display_span.remove()
            v_color = '#ff7043' if slider_v0.val > 0 else '#4fc3f7'
            V_display_span = ax1.axvspan(-barrier_width / 2, barrier_width / 2, color=v_color, alpha=0.2)

    slider_k0.on_changed(reset_sim)
    slider_sigma.on_changed(reset_sim)
    btn_fire.on_clicked(reset_sim)
    if slider_v0:
        slider_v0.on_changed(reset_sim)
        slider_a.on_changed(reset_sim)

    def animate(frame):
        nonlocal psi, sim_time
        try:
            for _ in range(n_steps_per_frame):
                if mode == 'well':
                    from scipy.fft import dst, idst
                    psi_k = dst(psi, type=1, norm='ortho')
                    psi_k = psi_k * np.exp(-1j * E_k * dt)
                    psi = idst(psi_k, type=1, norm='ortho')
                else:
                    new_psi = tasks.split_operator_step(psi, k_grid, V, dt)
                    if new_psi is None: raise NotImplementedError
                    psi = new_psi
                    psi *= mask
            sim_time += n_steps_per_frame * dt
        except Exception:
            return prob_line, real_line, norm_line, time_text
            
        prob = np.abs(psi)**2
        prob_line.set_ydata(prob)
        real_line.set_ydata(psi.real)
        norm = np.sum(prob) * dx
        norms.append(norm)

        if len(norms) > ax2.get_xlim()[1]:
            ax2.set_xlim(0, len(norms) + 100)
        norm_line.set_data(range(len(norms)), norms)

        if mode in ('barrier', 'finite_well', 'scattering'):
            R = np.sum(prob[x < -barrier_width/2]) * dx
            T = np.sum(prob[x > barrier_width/2]) * dx
            
            # bonus overlay analytical T if barrier
            bonus_T = ""
            if mode == 'barrier' and hasattr(tasks, 'compute_tunneling_probability'):
                try:
                    t_an = tasks.compute_tunneling_probability(slider_v0.val, slider_k0.val, slider_a.val)
                    bonus_T = f" | T_exact: {t_an*100:04.1f}%"
                except Exception:
                    pass

            status = f't={sim_time:.2f} | R:{R*100:04.1f}% | T:{T*100:04.1f}%{bonus_T}'
        else:
            status = f't={sim_time:.3f} | norm={norm:.6f}'

        time_text.set_text(status)
        return prob_line, real_line, norm_line, time_text

    anim = animation.FuncAnimation(fig, animate, interval=30, blit=False, cache_frame_data=False)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['well', 'barrier', 'finite_well', 'scattering'], default='barrier')
    args = parser.parse_args()
    print(f"Launching Wave Explorer in {args.mode} mode...")
    run_explorer(args.mode)
