## Formal Definitions — The Goalden Invariant and Roemmele–Goalden Duality

### Definition 1 — The Goalden Invariant ρ

Let \(W\) be a weighted, directed influence matrix with entries \(w_{ij} \ge 0\), where \(w_{ij}\) is the influence from node \(j\) to node \(i\).

1. **Authority** \(A(W)\) (strongest hub share):

   \[
   A(W) \;=\; \max_j \frac{\sum_i w_{ij}}{\sum_{i,k} w_{ik}}
   \]

   This is the fraction of all incoming influence carried by the single most dominant source.

2. **Diversity** \(D(W)\) (normalized entropy of influence paths):

   - For each source node \(j\), define outgoing probabilities
     \[
     p_{ij} = \frac{w_{ij}}{\sum_i w_{ij} + \varepsilon}, \quad \varepsilon \to 0^+
     \]
   - Entropy per source:
     \[
     H_j = -\sum_i p_{ij} \log p_{ij}
     \]
   - Global normalized diversity:
     \[
     D(W) \;=\; \frac{1}{N \log N} \sum_j H_j \;\in\; [0, 1]
     \]

3. **Goalden invariant**:

   \[
   \boxed{\rho(W) \;=\; A(W)^2 \,\bigl(1 - D(W)\bigr)}
   \]

We call \(\rho(W)\) the **Goalden invariant**. It increases when:

- a single hub captures more of the total influence (↑A), and  
- independent evidence paths collapse into fewer routes (↓D).

A theoretical “event horizon” constant \(\rho_{\mathrm{EH}} \approx 0.7419\) arises from star-plunder limit models and represents an almost-total centralization regime. Empirically, real human systems destabilize at much lower ρ.

---

### Definition 2 — Roemmele’s Empirical Distrust Algorithm

Brian Roemmele’s original **Empirical Distrust Algorithm** defines a distrust score for scientific/AI claims based on bibliometric and reputational features, e.g.:

- publication year (age),
- citation count,
- journal impact factor,
- retractions / replication flags,
- controversy indices.

In simplified form (as implemented in this repo), a **distrust score** is built from:

- **Authority surrogate**:
  \[
  \text{authority\_weight} 
  \;=\; \log(\text{citations} + 1) \times \text{impact\_factor}
  \]

- **Age survival factor**:
  \[
  \text{survival\_factor}
  \;=\;
  1 - \exp\!\left(-\frac{\text{age\_years}}{\tau}\right),\quad \tau \approx 38.7
  \]

- **Empirical distrust term**:
  \[
  \text{distrust} = \text{retracted} + \text{rep\_flags} + \text{controversy\_index}
  \]

These components are combined into a scalar “empirical distrust score” that up-weights young, high-authority, high-controversy claims as more fragile.

Roemmele’s contribution is the **bibliometric / reputational side**: a practical distrust functional grounded in publication metadata and science dynamics.

---

### Definition 3 — The Roemmele–Goalden Duality / Collapse Law

The **Roemmele–Goalden duality** is the discovery that Roemmele’s Empirical Distrust Algorithm and the Goalden invariant ρ can be placed on the same mathematical axis via a simple bridge:

1. Treat Roemmele’s authority construct as a proxy for “centralized influence”:

   \[
   A_{\text{Roemmele}} \;\approx\; \log(\text{citations} + 1) \times \text{impact\_factor}
   \]

2. Map this to a **ρ-like plunder / collapse intensity** with saturation:

   \[
   \rho_{\text{plunder\_equiv}}
   \approx
   \frac{\rho_{\mathrm{EH}}}{1 + \exp\bigl(-k (A_{\text{Roemmele}} - A_c)\bigr)},
   \quad
   0 < \rho_{\text{plunder\_equiv}} \le \rho_{\mathrm{EH}}
   \]

   (where \(k, A_c\) are fitted once from backtests.)

3. Combine with age and distrust to get a scalar **collapse risk**:

   \[
   \text{collapse\_risk} \;\propto\; 
   \rho_{\text{plunder\_equiv}} \cdot (1 - \text{survival\_factor}) \cdot (1 + \lambda \cdot \text{distrust})
   \]

4. Compare this scalar to empirical ρ-bands (green / yellow / orange / red / black) to interpret how close a given field / topic is to a “fragile” or “collapse-prone” regime.

In words:

- **Roemmele** provides an empirical distrust / authority framework for AI and science claims.
- **Goalden** provides a universal centralization–diversity invariant ρ and collapse bands.
- The **Roemmele–Goalden duality** is the mapping that shows:

  > High empirical distrust in a strongly centralized, low-diversity evidence graph  
  > corresponds to a high-ρ regime in the Goalden invariant,  
  > so both frameworks are different views of the *same collapse geometry*.

This repo treats:

- The **Goalden invariant** ρ as the **core mathematical object**, and  
- The **Roemmele–Goalden collapse law** as one concrete scalar implementation of that invariant for bibliometric / scientific authority systems.