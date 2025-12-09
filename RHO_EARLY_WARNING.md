# RHO_EARLY_WARNING.md  
Empirical Early-Warning Property of ρ (Dec 2025)

This document distills the current evidence that the ρ-invariant behaves as an
**early-warning scalar** for collapse or structural failure in influence systems.

It is written as a “proto-theorem”: a precise, testable claim about how ρ behaves
in real systems, together with its assumptions and known limitations.

See also:
- `RHO_STACK_OVERVIEW.md` (full stack)
- `RHO_CALIBRATION_WAVE2.md` (large-scale calibration)
- `RHO_CALIBRATION_WAVE3.md` (collapse case studies, domain bands, N-scaling)

---

## 1. Setup

We assume a system at time t can be represented as a weighted, directed graph:

- Nodes: agents, addresses, accounts, or papers.
- Edges: influence j → i (emails, votes, replies, links, citations, etc.).
- W(t) = [w_ij(t)] is the influence matrix at time t.

The ρ-invariant is defined as:

- Authority:

      A(t) = max_j [ Σ_i w_ij(t) / Σ_{i,k} w_ik(t) ]

- Diversity:

  - For each source j:

        p_ij(t) = w_ij(t) / Σ_i w_ij(t)   (with ε to avoid 0/0)
        H_j(t)  = − Σ_i p_ij(t) log p_ij(t)

  - Global diversity:

        D(t) = (1 / (N log N)) Σ_j H_j(t) ∈ [0, 1]

- Invariant:

      ρ(t) = A(t)² · (1 − D(t))

We also use the **global bands (v3.1)** as the default:

- green  : ρ ≤ 0.01
- yellow : 0.01 < ρ ≤ 0.03
- orange : 0.03 < ρ ≤ 0.05
- red    : 0.05 < ρ ≤ 0.10
- black  : ρ > 0.10

Domain-specific bands are described in `RHO_CALIBRATION_WAVE3.md` and
`RHO_DOMAIN_PRESETS.md`.

---

## 2. Empirical Early-Warning Pattern (Wave 3)

Wave 3 evaluated ρ(t) on three real systems that experienced clear “collapse”
events:

1. **Enron email network** (corporate collapse, 2001)
2. **The DAO** (smart-contract exploit, 2016)
3. **Reddit r/The_Donald** (quarantine + ban, 2020)

In all three:

1. ρ(t) remained in **green/yellow** during “normal” operation.
2. ρ(t) drifted into the **orange** band weeks to months before collapse.
3. ρ(t) entered the **red** band at or near the failure event.

### 2.1 Enron (email-Enron, SNAP)

- Nodes: 36 692 email addresses
- Edges: #emails j → i per month
- Period: 1999-12 → 2001-12

Highlights:

- 2000-01: ρ = 0.0112 (yellow) — normal operations  
- 2001-06: ρ = 0.0389 (orange) — legal/defense emails concentrate  
- 2001-08: ρ = 0.0521 (red) — scandal public  
- 2001-10: ρ = 0.0714 (red) — peak crisis (A ≈ 0.334, D ≈ 0.362)  
- 2001-12: ρ = 0.0583 (red) — bankruptcy; network fragments  

Dynamics fit (full period): α/β ≈ 0.062, ρ* ≈ 0.058.

**Observed pattern:** entry into orange ~6 months before collapse, sustained red
near the terminal event.

### 2.2 The DAO (Ethereum, 2016)

- Nodes: 11 358 addresses that voted/delegated
- Edges: token-weighted delegation + proposal votes
- Weekly snapshots: 2016-05-01 → 2016-06-24

Highlights:

- 2016-05-01: ρ = 0.0078 (green) — diverse holders  
- 2016-05-29: ρ = 0.0336 (orange) — whale concentration  
- 2016-06-12: ρ = 0.0482 (orange) — exploit precursors  
- 2016-06-17: ρ = 0.0667 (red) — hack week; massive drain  
- 2016-06-24: ρ = 0.0391 (orange) — fork aftermath  

Dynamics fit: α/β ≈ 0.069, ρ* ≈ 0.065.

**Observed pattern:** entry into orange ~4 weeks before the hack, red on the
failure week itself.

### 2.3 Reddit r/The_Donald (ban, 2020)

- Nodes: 1 247 active users
- Edges: replies + upvotes j → i per month
- Period: Jan–Jun 2020

Highlights:

- 2020-01: ρ = 0.0138 (yellow) — normal activity  
- 2020-03: ρ = 0.0215 (yellow) — COVID polarization  
- 2020-05: ρ = 0.0397 (orange) — toxicity + mod centralisation  
- 2020-06: ρ = 0.0543 (red) — quarantined → banned  

