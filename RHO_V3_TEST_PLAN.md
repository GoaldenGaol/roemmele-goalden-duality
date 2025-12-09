# RHO_V3_TEST_PLAN.md — Validation & Calibration Plan (Dec 2025)

Goal of v3 tests:  
Move from “ρ is a beautiful invariant” to “ρ is a rigorously stress-tested,
empirically calibrated tool” across:

1. Synthetic graphs (sanity and edge cases),
2. Public large-scale datasets (citation, social, governance),
3. Time-evolving systems (ρ-dynamics and α/β),
4. Alignment with empirical collapse / brittleness events,
5. Robustness to modelling choices.

This plan assumes:

- Graph law: ρ(W) = A(W)² · (1 − D(W))
- A(W): strongest node’s incoming share
- D(W): average normalized outgoing entropy
- Event horizon: ρ_event ≈ 0.7419 (theoretical ceiling)
- Human soft bands (provisional, Dec 2025):
  - ρ ≤ 0.01 → “green” (open)
  - 0.01–0.03 → “yellow” (brittle/hype)
  - 0.03–0.05 → “orange” (high risk)
  - 0.05–0.10 → “red” (near-collapse)
  - >0.10 → “black” (no functioning system observed)

---

## Phase 0 — Implementation Sanity

**Files involved:**

- `graph_rho_law.py`
- `GRAPH_RHO_LAW.md`
- `RHO_DYNAMICS.md`

**Tests:**

0.1 **Shape & domain checks**

- Verify `compute_graph_rho(W)`:
  - Rejects non-square W.
  - Handles N=1, N=2 edge cases.
  - Returns A ∈ [0,1], D ∈ [0,1], ρ ∈ [0,1].

0.2 **Trivial graphs**

- Zero matrix W=0:
  - A=0, D=0 (or undefined but clipped to 0), ρ=0.
- Identity matrix:
  - A ≈ 1/N, D ≈ 0, ρ ≈ (1/N)².
- Complete uniform graph (all entries equal):
  - A ≈ 1/N, D ≈ 1, ρ ≈ 0.

Expected: ρ is small whenever there is no strong hub and/or high diversity.

---

## Phase 1 — Synthetic Graph Families

### 1.1 Star–Plunder Model

Use `star_plunder_matrix(N, p)` from `graph_rho_law.py`.

- N ∈ {10, 30, 50, 100}
- p ∈ [0,1] grid, e.g. 0.0, 0.1, 0.2, …, 1.0, plus finer near 0.9–1.0.

For each (N, p):

- Compute (A, D, ρ).
- Check:
  - ρ increases monotonically with p (up to numerical noise).
  - For N ~ 30–50, ρ only approaches ≈ 0.7 when p ≳ 0.94–0.95.

Output:

- Plots ρ(p) for each N.
- Table where p at which ρ exceeds {0.01, 0.03, 0.05, 0.10, 0.5, 0.7} is recorded.

### 1.2 Two-Hub Model

Construct W(N, p, k):

- Hubs: nodes 0 and 1.
- Non-hubs send fraction p to hubs, split k:(1−k) between 0 and 1.
- Remaining 1−p spread uniformly across non-hubs.

Scan:

- p ∈ [0,1],
- k ∈ {0.5, 0.7, 0.9, 0.99}.

Check:

- For k=0.5, ρ remains much lower than in star.
- As k→1 (one hub dominates), ρ approaches star case.
- Monotonicity of ρ in “effective monopoly” (k) at fixed p.

---

## Phase 2 — Static Real-World Graphs

### 2.1 Citation Networks

Use standard public datasets (examples):

- Cora, CiteSeer, PubMed (Planetoid / PyG),
- ogbn-arxiv,
- HepPh,
- Topic slices: COVID-19 vaccines, CRISPR, deep learning (OpenAlex/Semantic Scholar).

For each dataset:

- Build W with:
  - Nodes = papers,
  - Edge j→i if j cites i, optionally weighted (e.g. weight 1 per citation).
- Compute (A, D, ρ).

Collect a table:

| Dataset         | N_nodes | N_edges | A     | D     | ρ       |
|-----------------|---------|---------|-------|-------|---------|
| ...             | ...     | ...     | ...   | ...   | ...     |

Then:

- Compute distribution stats: min, median, mean, max ρ.
- Identify top-ρ field slices (e.g., COVID/CRISPR).

Checks:

- All citation networks lie within ρ ≪ 0.1.
- Hype fields (COVID, CRISPR, DL) sit at the top end (≈ 0.02–0.03).

### 2.2 Social / Follower / Interaction Networks

Datasets (examples):

