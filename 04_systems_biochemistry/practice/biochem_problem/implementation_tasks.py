import numpy as np
from scipy.integrate import odeint, solve_ivp

# =============================================================================
# LEVEL 1: Mass-Action Kinetics & Singular Perturbation (QSSA)
# =============================================================================

def full_enzyme_system_rhs(state, t, k1=1.0, k_minus1=1.0, kcat=1.0, Etot=0.1):  #contains solution
    """
    Computes derivatives [d[S]/dt, d[C]/dt] for full mass-action enzyme kinetics.
    
    Parameters:
        state: list or np.array of [S, C]
        t: float time
        k1, k_minus1, kcat, Etot: float reaction rates and total enzyme
    Returns:
        [dS/dt, dC/dt]
    """
    S, C = state
    E = Etot - C
    dS = -k1 * E * S + k_minus1 * C
    dC = k1 * E * S - (k_minus1 + kcat) * C
    return [dS, dC]


def qssa_reduced_rhs(state, t, k1=1.0, k_minus1=1.0, kcat=1.0, Etot=0.1):  #contains solution
    """
    Computes derivative d[S]/dt using Michaelis-Menten QSSA reduction.
    
    Parameters:
        state: float or list [S]
        t: float time
    Returns:
        [dS/dt] or float dS/dt
    """
    S = state[0] if isinstance(state, (list, np.ndarray)) else state
    Km = (k_minus1 + kcat) / k1
    Vmax = kcat * Etot
    dS = -Vmax * S / (Km + S)
    return [dS] if isinstance(state, (list, np.ndarray)) else dS


def compute_boundary_layer_error(eps_array):  #contains solution
    """
    Integrates full and QSSA systems for initial conditions [S]_0=1.0, [C]_0=0.0 up to t=10.0
    for each epsilon in eps_array (where Etot = eps * S0, S0=1.0).
    
    Returns array of L2 relative errors ||S_full - S_qssa||_2 / ||S_full||_2.
    """
    S0 = 1.0
    k1, k_minus1, kcat = 1.0, 1.0, 1.0
    t = np.linspace(0, 10.0, 200)
    errors = []
    
    for eps in eps_array:
        Etot = eps * S0
        sol_full = odeint(full_enzyme_system_rhs, [S0, 0.0], t, args=(k1, k_minus1, kcat, Etot))
        sol_qssa = odeint(qssa_reduced_rhs, [S0], t, args=(k1, k_minus1, kcat, Etot))
        
        S_full = sol_full[:, 0]
        S_qssa = sol_qssa[:, 0]
        
        err = np.linalg.norm(S_full - S_qssa) / (np.linalg.norm(S_full) + 1e-12)
        errors.append(err)
        
    return np.array(errors)


# =============================================================================
# LEVEL 2: Goldbeter-Koshland & Signaling Cascades
# =============================================================================

def goldbeter_koshland(v1, v2, K1, K2):  #contains solution
    """
    Explicit Goldbeter-Koshland formula for modified fraction y = [P*]/[P]tot.
    """
    B = v2 - v1 + v1 * K2 + v2 * K1
    numerator = 2 * v1 * K2
    denominator = B + np.sqrt(B**2 - 4 * (v2 - v1) * v1 * K2 + 1e-15)
    return float(numerator / denominator)


def frz_pathway_rhs(state, t, k=None, k_bar=None, K=None, K_bar=None, signal_boost=0.1):  #contains solution
    """
    3-variable ODE for Myxococcus xanthus Frz pathway ([Frz], [FrzCD], [FrzE]).
    """
    if k is None: k = [0.2, 0.2, 0.2]
    if k_bar is None: k_bar = [0.1, 0.1, 0.1]
    if K is None: K = [0.05, 0.05, 0.05]
    if K_bar is None: K_bar = [0.05, 0.05, 0.05]
    
    Frz, FrzCD, FrzE = state
    kb0 = k_bar[0] + (signal_boost if t > 30.0 else 0.0)
    
    dFrz = k[0] * (1.0 - FrzE) * (1.0 - Frz) / (1.0 - Frz + K[0]) - kb0 * Frz / (Frz + K_bar[0])
    dFrzCD = k_bar[1] * (1.0 - FrzCD) / (1.0 - FrzCD + K_bar[1]) - k[1] * (1.0 - Frz) * FrzCD / (FrzCD + K[1])
    dFrzE = k_bar[2] * (1.0 - FrzE) / (1.0 - FrzE + K_bar[2]) - k[2] * (1.0 - FrzCD) * FrzE / (FrzE + K[2])
    
    return [dFrz, dFrzCD, dFrzE]


