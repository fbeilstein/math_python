import torch
import torch.nn as nn

# =============================================================================
#  STUDENT IMPLEMENTATION
# =============================================================================

hbar = 1.0
m = 1.0


def pt_split_operator_step(psi, k_sq, V, dt): #contains solution
    """
    One Trotter split-operator step in PyTorch (differentiable).

    Same physics as np_split_operator_step, but using torch operations
    so that autograd can backpropagate through it.

    Args:
        psi:   (N,) complex tensor — wavefunction
        k_sq:  (N,) float tensor  — k^2 values (squared momentum grid)
        V:     (N,) float tensor  — potential
        dt:    float              — time step

    Returns:
        (N,) complex tensor — evolved wavefunction
    """
    psi = psi * torch.exp(-1j * V * dt / (2 * hbar))
    psi_k = torch.fft.fft(psi)
    psi_k = psi_k * torch.exp(-1j * hbar * k_sq * dt / (2 * m))
    psi = torch.fft.ifft(psi_k)
    psi = psi * torch.exp(-1j * V * dt / (2 * hbar))
    return psi


class GridPotential(nn.Module):
    """
    Learnable potential V(x) represented as a smoothed grid.

    The raw parameter V_raw is convolved with a small Gaussian kernel
    to prevent unphysical high-frequency ringing.
    """
    def __init__(self, n_points):
        """
        Create nn.Parameter for V_raw, build a fixed Gaussian
        smoothing kernel and register it as a buffer.
        """
        super().__init__()
        self.V_raw = nn.Parameter(torch.zeros(1, 1, n_points))
        
        # Gaussian kernel
        kernel_size = 11
        sigma = 1.5
        k_grid = torch.arange(kernel_size, dtype=torch.float32) - kernel_size // 2
        kernel = torch.exp(-k_grid**2 / (2 * sigma**2))
        kernel = kernel / kernel.sum()
        self.register_buffer('kernel', kernel.view(1, 1, -1))

    def forward(self): #contains solution
        """Return the smoothed potential as a 1D tensor of shape (n_points,)."""
        pad = self.kernel.size(-1) // 2
        V_padded = torch.nn.functional.pad(self.V_raw, (pad, pad), mode='replicate')
        V_smooth = torch.nn.functional.conv1d(V_padded, self.kernel)
        return V_smooth.squeeze()


def run_teacher_forcing(V_pred, psi_observations, psi0, k_sq, dt): #contains solution
    """
    Compute the teacher-forcing loss over sparse observations.

    For each pair of consecutive snapshots (psi_i, psi_{i+1}):
      1. Start from the TRUE state psi_i (teacher forcing)
      2. Propagate forward using pt_split_operator_step with V_pred
      3. Accumulate MSE loss against psi_{i+1}

    Args:
        V_pred:            (N,) tensor — current potential estimate
        psi_observations:  list of (step_idx, psi_tensor) tuples
        psi0:              (N,) complex tensor — initial wavefunction
        k_sq:              (N,) float tensor — k^2 grid
        dt:                float — time step

    Returns:
        scalar tensor — total loss
    """
    loss = 0.0
    for i in range(len(psi_observations) - 1):
        step_start = psi_observations[i][0]
        psi_start = psi_observations[i][1]
        step_end = psi_observations[i+1][0]
        psi_end_true = psi_observations[i+1][1]

        psi_step = psi_start.clone()
        for _ in range(step_end - step_start):
            psi_step = pt_split_operator_step(psi_step, k_sq, V_pred, dt)

        loss += torch.mean(torch.abs(psi_step - psi_end_true)**2)
        
    return loss


# =============================================================================
#  SELF-TESTING
# =============================================================================
if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
