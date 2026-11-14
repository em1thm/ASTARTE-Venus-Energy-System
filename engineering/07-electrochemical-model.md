# ASTARTE V2 — Mechanoron V0.3: Electrical Cell Model and Mission-Level Sensitivity Analysis

**Document ID:** AST-ENG-007  
**Revision:** 0.1 — conceptual model, 14 November 2026  
**Related files:** [`01-mission-requirements.md`](01-mission-requirements.md), [`02-battery-chemistry.md`](02-battery-chemistry.md), [`06-battery-aware-network.md`](06-battery-aware-network.md)  
**Software:** [`../simulation/mechanoron_v03.py`](../simulation/mechanoron_v03.py), [`../simulation/test_mechanoron_v03.py`](../simulation/test_mechanoron_v03.py), [`../simulation/mechanoron_v03_results.csv`](../simulation/mechanoron_v03_results.csv)  
**Status:** Reproducible sensitivity analysis; no ASTARTE electrochemical cells or high-temperature power modules have been built or qualified.

## 1. Design question

Can the Mechanoron dispatch concept preserve a 60-Earth-day critical science workload when its two energy sources are constrained by hypothetical cell voltage, internal resistance, charge capacity, current limits, and source failures? How do parallel cell strings and electrical resistance change the attainable mobility days and resistive heating?

V0.1 evaluated graph connectivity and a nominal low-current DC network. V0.2 combined connectivity with idealized energy reservoirs and peak-power caps. **V0.3 adds a pack-level voltage/current calculation and coulomb-counted state of charge**, while retaining a simplified mission dispatch schedule. It remains a *concept-stage* model with independently regulated energy sources, not a full network power flow.

## 2. What the literature actually establishes

Scherzberg and Miller [E1] describe a lithium-silicon alloy anode, FeS cathode and alkali-halide molten-salt electrolyte. They report an approximately **1.32 V/cell discharge plateau** in a long-life configuration, a 5-cell endurance experiment lasting **152 days** at a half-scale load and a 17-cell battery remaining above 19 V for about **117 days**. NASA's overview describes an **118-day** 17-cell demonstration at Venus temperatures [E2]. The paper identifies parasitic cell-to-cell discharge and migration of lithium-bearing material as significant mechanisms affecting lifetime. These results pertain to the specific experimental conditions and power levels of the research program.

An equivalent-circuit representation of a battery can employ an open-circuit potential and series resistance, with additional RC branches for transient effects [E3, E4]. This is a useful *modelling method*. Neither the generic equivalent-circuit sources nor the long-life NASA paper supplies a calibrated open-circuit-voltage-versus-state-of-charge curve and full resistance/current/capacity map for the proposed ASTARTE V2 cells. Therefore all such parameters below are **declared assumptions**, rather than inferred NASA cell specifications.

## 3. Mathematical model

For each hypothetical cell, positive discharge current follows:

\[
V_{t}=V_{oc}(SOC)-I_{cell}R_{cell}.
\]

At the *source-module* level, for \(N_s\) series cells and \(N_{p,m}\) parallel strings per source:

\[
V_{oc,m}=N_s V_{oc,cell},\qquad
R_m=\frac{N_s R_{cell}}{N_{p,m}},\qquad
Q_m=N_{p,m}Q_{cell}.
\]

The synthetic voltage law used exclusively for sensitivity calculations is:

\[
V_{oc,cell}(SOC)=1.32+0.10(SOC-0.5)\ \mathrm V.
\]

**Important:** 1.32 V from [E1] is a measured **discharge plateau**, not a measured open-circuit voltage. Using it as the midpoint of this synthetic OCV law is a modelling choice that must be replaced once an applicable data series is found.

For a requested battery-terminal power \(P_m\):

\[
P_m=I_m(V_{oc,m}-I_m R_m),
\qquad
I_m=\frac{2P_m}{V_{oc,m}+\sqrt{V_{oc,m}^2-4R_mP_m}}.
\]

The lower-current root is used where a real solution exists. Each event also checks a hypothetical maximum current per parallel string and a minimum terminal voltage per series cell. The model calculates resistive heating as \(\dot Q_{ohmic}=I_m^2R_m\) and updates charge inventory using

