import numpy as np
from numpy.fft import fft, ifft, fftfreq
from scipy.fft import dst, idst

# --- Natural units: hbar = m = 1 ---
hbar = 1.0
m    = 1.0

# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENTS 1-3)
# =============================================================================

def gaussian_packet(x, x0, sigma, k0): #
    """
    Create a normalized Gaussian wave packet.

        psi(x) = A * exp(-(x - x0)^2 / (4*sigma^2)) * exp(i*k0*x)

    where A is chosen so that the integral of |psi|^2 dx over the grid = 1.
    """
    psi = (1 / (2 * np.pi * sigma**2))**0.25 * \
          np.exp(-(x - x0)**2 / (4 * sigma**2)) * \
          np.exp(1j * k0 * x)
    dx = x[1] - x[0]
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi


def momentum_wavefunction(psi, dx): #
    """
    Compute the momentum-space wavefunction phi(k) using FFT.
    Normalized so that integral |phi|^2 dk = 1.
    """
    N = len(psi)
    k = 2 * np.pi * fftfreq(N, d=dx)
    phi = fft(psi) * dx          # Riemann-sum approximation of Fourier integral
    dk = 2 * np.pi / (N * dx)
    phi /= np.sqrt(np.sum(np.abs(phi)**2) * dk)
    return k, phi


def evolve_free_particle(psi, k, dt): #
    """
    Evolve psi by dt under the free-particle propagator.
    H = hbar^2 k^2 / (2m)  =>  phase = exp(-i hbar k^2 dt / 2m)
    """
    psi_k = fft(psi)
    psi_k = psi_k * np.exp(-1j * hbar * k**2 * dt / (2 * m))
    return ifft(psi_k)


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENT 4)
# =============================================================================

def well_eigenfunction(x, n, L): #
    """
    n-th eigenfunction of the infinite square well [0, L].
    Normalized for integer n; boundary conditions break for non-integer n.
    """
    psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
    return psi


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENTS 5-6)
# =============================================================================

def split_operator_step(psi, k, V, dt): #
    """
    One Trotter split-operator step.
    exp(-iHdt) ≈ exp(-iV dt/2) · exp(-iT dt) · exp(-iV dt/2)
    """
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    psi_k = fft(psi)
    psi_k = psi_k * np.exp(-1j * hbar * k**2 * dt / (2 * m))
    psi = ifft(psi_k)
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    return psi


def dst_energy_levels(N, L): #
    """
    DST energy eigenvalues for infinite well: E_n = (n*pi/L)^2 / 2.
    """
    n_modes = np.arange(1, N + 1)
    E_k = (hbar**2 * (n_modes * np.pi / L)**2) / (2 * m)
    return E_k


# =============================================================================
#  STUDENT IMPLEMENTATION (ASSIGNMENT 7)
# =============================================================================

def absorbing_mask(N, gobble_frac=0.1): #
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

def compute_tunneling_probability(V0, k0, a): #
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
