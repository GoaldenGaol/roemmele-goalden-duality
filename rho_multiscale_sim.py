"""
rho_multiscale_sim.py

Toy multiscale simulation:
- Micro: agents with local plunder probability p_base
- Meso: trust matrix T(t)
- Macro: influence matrix W(t) and ρ(W(t))

Goal: show how different plunder regimes move ρ(t)
into different human bands (green/yellow/orange/red/black).

This is intentionally simple, not "realistic".
It's a testbed to connect the multiscale spec to numbers.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass

from graph_rho_law import compute_graph_rho, classify_human_rho


@dataclass
class SimulationConfig:
    N: int = 40                  # number of agents
    steps: int = 200             # time steps
    interactions_per_step: int = 200
    p_base: float = 0.01         # baseline plunder probability
    alpha_v: float = 0.05        # trust increase rate (voluntary)
    alpha_p: float = 0.20        # trust decrease rate (plunder)
    seed: int | None = 42        # RNG seed for reproducibility


@dataclass
class SimulationResult:
    config: SimulationConfig
    rho_series: np.ndarray       # shape (steps+1,)
    band_series: list[str]       # length steps+1
    A_series: np.ndarray         # authority over time
    D_series: np.ndarray         # diversity over time


def initialise_trust(N: int) -> np.ndarray:
    """
    Initial trust matrix T(0).

    Off-diagonal entries start at 0.5 (neutral),
    diagonal at 0.0 (we ignore self-interactions).
    """
    T = np.full((N, N), 0.5, dtype=float)
    np.fill_diagonal(T, 0.0)
    return T


def trust_to_weights(T: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """
    Convert trust matrix T into an influence matrix W.

    Simple choice: W = T normalised column-wise + small epsilon.
    """
    W = T.copy()
    # ensure non-negative
    W = np.clip(W, 0.0, None)

    col_sums = W.sum(axis=0, keepdims=True) + eps
    W = W / col_sums
    return W


def run_simulation(config: SimulationConfig) -> SimulationResult:
    rng = np.random.default_rng(config.seed)

    N = config.N
    T = initialise_trust(N)

    rho_series = []
    A_series = []
    D_series = []
    band_series: list[str] = []

    # initial macro state
    W0 = trust_to_weights(T)
    res0 = compute_graph_rho(W0)
    rho_series.append(res0.rho)
    A_series.append(res0.A)
    D_series.append(res0.D)
    band_series.append(classify_human_rho(res0.rho))

    for step in range(config.steps):
        # sample interactions (ordered pairs i != j)
        i_idx = rng.integers(0, N, size=config.interactions_per_step)
        j_idx = rng.integers(0, N, size=config.interactions_per_step)

        # enforce i != j
        mask_same = i_idx == j_idx
        while mask_same.any():
            i_idx[mask_same] = rng.integers(0, N, size=mask_same.sum())
            mask_same = i_idx == j_idx

        for i, j in zip(i_idx, j_idx):
            # local plunder probability (simple: uniform p_base for now)
            p_plunder = config.p_base

            if rng.random() < p_plunder:
                # plunder event j -> i
                # trust of i in j goes down
                T[i, j] = T[i, j] * (1.0 - config.alpha_p)
            else:
                # voluntary event j -> i
                # trust of i in j goes up
                T[i, j] = T[i, j] + config.alpha_v * (1.0 - T[i, j])

        # clip trust to [0, 1]
        T = np.clip(T, 0.0, 1.0)

        # update macro layer
        W = trust_to_weights(T)
        res = compute_graph_rho(W)

        rho_series.append(res.rho)
        A_series.append(res.A)
        D_series.append(res.D)
        band_series.append(classify_human_rho(res.rho))

    return SimulationResult(
        config=config,
        rho_series=np.asarray(rho_series),
        band_series=band_series,
        A_series=np.asarray(A_series),
        D_series=np.asarray(D_series),
    )


def summary(result: SimulationResult) -> str:
    rho = result.rho_series
    bands = result.band_series

    final_rho = rho[-1]
    final_band = bands[-1]

    return (
        f"N={result.config.N}, steps={result.config.steps}, "
        f"p_base={result.config.p_base:.3f}\n"
        f"  rho(0)   = {rho[0]:.6f}  band={bands[0]}\n"
        f"  rho(final)= {final_rho:.6f}  band={final_band}\n"
        f"  rho(min) = {rho.min():.6f}\n"
        f"  rho(max) = {rho.max():.6f}\n"
    )


if __name__ == "__main__":
    # Scenario 1: low plunder regime (should stay green / maybe yellow)
    low_cfg = SimulationConfig(p_base=0.01)
    low_res = run_simulation(low_cfg)
    print("=== Low plunder scenario ===")
    print(summary(low_res))

    # Scenario 2: medium plunder regime
    mid_cfg = SimulationConfig(p_base=0.05)
    mid_res = run_simulation(mid_cfg)
    print("=== Medium plunder scenario ===")
    print(summary(mid_res))

    # Scenario 3: high plunder regime
    high_cfg = SimulationConfig(p_base=0.15)
    high_res = run_simulation(high_cfg)
    print("=== High plunder scenario ===")
    print(summary(high_res))