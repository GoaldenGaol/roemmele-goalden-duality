"""
graph_rho_law.py

Graph ρ-Law (v3) — compute authority, diversity, and ρ for influence graphs,
plus a minimal star–plunder toy model.

Nodes: 0..N-1
Weights: w_ij = influence from j -> i
"""

import math
from dataclasses import dataclass
from typing import Tuple, List

import numpy as np

RHO_CRITICAL = 0.7419  # universal instability threshold (conjectured)


@dataclass
class GraphRhoResult:
    A: float          # authority
    D: float          # diversity
    rho: float        # invariant A^2 * (1 - D)


def compute_authority(W: np.ndarray) -> float:
    """
    Authority A = max incoming fraction:

        A = max_j incoming_j / total_incoming

    where incoming_j = sum_i w_ij.

    W must be shape (N, N) with w_ij >= 0.
    """
    incoming = W.sum(axis=0)          # column sums: incoming to each node
    total = incoming.sum() + 1e-12
    return float(incoming.max() / total)


def compute_diversity(W: np.ndarray) -> float:
    """
    Diversity D = average normalized entropy of outgoing distributions.

    For each source j, we normalize the column W[:, j] to probabilities p_ij
    and compute H_j = -sum_i p_ij log p_ij, then normalize by log N and
    average over j.
    """
    N = W.shape[0]
    eps = 1e-12

    # columns are outgoing from j
    outgoing = W.copy()
    col_sums = outgoing.sum(axis=0) + eps
    P = outgoing / col_sums  # p_ij

    entropies = []
    for j in range(N):
        p = P[:, j]
        # avoid log(0)
        mask = p > 0
        Hj = -float((p[mask] * np.log(p[mask])).sum())
        entropies.append(Hj)

    H_avg = float(np.mean(entropies))
    H_max = math.log(N + eps)
    D = H_avg / H_max if H_max > 0 else 0.0
    return D


def compute_graph_rho(W: np.ndarray) -> GraphRhoResult:
    """
    Compute A, D, and ρ for a given weight matrix W.
    """
    A = compute_authority(W)
    D = compute_diversity(W)
    rho = A * A * (1.0 - D)
    return GraphRhoResult(A=A, D=D, rho=rho)


# ---------------------------------------------------------------------------
# Star–Plunder toy model
# ---------------------------------------------------------------------------

def star_plunder_matrix(N: int, p: float) -> np.ndarray:
    """
    Build the star–plunder weight matrix for N nodes and plunder parameter p.

    Node 0 is the hub. Each node emits total weight 1.

    - Hub (0) -> all nodes with weight 1/N each.
    - Non-hub j:
        weight p to hub,
        weight (1-p)/(N-1) to each non-hub.
    """
    W = np.zeros((N, N), dtype=float)

    # Hub column (outgoing from 0): uniform to all nodes
    W[:, 0] = 1.0 / N

    # Non-hub columns
    for j in range(1, N):
        # to hub
        W[0, j] = p
        # to non-hubs (including self)
        for i in range(1, N):
            W[i, j] = (1.0 - p) / (N - 1)

    return W


def demo_star_plunder(N: int = 10, ps: List[float] | None = None) -> None:
    """
    Demo: print A, D, and ρ for a range of plunder values p in [0,1].
    """
    if ps is None:
        ps = [0.0, 0.2, 0.5, 0.8, 0.9, 1.0]

    print(f"Star–plunder demo (N={N})")
    print("p\tA\t\tD\t\trho\t\t>rho_crit?")
    for p in ps:
        W = star_plunder_matrix(N, p)
        res = compute_graph_rho(W)
        print(
            f"{p:.2f}\t"
            f"{res.A:.4f}\t"
            f"{res.D:.4f}\t"
            f"{res.rho:.4f}\t"
            f"{res.rho > RHO_CRITICAL}"
        )


if __name__ == "__main__":
    demo_star_plunder()