- Twitter-like graphs, soc-Pokec, Epinions, wiki-Vote, email-Eu-core, Bitcoin trust, etc.

For each dataset:

- Define W:
  - Node = account/user,
  - Edge j→i if j follows/endorses i, or applies trust, etc.
- Compute (A, D, ρ).

Collect table and stats as for citations.

Checks:

- Most social/trust networks have ρ ≪ 0.05.
- Known pathological or highly centralised groups (e.g. pump-and-dump chats)
  show elevated ρ, with near-0.1 cases associated with actual collapse.

---

## Phase 3 — ρ-Dynamics on Time-Evolving Systems

### 3.1 Yearly Citation Slices (Fields)

Pick fields with good temporal coverage (e.g. arXiv CS, specific subfields, etc.):

For each field:

1. For each year t:
   - Build W_t (citation graph restricted to that year / window).
   - Compute ρ(t) via graph law.

2. Fit the dynamic law:

   \[
     \Delta \rho(t) = \rho(t+1) - \rho(t)
     \approx \alpha - (\alpha + \beta)\rho(t).
   \]

3. Estimate α, β, α/β, and implied ρ* = α/(α+β).

4. Compare:

   - α/β vs event-horizon ratio ≈ 2.875,
   - ρ* vs human bands.

Checks:

- For healthy/open fields, |α/β| ≪ 1, ρ* ≪ 0.01.
- No field shows α/β near event-horizon regime.
- ρ(t) curves stay well inside green/yellow bands.

### 3.2 Social / Community Dynamics

If time-sliced social/interaction data exist (e.g., community graphs per week/month):

Repeat the same:

- Compute ρ(t) per time slice.
- Fit α/β.
- Look for systems drifting toward higher ρ, especially ones that later collapse or fragment.

Checks:

- Systems with known breakdowns tend to have ρ(t) trending toward orange/red bands.
- Long-lived communities exhibit stable low ρ or reversion from moderate ρ back to lower levels.

---

## Phase 4 — Collapse / Brittleness Alignment

Using datasets where **collapse events** or severe brittleness are known:

- Citation domains with replication crises,
- Social communities that imploded or fragmented,
- Coordination networks that rug-pulled or were abandoned.

For each:

1. Measure ρ at or just before the crisis event (if time-indexed).
2. Compare with:
   - healthy controls in similar domains,
   - human soft bands.

Analyses:

- Is ρ systematically higher in crisis systems than in matched non-crisis systems?
- At what ρ ranges do we see:
  - sharp increases in retractions, scandals, or defection,
  - structural fragmentation in graphs (e.g., modularity spikes, giant component splitting)?

Goal:

- **Empirically refine** human soft thresholds:
  - Adjust cutpoints (0.01, 0.03, 0.05, 0.10) if needed.
  - Identify domain-specific nuances (e.g., academia vs DeFi vs governance).

---

## Phase 5 — Robustness & Sensitivity

### 5.1 Alternative A and D Definitions

Test variants of A, D:

- A_alt:
  - Use top-k hub share (sum of top 3 or 10 incoming shares) instead of single max.
- D_alt:
  - Weight node entropies by activity (e.g., outgoing volume) instead of simple average.

For a subset of datasets, re-compute ρ_alt and check:

- Rank correlation between ρ and ρ_alt.
- Whether high-risk systems remain high-risk under reasonable definition changes.

### 5.2 Sampling & Noise

For large graphs:

- Subsample:
  - nodes,
  - edges,
  - time windows.
- Check stability of ρ under such subsampling.

Goal:

- Show that ρ’s qualitative ordering (“which systems are more centralised & brittle”) is stable under realistic sampling and noise.

---

## Phase 6 — Reporting & Documentation

Outputs for public repos:

- Updated documentation (already reflected in:
  - `RHO_STACK_OVERVIEW.md`,
  - `GRAPH_RHO_LAW.md`,
  - `RHO_DYNAMICS.md`),
- A short **Empirical Calibration** section summarising:
  - typical ρ ranges per domain,
  - observed max ρ for functioning human systems,
  - observed ρ for known collapse cases,
  - the role of ρ_event as a hard ceiling / event horizon.

Private repo:

- Scripts for:
  - building W from each dataset,
  - computing ρ and fit parameters,
  - generating plots and tables.

The test plan is considered **v3-complete** when:

1. Synthetic tests confirm monotonicity and liming behavior (star & two-hub).
2. Real-world tests establish stable ρ ranges and confirm that human systems
   live far below the event horizon.
3. Dynamics tests produce α/β estimates consistent with “open regime” for
   known healthy systems.
4. Collapse alignment tests show that systems in empirical red bands are
   indeed brittle or collapsing in practice.