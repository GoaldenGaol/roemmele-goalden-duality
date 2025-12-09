"""
graph_rho_law.py

Reference implementation of the graph-level ρ-invariant.

- ρ(W) = A(W)^2 * (1 - D(W))
- A(W): strongest node's incoming share
- D(W): average normalized entropy of outgoing distributions

This module also defines:
- RHO_EVENT_HORIZON: theoretical event horizon (~0.7419)
- Human "soft" bands (Dec 2025) for interpreting ρ in real systems
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

# Theoretical event horizon (universal ceiling from scalar law / synthetic graphs)
RHO_EVENT_HORIZON: float = 0.7419

# Empirical "soft" bands for human systems (Dec 2025, provisional)
HUMAN_GREEN_MAX: float = 0.01   # typical healthy / open
HUMAN_YELLOW_MAX: float = 0.03  # hype / brittle but functioning
HUMAN_ORANGE_MAX: float = 0.05  # high risk
HUMAN_RED_MAX: float = 0.10     # near-collapse; only rare systems near here


@dataclass
class GraphRhoResult:
    """Container for A, D, ρ for a given graph."""
    A: float          # authority (0–1)
    D: float          # diversity (0–1)
    rho: float        # rho = A^2 * (1 - D)


def compute_authority(W: np.ndarray) -> float:
    """
    Compute authority A(W) = max incoming fraction.

    Parameters
    ----------
    W : np.ndarray
        (N, N) weight matrix, w_ij >= 0, where w_ij is influence from j -> i.

    Returns
    -------
    float
        A(W) in [0, 1]. 0 if total influence is zero.
    """
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError("W must be a square (N, N) matrix")

    # Column sums: total outgoing from each source j, but also total incoming per source column
    incoming = W.sum(axis=0)  # shape (N,)
    total = incoming.sum()
    if total <= 0:
        return 0.0
    return float(incoming.max() / total)


def compute_diversity(W: np.ndarray, eps: float = 1e-12) -> float:
    """
    Compute diversity D(W) = average normalized entropy of outgoing distributions.

    For each source j:
      p_ij = w_ij / sum_i w_ij
      H_j = -sum_i p_ij log p_ij
      H_j_norm = H_j / log(N)
    Then:
      D = mean_j H_j_norm

    Parameters
    ----------
    W : np.ndarray
        (N, N) weight matrix, w_ij >= 0.
    eps : float
        Small constant to avoid division by zero and log(0).

    Returns
    -------
    float
        D(W) in [0, 1].
    """
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError("W must be a square (N, N) matrix")

    N = W.shape[0]
    if N <= 1:
        return 0.0

    # Column-wise normalisation to probabilities
    col_sums = W.sum(axis=0) + eps  # shape (N,)
    P = W / col_sums  # p_ij

    entropies = []
    for j in range(N):
        p = P[:, j]
        # mask to avoid log(0)
        mask = p > eps
        if not mask.any():
            entropies.append(0.0)
            continue
        Hj = -float((p[mask] * np.log(p[mask])).sum())
        entropies.append(Hj)

    H_avg = float(np.mean(entropies))
    H_max = math.log(N + eps)
    if H_max <= 0:
        return 0.0

    D = H_avg / H_max
    # Clip to [0, 1] for numerical stability
    return float(max(0.0, min(1.0, D)))


def compute_graph_rho(W: np.ndarray) -> GraphRhoResult:
    """
    Compute A(W), D(W), and ρ(W) for a given weight matrix W.

    Parameters
    ----------
    W : np.ndarray
        (N, N) weight matrix, w_ij >= 0, influence from j -> i.

    Returns
    -------
    GraphRhoResult
        A, D, rho for the given graph.
    """
    A = compute_authority(W)
    D = compute_diversity(W)
    rho = A * A * (1.0 - D)
    return GraphRhoResult(A=A, D=D, rho=rho)


def classify_human_rho(rho: float) -> Literal["green", "yellow", "orange", "red", "black"]:
    """
    Rough empirical classification of ρ for human systems (Dec 2025).

    Bands (provisional):
    - green : ρ <= 0.01    (healthy / open)
    - yellow: 0.01 < ρ <= 0.03 (hype / brittle but functioning)
    - orange: 0.03 < ρ <= 0.05 (high risk)
    - red   : 0.05 < ρ <= 0.10 (near-collapse; only rare systems near here)
    - black : ρ > 0.10    (no functioning system observed; likely flash-collapse)
    """
    if rho <= HUMAN_GREEN_MAX:
        return "green"
    if rho <= HUMAN_YELLOW_MAX:
        return "yellow"
    if rho <= HUMAN_ORANGE_MAX:
        return "orange"
    if rho <= HUMAN_RED_MAX:
        return "red"
    return "black"


def star_plunder_matrix(N: int, p: float) -> np.ndarray:
    """
    Construct the "star–plunder" test matrix.

    N nodes, node 0 is the hub, each node emits total weight 1.

    - Hub (0) sends uniformly to all nodes: w_i0 = 1/N
    - Non-hub j:
        weight p to hub (node 0),
        weight (1-p)/(N-1) to each non-hub (including itself).

    Parameters
    ----------
    N : int
        Number of nodes (>= 2).
    p : float
        Plunder parameter in [0, 1].

    Returns
    -------
    np.ndarray
        (N, N) weight matrix.
    """
    if N < 2:
        raise ValueError("N must be >= 2")
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0, 1]")

    W = np.zeros((N, N), dtype=float)

    # Hub column (outgoing from node 0): uniform
    W[:, 0] = 1.0 / N

    # Non-hub columns
    for j in range(1, N):
        # p fraction to hub
        W[0, j] = p
        # remaining (1 - p) spread over non-hubs (including self)
        for i in range(1, N):
            W[i, j] = (1.0 - p) / (N - 1)

    return W


if __name__ == "__main__":
    # Simple demo sweep for the star–plunder model
    N = 50
    ps = [0.0, 0.2, 0.5, 0.8, 0.9, 0.94, 0.96, 0.98, 1.0]

    print(f"Star–plunder demo (N={N})")
    print("p\tA\t\tD\t\trho\t\tband")
    for p in ps:
        W = star_plunder_matrix(N, p)
        res = compute_graph_rho(W)
        band = classify_human_rho(res.rho)
        print(
            f"{p:.2f}\t{res.A:.4f}\t{res.D:.4f}\t{res.rho:.6f}\t{band}"
        )