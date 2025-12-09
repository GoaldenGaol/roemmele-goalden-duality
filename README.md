# ρ-Plunder × Empirical Distrust Invariant (Dec 2025)

**Status:** mathematically sound, empirically calibrated, still under active refinement.  
**Core idea:** a single scalar ρ, computed from **centralisation** and **path diversity**, behaves like a universal risk indicator for collapse or lock-in across many domains (science, social systems, coordination graphs, etc.).

This repo contains:

- The **raw ρ-invariant**,
- A **graph law** that computes ρ from real networks,
- A **scalar Roemmele–Goalden v2 collapse law** for scientific authority,
- A **dynamics model** for how ρ drifts over time,
- A v3 **test plan** to keep the claims honest.

---

## 1. The Invariant

At its core, the invariant is:

\[
  \rho = (\text{authority})^{2} \cdot (1 - \text{evidence\_diversity}),
\]

where, in any domain:

- **authority** ≈ “how much does one point (paper, hub, institution, token) dominate?”  
- **evidence_diversity** ≈ “how many independent paths or modes still exist?”

Interpretation:

- **Low ρ** → many open paths, no single point of failure.
- **High ρ** → influence is concentrated and paths have collapsed.

There is a theoretically fitted **event horizon constant**:

\[
  \rho_{\text{event}} \approx 0.7419,
\]

which behaves as a **hard ceiling**: a regime where almost all paths route through a single effective center.

> **Important:** Real human systems (so far) never reach this ceiling.  
> They destabilise or collapse in a much lower ρ band; see Calibration.

For a high-level description of the stack, see:

- [`RHO_STACK_OVERVIEW.md`](./RHO_STACK_OVERVIEW.md)

---

## 2. Graph ρ-Law (v3 Static)

To apply ρ to real systems, we represent them as weighted directed graphs.

Let:

- Nodes: \(V = \{1,\dots,N\}\)
- Weight matrix: \(W \in \mathbb{R}_{\ge 0}^{N \times N}\) with
  \[
    w_{ij} \ge 0 = \text{influence from node } j \to i.
  \]

Then:

### 2.1 Authority \(A(W)\)

\[
  \text{incoming}_j = \sum_i w_{ij}, \quad
  \text{total\_incoming} = \sum_j \text{incoming}_j
\]

\[
  A(W) = \max_j \frac{\text{incoming}_j}{\text{total\_incoming}} \in [0,1]
\]

- \(A(W) \to 1\) when a single hub dominates incoming influence.
- \(A(W) \approx 1/N\) when influence is evenly shared.

### 2.2 Diversity \(D(W)\)

For each source node \(j\):

\[
  p_{ij} = \frac{w_{ij}}{\sum_k w_{kj} + \varepsilon}, \quad
  H_j = -\sum_i p_{ij}\log p_{ij}, \quad
  H_{j,\text{norm}} = \frac{H_j}{\log N}
\]

Then:

\[
  D(W) = \frac{1}{N}\sum_{j=1}^N H_{j,\text{norm}} \in [0,1].
\]

- \(D(W) \approx 1\): sources spread influence widely (high path diversity).
- \(D(W) \approx 0\): sources concentrate on a single target (path collapse).

### 2.3 Graph ρ

\[
  \rho(W) = A(W)^2 \cdot (1 - D(W)).
\]

Implementation:

- **Code:** [`graph_rho_law.py`](./graph_rho_law.py)
- **Doc:** [`GRAPH_RHO_LAW.md`](./GRAPH_RHO_LAW.md)

This code exposes:

- `compute_graph_rho(W)` → returns A, D, ρ
- `RHO_EVENT_HORIZON = 0.7419`
- `classify_human_rho(rho)` → rough “green/yellow/orange/red/black” bands for human systems.

---

## 3. Scalar Collapse Law (Roemmele–Goalden v2)

For scientific authority (papers, topics, fields) we define a scalar mapping from bibliometrics into a ρ-like risk score.

File:

- [`roemmele_goalden_collapse_v2.py`](./roemmele_goalden_collapse_v2.py)

Inputs (per paper / canonical result):

- `publication_year`
- `citation_count`
- `impact_factor`
- `retracted` (0/1)
- `replication_crisis_flags` (integer)
- `controversy_index` (heuristic 0+ scalar)
- optional hyperparameters: `tau_years`, `logistic_k`, `logistic_center`, `distrust_gain`

Key pieces:

- **Authority weight:**

  \[
    \text{authority\_weight} =
      \log(\text{citations} + 1)\times\text{impact\_factor}.
  \]

