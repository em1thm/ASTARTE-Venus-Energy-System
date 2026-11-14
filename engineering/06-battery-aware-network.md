# ASTARTE V2 — Mechanoron V0.2: Battery-Constrained Dispatch Study

**Document ID:** AST-ENG-006  
**Revision:** 0.1 — algorithmic feasibility model  
**Date:** 12 November 2026  
**Related work:** [Mission requirements](01-mission-requirements.md), [Battery chemistry](02-battery-chemistry.md), [Mechanoron topology](05-mechanoron-network.md)

## Design question

Can a fault-tolerant topological distribution network maintain the stationary science workload when one battery source is lost, while suspending optional mobility when peak power is insufficient?

## Method

`simulation/mechanoron_v02.py` combines the existing pentakis-dodecahedron connectivity model with two energy sources and the preliminary 60-day daily load schedule from AST-ENG-001. It checks source-to-critical-load connectivity, aggregate power constraints, remaining module energy, reserve and assumed daily self-discharge. Each modeled day includes housekeeping, science, communication and an optional traverse. The controller serves the required activities first; mobility is skipped if it cannot meet the modeled power and energy conditions.

### Hypothetical assumptions

| Quantity | Assumed value | Evidence status |
|---|---:|---|
| Sources / positions | 2; `u0`, `u5` | Network modelling assumption |
| Usable energy at start | 1,500 Wh per source | Hypothetical; **not a measured LiSi/FeS capacity** |
| Input power limit | 65 W per source | Hypothetical; **not a validated high-temperature cell power limit** |
| Distribution efficiency | 85% | System-design assumption |
| Daily self-discharge | 0.1% of current inventory | Sensitivity assumption |
| Protected reserve | 20% of each source's initial energy | Controller policy assumption |
| Fault event | `u5` unavailable from day 20 | Scenario definition |
| Daily delivered energy, if mobility is completed | 22 Wh | Derived from assumed AST-ENG-001 load schedule |
| Critical load schedule without mobility | 9.5 Wh/day | Derived from AST-ENG-001 |

**Interpretation:** The numerical results below demonstrate a controller concept *under the specified assumptions*. They establish neither a 60-day Venus-qualified battery nor an electrical hardware implementation.

## Energy equations

For source `i` in day `d`, the simplified charge inventory evolves as:

\[
E_{i,d}^{\mathrm{after\ leak}} = E_{i,d}^{\mathrm{before\ leak}}(1-s),
\qquad
E_{i,d+1} = E_{i,d}^{\mathrm{after\ leak}} - E_{i,d}^{\mathrm{drawn}}.
\]

To authorize a load event of delivered power `P` lasting `t`, the model checks (a) reachability of the critical loads, (b) aggregate source power limit, and (c) accessible energy above each module's protected reserve. Discharged battery energy for that event is approximated by

\[
E_{\mathrm{drawn}} = Pt/\eta_d.
\]

The model reserves concurrent housekeeping power in the peak-power screen for short science, communications and mobility events. Event-level energy withdrawal uses the incremental load to avoid double-counting the housekeeping energy charged over 24 hours.

## Verification cases

1. Nominal two-source mission: check that critical work and optional mobility can be completed for 60 days in the assumed case.
2. Failure of `u5` on day 20: check the controller retains required work and suspends mobility if remaining power is insufficient.
3. Failure of `u5` on day 1: check optional mobility is suspended immediately.
4. Graph disconnection: isolate a critical ring node by cutting two of its edges and verify failure is reported.
5. Sensitivity: larger assumed self-discharge must reduce end-of-mission energy.

## Scope and planned V0.3 corrections

- **Node accessibility is a binary topological gate**, not post-fault nodal DC power-flow analysis.
- Both sources are idealized as interchangeable energy reservoirs with peak input power constraints. Real cells require terminal voltage curves, temperature/state-of-charge dependent internal resistance and continuous/pulse current specifications.
- Existing V0.1 CSV voltage and ohmic-loss values are *pre-fault nominal values* repeated alongside fault-count summaries; they should not be interpreted as post-fault electrical predictions.
- Dynamic loads, source balancing and protective actions are simplified at a daily granularity. No cell aging, thermal transients, motor start-up surge, switch leakage, connector failure or physical cable geometry is included.
- A later design must allocate sources and switches to physically realizable battery strings and confirm that switching cannot cause undesired shorts or incompatible voltage combinations.

**Next evidence gate:** obtain a defensible per-cell energy/power model at 465°C before assigning physical module counts and CAD dimensions.

## Reproduction

From repository root (Python 3.10+, standard library):

```powershell
python -m unittest discover -s simulation -p "test_*.py" -v
python simulation/mechanoron_v02.py simulation/mechanoron_v02_results.csv
```

This document belongs to the **2026 independent redesign**; the original 2022 ASTARTE was a Team Aldebaran collaboration.
