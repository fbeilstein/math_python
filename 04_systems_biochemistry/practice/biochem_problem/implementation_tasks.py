import numpy as np
from scipy.integrate import odeint

def calculate_pH(pKa: float, C_acid_init: float, C_base_init: float, V_add: float, C_titrant: float, is_acid: bool) -> float: #contains solution
    """
    Problem 1: Calculate the pH of a buffer after adding a strong titrant.

    Arguments:
    - pKa (float): pKa of the weak acid.
    - C_acid_init (float): Initial concentration of the weak acid.
    - C_base_init (float): Initial concentration of the conjugate base.
    - V_add (float): Volume of titrant added to 1L of buffer.
    - C_titrant (float): Concentration of the titrant.
    - is_acid (bool): True if titrant is a strong acid, False if strong base.
    
    Returns:
    - pH (float): The resulting pH.
    """
    n_acid = C_acid_init * 1.0
    n_base = C_base_init * 1.0
    n_titrant = V_add * C_titrant
    
    if is_acid:
        n_acid += n_titrant
        n_base -= n_titrant
    else:
        n_acid -= n_titrant
        n_base += n_titrant
        
    if n_base <= 0:
        excess_H = -n_base
        if excess_H == 0:
            return 7.0 
        return -np.log10(excess_H / (1 + V_add))
    elif n_acid <= 0:
        excess_OH = -n_acid
        if excess_OH == 0:
            return 7.0
        pOH = -np.log10(excess_OH / (1 + V_add))
        return 14.0 - pOH
        
    return pKa + np.log10(n_base / n_acid)

def analyze_inhibition(S_array: np.ndarray, V_no_inh: np.ndarray, V_with_inh: np.ndarray, I_conc: float) -> tuple[float, float, str, float]: #contains solution
    """
    Problem 2: Analyze enzyme inhibition using Lineweaver-Burk.
    
    Arguments:
    - S_array (np.ndarray): Substrate concentrations.
    - V_no_inh (np.ndarray): Velocities without inhibitor.
    - V_with_inh (np.ndarray): Velocities with inhibitor.
    - I_conc (float): The inhibitor concentration.
    
    Returns:
    - (Km_true, Vmax_true, type_str, calc_Ki) (tuple): 
        - Km_true (float): True Km.
        - Vmax_true (float): True Vmax.
        - type_str (str): 'competitive', 'uncompetitive', or 'noncompetitive'.
        - calc_Ki (float): Calculated inhibition constant.
    """
    inv_S = 1.0 / S_array
    inv_V_no = 1.0 / V_no_inh
    inv_V_with = 1.0 / V_with_inh
    
    m_no, c_no = np.polyfit(inv_S, inv_V_no, 1)
    m_with, c_with = np.polyfit(inv_S, inv_V_with, 1)
    
    Vmax_true = 1.0 / c_no
    Km_true = m_no * Vmax_true
    Vmax_app = 1.0 / c_with
    Km_app = m_with * Vmax_app
    
    tol = 1e-3
    if abs(c_no - c_with) < tol:
        type_str = 'competitive'
        calc_Ki = I_conc / (Km_app / Km_true - 1.0)
    elif abs(m_no - m_with) < tol:
        type_str = 'uncompetitive'
        calc_Ki = I_conc / (Vmax_true / Vmax_app - 1.0)
    else:
        type_str = 'noncompetitive'
        calc_Ki = I_conc / (Vmax_true / Vmax_app - 1.0)
        
    return Km_true, Vmax_true, type_str, calc_Ki

def frz_pathway_rhs(state: list, t: float, external_signal: float) -> list: #contains solution
    """
    Problem 3: Myxococcus xanthus C-signal pathway.
    
    Arguments:
    - state (list): [Frz, FrzCD, FrzE] relative concentrations.
    - t (float): Current time.
    - external_signal (float): Additive modifier to k_bar_0.
    
    Returns:
    - derivatives (list): [dFrz, dFrzCD, dFrzE]

    Parameters:
    - you can use the following parameters: 
    k0 = 1.0, k1 = 4.0, k2 = 4.0
    kbar0 = 0.08 + external_signal, kbar1 = 2.0, kbar2 = 2.0
    K0 = 0.005, K1 = 0.005, K2 = 0.005
    Kbar0 = 0.01, Kbar1 = 0.005, Kbar2 = 0.005
    """
    k0, k1, k2 = 1.0, 4.0, 4.0
    kbar0 = 0.08 + external_signal
    kbar1, kbar2 = 2.0, 2.0
    K0, K1, K2 = 0.005, 0.005, 0.005
    Kbar0, Kbar1, Kbar2 = 0.01, 0.005, 0.005
    
    Frz, FrzCD, FrzE = state
    
    dFrz = k0 * (1 - FrzE) * (1 - Frz) / (1 - Frz + K0) - kbar0 * Frz / (Frz + Kbar0)
    dFrzCD = kbar1 * (1 - FrzCD) / (1 - FrzCD + Kbar1) - k1 * (1 - Frz) * FrzCD / (FrzCD + K1)
    dFrzE = kbar2 * (1 - FrzE) / (1 - FrzE + Kbar2) - k2 * (1 - FrzCD) * FrzE / (FrzE + K2)
    
    return [dFrz, dFrzCD, dFrzE]

