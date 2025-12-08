# ρ-Stack Overview — From Invariant to Dynamics

This document summarizes the current ρ-stack:

1. **Level 0 — Invariant (Raw ρ-Law)**
2. **Level 1 — v2 Roemmele–Goalden Collapse Law (Scalar Implementation)**
3. **Level 2 — Graph ρ-Law (v3 Static)**
4. **Level 3 — ρ-Dynamics (v3 Dynamics / Critical Ratio)**

The public repos contain the *math* and reference code. Private repos contain
P-scanner pipelines, datasets, and domain-specific heuristics.

---

## Level 0 — Raw Invariant

**Definition**

\[
  \rho = (\text{authority})^{2} \cdot (1 - \text{evidence\_diversity}),
\]

with a universal collapse threshold

\[
  \rho_{\text{crit}} \approx 0.7419.
\]

- **authority**: domain-specific measure of centralised control / dominance  
  (citations × impact factor, dark-energy fraction, copy number, etc.).
- **evidence_diversity**: domain-specific measure of independent paths / modes  
  (independent data sources, matter fraction, novelty, residual uncertainty).

Interpretation:

- \( \rho \ll \rho_{\text{crit}} \): open futures, structure still forming.
- \( \rho \approx \rho_{\text{crit}} \): onset of lock-in / de Sitter-like regimes.
- \( \rho \gg \rho_{\text{crit}} \): effectively no new interesting structure.

Level 0 is the **core invariant** used across domains.

---

## Level 1 — v2 Roemmele–Goalden Collapse Law (Scalar)

**File:** `roemmele_goalden_collapse_v2.py` (or equivalent)

Implements a scalar collapse law for **scientific authority systems**:

- Inputs:
  - publication_year
  - citation_count
  - impact_factor
  - retracted (0/1)
  - replication_crisis_flags
  - controversy_index

- Core pieces:
  - \( \text{authority\_weight} = \log(\text{citations}+1) \times \text{impact\_factor} \)
  - Age survival factor: \( \text{survival\_factor} = 1 - \exp(-\text{age}/\tau) \)  
    with a shared \( \tau \approx 38.7 \) years.
  - Saturating mapping to \( \rho_{\text{plunder\_equiv}} \in (0, 0.7419] \).
  - Empirical distrust amplifies risk via \( (1 + \alpha_D \cdot \text{distrust}) \).

Outputs:

- \( \rho_{\text{plunder\_equiv}} \) (ρ-like scalar),
- `collapse_risk`,
- `will_collapse` boolean.

Level 1 = **“plug 6 numbers → get collapse risk”** for papers / fields.

---

## Level 2 — Graph ρ-Law (v3 Static)

**File:** `GRAPH_RHO_LAW.md`, `graph_rho_law.py`

We lift ρ from a scalar rule to a **functional on influence graphs**.

System at time \(t\):

- Weighted directed graph \( W(t) = [w_{ij}(t)] \),
- \(w_{ij}(t) \ge 0\): influence from node j → i.

Definitions:

- **Authority**:
  \[
    A(t) := \max_j \frac{\sum_i w_{ij}(t)}{\sum_{i,k} w_{ik}(t)},
  \]
  the strongest hub’s share of total incoming influence.

- **Diversity**:
  - Normalize columns to probabilities \( p_{ij}(t) \).
  - Node entropies \( H_j(t) = -\sum_i p_{ij}\log p_{ij} \).
  - Global:
    \[
      D(t) := \frac{1}{N\log N}\sum_j H_j(t) \in [0,1].
    \]

- **Graph ρ**:
  \[
    \rho(t) := A(t)^2 \bigl(1 - D(t)\bigr).
  \]

**Star–Plunder Model**

- N-node graph with a single hub and a plunder parameter \( p \in [0,1] \).
- As \(p\) increases (more centralisation), ρ increases.
- For moderate N (e.g. N=10):

  - \(p = 0\): ρ ≈ 0 (no centralisation).
  - \(p = 1\): ρ ≈ 0.745, i.e. the graph crosses \( \rho_{\text{crit}} \approx 0.7419 \)
    only when **plunder is essentially total**.

Level 2 = **“given a real network W, compute A, D, ρ and compare to ρ_crit.”**

---

## Level 3 — ρ-Dynamics (v3 Dynamics / Critical Ratio)

**File:** `RHO_DYNAMICS.md`

We model the **time evolution** of ρ as the competition between:

- **Voluntary exchange** (decentralising) and
- **Plunder** (centralising).

At the graph level:

- Voluntary exchange: \( \dot{A}_\text{vol} \le 0,\ \dot{D}_\text{vol} \ge 0 \Rightarrow \dot{\rho}_\text{vol} \le 0 \).
- Plunder: \( \dot{A}_\text{pl} \ge 0,\ \dot{D}_\text{pl} \le 0 \Rightarrow \dot{\rho}_\text{pl} \ge 0 \).

A coarse-grained evolution law:

\[
  \dot{\rho} = \alpha(1 - \rho) - \beta\,\rho
\]

with:

- \(\alpha\): plunder intensity,
- \(\beta\): voluntary / anti-plunder intensity.

Fixed point:

\[
  \rho_* = \frac{\alpha}{\alpha + \beta}.
\]

Comparing to \( \rho_{\text{crit}} \approx 0.7419 \) yields a **critical ratio**:

\[
  \frac{\alpha}{\beta} \lessgtr \frac{\rho_{\text{crit}}}{1 - \rho_{\text{crit}}}
  \approx 2.875.
\]

- If \( \alpha/\beta < 2.875 \): the system flows to a **subcritical**, open regime.
- If \( \alpha/\beta > 2.875 \): the system flows to a **supercritical**, collapsed regime.

Level 3 = **“given ρ over time, estimate α/β and see which basin you’re in.”**

---

## Public vs Private Layers

- **Public** (this and related repos):
  - Invariant, v2 law, graph ρ-law, ρ-dynamics.
  - Small reference implementations and toy models.

- **Private** (separate private repo):
  - Ingestion / ETL for real systems,
  - domain-specific heuristics (controversy indices, risk transforms),
  - curated datasets,
  - private scripts (e.g. `rho_eval_private.py`, `PlunderScanner`).

This file is the high-level map: it shows how all pieces relate so that
future work (by me or others) can plug into the correct level.