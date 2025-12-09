"""
roemmele_goalden_collapse_v2.py

Roemmele–Goalden v2: scalar collapse risk for scientific authority systems.

This maps bibliometric quantities (citations, impact, retractions, controversy)
into a ρ-like plunder scalar bounded by the theoretical event horizon ρ_EVENT,
plus a dimensionless collapse_risk index.

Empirical calibration (Dec 2025):
- Real human fields / networks appear to become brittle in the ρ ≈ 0.02–0.03 band.
- Strong collapse / flash phenomena have only been seen near ρ ≈ 0.1 in social graphs.
- No human system observed has saturated the theoretical event horizon ρ_EVENT ≈ 0.7419.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

# Theoretical event horizon from the invariant / graph law
RHO_EVENT: float = 0.7419

# Rough human risk bands (scalar context, aligned with graph calibration)
RHO_HUMAN_LOW_MAX: float = 0.01    # typical "safe / open"
RHO_HUMAN_WARN_MAX: float = 0.03   # hype / brittle
RHO_HUMAN_HIGH_MAX: float = 0.05   # high risk
RHO_HUMAN_EXTREME_MAX: float = 0.10  # extreme / near-collapse


@dataclass
class CollapseResult:
    rho_plunder_equiv: float
    collapse_risk: float
    rho_band: Literal["low", "warn", "high", "extreme", "beyond"]
    # internal diagnostics
    authority_weight: float
    survival_factor: float
    empirical_distrust: float


def classify_rho_band(rho: float) -> Literal["low", "warn", "high", "extreme", "beyond"]:
    """
    Rough scalar risk bands, informed by empirical ρ calibration.

    - low:     ρ <= 0.01
    - warn:    0.01 < ρ <= 0.03
    - high:    0.03 < ρ <= 0.05
    - extreme: 0.05 < ρ <= 0.10
    - beyond:  ρ > 0.10 (no functioning systems observed here so far)
    """
    if rho <= RHO_HUMAN_LOW_MAX:
        return "low"
    if rho <= RHO_HUMAN_WARN_MAX:
        return "warn"
    if rho <= RHO_HUMAN_HIGH_MAX:
        return "high"
    if rho <= RHO_HUMAN_EXTREME_MAX:
        return "extreme"
    return "beyond"


def compute_collapse_risk_v2(
    publication_year: int,
    citation_count: int,
    impact_factor: float,
    retracted: int = 0,
    replication_crisis_flags: int = 0,
    controversy_index: float = 0.0,
    current_year: int = 2025,
    tau_years: float = 38.7,
    logistic_k: float = 5.2,
    logistic_center: float = 8.4,
    distrust_gain: float = 6.2,
) -> CollapseResult:
    """
    v2 scalar mapping from bibliometrics to a ρ-like plunder metric.

    Parameters
    ----------
    publication_year : int
        Year the paper (or canonical result) was published.
    citation_count : int
        Total citation count.
    impact_factor : float
        Journal impact factor or an analogous authority multiplier.
    retracted : int
        1 if retracted, else 0.
    replication_crisis_flags : int
        Count of replication crisis flags (meta-science concerns, failed replications).
    controversy_index : float
        Heuristic 0+ scalar summarising controversy intensity.
    current_year : int
        Year of evaluation.
    tau_years : float
        Time constant for the survival_factor; fitted once (≈38.7).
    logistic_k : float
        Slope of the authority → ρ logistic.
    logistic_center : float
        Authority value at the “knee” of the logistic.
    distrust_gain : float
        Gain on the empirical_distrust term in the final risk.

    Returns
    -------
    CollapseResult
        rho_plunder_equiv : ρ-like scalar in (0, RHO_EVENT]
        collapse_risk     : dimensionless risk index (relative, not absolute prob)
        rho_band          : qualitative band ("low".."beyond")
    """

    # 1. Authority weight: centralised authority measure
    citation_count = max(0, citation_count)
    impact_factor = max(0.0, impact_factor)
    authority_weight = math.log(citation_count + 1.0) * impact_factor

    # 2. Empirical distrust
    empirical_distrust = max(
        0.0,
        float(retracted) + float(replication_crisis_flags) + float(controversy_index),
    )

    # 3. Survival factor: older surviving results gain credibility
    age_years = max(0, current_year - publication_year)
    tau_years = max(tau_years, 1e-6)
    survival_factor = 1.0 - math.exp(-age_years / tau_years)

    # 4. Saturating authority → ρ mapping (bounded by event horizon)
    #    ρ_auth_raw ∈ (0, 1), then scaled by RHO_EVENT
    logistic_arg = logistic_k * (authority_weight - logistic_center)
    rho_auth_raw = 1.0 / (1.0 + math.exp(-logistic_arg))
    rho_plunder_equiv = RHO_EVENT * rho_auth_raw

    # 5. Collapse risk: high ρ, low survival, high distrust
    #    This is a relative index, not a universal probability.
    collapse_risk = rho_plunder_equiv * (1.0 - survival_factor) * (
        1.0 + distrust_gain * empirical_distrust
    )

    rho_band = classify_rho_band(rho_plunder_equiv)

    return CollapseResult(
        rho_plunder_equiv=rho_plunder_equiv,
        collapse_risk=collapse_risk,
        rho_band=rho_band,
        authority_weight=authority_weight,
        survival_factor=survival_factor,
        empirical_distrust=empirical_distrust,
    )


if __name__ == "__main__":
    # Example: modern high-authority, crisis-prone paper
    example = compute_collapse_risk_v2(
        publication_year=2020,
        citation_count=2000,
        impact_factor=90.0,
        retracted=1,
        replication_crisis_flags=1,
        controversy_index=1.0,
        current_year=2025,
    )
    print("Roemmele–Goalden v2 example:")
    print(f"  rho_plunder_equiv: {example.rho_plunder_equiv:.4f} (band={example.rho_band})")
    print(f"  collapse_risk:     {example.collapse_risk:.4f}")
    print(f"  authority_weight:  {example.authority_weight:.3f}")
    print(f"  survival_factor:   {example.survival_factor:.3f}")
    print(f"  empirical_distrust:{example.empirical_distrust:.3f}")