# =============================================================================
# LEVEL 3: Synergetics & Haken's Slaving Principle
# =============================================================================

def synergetic_2d_rhs(state, t, gamma_u=0.1, gamma_v=2.0):  #contains solution
    """
    2D system: du/dt = gamma_u * u - u * v,  dv/dt = -gamma_v * v + u^2.
    """
    u, v = state
    du = gamma_u * u - u * v
    dv = -gamma_v * v + u**2
    return [du, dv]


def slaved_order_parameter_rhs(u, t, gamma_u=0.1, gamma_v=2.0):  #contains solution
    """
    Reduced 1D order parameter ODE: du/dt = gamma_u * u - (1/gamma_v) * u^3.
    """
    u_val = u[0] if isinstance(u, (list, np.ndarray)) else u
    du = gamma_u * u_val - (1.0 / gamma_v) * (u_val**3)
    return [du] if isinstance(u, (list, np.ndarray)) else du


def verify_manifold_collapse(initial_conditions, gamma_u=0.1, gamma_v=2.0, t_span=None):  #contains solution
    """
    Integrates 2D trajectories from initial_conditions [(u0, v0), ...] up to t_span[-1].
    Returns array of final distances |v(t_final) - u(t_final)^2 / gamma_v|.
    """
    if t_span is None:
        t_span = np.linspace(0, 10.0, 100)
        
    distances = []
    for u0, v0 in initial_conditions:
        sol = odeint(synergetic_2d_rhs, [u0, v0], t_span, args=(gamma_u, gamma_v))
        u_final, v_final = sol[-1, 0], sol[-1, 1]
        v_slaved = (u_final**2) / gamma_v
        dist = abs(v_final - v_slaved)
        distances.append(dist)
        
    return np.array(distances)


# =============================================================================
# LEVEL 4: Glycolytic Oscillations & Hopf Bifurcation
# =============================================================================

def glycolysis_rhs(state, t, Km=12.0, Vin=0.36, k1=0.02, kp=6.0):  #contains solution
    """
    Bier-Bakker-Westerhoff 2D glycolytic model:
        d[G]/dt = Vin - k1 * G * ATP
        d[ATP]/dt = 2 * k1 * G * ATP - kp * ATP / (ATP + Km)
    """
    G, ATP = state
    dG = Vin - k1 * G * ATP
    dATP = 2.0 * k1 * G * ATP - kp * ATP / (ATP + Km)
    return [dG, dATP]


def glycolysis_fixed_point(Km=12.0, Vin=0.36, k1=0.02, kp=6.0):  #contains solution
    """
    Return the positive steady state ``(G_star, ATP_star)`` of the
    Bier--Bakker--Westerhoff model.

    A positive steady state exists only when ``kp > 2 * Vin``. Raise
    ValueError otherwise, since the formula would not represent physical
    concentrations.
    """
    if kp <= 2.0 * Vin:
        raise ValueError("A positive steady state requires kp > 2 * Vin")
    ATP_star = 2.0 * Vin * Km / (kp - 2.0 * Vin)
    G_star = Vin / (k1 * ATP_star)
    return float(G_star), float(ATP_star)


def glycolysis_jacobian(state, Km=12.0, Vin=0.36, k1=0.02, kp=6.0):  #contains solution
    """Return the 2-by-2 Jacobian of ``glycolysis_rhs`` at ``state``."""
    G, ATP = state
    return np.array([
        [-k1 * ATP, -k1 * G],
        [2.0 * k1 * ATP, 2.0 * k1 * G - kp * Km / (ATP + Km)**2],
    ])

