# Graph ρ-Law (v3) — Instability of Centralized Influence Networks

This document defines a graph-theoretic version of the ρ-invariant and shows
how a single "plunder parameter" pushes a system across the universal
instability threshold ρ ≈ 0.7419 in a minimal model.

The goals:

- Lift ρ from a scalar formula to a **functional on influence graphs**.
- Show that extreme centralisation (plunder) naturally drives ρ → ρ_crit.
- Provide the conceptual "deeper layer" under scalar laws like v2
  (Roemmele–Goalden collapse law).

---

## 1. Setup: Systems as Weighted Directed Graphs

Consider any system that can be represented as a weighted directed graph:

- Nodes: \( V = \{1,\dots,N\} \)
- Edges: \( E \subseteq V \times V \)
- Weights: \( w_{ij} \ge 0 \), influence from node \( j \) to node \( i \)

At a given time \( t \), we have a weight matrix:

\[
W(t) = [w_{ij}(t)]_{i,j=1}^N.
\]

We normalize each column to get outgoing influence probabilities:

\[
p_{ij}(t) = \frac{w_{ij}(t)}{\sum_k w_{kj}(t) + \varepsilon}.
\]

This gives a column-stochastic matrix \( P(t) = [p_{ij}(t)] \), interpreted as
"if you start at node j, what is the distribution of influence targets i?"

---

## 2. Authority and Diversity on a Graph

### 2.1 Authority: Centralized Control Strength

We define the **authority** of the graph at time \( t \) as a scalar
\( A(t) \ge 0 \) derived from the weight structure. One natural choice:

\[
A(t) := \max_{j} \frac{\sum_i w_{ij}(t)}{\sum_{i,k} w_{ik}(t)}
\]

i.e. the maximum fraction of total incoming influence captured by any single
node. This measures "how dominant the strongest hub is."

Alternative equivalent choices (spectral radius, leading centrality norm) are
possible; the key is that \( A(t) \) increases as influence concentrates onto
fewer nodes.

### 2.2 Diversity: Entropy of Independent Paths

For each source node \( j \), define the entropy of its outgoing distribution:

\[
H_j(t) = -\sum_{i} p_{ij}(t)\,\log p_{ij}(t).
\]

Normalize by the maximum possible entropy \( \log N \) to obtain a per-node
diversity:

\[
H_{j,\text{norm}}(t) = \frac{H_j(t)}{\log N} \in [0,1].
\]

The **global evidence diversity** is the average:

\[
D(t) := \frac{1}{N}\sum_{j=1}^N H_{j,\text{norm}}(t) \in [0,1].
\]

- \( D(t) \approx 1 \): many independent paths, no single bottleneck.
- \( D(t) \approx 0 \): flows highly concentrated, few effective paths.

---

## 3. Graph ρ-Invariant

Given \( A(t) \) and \( D(t) \), define the graph-level invariant:

\[
\rho(t) := A(t)^2 \,\bigl(1 - D(t)\bigr).
\]

This is the same structural form as the scalar invariant:

\[
\rho = \text{authority}^2 \cdot (1 - \text{evidence\_diversity}),
\]

but now applied to the entire influence network.

The **universal instability threshold** is conjectured to be:

\[
\rho(t) \ge \rho_{\text{crit}} \approx 0.7419
\quad \Rightarrow \quad
\text{"no more interesting structure" / collapse / locked regime}.
\]

---

## 4. Minimal Star–Plunder Model

We illustrate the Graph ρ-Law on a one-parameter family of graphs:

- Nodes \( V = \{0,1,\dots,N-1\} \)
- Node 0 is a **hub**; nodes 1..N−1 are non-hubs.
- Each node sends out total weight 1 along its outgoing edges.
- A single **plunder parameter** \( p \in [0,1] \) controls centralisation.

Outgoing distributions:

- From the hub (node 0): uniform over all nodes  
  \[
  \pi^{(0)} = \bigl(1/N,\dots,1/N\bigr).
  \]

