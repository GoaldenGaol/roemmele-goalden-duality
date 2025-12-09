ρ-Stack Overview — From Invariant to Dynamics (Dec 2025)

This document summarizes the current ρ-stack:

  1. Level 0 — Invariant (Raw ρ-Law)
  2. Level 1 — v2 Roemmele–Goalden Collapse Law (Scalar Implementation)
  3. Level 2 — Graph ρ-Law (v3 Static)
  4. Level 3 — ρ-Dynamics (v3 Dynamics / Critical Ratio)
  5. Empirical Calibration & Human Bands (Wave-2 Updated)

Public repos contain the math and reference code. Private repos contain P-scanner pipelines, datasets, and domain-specific heuristics.


================================
Level 0 — Raw Invariant
================================

Definition:

    ρ = (authority)² · (1 − evidence_diversity),

with a universal event-horizon constant:

    ρ_EH ≈ 0.7419.

Intuition (domain-agnostic):

- authority: domain-specific measure of centralised control / dominance  
  (e.g., citations × impact factor, dark-energy fraction, copy number, hub centrality).
- evidence_diversity: domain-specific measure of independent paths / modes  
  (e.g., independent data sources, matter fraction, novelty, residual uncertainty).

Interpretation (theoretical):

- ρ ≪ ρ_EH : open futures, structure still forming; influence and evidence remain distributed.
- ρ ≈ ρ_EH : event-horizon regime where almost all paths route through one effective center.
- ρ > ρ_EH : not expected for functioning influence systems; mathematically corresponds to “no more interesting structure.”

Empirical fact (Dec 2025): in real human systems sampled so far, ρ remains far below ρ_EH. Human systems destabilise or change long before reaching this theoretical ceiling; see “Empirical Calibration & Human Bands” below.


================================
Level 1 — v2 Roemmele–Goalden Collapse Law (Scalar)
================================

File: roemmele_goalden_collapse_v2.py

Implements a scalar collapse law for scientific authority systems that maps bibliometric quantities into a ρ-like risk.

Inputs (per paper / topic):

- publication_year
- citation_count
- impact_factor
- retracted (0/1)
- replication_crisis_flags
- controversy_index (0–something)

Core pieces:

- Authority:

      authority_weight = log(citations + 1) × impact_factor

- Age survival factor:

      survival_factor = 1 − exp(−age_years / τ),    τ ≈ 38.7

- Empirical distrust:

      empirical_distrust = retracted + rep_flags + controversy_index

- Saturating mapping to a ρ-like scale bounded by the event horizon:

      ρ_plunder_equiv ∈ (0, ρ_EH]

  with a logistic “knee” tuned once from backtests.

Outputs:

- ρ_plunder_equiv  (ρ-like scalar in [0, ρ_EH]),
- collapse_risk     (dimensionless risk index),
- a qualitative band (“low / warn / high / extreme / beyond”) aligned with human bands from the graph law.

Important: v2 treats ρ_EH as a theoretical ceiling. Empirical calibration suggests that human systems already look pathological in much lower bands (≈0.05–0.10 for some domains), long before saturating the logistic. The scalar law’s ρ_plunder_equiv is therefore best interpreted relative to the empirical human bands, not as a direct “hit 0.7419 = instant collapse” rule.


================================
Level 2 — Graph ρ-Law (v3 Static)
================================

Files: GRAPH_RHO_LAW.md, graph_rho_law.py

We lift ρ from a scalar rule to a functional on influence graphs.

System at time t:

- Weighted directed graph W(t) = [w_ij(t)]
- w_ij(t) ≥ 0 : influence from node j → i

Definitions:

- Authority:

      A(t) := max_j [ Σ_i w_ij(t) / Σ_{i,k} w_ik(t) ]

  i.e. the strongest hub’s share of total incoming influence.

- Diversity:

  1. Normalize columns to probabilities p_ij(t):
     
         p_ij(t) = w_ij(t) / Σ_i w_ij(t)
  
  2. Node entropies:
     
         H_j(t) = − Σ_i p_ij(t) log p_ij(t)
  
  3. Global diversity:
     
         D(t) := (1 / (N log N)) Σ_j H_j(t) ∈ [0, 1]

- Graph ρ:

      ρ(t) := A(t)² · (1 − D(t))