def calc_quiver_arrows(trajectory, threshold=0.5):  #contains solution
    """
    Sub-samples trajectory array (N x 2) to compute direction vectors [x, y, dx/norm, dy/norm]
    separated by at least threshold distance.
    """
    arrows = []
    diffs = np.diff(trajectory, axis=0)
    
    for i in range(len(diffs)):
        x, y = trajectory[i]
        dx, dy = diffs[i]
        use_point = True
        for ax, ay, dax, day in arrows:
            if (ax - x)**2 + (ay - y)**2 < threshold**2:
                use_point = False
                break
        if use_point:
            norm = np.sqrt(dx**2 + dy**2) + 1e-12
            arrows.append([x, y, dx / norm, dy / norm])
            
    return np.array(arrows).T if len(arrows) > 0 else np.empty((4, 0))


def bifurcation_sweep_km(Km_range, Vin=0.36, k1=0.02, kp=6.0, t_span=None):  #contains solution
    """
    Sweeps Km over Km_range, integrates glycolysis_rhs, discards transients,
    and returns (G_max, G_min, G_fixed).
    """
    if t_span is None:
        t_span = np.linspace(0.0, 600.0, 6000)
        
    G_max, G_min, G_fixed = [], [], []
    initial = [10.0, 5.0]
    
    for Km in Km_range:
        sol = odeint(glycolysis_rhs, initial, t_span, args=(Km, Vin, k1, kp))
        cutoff = int(len(sol) * 0.7)
        G_steady = sol[cutoff:, 0]
        G_max.append(np.amax(G_steady))
        G_min.append(np.amin(G_steady))
        fixed_val = (kp - 2.0 * Vin) / (2.0 * k1 * Km)
        G_fixed.append(fixed_val)
        
    return np.array(G_max), np.array(G_min), np.array(G_fixed)


# =============================================================================
# LEVEL 5: Biological Switches, Nullclines & Hysteresis
# =============================================================================

def bioswitch_rhs(state, t, S_func=None, params=None):  #contains solution
    """
    Tyson co-activation ODE model for [R] and [E].
    """
    if S_func is None: S_func = lambda time: 0.0
    if params is None:
        k_R = [0.22, 0.001]
        k_E = [0.8, 0.01]
        Km = [0.01, 0.01]
        Etot = 0.5
    else:
        k_R = params.get('k_R', [0.22, 0.001])
        k_E = params.get('k_E', [0.8, 0.01])
        Km = params.get('Km', [0.01, 0.01])
        Etot = params.get('Etot', 0.5)
        
    R, E = state
    S_val = S_func(t) if callable(S_func) else float(S_func)
    
    dR = k_R[0] * (Etot - E + S_val) - k_R[1] * R
    dE = k_E[0] * (Etot - E) / (Etot - E + Km[0]) - k_E[1] * R * E / (E + Km[1])
    return [dR, dE]


def gaussian_pulse(t, amp=0.05, center=10000.0, width=1000.0):  #contains solution
    """
    Evaluates gaussian stimulus pulse: amp * exp( -(t - center)^2 / (2 * width^2) ).
    """
    return float(amp * np.exp(-(t - center)**2 / (2.0 * width**2)))


def hysteresis_continuation(S_range, initial_low=None, initial_high=None, params=None):  #contains solution
    """
    Performs forward/backward continuation sweep over S_range to find R_high, R_low, and S_thr.
    """
    if initial_low is None: initial_low = [0.0, 0.0]
    if initial_high is None: initial_high = [200.0, 0.0]
    
    t_span = np.linspace(0.0, 50000.0, 1000)
    low_R, high_R = [], []
    
    for S in S_range:
        sol_low = odeint(bioswitch_rhs, initial_low, t_span, args=(lambda time: S, params))
        sol_high = odeint(bioswitch_rhs, initial_high, t_span, args=(lambda time: S, params))
        low_R.append(sol_low[-1, 0])
        high_R.append(sol_high[-1, 0])
        
    low_R = np.array(low_R)
    high_R = np.array(high_R)
    
    S_thr = S_range[-1]
    for _low, _high, _S in zip(low_R, high_R, S_range):
        if abs(_high - _low) < 1e-3:
            S_thr = _S
            break
            
    return high_R, low_R, float(S_thr)


