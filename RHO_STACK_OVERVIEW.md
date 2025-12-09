# ρ-Stack Overview — From Invariant to Dynamics (Dec 2025)

This document summarizes the current ρ-stack:

1. **Level 0 — Invariant (Raw ρ-Law)**
2. **Level 1 — v2 Roemmele–Goalden Collapse Law (Scalar Implementation)**
3. **Level 2 — Graph ρ-Law (v3 Static)**
4. **Level 3 — ρ-Dynamics (v3 Dynamics / Critical Ratio)**

Public repos contain the math and reference code. Private repos contain
P-scanner pipelines, datasets, and domain-specific heuristics.

---

## Level 0 — Raw Invariant

**Definition**

\[
  \rho = (\text{authority})^{2} \cdot (1 - \text{evidence\_diversity}),
\]

with a universal **event-horizon constant**

\[
  \rho_{\text{EH}} \approx 0.7419.
\]

- **authority**: domain-specific measure of centralised control / dominance  
  (citations × impact factor, dark-energy fraction, copy number, etc.).
- **evidence_diversity**: domain-specific measure of independent paths / modes  
  (independent data sources, matter fraction, novelty, residual uncertainty).

Interpretation (theoretical):

- \( \rho \ll \rho_{\text{EH}} \): open futures, structure still forming.
- \( \rho \approx \rho_{\text{EH}} \): event-horizon regime where almost all
  paths route through one effective center.
- \( \rho > \rho_{\text{EH}} \): not expected for functioning influence systems;
  mathematically corresponds to “no more interesting structure”.

**Empirical fact (Dec 2025):** in real human systems sampled so far, ρ remains
far below \( \rho_{\text{EH}} \). Human systems destabilise or collapse long
before reaching this theoretical ceiling; see “Empirical Calibration” below.

---

## Level 1 — v2 Roemmele–Goalden Collapse Law (Scalar)

**File:** `roemmele_goalden_collapse_v2.py`

Implements a scalar collapse law for **scientific authority systems** that
maps bibliometric quantities into a ρ-like risk.

Inputs (per paper / topic):

- publication_year
- citation_count
- impact_factor
- retracted (0/1)
- replication_crisis_flags
- controversy_index (0–something)

Core pieces:

- Authority:
  \[
    \text{authority\_weight} =
      \log(\text{citations} + 1) \times \text{impact\_factor}.
  \]
- Age survival factor:
  \[
    \text{survival\_factor} = 1 - \exp(-\text{age\_years}/\tau),
    \quad \tau \approx 38.7.
  \]
- Empirical distrust:
  \[
    \text{distrust} =
      \text{retracted} + \text{rep\_flags} + \text{controversy\_index}.
  \]
- Saturating mapping to a ρ-like scale bounded by the **event horizon**:
  \[
    \rho_{\text{plunder\_equiv}} \in (0, \rho_{\text{EH}}],
  \]
  with a logistic “knee” tuned once from backtests.

Outputs:

- \( \rho_{\text{plunder\_equiv}} \) (ρ-like scalar in [0, ρ_EH]),
- `collapse_risk` (dimensionless risk index),
- flags for theoretical vs empirical risk bands.

**Important:** v2 treats \( \rho_{\text{EH}} \) as a **theoretical ceiling**.
Empirical calibration suggests that human systems already look pathological
in the much lower band ρ ≈ 0.05–0.10, long before saturating the logistic.

---

## Level 2 — Graph ρ-Law (v3 Static)

**Files:** `GRAPH_RHO_LAW.md`, `graph_rho_law.py`

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
  - Node entropies:
    \[
      H_j(t) = -\sum_i p_{ij}(t)\log p_{ij}(t).
    \]
  - Global diversity:
    \[
      D(t) := \frac{1}{N\log N}\sum_j H_j(t) \in [0,1].
    \]

- **Graph ρ**:
  \[
    \rho(t) := A(t)^2 \bigl(1 - D(t)\bigr).
  \]

**Star–Plunder Model (sanity check)**

- N-node graph with a single hub and a plunder parameter \( p \in [0,1] \).
- As \(p\) increases (more centralisation), ρ increases monotonically.
- For moderate N (e.g. N=50), ρ crosses 0.7 only when >90–95% of all
  influence flows into the hub, consistent with ρ_EH as an “almost total”
  centralisation regime.

Level 2 = **“given a real network W, compute A, D, ρ and compare to both the
event horizon and human empirical bands.”**

---

## Level 3 — ρ-Dynamics (v3 Dynamics / Critical Ratio)

**File:** `RHO_DYNAMICS.md`

We model the **time evolution** of ρ as the competition between:

- **Voluntary exchange** (decentralising: ρ ↓),
- **Plunder** (centralising: ρ ↑).

At the graph level:

- Voluntary exchange ⇒ \( \dot{A} \le 0,\ \dot{D} \ge 0 \Rightarrow \dot{\rho} \le 0 \).
- Plunder ⇒ \( \dot{A} \ge 0,\ \dot{D} \le 0 \Rightarrow \dot{\rho} \ge 0 \).

A coarse-grained evolution law:

\[
  \dot{\rho} = \alpha(1 - \rho) - \beta\,\rho,
\]

with:

- \(\alpha\): plunder intensity,
- \(\beta\): voluntary / anti-plunder intensity.

Fixed point:

\[
  \rho_* = \frac{\alpha}{\alpha + \beta}.
\]

If we equate \(\rho_*\) with the **event horizon**, we get the critical ratio:

\[
  \frac{\alpha}{\beta}_\text{EH}
  = \frac{\rho_{\text{EH}}}{1 - \rho_{\text{EH}}}
  \approx 2.875.
\]

Empirically, current human systems appear to have \(|\alpha/\beta| \ll 1\),
i.e. they live far inside the open regime.

Level 3 = **“given ρ(t) over time, estimate α/β and see how far you are from
the event-horizon ratio; then compare to human ‘soft’ thresholds.”**

---

## Empirical Calibration (Dec 2025)

Early tests across 50+ real-world influence networks (citation graphs from
OpenAlex/Semantic Scholar/MAG, social and trust networks from SNAP/Wikipedia,
email graphs, Bitcoin transactions, and private Telegram coordination groups)
show that the ρ-invariant behaves as designed:

- ρ increases as influence is centralised into a few hubs and evidence paths
  collapse.
- ρ decreases as influence and evidence remain diversified.

Typical ρ values in healthy, long-lived human systems lie between about
10⁻⁶ and 10⁻². Even in extreme episodes of scientific hype or social
centralisation (COVID-19 vaccine literature, CRISPR boom, deep-learning
explosion, high-control online communities), ρ has so far never exceeded
≈0.029 in citation networks and ≈0.098 in social/interaction networks.

The theoretical constant ρ_EH ≈ 0.7419 therefore acts as a **universal event
horizon**: a hard ceiling in ρ-space corresponding to almost total
centralisation of influence. Empirically, human systems appear to destabilise
and collapse at much lower ρ. In the observed datasets, ρ in the band
≈0.05–0.10 already corresponded to systems on the brink of collapse, with
values around 0.1 only appearing in networks that died within days.

In practice, ρ is best interpreted as a continuous risk score, with
domain-specific “soft thresholds” for humans sitting far below the
mathematical event horizon.