\[
SOC_{new}=SOC_{old}-\frac{I_m\Delta t}{Q_m}.
\]

Daily self-discharge is applied as a hypothetical fractional loss of remaining SOC at the start of each day. A separate **85% path efficiency** accounts for aggregated conversion and distribution loss; this factor **excludes the cell's internal \(I^2R\) loss**, preventing that electrical loss from being counted twice. Terminal electrical energy supplied by the source is \(E_{load}/0.85\). The model also sums ohmic heating in watt-hours.

### Mission policy

The 60-day load schedule comes from AST-ENG-001:

| Load | Power when active | Daily duration | Daily delivered energy |
|---|---:|---:|---:|
| Housekeeping | 0.25 W | 24 h | 6.0 Wh |
| Science (incremental) | 2.00 W | 0.50 h | 1.0 Wh |
| Communications (incremental) | 10.00 W | 0.25 h | 2.5 Wh |
| Mobility (incremental) | 75.00 W | 1/6 h | 12.5 Wh |

The 24-hour period is divided into mutually exclusive operating slots. The active-slot power includes concurrent housekeeping, while a skipped traverse becomes a housekeeping-only slot. Thus a fully completed mobile day delivers **22 Wh**, a stationary-only day **9.5 Wh**.

The controller prioritises all three critical science activities. For a proposed mobility event it also runs a conservative **remaining-days critical-energy screening** based on future 9.5 Wh/day usage at the assumed lower voltage limit; that screening is not an accurate predictor of an actual aging battery's future energy. A source failure causes the optional mobility task to be suspended by **explicit conservative policy**, rather than because an electrical failure to deliver the mobility power has been proved.

## 4. Assumptions and provenance

| Parameter | V0.3 assumed value | Status |
|---|---:|---|
| Cell chemistry label | LiSi/FeS molten-salt reference | Research direction [E1] |
| Cells per series string | 19 | Design candidate |
| Parallel strings per source | 2 or 3 | Sensitivity cases; two source modules total |
| Hypothetical cell charge capacity | 20 Ah | Assumed, **not measured in [E1]** |
| Midpoint voltage anchor | 1.32 V | Based on reported *loaded plateau* [E1] |
| OCV versus SOC slope | 0.10 V per unit SOC | Synthetic |
| Internal resistance per cell at 465°C | 0.10 or 0.35 Ω | Synthetic |
| Per-string current cap | 0.70 or 2.0 A | Synthetic |
| Terminal lower-voltage cutoff | 1.00 V per cell | Synthetic |
| Self-discharge | 0.1% of remaining charge/day | Synthetic |
| Path efficiency | 85% | Engineering assumption |
| Protected final SOC | 20% | Operating policy |
| Temperature | 465°C | Reference environment; only an *optional* linear resistance sensitivity factor exists |

The **19S4P** candidate has a total of 76 hypothetical cells, divided into two nominally 19S2P energy-source modules. The **19S6P** candidate uses 114 hypothetical cells as two 19S3P modules. These counts describe electrical groupings only. Geometry, total pack mass, seals, switching devices, physical cell dimensions, module voltage balancing and high-temperature qualification are open.

## 5. Reproduced V0.3 results

All results below were generated by the supplied Python V0.3 code with the parameter values in Section 4. **They are outputs of a hypothetical parameter study, not performance predictions for a flight-qualified LiSi/FeS battery.**

| Simulation case | Critical science days | Mobile days | Integrated cell ohmic heat | Lowest remaining active-source SOC at day 60 |
|---|---:|---:|---:|---:|
| 19S4P, 2.0 A/string | **60/60** | 55/60 | 63.71 Wh | 0.201 |
| 19S4P, 0.70 A/string | **60/60** | 0/60 | 1.84 Wh | 0.624 |
| 19S6P, 2.0 A/string | **60/60** | 60/60 | 43.15 Wh | 0.435 |
| 19S6P, one source fails on day 20 | **60/60** | 19/60 | 14.96 Wh | 0.491 |
| 19S6P, 0.35 Ω/cell instead of 0.10 Ω | **60/60** | 60/60 | 207.42 Wh | 0.382 |

**Reading the comparisons:**

