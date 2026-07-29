import numpy as np
from numpy.fft import fft, ifft, fftfreq

# --- Natural units: hbar = m = 1 ---
hbar = 1.0
m    = 1.0

# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENTS 1-3)
# =============================================================================

def gaussian_packet(N, dx, x_start, x0, sigma, k0): #contains solution
    """
    Initializes a Gaussian wave packet.
    """
    x = x_start + np.arange(N) * dx
    psi = (1 / (2 * np.pi * sigma**2))**0.25 * \
          np.exp(-(x - x0)**2 / (4 * sigma**2)) * \
          np.exp(1j * k0 * x)
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi


def to_momentum_space(psi, dx): #contains solution
    """
    Compute the momentum-space wavefunction phi(k) using FFT.
    """
    N = len(psi)
    k = 2 * np.pi * fftfreq(N, d=dx)
    phi = fft(psi) * dx / np.sqrt(2 * np.pi)
    return k, phi


def to_position_space(phi, dx): #contains solution
    """
    Compute the position-space wavefunction psi(x) from phi(k) using IFFT.
    """
    psi = ifft(phi) / dx * np.sqrt(2 * np.pi)
    return psi


def evolve_free_particle(psi, dx, dt): #contains solution
    """
    Evolve psi by dt under the free-particle propagator.
    H = hbar^2 k^2 / (2m)  =>  phase = exp(-i hbar k^2 dt / 2m)
    """
    k, phi = to_momentum_space(psi, dx)
    phi = phi * np.exp(-1j * hbar * k**2 * dt / (2 * m))
    psi = to_position_space(phi, dx)
    return psi


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENT 4)
# =============================================================================

def split_operator_step(psi, V, dx, dt): #contains solution
    """
    One Trotter split-operator step:
    exp(-iHdt) ≈ exp(-iV dt/2) · exp(-iT dt) · exp(-iV dt/2)
    """
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    psi = evolve_free_particle(psi, dx, dt)
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    return psi


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENT 5)
# =============================================================================

def apply_absorbing_mask(psi, gobble_frac=0.1): #contains solution
    """
    Applies a sine-squared absorbing boundary mask to the wavefunction.
    """
    N = len(psi)
    mask = np.ones(N)
    gobble_width = int(gobble_frac * N)
    taper = np.sin(np.linspace(0, np.pi / 2, gobble_width))**2
    mask[:gobble_width]  = taper
    mask[-gobble_width:] = taper[::-1]
    return psi * mask


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENT 6)
# =============================================================================

def calculate_energy(psi, V, dx): #contains solution
    """
    Calculates <E> = <psi | H | psi>.
    """
    k, phi = to_momentum_space(psi, dx)
    kinetic_phi = (hbar**2 * k**2 / (2 * m)) * phi
    kinetic_psi = to_position_space(kinetic_phi, dx)
    
    K = np.sum(np.conj(psi) * kinetic_psi) * dx
    U = np.sum(np.conj(psi) * V * psi) * dx
    return np.real(K + U)


def kick_to_energy(psi, E_target, V, dx): #contains solution
    """
    Calculates the exact momentum kick required to reach E_target,
    and returns the phase-shifted wavefunction.
    """
    E_current = calculate_energy(psi, V, dx)
    
    # Calculate <p>
    k, phi = to_momentum_space(psi, dx)
    p_phi = hbar * k * phi
    p_psi = to_position_space(p_phi, dx)
    p_expected = np.real(np.sum(np.conj(psi) * p_psi) * dx)
    
    # Quadratic equation: p^2/2m + p*<p>/m + (E_current - E_target) = 0
    # Assuming m=1 for the discriminant:
    discriminant = p_expected**2 - 2 * m * (E_current - E_target)
    if discriminant < 0:
        return psi # Cannot reach this energy via real momentum kick!
        
    # We preserve the current direction of motion!
    if p_expected >= 0:
        p_kick = -p_expected + np.sqrt(discriminant)
    else:
        p_kick = -p_expected - np.sqrt(discriminant)
        
    x = np.arange(len(psi)) * dx
    return psi * np.exp(1j * p_kick * x / hbar)


def imaginary_time_step(psi, V, dx, dt_imag): #contains solution
    """
    One imaginary time step using the split-operator method, followed by re-normalization.
    """
    psi_decay = split_operator_step(psi, V, dx, -1j * dt_imag)
    norm = np.sqrt(np.sum(np.abs(psi_decay)**2) * dx)
    return psi_decay / norm


def project_out(psi, state, dx): #contains solution
    """
    Gram-Schmidt orthogonalization: psi_new = psi - <state | psi> * state
    """
    overlap = np.sum(np.conj(state) * psi) * dx
    psi_new = psi - overlap * state
    norm = np.sqrt(np.sum(np.abs(psi_new)**2) * dx)
    if norm > 1e-10:
        return psi_new / norm
    return psi_new


# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