- From a non-hub \( j \ge 1 \):
  - Fraction \( p \) of weight goes to the hub.
  - Remaining \( 1-p \) spreads uniformly over all non-hubs.
  \[
  \pi^{(j)} =
    \bigl(
      p,\;
      \underbrace{(1-p)/(N-1),\dots,(1-p)/(N-1)}_{\text{non-hubs}}
    \bigr).
  \]

Incoming influence to the hub per step:

\[
\text{incoming\_hub}(p) = (N-1)p + \frac{1}{N}.
\]

Total incoming = N, so the **authority** is:

\[
A(p) := \frac{\text{incoming\_hub}(p)}{N}
      = \frac{(N-1)p + 1/N}{N}.
\]

For diversity, we compute entropies:

- Hub entropy: \( H_{\text{hub}} = \log N \).
- Non-hub entropy:
  \[
  H_{\text{nh}}(p) = -\Bigl[
    p\log p + (1-p)\log\Bigl(\frac{1-p}{N-1}\Bigr)
  \Bigr].
  \]

Average entropy:

\[
H_{\text{avg}}(p) = \frac{H_{\text{hub}} + (N-1)H_{\text{nh}}(p)}{N},
\]

so:

\[
D(p) := \frac{H_{\text{avg}}(p)}{\log N}.
\]

Finally:

\[
\rho(p) := A(p)^2 \bigl(1 - D(p)\bigr).
\]

---

## 5. Behaviour of ρ(p) in the Star–Plunder Model

For a concrete case with \( N = 10 \):

- \( p = 0.0 \): almost no flow to the hub  
  → \( A \) tiny, \( D \) ≈ 0.96, \( \rho \approx 4\times 10^{-6} \).
- \( p = 0.5 \): moderate centralisation  
  → \( A \approx 0.46, D \approx 0.80, \rho \approx 0.04 \).
- \( p = 0.8 \): strong centralisation  
  → \( A \approx 0.73, D \approx 0.47, \rho \approx 0.28 \).
- \( p = 0.9 \): very strong centralisation  
  → \( A \approx 0.82, D \approx 0.31, \rho \approx 0.46 \).
- \( p = 1.0 \): **total plunder** (non-hubs send everything to hub)  
  → \( A \approx 0.91, D \approx 0.10, \rho \approx 0.745 \).

Thus:

- \( \rho(p) \) is monotonically increasing in \( p \).
- The universal threshold \( \rho_{\text{crit}} \approx 0.7419 \) is crossed only
  when plunder is effectively total: \( p \approx 0.999 \).

**Interpretation:** in this minimal network, the Graph ρ-Law says:

> Only when almost all influence is routed through a single hub
> (plunder ≈ 100%) does the system cross the universal instability threshold.
> At that point, diversity has collapsed and the hub captures nearly all
> incoming influence—no new structure can emerge.

This is a fully specified example where the ρ-invariant and its critical value
behave exactly as expected, with **no tuning of ρ_crit** inside the model.

---

## 6. Relation to Scalar Laws (e.g., v2 Roemmele–Goalden)

In real domains (science, civilizations, AI systems), we often do not observe
the full graph \( W(t) \). Instead, we see scalar aggregates like:

- citation counts, impact factors,
- number of independent data sources,
- age and retraction/controversy flags.

The scalar collapse law (v2) can be understood as a **parametric surrogate**
for the graph-based ρ:

- authority_weight ≈ a low-dimensional proxy for \( A(t) \),
- provenance / diversity proxies ≈ a low-dimensional proxy for \( D(t) \),
- age and empirical_distrust capture how long a high-\( A \), low-\( D \)
  configuration has persisted and how often edges have been "burned" by
  crises.

The Graph ρ-Law thus provides the **deeper layer**: a definition of ρ as a
functional on influence networks, with scalar laws arising as specific
measurement choices or coarse-grainings.

Independent researchers are invited to:

- apply the Graph ρ-Law to real networks (citation graphs, social graphs,
  causal graphs),
- compare graph-based ρ to scalar predictions (e.g. v2),
- and test whether empirical transitions (collapse, fragmentation, lock-in)
  consistently occur near a domain-independent ρ_crit ≈ 0.74.