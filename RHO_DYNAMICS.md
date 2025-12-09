# RHO_DYNAMICS.md — ρ-Dynamics and the Event-Horizon Ratio

This document describes how the ρ-invariant can be treated as a **state
variable** that evolves over time under two competing forces:

- Voluntary exchange (decentralising, ρ ↓),
- Plunder / capture (centralising, ρ ↑).

We build a simple coarse-grained evolution law and connect it to:

- The **theoretical event horizon** ρ_event ≈ 0.7419, and
- The **empirical human bands** (ρ ≪ 0.1 as of Dec 2025).

---

## 1. Intuition: What Moves ρ Up or Down?

From the graph ρ-law:

\[
  \rho(t) = A(t)^2 \,\bigl(1 - D(t)\bigr),
\]

where:

- A(t): strongest hub’s share of incoming influence,
- D(t): average normalized entropy of outgoing distributions.

Then:

- Voluntary exchange (more peer-to-peer, more open paths):
  - tends to **reduce** A(t),
  - tends to **increase** D(t),
  - ⇒ **decreases** ρ(t).

- Plunder / capture (monopolisation, censorship, “all roads lead to X”):
  - tends to **increase** A(t),
  - tends to **decrease** D(t),
  - ⇒ **increases** ρ(t).

So at a coarse-grained level, we can write:

\[
  \dot{\rho}(t) = \dot{\rho}_\text{plunder}(t)
                + \dot{\rho}_\text{voluntary}(t),
\]

with the sign of each contribution fixed by construction.

---

## 2. Coarse-Grained Evolution Law

We approximate:

- Plunder contribution:

  \[
    \dot{\rho}_\text{plunder} \approx \alpha (1 - \rho),
  \]

  where α ≥ 0 is an effective **plunder intensity** and (1−ρ) ensures
  diminishing returns near the ceiling.

- Voluntary contribution:

  \[
    \dot{\rho}_\text{voluntary} \approx -\beta \rho,
  \]

  where β ≥ 0 is an effective **voluntary / anti-plunder intensity** and ρ
  ensures that the downward pull is stronger when ρ is already high.

Combining:

\[
  \dot{\rho} = \alpha(1 - \rho) - \beta \rho
             = \alpha - (\alpha + \beta)\rho.
\]

In discrete time (e.g., yearly snapshots):

\[
  \Delta \rho(t) \approx \alpha - (\alpha + \beta)\rho(t).
\]

---

## 3. Fixed Point and α/β Ratio

If α and β are approximately constant over some time window, then the
fixed point is:

\[
  \rho_* = \frac{\alpha}{\alpha + \beta} \in [0,1].
\]

- High α/β ⇒ ρ* closer to 1 (plunder dominates in the long run).
- Low α/β ⇒ ρ* closer to 0 (voluntary exchange dominates).

We can also invert:

\[
  \frac{\alpha}{\beta} = \frac{\rho_*}{1 - \rho_*}
\]

whenever β > 0.

---

## 4. Event-Horizon Ratio (Theoretical)

The scalar theory and synthetic graph experiments identify a **universal
event horizon** at:

\[
  \rho_{\text{event}} \approx 0.7419.
\]

If we imagine a system that has settled exactly at this event horizon
as its fixed point (ρ* = ρ_event), then the corresponding α/β is:

\[
  \frac{\alpha}{\beta}_\text{event}
  = \frac{\rho_{\text{event}}}{1 - \rho_{\text{event}}}
  \approx \frac{0.7419}{0.2581}
  \approx 2.875.
\]

Interpretation:

- Systems with α/β **near 2.875** (under this simple model) would be
  “tuned” to live in an event-horizon regime, where plunder dominates
  strong enough to keep ρ near ~0.74.

Empirical finding (Dec 2025):

- In at least one large, real system (arXiv Computer Science citation
  network, 1991–2024), fitting this law yields |α/β| ≪ 1, i.e. the
  system operates deep in the open regime with a very low implied ρ*.

So far, **no large human influence system studied has shown an α/β even
remotely near 2.875**; this matches the observation that realised ρ values
for humans remain ≪ 0.1.

---

## 5. Estimating α and β from Data

Given a time series of ρ(t_k), for k = 0,1,…,T (e.g., yearly ρ for a field
or community):

1. Compute the increments:

   \[
     \Delta \rho_k = \rho(t_{k+1}) - \rho(t_k).
   \]

2. Fit the linear model:

   \[
     \Delta \rho_k \approx \alpha - (\alpha + \beta)\rho(t_k)
   \]

   using standard regression to solve for:

   - intercept ≈ α,
   - slope ≈ −(α + β).

3. Recover:

   - α from the intercept,
   - (α + β) from the negative slope,
   - β = (α + β) − α,
   - α/β and ρ* = α/(α + β), when β is not too close to 0.

4. Compare:

   - α/β vs the **event-horizon ratio** ≈ 2.875.
   - ρ* vs **empirical human bands** (e.g., <0.01, 0.03, 0.05, 0.10).

If the fitted α/β is small (|α/β| ≪ 1) and ρ* ≪ 0.1, the system is far
inside the open, structure-forming regime.

---

## 6. Example: arXiv CS 1991–2024 (Empirical)

For the arXiv Computer Science citation network (nodes = papers, edges =
j→i if j cites i), yearly ρ(t) was estimated from 1991–2024 using the
graph ρ-law.

Observed properties:

- ρ rose slowly from ~10⁻⁴ to ~2.3×10⁻³ over three decades.
- It remained orders of magnitude below any known “danger” band for humans.

Linear fit yields:

- α ≈ 2.2×10⁻⁵,
- β slightly negative (due to model mismatch / saturation effects),
- |α/β| ≪ 1.

Interpretation:

- arXiv CS sits deep in the low-ρ regime.
- The plunder vs voluntary balance implied by this fit is nowhere near
  the theoretical event-horizon ratio.

---

## 7. Human Interpretive Bands (Dec 2025, Provisional)

Empirical calibration across multiple domains suggests:

- ρ ≲ 0.01:
  - “Green zone” — open, multi-path, low risk.
- 0.01 ≲ ρ ≲ 0.03:
  - “Yellow zone” — canon/hype, brittle but still functioning.
- 0.03 ≲ ρ ≲ 0.05:
  - “Orange zone” — high-risk centralisation.
- 0.05 ≲ ρ ≲ 0.10:
  - “Red zone” — near-collapse; systems observed here tended to fragment or
    die shortly thereafter (e.g., a pump-and-dump group at ρ ~ 0.098).

The event horizon ρ_event ≈ 0.7419 remains a **theoretical ceiling**:
no functioning human system has yet reached anywhere near it.

In practice:

- Use ρ(t) as a **continuous risk indicator**,
- Use α/β to characterise the **direction of drift**:
  - α/β ≪ 1: voluntarily dominated, open regime.
  - Large α/β (if ever observed) would indicate a system being driven
    toward an event-horizon-like configuration.

---

## 8. Relation to Other Levels of the Stack

- **Graph ρ-law (Level 2)**: gives ρ(W_t) at each time slice from network
  structure.
- **ρ-dynamics (this document)**: interprets changes in ρ over time in terms
  of effective plunder and voluntary exchange.
- **Scalar collapse law (Level 1)**: maps domain-specific quantities
  (e.g. bibliometrics) into a ρ-like scalar, which can itself be tracked
  over time and analysed with the same dynamic model.