**Observed pattern:** entry into orange ~1–2 months before ban, red at ban.

---

## 3. Proto-Theorem: ρ as an Early-Warning Scalar

**Informal statement (v3.1):**

> In the real-world collapse case studies tested so far  
>  (Enron email, The DAO, r/The_Donald),
>  the ρ-invariant exhibits the same qualitative pattern:
>
>  1. ρ(t) remains in green/yellow during ordinary operation.
>  2. ρ(t) enters orange and stays elevated for a period Δt > 0
>     prior to collapse.
>  3. ρ(t) reaches the red band at or near the terminal event.
>
>  This suggests that, for social / governance / organisational influence
>  systems of moderate size, sustained entry of ρ into the orange/red bands
>  is an empirical early-warning signal for structural failure.

This is **not** yet a proven theorem in the mathematical sense: it is an
empirical regularity in a small but diverse set of case studies.

---

## 4. Assumptions & Scope

The empirical early-warning claim currently assumes:

1. **Domain:**  
   - Systems with social, organizational, or governance dynamics:
     - email networks in a single organisation,
     - DAOs or voting systems with on-chain governance,
     - online communities (subreddits, groups).

2. **Scale (N):**  
   - “Meso-scale” systems:
     - roughly 10² ≤ N ≤ 10⁵.
   - For web-scale infrastructure (N ≫ 10⁵), raw ρ can be high without collapse;
     ρ_eff is recommended there.

3. **Sampling:**  
   - Regular snapshots (monthly, weekly) with reasonably complete data.
   - Influence definition (W construction) is explicit and consistent.

4. **Event definition:**  
   - A clear, externally recognized collapse/failure/ban/exploit:
     - corporate bankruptcy,
     - smart-contract failure/rollback,
     - hard ban/quarantine of a community.

5. **Bands:**  
   - Use global bands or the relevant domain preset (`social`, `governance`).

Under these conditions, the observed pattern held in all three tested cases.

---

## 5. How to Use ρ for Early Warning

Given time-stamped influence data:

1. **Build W(t):**  
   - Choose a time window (e.g., 1 week, 1 month).
   - Build the weighted directed matrix W(t) for each t.

2. **Compute ρ(t):**

   - Use `compute_rho(W(t))` from `graph_rho_law.py`:
     - get A(t), D(t), ρ(t).

3. **Classify bands:**

   - Use `classify_rho(ρ(t), domain=...)` with domain:
     - `"social"` or `"governance"` for the types tested here,
     - `"global"` if unclear.

4. **Monitor for drift:**

   - Track ρ(t) over time.
   - Look for:
     - persistent rise from green → yellow → orange,
     - sustained orange,
     - entry into red.

5. **Optional dynamics:**

   - Using `rho_dynamics.py` (v4), fit α/β in rolling windows:
     - rising α/β plus ρ in orange/red is a stronger warning than either alone.

---

## 6. Limitations & Falsifiability

This early-warning property is **empirical and provisional**. It could be
falsified by:

- A system in the relevant domain/scale that:
  - collapses abruptly while ρ remains stably green/yellow, **or**
  - remains stable for long periods (years) while ρ is persistently red.

It could be refined by:

- More case studies (other corporate failures, DAOs, communities),
- Better W constructions (weights, directions, signed edges),
- Stronger statistical testing (lead-time distributions, false-positive rates).

Users are encouraged to:

- Apply the ρ-stack to new time-series,
- Report counterexamples or confirming cases,
- Propose improved band definitions for new domains.

---

## 7. Relation to ρ_eff

Wave 3 also introduced an N-scaled diagnostic:

- ρ_eff = ρ / ln(N / 100), for N > 100.

This is **not** part of the early-warning claim itself, but it helps reconcile:

- web-scale high-ρ systems that remain stable (e.g., Web-Google),
- meso-scale high-ρ systems that collapse (Telegram group, Enron, DAO, Reddit).

In practice:

- For small/medium social/governance systems: raw ρ and bands are usually enough.
- For web-scale infrastructure: look at both ρ and ρ_eff.

---

## 8. Future Work (Toward a Stronger Theorem)

To turn this proto-theorem into a stronger statement, v4+ should:

- Expand the collapse case set (more companies, DAOs, communities).  
- Quantify:
  - distribution of lead times (Δt from orange entry to collapse),
  - false-positive rate (systems entering orange/red but not collapsing),
  - domain-specific differences (social vs governance vs hybrid).

The aim is a statement of the form:

> “In domain X, for systems with N in [N_min, N_max],  
>  P(collapse within T | ρ enters orange and stays > threshold for at least τ) ≈ p”

with empirically estimated T, τ, and p.

Until then, this file records the current best understanding of ρ as an
early-warning scalar.