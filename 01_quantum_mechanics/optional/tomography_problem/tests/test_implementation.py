import pytest
import torch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks

def test_pt_split_operator_step():
    N = 256
    x = torch.linspace(-10, 10, N)
    psi = torch.exp(-(x**2) / 2) + 0j
    psi = psi / torch.sqrt(torch.sum(torch.abs(psi)**2))
    
    k_sq = torch.ones(N)
    V = torch.zeros(N)
    dt = 0.01
    
    psi.requires_grad = True
    
    psi_next = tasks.pt_split_operator_step(psi, k_sq, V, dt)
    assert psi_next.shape == (N,), f"Expected shape {(N,)}, got {psi_next.shape}"
    
    norm_diff = torch.abs(torch.sum(torch.abs(psi_next)**2) - 1.0)
    assert norm_diff < 1e-4, "Evolution is not unitary (norm not preserved)"
    
    loss = torch.sum(torch.abs(psi_next)**2)
    loss.backward()
    assert psi.grad is not None, "Gradients not flowing through pt_split_operator_step"

def test_grid_potential():
    N = 512
    model = tasks.GridPotential(N)
    
    out = model()
    assert out.shape == (N,), f"Expected shape {(N,)}, got {out.shape}"
    
    loss = out.sum()
    loss.backward()
    assert model.V_raw.grad is not None, "Gradients not flowing through GridPotential"

def test_run_teacher_forcing():
    N = 256
    V_pred = torch.zeros(N, requires_grad=True)
    
    # Mock some observations
    psi0 = torch.ones(N, dtype=torch.complex64)
    psi1 = torch.ones(N, dtype=torch.complex64) * 0.9
    
    observations = [(0, psi0), (10, psi1)]
    k_sq = torch.ones(N)
    dt = 0.01
    
    loss = tasks.run_teacher_forcing(V_pred, observations, psi0, k_sq, dt)
    assert loss.item() >= 0, "Loss should be non-negative"
    
    loss.backward()
    assert V_pred.grad is not None, "Gradients not flowing through run_teacher_forcing"