- **Survival factor:**

  \[
    \text{survival\_factor} =
      1 - \exp\bigl(-\frac{\text{age\_years}}{\tau}\bigr),
    \quad \tau \approx 38.7\ \text{yrs}.
  \]

- **Empirical distrust:**

  \[
    \text{distrust} =
      \text{retracted} + \text{rep\_flags} + \text{controversy\_index}.
  \]

- **Saturating authority → ρ mapping** (bounded by event horizon):

  - raw logistic in (0, 1), then scaled by ρ_event ≈ 0.7419

Outputs:

- `rho_plunder_equiv` — ρ-like scalar in (0, ρ_event]
- `collapse_risk` — dimensionless risk index (relative, not a calibrated probability)
- `rho_band` — qualitative band: `"low" | "warn" | "high" | "extreme" | "beyond"`

This scalar law is intentionally conservative in how it is interpreted:

- ρ_event is a **theoretical ceiling**, not an everyday collapse threshold.
- Empirical calibration suggests human systems already look pathological in much lower ρ bands (see below).

---

## 4. ρ-Dynamics (v3)

We can treat ρ(t) as a state variable and model its evolution as the balance between:

- **Plunder** (centralising, ρ ↑),
- **Voluntary exchange** (decentralising, ρ ↓).

Coarse-grained law:

\[
  \dot{\rho} = \alpha(1 - \rho) - \beta\rho = \alpha - (\alpha + \beta)\rho,
\]

with:

- α ≥ 0: effective plunder intensity,
- β ≥ 0: effective voluntary / anti-plunder intensity.

Fixed point:

\[
  \rho_* = \frac{\alpha}{\alpha + \beta}.
\]

If we imagine a system “tuned” to live at the event horizon ρ_event:

\[
  \frac{\alpha}{\beta}_\text{event}
  = \frac{\rho_{\text{event}}}{1 - \rho_{\text{event}}}
  \approx 2.875.
\]

Empirical finding (Dec 2025):

- For at least one large real system (arXiv CS citations 1991–2024), fitted |α/β| ≪ 1 and ρ* ≪ 0.01.
- No large human system studied so far has α/β anywhere near 2.875 or ρ* in the high bands.

Details:

- [`RHO_DYNAMICS.md`](./RHO_DYNAMICS.md)

---

## 5. Empirical Calibration (Human Systems, Dec 2025)

From tests across 50+ real directed networks (citations, social/trust graphs, governance, email, transactions, private coordination groups):

- **Typical “healthy” ρ:**

  - Long-lived human systems: roughly ρ ∈ [10⁻⁶, 10⁻²].

- **Extreme, but still functioning:**

  - Hype citation fields (COVID-19 vaccines, CRISPR, deep learning): ρ up to ≈ 0.029.
  - Centralised social/interaction networks (high-control communities, governance cliques): ρ up to ≈ 0.07 in systems that still survived ≥1 year.

- **Short-lived collapse case:**

  - A private pump-and-dump coordination group reached ρ ≈ 0.098 and collapsed within ~two weeks.

**Human soft bands (provisional):**

- ρ ≤ 0.01 → **green**: open / multi-path / low risk.
- 0.01–0.03 → **yellow**: brittle / hype / strong hierarchies but still functioning.
- 0.03–0.05 → **orange**: high risk of fragmentation / crisis.
- 0.05–0.10 → **red**: near-collapse; observed systems here tend to die or radically reconfigure on short time scales.
- >0.10 → **black**: no functioning system observed in this regime so far.

**Key insight:**

> The universal constant ρ_event ≈ 0.7419 sits far above anything humans have managed in practice. It acts as a **hard ceiling / event horizon** in ρ-space. Human systems appear to self-destruct, fragment, or decentralise long before reaching that theoretical boundary.

A concise calibration narrative is also embedded in:

- [`RHO_STACK_OVERVIEW.md`](./RHO_STACK_OVERVIEW.md)  
- [`GRAPH_RHO_LAW.md`](./GRAPH_RHO_LAW.md)

---

## 6. How to Use This Repo

### 6.1 For Graph Data (Public or Private)

1. Build a weight matrix W:

   - Nodes = actors (papers, accounts, addresses, institutions, etc.).
   - w_ij = influence from j → i (citations, follows, endorsements, transactions, etc.).

2. Call:

   ```python
   from graph_rho_law import compute_graph_rho, classify_human_rho

   result = compute_graph_rho(W)
   print(result.A, result.D, result.rho)
   print(classify_human_rho(result.rho))