# RHO_V4_PLAN.md  
Roadmap for ρ-Stack v4 (Early-Warning Engine)

Status as of Dec 2025:
- v3.1: Core invariant ρ is stable and well-defined across domains.
- Wave 2: Large-scale calibration (citation, social, web) → domain-specific band nuance.
- Wave 3: Collapse case studies + N-scaling → ρ is empirically predictive; ρ_eff emerges as useful cross-scale diagnostic.

v4 is not about changing the core law.  
v4 is about turning ρ into a **practical early-warning engine** with:

- clean API,
- domain presets,
- time-series diagnostics,
- and a clear “theorem-like” early-warning claim (backed by data).

---

## 0. Core Principles for v4

1. **Invariant is sacred.**  
   - ρ(W) = A(W)² · (1 − D(W)) remains the core.
   - Authority A and Diversity D stay as defined in `graph_rho_law.py`.

2. **ρ_eff is optional.**  
   - ρ_eff = ρ / ln(N / 100) for N > 100 is a **view**, not a new definition.
   - Use ρ for theory; use ρ_eff for cross-scale comparisons.

3. **Bands are layered, not replaced.**  
   - Global bands (v3.1) remain default.  
   - Domain-specific presets are overlays (academic / social / governance / web).

4. **Time-series is first-class.**  
   - ρ(t), bands(t), and α/β(t) become standard outputs for any dataset with timestamps.

5. **Early-warning is conditional, not mystical.**  
   - “In the datasets tested so far, ρ entering orange/red is an empirical early-warning sign for collapse in certain domains.”  
   - Make assumptions explicit (domain, N range, sampling, etc.).

---

## 1. v4 Components

### 1.1 Core ρ API (no change, just formalization)

**File:** `graph_rho_law.py`

Expose a primary function:

```python
def compute_rho(W, eps=1e-12):
    """
    Compute A, D, rho for a weighted directed influence matrix W.
    Returns:
        A (float): authority
        D (float): diversity
        rho (float): raw invariant
    """
    ...