def glycolysis_rhs(state: list, t: float, Km: float) -> list: #contains solution
    """
    Problem 4: Yeast Glycolysis feedback loop (Bier model) RHS.
    
    Arguments:
    - state (list): [G, ATP] concentrations.
    - t (float): Current time.
    - Km (float): Michaelis constant.
    
    Returns:
    - derivatives (list): [dG, dATP]

    Parameters:
    - you can use the following parameters: 
    Vin = 0.36, k1 = 0.02, kp = 6.0
    """
    Vin, k1, kp = 0.36, 0.02, 6.0
    G, ATP = state
    dG = Vin - k1 * G * ATP
    dATP = 2 * k1 * G * ATP - kp * ATP / (ATP + Km)
    return [dG, dATP]

def glycolysis_fixed_point(Km: float) -> tuple: #contains solution
    """
    Problem 4: Yeast Glycolysis analytical fixed point.
    
    Arguments:
    - Km (float): Michaelis constant.
    
    Returns:
    - (G_eq, ATP_eq) (tuple): The fixed point coordinates.

    Parameters:
    - you can use the following parameters: 
    Vin = 0.36, k1 = 0.02, kp = 6.0
    """
    Vin, k1, kp = 0.36, 0.02, 6.0
    ATP_eq = (2 * Vin * Km) / (kp - 2 * Vin)
    G_eq = Vin / (k1 * ATP_eq)
    return (G_eq, ATP_eq)

def bioswitch_rhs(state: list, t: float, S: float) -> list: #contains solution
    """
    Problem 5: Bio-switch with Mutual Activation (Goldbeter-Koshland).
    Return the derivatives [dR/dt, dE/dt] for the zero-order ultrasensitivity switch.
    
    Arguments:
    - state (list): Current state [R, E].
    - t (float): Current time.
    - S (float): External stimulus S(t).
    
    Returns:
    - list: [dR/dt, dE/dt]

    Parameters:
    - k_R0 = 0.22, k_R1 = 0.001
    - k_E0 = 0.8, k_E1 = 0.01
    - K0 = 0.01, K1 = 0.01
    - E_tot = 0.5
    """
    R, E = state
    kR0, kR1 = 0.22, 0.001
    kE0, kE1 = 0.8, 0.01
    K0, K1 = 0.01, 0.01
    E_tot = 0.5
    
    Ep = E_tot - E
    dR = kR0 * Ep + S - kR1 * R
    dE = kE0 * Ep / (Ep + K0) - kE1 * R * E / (E + K1)
    
    return [dR, dE]

def cell_cycle_steady_state(cyclin: float, wee1: float, current_C: float) -> float: #contains solution
    """
    Problem 6: Cell Cycle Checkpoint (Cusp Catastrophe).
    Calculate the steady-state concentration(s) of active Cdc2.
    
    Arguments:
    - cyclin (float): Cyclin concentration (normal factor).
    - wee1 (float): Wee1 activity (splitting factor).
    - current_C (float): The system's current C value (for hysteresis).
    
    Returns:
    - float: The steady-state concentration of C.
    """
    # 1. Derive the ODE from the phenomenological diagram.
    # 2. To find the steady state(s), set dC/dt = 0 and solve for C.
    
    coefficients = [-1, 0, wee1, cyclin]
    roots = np.roots(coefficients)
    
    # Filter for real roots
    real_roots = np.real(roots[np.abs(np.imag(roots)) < 1e-5])
    
    # Hysteresis: select the real root closest to current state
    closest_root = real_roots[np.argmin(np.abs(real_roots - current_C))]
    return closest_root

if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here...
    unittest.main(verbosity=2)