Star–Plunder Model (sanity check):

- N-node graph with a single hub and a plunder parameter p ∈ [0, 1].
- As p increases (more centralisation, more traffic into the hub), ρ increases monotonically.
- For moderate N (e.g. N = 50), ρ only approaches ≈0.7 when >90–95% of all influence flows into the hub, consistent with ρ_EH as an “almost total” centralisation regime.

Level 2 = “given a real network W, compute A, D, ρ and compare to both the event horizon and the empirically calibrated human bands.”


--------------------------------
Human Bands (v3.1 — with Wave-2 Calibration)
--------------------------------

We keep the same numeric bands as in v3, but the interpretation is now explicitly domain- and scale-dependent (based on wave-2 calibration):

- **green** : ρ ≤ 0.01  
  - Very low centralisation, high diversity.  
  - Empirically: systems with ρ < 0.005–0.01 have not been seen to collapse quickly; long-lived citation fields and many open communities live here comfortably.

- **yellow** : 0.01 < ρ ≤ 0.03  
  - Mild centralisation, still high diversity.  
  - “Brittle / hype” in some domains (fast-moving social or scientific trends), but many systems (e.g. Wikipedia, large email graphs) can remain stable here for years.

- **orange** : 0.03 < ρ ≤ 0.05  
  - Noticeable centralisation; multiple hubs or cliques dominate.  
  - In small/medium social or financial systems, this often correlates with emerging fragility or conflict, but is not yet a universal “doom” band.

- **red** : 0.05 < ρ ≤ 0.10  
  - Strong centralisation: a small set of nodes controls a large fraction of paths.  
  - For small/medium social or financial systems (e.g., pump-and-dump groups), values near the upper red range have been observed shortly before failure.  
  - For massive web-scale infrastructure (e.g., Web-Google with ρ ≈ 0.089 unweighted), red can coexist with long-term stability due to huge N and redundancy.

- **black** : ρ > 0.10  
  - Extreme centralisation / unexplored regime.  
  - No clearly stable meso-scale human institutions have been observed above ~0.12, but some web-scale weighting choices push web graphs into ≈0.11–0.12 without immediate collapse.  
  - Treat black as a serious warning signal that requires careful interpretation of:
    - domain (academic vs social vs web vs governance),
    - scale (small/medium vs global web),
    - and how W was constructed (weights, directions, signed edges).

For the detailed dataset list and second-wave results, see RHO_CALIBRATION_WAVE2.md. Future calibration waves should refine these bands rather than changing the invariant itself.


================================
Level 3 — ρ-Dynamics (v3 Dynamics / Critical Ratio)
================================

File: RHO_DYNAMICS.md

We model the time evolution of ρ as the competition between:

- Voluntary exchange (decentralising: ρ ↓),
- Plunder (centralising: ρ ↑).

At the graph level:

- Voluntary exchange ⇒  Ẋ:

      Ẋ:  dot{A} ≤ 0, dot{D} ≥ 0  ⇒ dot{ρ} ≤ 0

- Plunder ⇒

      dot{A} ≥ 0, dot{D} ≤ 0  ⇒ dot{ρ} ≥ 0

A coarse-grained evolution law:

    dot{ρ} = α(1 − ρ) − βρ,

with:

- α : plunder intensity (net centralising force),
- β : voluntary / anti-plunder intensity (net decentralising force).

Fixed point:

    ρ* = α / (α + β).

If we equate ρ* with the event horizon, we get the “event ratio”:

    (α/β)_EH = ρ_EH / (1 − ρ_EH) ≈ 2.875.

Empirically, current human systems appear to have |α/β| ≪ 1, i.e. they live far inside the open regime and drift in ρ is typically very slow.

Level 3 = “given ρ(t) over time, estimate α/β and see how far you are from the event-horizon ratio; then compare to human soft thresholds and domain-specific interpretations.”


================================
Empirical Calibration & Human Bands (Dec 2025, Wave 2)
================================

Early tests across 50+ real-world influence networks (citation graphs from OpenAlex/Semantic Scholar/MAG, social and trust networks from SNAP/Wikipedia, email graphs, Bitcoin transactions, and private Telegram coordination groups) show that the ρ-invariant behaves as designed:

- ρ increases as influence is centralised into a few hubs and evidence paths collapse or become redundant.
- ρ decreases as influence and evidence remain diversified across many independent paths.

**Typical ρ ranges (wave 1 + wave 2):**

- Healthy, long-lived citation systems:
  - ρ ≈ 10⁻⁶–10⁻²  
  - Even extreme hype fields (COVID-19 vaccines, CRISPR, deep learning explosion) rarely exceed ρ ≈ 0.029.

- Social / interaction networks:
  - Most lie in ρ ≈ 10⁻⁶–10⁻² or slightly higher.
  - A notable high-ρ case is a pump-and-dump Telegram group with ρ ≈ 0.098 that collapsed within ~2 weeks.

- Web-scale infrastructure:
  - Web-Google (unweighted) shows ρ ≈ 0.089 (strongly centralised, red band by original v3).
  - PageRank-style weighting can push this to ρ ≈ 0.112.
  - Inverting direction (backlinks as influence) drops ρ to ≈ 0.045.

These results imply:

1. ρ_EH ≈ 0.7419 acts as a **universal event horizon**: a hard ceiling in ρ-space corresponding to almost total centralisation of influence. Only artificial star-plunder constructions with extreme parameters approach it.

2. Human systems appear to destabilise or change at much lower ρ:
   - For small/medium social or financial systems, ρ in the ≈0.05–0.10 band often correlates with short-lived or brittle behavior (e.g., pump groups).
   - For massive web-scale systems, high ρ (≈0.08–0.11) can coexist with resilience due to scale, redundancy, and external scaffolding.

3. The **numeric bands (green/yellow/orange/red/black)** remain useful, but their interpretation is:

   - Band-aware (by ρ),
   - Domain-aware (academic vs social vs web vs governance),
   - Scale-aware (small/medium vs global).

In practice, ρ should be interpreted as a continuous risk/centralisation score:

- Very low ρ (≲ 0.005–0.01) → no observed collapses so far; “deep green”.
- ρ ≈ 0.01–0.05 → “normal → brittle” depending on domain; long-lived systems can persist here.
- ρ ≈ 0.05–0.10 → strong centralisation; high-risk for small/medium systems, ambiguous for web-scale infrastructures and should trigger closer analysis.
- ρ > 0.10 → extreme centralisation / unexplored; treat as a serious warning and examine domain, scale, and W-construction carefully.

Future calibration waves (wave 3 and beyond) should:

- Track real collapse events (e.g., Enron email, failed DAOs, imploded communities) and ρ(t) dynamics.
- Develop domain-specific band profiles (academic vs social vs governance vs web).
- Explore N-scaling (e.g., ρ_eff = ρ / log(N/100)) to separate web-scale red from meso-scale red.
- Continue searching for stable systems clearly > 0.12, or short-lived systems with very high ρ, to refine the meaning of the black band.

### Optional Cross-Scale View: ρ_eff (v4 Preview)

Wave 3 experiments introduced an N-aware diagnostic:

- ρ_eff = ρ / ln(N / 100), for N > 100.

This does **not** change the core invariant ρ. Instead, it offers a way to compare small and web-scale systems on a more equal footing:

- Web-scale stable systems (e.g., Web-Google) move from raw red/black into ρ_eff green.
- Small, flash-collapsing systems (Telegram pump, Enron, The DAO, r/The_Donald) remain clearly elevated.

ρ_eff is recommended as an optional diagnostic in v4 for cross-scale comparisons. The core law and bands are always defined in terms of raw ρ.

### Optional Cross-Scale View: ρ_eff (v4 Preview)

Wave 3 experiments introduced an N-aware diagnostic:

- ρ_eff = ρ / ln(N / 100), for N > 100.

This does **not** change the core invariant ρ. Instead, it offers a way to compare small and web-scale systems on a more equal footing:

- Web-scale stable systems (e.g., Web-Google) move from raw red/black into ρ_eff green.
- Small, flash-collapsing systems (Telegram pump, Enron, The DAO, r/The_Donald) remain clearly elevated.

ρ_eff is recommended as an optional diagnostic in v4 for cross-scale comparisons. The core law and bands are always defined in terms of raw ρ.

This overview is meant as the top-level index: Level 0–3 define the math and dynamics; the Empirical Calibration & Human Bands section pins those abstractions to real-world behavior as of Dec 2025.


