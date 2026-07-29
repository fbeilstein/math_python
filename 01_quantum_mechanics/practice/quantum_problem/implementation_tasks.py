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
    Create a normalized Gaussian wave packet on a uniform spatial grid.

        psi(x) = A * exp(-(x - x0)^2 / (4*sigma^2)) * exp(i*k0*x)

    where A is chosen so that the integral of |psi|^2 dx over the grid = 1.
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
    Uses the symmetric physicist convention (1/sqrt(2pi) scaling).
    """
    N = len(psi)
    k = 2 * np.pi * fftfreq(N, d=dx)
    phi = fft(psi) * dx / np.sqrt(2 * np.pi)
    return k, phi


def to_position_space(phi, dx): #contains solution
    """
    Compute the position-space wavefunction psi(x) from phi(k).
    Uses the symmetric physicist convention (1/sqrt(2pi) scaling).
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

def well_eigenfunction(x, n, L): #contains solution
    """
    n-th eigenfunction of the infinite square well [0, L].
    Normalized for integer n; boundary conditions break for non-integer n.
    """
    psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
    return psi


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENTS 5-6)
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


def dst_energy_levels(N, L): #contains solution
    """
    DST energy eigenvalues for infinite well: E_n = (n*pi/L)^2 / 2.
    """
    n_modes = np.arange(1, N + 1)
    E_k = (hbar**2 * (n_modes * np.pi / L)**2) / (2 * m)
    return E_k


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENT 7)
# =============================================================================

def absorbing_mask(N, gobble_frac=0.1): #contains solution
    """
    Sine-squared absorbing boundary mask (the Gobbler).
    """
    mask = np.ones(N)
    gobble_width = int(gobble_frac * N)
    taper = np.sin(np.linspace(0, np.pi / 2, gobble_width))**2
    mask[:gobble_width]  = taper
    mask[-gobble_width:] = taper[::-1]
    return mask


# =============================================================================
#  BONUS (EXTRA CREDIT)
# =============================================================================

def compute_tunneling_probability(V0, k0, a): #contains solution
    """
    Analytic tunneling transmission for a rectangular barrier.
    """
    E = hbar**2 * k0**2 / (2 * m)
    if E >= V0:
        return 1.0
    kappa = np.sqrt(2 * m * (V0 - E)) / hbar
    T = 1.0 / (1.0 + (V0**2 * np.sinh(kappa * a)**2) / (4 * E * (V0 - E)))
    return T


# =============================================================================
#  SELF-TESTING (add your own tests below)
# =============================================================================
if __name__ == '__main__':
    import unittest
    # Add your own unittest.TestCase classes here, then run:
    #     python implementation_tasks.py
    unittest.main(verbosity=2)
