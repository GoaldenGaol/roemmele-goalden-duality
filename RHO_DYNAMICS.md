# ρ-Dynamics Spec (v3 Dynamics)  
## A Minimal Evolution Law for the ρ-Invariant

This document defines a **dynamical law** for the ρ-invariant,

\[
  \rho(t) = A(t)^2 \bigl(1 - D(t)\bigr),
\]

where:

- \(A(t)\) is **authority** (centralised control strength), and  
- \(D(t)\) is **evidence diversity** (fraction of independent information paths),

and shows how systems flow toward either:

- a **subcritical open-futures regime** (\(\rho < \rho_\text{crit}\)), or  
- a **supercritical collapse regime** (\(\rho > \rho_\text{crit}\)),

depending on the balance between **plunder** and **voluntary exchange**.

The universal critical threshold is

\[
  \rho_\text{crit} \approx 0.7419.
\]

---

## 1. Setup: Graph ρ-Law Recap

At each time \(t\), the system is represented by a weighted directed graph:

- Nodes \(V = \{1,\dots,N\}\)
- Weights \(w_{ij}(t) \ge 0\): influence from node \(j\) to node \(i\)

Weight matrix:

\[
W(t) = [w_{ij}(t)]_{i,j=1}^N.
\]

Outgoing distributions (column normalisation):

\[
p_{ij}(t) = \frac{w_{ij}(t)}{\sum_k w_{kj}(t) + \varepsilon}.
\]

### 1.1 Authority \(A(t)\)

We define authority as the **maximum incoming share** captured by any node:

\[
A(t) := \max_j \frac{\sum_i w_{ij}(t)}{\sum_{i,k} w_{ik}(t)}.
\]

Interpretation: the fraction of total influence captured by the strongest hub.

(Alternative equivalent definitions—e.g. spectral radius or max centrality—can
be used without changing the qualitative results.)

### 1.2 Diversity \(D(t)\)

Per-node entropy of outgoing distribution:

\[
H_j(t) = -\sum_i p_{ij}(t)\,\log p_{ij}(t).
\]

Normalized per-node diversity:

\[
H_{j,\text{norm}}(t) = \frac{H_j(t)}{\log N} \in [0,1].
\]

Global diversity:

\[
D(t) := \frac{1}{N}\sum_{j=1}^N H_{j,\text{norm}}(t) \in [0,1].
\]

- \(D(t) \approx 1\): many independent paths, no bottleneck.  
- \(D(t) \approx 0\): flows highly concentrated, few effective paths.

### 1.3 Invariant ρ(t)

\[
\rho(t) := A(t)^2 \bigl(1 - D(t)\bigr).
\]

- High \(A(t)\) = strong hub(s).  
- Low \(D(t)\) = collapsed path diversity.  
- High \(\rho(t)\) = centralised, low-diversity regime.

---

## 2. Voluntary Exchange vs Plunder

We model changes in the graph as the net effect of two processes:

1. **Voluntary exchange** (cooperative, decentralising)
2. **Plunder** (centralising, extractive)

At each timestep:

\[
W(t+\Delta t) = W(t) + \Delta W_\text{vol}(t) - \Delta W_\text{pl}(t).
\]

We impose only **directional constraints**:

### 2.1 Voluntary Exchange

Voluntary moves:

- Soften hubs (reduce the strongest share),
- Create / strengthen alternative paths.

Formally:

\[
\dot{A}_\text{vol}(t) \le 0, \quad
\dot{D}_\text{vol}(t) \ge 0.
\]

### 2.2 Plunder

Plunder moves:

- Strengthen hubs (grow the strongest share),
- Destroy / weaken alternative paths.

Formally:

\[
\dot{A}_\text{pl}(t) \ge 0, \quad
\dot{D}_\text{pl}(t) \le 0.
\]

Total rates:

\[
\dot{A}(t) = \dot{A}_\text{vol}(t) + \dot{A}_\text{pl}(t), \quad
\dot{D}(t) = \dot{D}_\text{vol}(t) + \dot{D}_\text{pl}(t).
\]

---

## 3. Sign of ρ̇: Monotone Effects

Differentiate

\[
\rho(t) = A(t)^2 \bigl(1 - D(t)\bigr),
\]

to get:

\[
\dot{\rho}(t) = 2A(1-D)\dot{A} - A^2 \dot{D}.
\]

Split into voluntary and plunder contributions:

\[
\dot{\rho} = \dot{\rho}_\text{vol} + \dot{\rho}_\text{pl},
\]

with

\[
\dot{\rho}_\text{vol}
  = 2A(1-D)\dot{A}_\text{vol} - A^2 \dot{D}_\text{vol},
\]
\[
\dot{\rho}_\text{pl}
  = 2A(1-D)\dot{A}_\text{pl} - A^2 \dot{D}_\text{pl}.
\]

Using the sign constraints:

- Voluntary:
  - \(\dot{A}_\text{vol} \le 0\) and \(1-D \ge 0\) ⇒ first term ≤ 0.
  - \(\dot{D}_\text{vol} \ge 0\) ⇒ second term ≤ 0.
  ⇒ **\(\dot{\rho}_\text{vol} \le 0\)** (voluntary exchange always pushes ρ down).

- Plunder:
  - \(\dot{A}_\text{pl} \ge 0\) ⇒ first term ≥ 0.
  - \(\dot{D}_\text{pl} \le 0\) ⇒ second term ≥ 0.
  ⇒ **\(\dot{\rho}_\text{pl} \ge 0\)** (plunder always pushes ρ up).