# =============================================================================
# LEVEL 6: Morphogenesis & Spatial Synergetics (Turing Patterns)
# =============================================================================

def schnakenberg_pde_rhs(flat_state, t, a=0.1, b=0.9, Du=1.0, Dv=20.0, dx=1.0, N=50):  #contains solution
    """
    1D Schnakenberg reaction-diffusion PDE discretized using central finite differences.
    """
    u = flat_state[:N]
    v = flat_state[N:]
    
    # 2nd derivative Laplacian with periodic boundary conditions
    d2u = (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (dx**2)
    d2v = (np.roll(v, -1) - 2.0 * v + np.roll(v, 1)) / (dx**2)
    
    du = a - u + (u**2) * v + Du * d2u
    dv = b - (u**2) * v + Dv * d2v
    
    return np.concatenate([du, dv])


def analyze_turing_modes(spatial_u, dx=1.0):  #contains solution
    """
    Computes spatial FFT of 1D activator state spatial_u and returns dominant wavenumber k_max.
    """
    N = len(spatial_u)
    fft_vals = np.abs(np.fft.rfft(spatial_u - np.mean(spatial_u)))
    freqs = np.fft.rfftfreq(N, d=dx)
    k_vals = 2.0 * np.pi * freqs
    dominant_idx = np.argmax(fft_vals[1:]) + 1
    return float(k_vals[dominant_idx])


def schnakenberg_2d_pde_rhs_flat(t, flat_state, a=0.1, b=0.9, Du=1.0, Dv=20.0, dx=1.0, Nx=30, Ny=30):  #contains solution
    """
    2D Schnakenberg reaction-diffusion on an Nx×Ny grid with periodic BCs.
    State is a flat array of length 2*Nx*Ny (u then v).
    Uses vectorised Laplacian via np.roll for speed with solve_ivp.
    """
    N = Nx * Ny
    u = flat_state[:N].reshape(Nx, Ny)
    v = flat_state[N:].reshape(Nx, Ny)

    lap_u = (np.roll(u, 1, 0) + np.roll(u, -1, 0) +
             np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4.0 * u) / (dx**2)
    lap_v = (np.roll(v, 1, 0) + np.roll(v, -1, 0) +
             np.roll(v, 1, 1) + np.roll(v, -1, 1) - 4.0 * v) / (dx**2)

    du = a - u + (u**2) * v + Du * lap_u
    dv = b - (u**2) * v + Dv * lap_v

    return np.concatenate([du.ravel(), dv.ravel()])


def turing_dispersion_relation(k_array, a=0.1, b=0.9, Du=1.0, Dv=20.0):  #contains solution
    """
    Compute σ(k) — the largest eigenvalue of (J − D·k²) for each k.

    J is the Jacobian of the Schnakenberg reaction terms at the homogeneous
    steady state (u₀, v₀) = (a + b, b / (a + b)²).
    """
    u0 = a + b
    v0 = b / (u0**2)

    # Jacobian of reaction part
    fu = -1.0 + 2.0 * u0 * v0    # ∂f/∂u
    fv = u0**2                     # ∂f/∂v
    gu = -2.0 * u0 * v0           # ∂g/∂u
    gv = -(u0**2)                  # ∂g/∂v

    sigma = np.zeros_like(k_array, dtype=float)
    for idx, k in enumerate(k_array):
        k2 = k**2
        J = np.array([
            [fu - Du * k2, fv],
            [gu, gv - Dv * k2],
        ])
        eigs = np.linalg.eigvals(J)
        sigma[idx] = np.max(eigs.real)

    return sigma


# =============================================================================
# SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
