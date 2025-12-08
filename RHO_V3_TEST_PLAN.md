# RHO v3 Test Plan — Graph ρ-Law & ρ-Dynamics

This document outlines a concrete test plan for the graph ρ-law (v3) and the
ρ-dynamics conjecture. The goal is to move from toy examples to **real
networks** and check whether:

1. ρ = A²(1 − D) behaves as predicted under controlled perturbations.
2. Empirical transitions (collapse, lock-in, fragmentation) occur near
   a domain-independent ρ_crit ≈ 0.7419.
3. Scalar v2 estimates track graph-based ρ on the same systems.

---

## Phase 1 — Controlled Graph Experiments

### 1.1 Star–Plunder Reproduction (Sanity Check)

- Use `graph_rho_law.py` and `demo_star_plunder(N, ps)` to:
  - Verify monotonicity of ρ(p) for a range of N (e.g. N = 5, 10, 20, 50).
  - Record ρ(p) for p ∈ {0, 0.2, 0.5, 0.8, 0.9, 1.0}.
- Check numerically:
  - ρ(p) is strictly increasing in p.
  - ρ(p) → a value in the 0.7–0.8 band as p → 1 for moderate N.
- Output:
  - Tables and plots ρ(p) vs p for the paper / notes.

### 1.2 Competing Hubs Model

- Construct graphs with:
  - Two hubs (A and B) instead of one.
  - A plunder parameter p controlling how much non-hub flow goes to the
    **stronger** hub vs shared between both.
- Questions:
  - Does ρ stay lower when authority is split across hubs?
  - At what point (asymmetry increase) does ρ cross ρ_crit?
- Output:
  - Plots of ρ vs “hub asymmetry parameter”, highlighting the crossing of
    ρ_crit.

---

## Phase 2 — Real Network Case Studies

### 2.1 Small Citation Subgraphs

**Goal:** test ρ on real scientific influence networks.

Steps:

1. Select a small citation subgraph:
   - e.g. papers about a specific topic, one journal, or a time slice.
2. Build the weight matrix W:
   - Nodes = papers or journals.
   - Edges = citations (optionally weighted by recency or journal rank).
3. Compute:
   - Graph A, D, ρ via `compute_graph_rho(W)`.
4. Perturb toward plunder:
   - Artificially increase edges into the top hub(s).
   - Remove or down-weight non-hub edges.
5. Recompute ρ after each perturbation.
6. Evaluate:
   - Does ρ increase as the network is centralised?
   - Does the network’s structure (e.g. modularity, path diversity) visibly
     degrade as ρ approaches the 0.7–0.8 band?

Optional: compare graph-based ρ to v2 scalar estimates for the same field.

---

### 2.2 Social / Interaction Networks

**Goal:** test ρ on human or agent interaction graphs.

Examples:

- Friendship / follower networks (anonymised),
- Organisation charts with communication edges,
- Online community interaction graphs.

Steps:

1. Obtain an anonymised edge list (source,target,weight).
2. Build W and compute A, D, ρ.
3. Identify events:
   - Increased centralisation (e.g. one account or team becomes a bottleneck),
   - Fragmentation or collapse events (community dies, org restructures).
4. Track ρ over time (snapshots):
   - Does ρ rise toward/above ρ_crit near collapse or lock-in events?
5. Compare:
   - Graph ρ vs simpler scalar metrics (Gini of degree, etc.).

---

## Phase 3 — ρ-Dynamics Estimation

Using `rho_eval_private.py` or equivalent private tooling:

### 3.1 Estimate α/β from ρ Time Series

For systems where multiple snapshots over time are available:

1. Compute ρ(t_k) for k = 0..T.
2. Fit the coarse-grained evolution law:

   \[
     \dot{\rho} \approx \alpha - (\alpha + \beta)\rho,
   \]

   e.g. via regression on:

   \[
     \Delta\rho \approx \alpha - (\alpha + \beta)\rho(t).
   \]

3. Extract estimated \(\alpha\) and \(\beta\), then compute:

   \[
     \rho_* = \frac{\alpha}{\alpha + \beta}, \quad
     \frac{\alpha}{\beta}.
   \]

4. Compare \(\alpha/\beta\) to the critical ratio:

   \[
     \frac{\alpha}{\beta}_\text{crit} \approx 2.875.
   \]

5. Check:
   - Systems that empirically collapse / lock-in have \(\alpha/\beta\) above
     the critical ratio.
   - Systems that remain open / dynamic have \(\alpha/\beta\) below it.

---

## Phase 4 — Scalar vs Graph ρ Cross-Checks

Whenever both scalar and graph views are possible:

1. Compute v2 scalar outputs for the system (e.g. a field, journal, or
   canonical paper).
2. Compute graph-based ρ for the corresponding influence network.
3. Examine:
   - Correlation between v2 `rho_plunder_equiv` and graph-based ρ.
   - Whether both cross their respective collapse thresholds around the same
     period.

Goal: demonstrate that v2 is a **good low-dimensional proxy** for the deeper
graph-based invariant.

---

## Notes

- This test plan is deliberately modular: any lab can pick one phase and
  reproduce/extend.
- The most critical evidence will come from:
  - Time-series ρ(t) around real collapse / lock-in events.
  - Cross-domain consistency of ρ_crit and the critical α/β ratio.

Results from these tests can be linked back to:

- `GRAPH_RHO_LAW.md` (definitions),
- `RHO_DYNAMICS.md` (evolution law),
- and any future formal theorems about ρ on specific graph families.