Thus ρ is a **competition** between one process that monotonically decreases it
and one that monotonically increases it.

---

## 4. Coarse-Grained Evolution Law for ρ(t)

We approximate the net effect as:

\[
\dot{\rho}(t) = \alpha(t)\,F_\text{pl}(\rho) - \beta(t)\,F_\text{vol}(\rho),
\]

where:

- \(\alpha(t) \ge 0\): **plunder intensity** at time t,  
- \(\beta(t) \ge 0\): **voluntary / anti-plunder intensity** at time t,  
- \(F_\text{pl}, F_\text{vol} \ge 0\): sensitivity of ρ to each process.

A minimal choice with the right qualitative behavior is:

- \(F_\text{pl}(\rho) = (1 - \rho)\): plunder has more effect when ρ is low.  
- \(F_\text{vol}(\rho) = \rho\): voluntary corrections have more effect when ρ is high.

Then:

\[
\dot{\rho}(t) = \alpha(t)(1 - \rho(t)) - \beta(t)\rho(t).
\]

On any time interval where \(\alpha\) and \(\beta\) can be treated as
approximately constant, this reduces to a linear ODE:

\[
\dot{\rho} = \alpha - (\alpha + \beta)\rho.
\]

Solution:

\[
\rho(t) = \rho_* + \bigl(\rho(0) - \rho_*\bigr)e^{-(\alpha + \beta)t},
\]

with unique fixed point:

\[
\rho_* = \frac{\alpha}{\alpha + \beta}.
\]

---

## 5. Universal Critical Ratio

The universal collapse threshold is:

\[
\rho_\text{crit} \approx 0.7419.
\]

In the coarse-grained dynamics, the long-run regime is decided by whether

\[
\rho_* \lessgtr \rho_\text{crit}.
\]

Compute the critical ratio of plunder to voluntary intensities:

\[
\rho_* < \rho_\text{crit}
\quad\Leftrightarrow\quad
\frac{\alpha}{\alpha + \beta} < \rho_\text{crit}
\quad\Leftrightarrow\quad
\frac{\alpha}{\beta}
    < \frac{\rho_\text{crit}}{1 - \rho_\text{crit}}.
\]

Numerically:

\[
\frac{\rho_\text{crit}}{1 - \rho_\text{crit}}
\approx \frac{0.7419}{0.2581} \approx 2.875.
\]

**Result:**

- If
  \[
    \frac{\alpha}{\beta} < 2.875,
  \]
  then \(\rho_* < \rho_\text{crit}\): the system converges to a
  **subcritical, open-futures regime**.

- If
  \[
    \frac{\alpha}{\beta} > 2.875,
  \]
  then \(\rho_* > \rho_\text{crit}\): the system converges to a
  **supercritical, collapsed / locked regime**.

In words:

> There is a universal critical ratio of centralising processes (plunder)
> to decentralising processes (voluntary exchange) such that if plunder
> overwhelms voluntary exchange by more than ≈ 2.875×, the system’s long-run
> ρ is forced into the collapse band.

---

## 6. Connection to Scalar Laws (e.g., v2 Roemmele–Goalden)

In many domains we do not observe the full graph \(W(t)\), but only scalar
aggregates over time:

- counts of centralised authority (citations, wealth, power),
- proxies for diversity (number of independent sources, variety of players),
- plus age and crisis markers (retractions, scandals, wars, crashes).

The **v2 Roemmele–Goalden collapse law** is then interpreted as a
**low-dimensional estimator** of ρ and of the effective ratio \(\alpha/\beta\):

- Bibliometric authority and impact approximate \(A(t)\);
- Provenance and authorship diversity approximate \(D(t)\);
- Age and empirical distrust modulate how long a high-ρ configuration has
  persisted and how often it has been partially reset by crises.

If repeated estimates of ρ from scalar laws and from graph-based ρ both
cluster their empirical transitions near \(\rho_\text{crit} \approx 0.7419\),
this supports the claim that the same **underlying ρ-dynamics** governs
a wide class of physical, social, and epistemic systems.

---

## 7. Usage and Open Questions

**Usage:**

- Estimate \(\alpha\) and \(\beta\) in a given domain by regressing observed
  changes in ρ (scalar or graph-based) against plausible plunder vs voluntary
  signals.
- Check whether observed trajectories ρ(t) are consistent with the linear
  evolution law:
  \[
    \dot{\rho} \approx \alpha - (\alpha + \beta)\rho.
  \]
- Evaluate whether real-world systems that collapse or lock-in indeed exhibit
  long-run \(\rho_*\) above \(\rho_\text{crit}\), and whether stable, open
  systems exhibit \(\rho_* < \rho_\text{crit}\).

**Open questions:**

- Can we derive the specific form
  \(\dot{\rho} = \alpha(1-\rho) - \beta\rho\) from microscopic update rules
  on \(W(t)\) for broad classes of systems?
- Is \(\rho_\text{crit} \approx 0.7419\) truly universal across network
  ensembles and domains, or does it emerge as a fixed point under
  coarse-graining (RG-like behavior)?
- How do higher-order structures (motifs, cycles, communities) modify
  the effective \(\alpha/\beta\) ratio and thus the long-run regime?

This document records the **ρ-dynamics conjecture**: that a simple evolution
law for ρ, driven by the relative strength of plunder vs voluntary exchange,
underlies a wide family of collapse and lock-in phenomena in physical,
social, and epistemic systems.