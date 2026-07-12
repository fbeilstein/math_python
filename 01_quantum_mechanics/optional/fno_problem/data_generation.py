import torch
import numpy as np

# --- Natural units: hbar = m = 1 ---
hbar = 1.0
m    = 1.0

def gaussian_packet(x, x0, sigma, k0):
    """Normalized Gaussian wave packet (NumPy) for single inference usage."""
    if isinstance(x, torch.Tensor):
        x = x.cpu().numpy()
    norm = (np.pi * sigma ** 2) ** (-0.25)
    psi = norm * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) * np.exp(1j * k0 * x)
    return psi

def np_split_operator_step(psi, k, V, dt):
    """NumPy split-operator step for single inference usage."""
    from numpy.fft import fft, ifft
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    psi_k = fft(psi)
    psi_k = psi_k * np.exp(-1j * hbar * k**2 * dt / (2 * m))
    psi = ifft(psi_k)
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    return psi


class BatchedSSFM:
    """
    Batched SSFM solver running entirely on GPU via PyTorch.

    Generates random freeform potential landscapes and varying initial
    wavepackets, then propagates them to produce training pairs for the FNO.
    """
    def __init__(self, N_x=256, x_min=-10.0, x_max=10.0, dt=0.005, T_final=3.0, device='cuda'):
        self.N_x = N_x
        self.x_min = x_min
        self.x_max = x_max
        self.dt = dt
        self.T_final = T_final
        self.device = device

        self.x = torch.linspace(x_min, x_max, N_x, device=device)
        self.dx = (x_max - x_min) / N_x

        # Momentum grid for kinetic operator
        p = torch.fft.fftfreq(N_x, d=self.dx) * 2 * torch.pi
        self.p = p.to(device)

        self.steps = int(T_final / dt)
        self.K_op = torch.exp(-1j * (self.p ** 2 / 2) * dt)

    def generate_batch(self, batch_size=128, num_bumps=1):
        V = torch.zeros(batch_size, self.N_x, device=self.device)
        x_expanded = self.x.unsqueeze(0)

        # X0 in [-5.5, -4.5], P0 in [2.5, 3.5], SIGMA in [0.4, 0.6]
        X0 = (torch.rand(batch_size, 1, device=self.device) * 1.0) - 5.5
        P0 = (torch.rand(batch_size, 1, device=self.device) * 1.0) + 2.5
        SIGMA = (torch.rand(batch_size, 1, device=self.device) * 0.2) + 0.4

        norm = (torch.pi * SIGMA ** 2) ** (-0.25)
        gaussian = norm * torch.exp(-(x_expanded - X0) ** 2 / (2 * SIGMA ** 2))
        phase = torch.exp(1j * P0 * x_expanded)
        psi0_batch = (gaussian * phase).to(torch.complex64)

        for _ in range(num_bumps):
            heights = (torch.rand(batch_size, 1, device=self.device) * 30.0) - 15.0
            widths = torch.rand(batch_size, 1, device=self.device) * 0.8 + 0.2
            centers = torch.rand(batch_size, 1, device=self.device) * 2.0 - 1.0
            V += heights * torch.exp(-(x_expanded - centers) ** 2 / (2 * widths ** 2))

        V = torch.clamp(V, min=-15.0, max=15.0)

        history = []
        psi = psi0_batch.clone()
        V_op_half = torch.exp(-1j * V * (self.dt / 2))

        for step in range(1, self.steps + 1):
            psi = psi * V_op_half
            psi_f = torch.fft.fft(psi)
            psi_f = psi_f * self.K_op
            psi = torch.fft.ifft(psi_f)
            psi = psi * V_op_half

            if step % 10 == 0:
                history.append(psi.clone())

        psi_history = torch.stack(history, dim=1)
        return V, psi_history, psi0_batch
