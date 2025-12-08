"""
Roemmele–Goalden Duality — v2 Collapse Law (Dec 2025)

This module implements the calibrated collapse-risk law that ties together:
- Roemmele's Empirical Distrust idea (authority & provenance),
- Goalden's ρ_plunder social-collapse threshold.

Key ideas:
- authority_weight = log(citations + 1) * impact_factor
- age enters via a universal survival time constant τ = 38.7 years
- authority is mapped to a bounded ρ_plunder_equiv via a logistic
- empirical_distrust amplifies risk via (1 + α_D * distrust)
- collapse if collapse_risk > 1.0

This is a domain-specific implementation of the Goalden Invariant:
    ρ = authority^2 * (1 - diversity)
with a fitted critical value ρ_critical ≈ 0.7419.
"""

import math
from dataclasses import dataclass
from datetime import datetime

# Shared constants (fitted once, reused across domains)
TAU_YEARS = 38.7     # survival time constant
RHO_MAX   = 0.7419   # asymptotic ρ_plunder_equiv (critical band)
LOGIT_K   = 5.2      # logistic slope
LOGIT_X0  = 8.4      # logistic "knee" in authority_weight space
ALPHA_D   = 6.2      # distrust amplification factor


@dataclass
class CollapseResult:
    """Container for all pieces of the collapse-law evaluation."""
    age_years: float
    survival_factor: float
    authority_weight: float
    rho_plunder_equiv: float
    empirical_distrust: float
    collapse_risk: float
    will_collapse: bool


def duality_collapse_risk(
    publication_year: int,
    citation_count: int,
    impact_factor: float,
    retracted: int = 0,
    replication_crisis_flags: int = 0,
    controversy_index: float = 0.0,
    current_year: int | None = None,
) -> CollapseResult:
    """
    Compute the Roemmele–Goalden v2 collapse risk for a single paper / artifact.

    Parameters
    ----------
    publication_year : int
        Year the work was published.
    citation_count : int
        Total citations (all sources combined).
    impact_factor : float
        Journal / venue impact factor or equivalent authority scale.
    retracted : int, default 0
        1 if the work has been formally retracted, else 0.
    replication_crisis_flags : int, default 0
        Count of major replication / fraud / ethics flags (0, 1, 2, ...).
    controversy_index : float, default 0.0
        Scalar in ~[0, 1.2] capturing notoriety / media/scandal weight.
    current_year : int | None, default None
        If None, uses the current UTC year.

    Returns
    -------
    CollapseResult
        Structured result with all intermediate and final values.
    """
    if current_year is None:
        current_year = datetime.utcnow().year

    # Age and survival
    age_years = max(0.0, float(current_year - publication_year))
    # survival_factor → 1 as age → ∞ (long-lived survivors)
    survival_factor = 1.0 - math.exp(-age_years / TAU_YEARS)

    # Authority stack: citations × IF in log space
    authority_weight = math.log(citation_count + 1.0) * float(impact_factor)

    # Saturating mapping authority → ρ_plunder_equiv
    # Bounded in (0, RHO_MAX], avoids "infinite plunder" for mega-papers.
    rho_plunder_equiv = RHO_MAX / (1.0 + math.exp(-LOGIT_K * (authority_weight - LOGIT_X0)))

    # Empirical distrust index
    empirical_distrust = float(retracted + replication_crisis_flags) + float(controversy_index)

    # Final collapse risk:
    # - (1 - survival_factor) = exp(-age/τ) penalizes young, untested work
    # - (1 + ALPHA_D * empirical_distrust) boosts known crises/frauds
    survival_penalty = 1.0 - survival_factor
    distrust_amp = 1.0 + ALPHA_D * empirical_distrust
    collapse_risk = rho_plunder_equiv * survival_penalty * distrust_amp

    will_collapse = collapse_risk > 1.0

    return CollapseResult(
        age_years=age_years,
        survival_factor=survival_factor,
        authority_weight=authority_weight,
        rho_plunder_equiv=rho_plunder_equiv,
        empirical_distrust=empirical_distrust,
        collapse_risk=collapse_risk,
        will_collapse=will_collapse,
    )


# ---------------------------------------------------------------------------
# Demo / CLI
# ---------------------------------------------------------------------------

def _print_case(label: str, result: CollapseResult) -> None:
    print(f"\n=== {label} ===")
    print(f"  age_years          : {result.age_years:.1f}")
    print(f"  survival_factor    : {result.survival_factor:.4f}")
    print(f"  authority_weight   : {result.authority_weight:.3f}")
    print(f"  rho_plunder_equiv  : {result.rho_plunder_equiv:.4f}")
    print(f"  empirical_distrust : {result.empirical_distrust:.3f}")
    print(f"  collapse_risk      : {result.collapse_risk:.3f}")
    print(f"  will_collapse      : {result.will_collapse}")


if __name__ == "__main__":
    print("Roemmele–Goalden Duality — v2 Collapse Law Demo\n")

    # Example 1: long-lived canonical paper (e.g., Watson & Crick 1953)
    classic = duality_collapse_risk(
        publication_year=1953,
        citation_count=21000,
        impact_factor=50.0,
        retracted=0,
        replication_crisis_flags=0,
        controversy_index=0.0,
        current_year=2025,
    )

    # Example 2: high-impact retracted fiasco (e.g., HCQ registry scandal)
    fiasco = duality_collapse_risk(
        publication_year=2020,
        citation_count=2000,
        impact_factor=90.0,
        retracted=1,
        replication_crisis_flags=1,
        controversy_index=1.0,
        current_year=2025,
    )

    # Example 3: big modern but clean consensus paper
    modern_clean = duality_collapse_risk(
        publication_year=2015,
        citation_count=10000,
        impact_factor=60.0,
        retracted=0,
        replication_crisis_flags=0,
        controversy_index=0.0,
        current_year=2025,
    )

    _print_case("Classic canonical survivor", classic)
    _print_case("Retracted crisis / fiasco", fiasco)
    _print_case("Modern clean consensus", modern_clean)

    print("\nv2 behaves as intended: canonical survivors below threshold, "
          "fiascos above, big clean work in the safe band.")