1. Under the specified assumed electrical ratings, protecting future critical science energy causes the 19S4P system to skip five optional traverse days.
2. Tightening the hypothetical cell current cap to 0.70 A/string prevents the mobility power request, even though substantial charge remains.
3. Increasing the number of hypothetical parallel strings reduces current per string, makes more charge available and changes resistive heating.
4. The day-20 source failure removes the failed source's remaining charge from the *accessible* inventory and triggers a **software rule** that suspends further optional mobility. It does not prove that a real surviving battery could not sustain motion.
5. Increasing the assumed internal resistance raises the cell heating integrated over the scheduled load events. No coupled transient thermal calculation is present.

For the full 60-day mobile case, the total delivered-load energy is **1,320 Wh**. With an 85% path efficiency the corresponding path loss is approximately **232.94 Wh**, distinct from the separately reported cell ohmic heat. Self-discharge consumes charge inventory but is not reported as measured dissipated heat.

## 6. Validation and reproducibility

All scripts require Python 3.10 or later and standard-library modules only. V0.3 **imports `mechanoron_network.py` from V0.1**, which must remain in the same `simulation` folder.

Run from the repository root:

```powershell
python -m unittest discover -s simulation -p "test_*.py" -v
python simulation/mechanoron_v03.py simulation/mechanoron_v03_results.csv
```

The new test file contains **13 passing V0.3 tests** for the power equation, resistance, current limits, reserve policy, charging accounting, graph reachability and fault response. With the already uploaded V0.1/V0.2 files, the test-discovery command is expected to find **22 tests** (4 + 5 + 13), provided all names and files remain unchanged.

The CSV records **five scenarios × 60 days = 300 rows** and includes day, active-source list, critical/mobility completion flags, minimum cell-source terminal voltage under load, per-source SOC, delivered energy, integrated daily ohmic heat and decision flags.

## 7. Limitations and upcoming evidence gates

- The LiSi discharge plateau is used solely to anchor a synthetic SOC/OCV law. Actual \(V_{oc}(SOC,T,t)\), dynamic polarization, capacity and resistance measurements are missing for the selected chemistry.
- The model assumes a constant 465°C baseline. Its optional linear resistance-temperature coefficient is a user-defined sensitivity parameter, not fitted to a measured high-temperature dataset. There is no heat-transfer feedback.
- The sources feed a common bus through **idealized independently regulated paths** and share power equally. The graph provides **binary connectivity only**. There is no combined nodal current/voltage solution after a fault, high-temperature switching transient, converter saturation or uneven string-sharing calculation.
- The mission treats all days alike. Rover motor starting surges, scientific communication windows, finite fuel/motion mechanics, high-temperature electronics consumption and actual cell life remain unverified.
- After a source failure, optional mobility is stopped by policy; this should be replaced with an explicit post-fault available-power and mission-optimal dispatch model.
- Cell sizing is **conceptual**; 19S4P or 19S6P cannot yet be used as dimensioned CAD or procurement specifications.

**Next gate:** obtain or digitize *permitted, traceable* cell test data for discharge voltage versus time/current at 465°C, with cell mass, usable capacity, resistance and current constraints. Fit and validate the OCV/resistance model, then introduce thermal coupling and explicit post-fault DC distribution. Retain failed cases and sensitivity ranges in the public repository.

## Primary sources

**[E1]** Scherzberg, E., and Miller, T. (2023). *Long Life Molten Salt Battery for NASA Venus Application.* 49th Power Sources Conference, NASA NTRS 20230009302. https://ntrs.nasa.gov/citations/20230009302

**[E2]** NASA Science (2023). *Providing Power on Earth's Evil Twin.* https://science.nasa.gov/science-research/science-enabling-technology/providing-power-on-earth-s-evil-twin/

**[E3]** NASA Technical Memorandum (2023). *Equivalent Circuit Model of Battery Capacity*, Section 4. https://ntrs.nasa.gov/api/citations/20230012868/downloads/NASA-TM-20230012868.pdf

**[E4]** *How to parameterise an equivalent-circuit empirical battery model from time-domain data* (2026), open-access article. https://pmc.ncbi.nlm.nih.gov/articles/PMC13049963/

---

*2022 ASTARTE was developed by Team Aldebaran. This document records the subsequent independent 2026 numerical redesign and preserves source measurements separately from model assumptions.*
