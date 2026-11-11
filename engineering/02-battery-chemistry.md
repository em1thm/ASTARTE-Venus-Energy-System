# ASTARTE V2 — Battery Chemistry and Preliminary Cell-Stack Sizing

**Document ID:** AST-ENG-002  
**Revision:** 0.1 — literature-based feasibility analysis  
**Date:** 11 November 2026  
**Project:** ASTARTE Venus Energy System  
**Design status:** Concept / preliminary sizing. No ASTARTE V2 cell or battery pack has been manufactured or qualified.

## 1. Engineering question

The original ASTARTE proposal considered a lithium-sulfur-based energy system within a 60-triangle enclosure. In this redesign, I am examining which electrochemistry could supply a 60-Earth-day Venus mission and how the required energy and peak power affect the number and configuration of cells.

Two cases have already been defined in [`01-mission-requirements.md`](01-mission-requirements.md): a stationary science platform (Scenario S) and a short-traverse rover (Scenario M). The cell design must be assessed against both *energy over 60 days* and *instantaneous power during a communication or drive event*. The second requirement is especially uncertain for long-life, low-discharge thermal batteries.

The battery chemistry selected in this document is a **reference research direction**, subject to the evidence gates in Section 9. Selection of an electrode couple does not establish a working battery pack: separator, electrolyte, seals, terminals, thermal environment, current collectors, packaging and power electronics are also required.

## 2. Evidence extracted from published work

| Source | Chemistry / test | Reported result | Engineering interpretation |
|---|---|---|---|
| [S1] Scherzberg & Miller (2023), NASA NTRS | LiSi anode / FeS cathode / alkali-halide molten-salt electrolyte | 1.32 V per cell on a stated LiSi discharge plateau; 5-cell battery operated **152 days** at a half-scale load; 17-cell battery operated **117 days** before falling below 19 V | Evidence for extended-duration *low-load* battery operation at high temperature; neither number is a measured ASTARTE cell capacity |
| [S2] NASA Science (2023) | 17-cell ATB battery | NASA describes operation for **118 days** at Venus temperatures | The 117/118-day descriptions use different reporting endpoints/rounding; retain the original wording with source attribution |
| [S3] Hunter, NASA Glenn (2023) | LLISSE mission power requirements and battery status | ±25 V-oriented supply; slide lists a **0.2 A** current with pulses up to **12 A** as a performance summary; chemistry demonstrated for 118 days | Treat the current and pulse figures as **mission/system requirements**, not proof that the 17-cell endurance prototype delivered those pulses |
| [S4] Glass et al., *Journal of Power Sources* (2020) | Li–Al anode, LiCl–KCl molten salt, FeS cathode | Laboratory cells demonstrated approximately **26 days** at **475°C** | Separate, peer-reviewed candidate for high-temperature primary cells; different anode and test design from [S1] |
| [S5] JPL energy-storage technology review (2017) | Proposed high-temperature primary battery technology | Approximately **100 Wh/kg** projected specific energy for an advanced battery concept | Useful **scenario input** for mass sensitivity, not a measured value for the 2023 ATB cell or an ASTARTE pack |
| [S6] NASA TechPort (updated 2026) | Proposed high-temperature LiAl–CO₂ system | **948 Wh/kg** cited as a Phase-I development *goal* | Concept worth tracking because Venus has abundant CO₂; no equivalent validated 60-day pack result established by this record |

**Reading note.** [S1] gives more precise endpoints than [S2]; both remain cited. [S1]'s detailed experimental setup and failure analysis are particularly relevant to ASTARTE's proposed modular interconnections.

## 3. Chemistry selection

### Candidate A — LiSi / FeS / molten salt: baseline reference

Lithium-silicon alloy supplies the anode, iron monosulfide the cathode, and a molten alkali-halide phase permits ionic transport at high temperature. The 2023 NASA/ATB paper identifies a lithium-silicon discharge plateau at approximately **1.32 V per cell** in its best-performing long-life configuration [S1]. This value is a *reported plateau reference*; the actual voltage varies with time, load, temperature and the selected electrochemical plateau.

The principal barrier identified in the work is **parasitic cell-to-cell discharge**. Migration of lithium-containing electrolyte/material can form unintended ionic pathways between cells. The researchers compared an exposed stack, an alumina sleeve, and a stacking-ring arrangement. The sleeve produced accelerated discharge in reported tests; the stacked-ring concept was selected for subsequent full-scale development [S1]. This makes separator geometry and interfaces part of the core design problem, rather than a late packaging detail.

**Decision:** use LiSi/FeS as the **baseline chemistry for numerical architecture studies**, with parameters explicitly identified as measured, assumed or still unavailable.

### Candidate B — Li–Al / FeS / LiCl–KCl: research comparator

JPL researchers demonstrated approximately 26 days of continuous cell operation at 475°C in a Li–Al/FeS molten-salt system [S4]. The study supports material and architecture comparison. Its reported life and cell design do not, by themselves, establish a 60-day mobile rover pack.

### Candidate C — LiAl–CO₂: exploratory comparator

A NASA TechPort record describes development of a high-temperature solid-state LiAl–CO₂ system using CO₂ as a reactant; it lists 948 Wh/kg as a targeted Phase-I specific energy [S6]. This is an interesting research path, especially for a CO₂-rich atmosphere. It will stay in the **exploratory** category until test results, usable current, duration, reactant access and containment have been established.

### What happened to the 2022 Li₂S idea?

The original concept remains part of the project history. Li₂S is a possible sulfur-bearing cathode material in some lithium–sulfur electrochemistries, but the name of a cathode component does not fully specify a functioning cell. To reproduce it we would need the complete anode/electrolyte/separator/cathode system, a temperature-dependent stability model and experimentally supported performance. For the first buildable engineering baseline, LiSi/FeS has stronger directly relevant published longevity evidence.

## 4. The published load test: why peak power requires its own analysis

In [S1], eight five-cell units were evaluated. For the described experiment the authors used a **12 kΩ base resistive load** and a **160 Ω pulse resistive load**, switched to the pulse load for **two minutes every eight hours**. The oven was maintained at **465°C**.

Using *only as an illustration* a 5-cell stack at $5\times1.32=6.6\ \mathrm{V}$, Ohm's law gives:

$$
I_{\mathrm{base}} \approx \frac{6.6}{12000}=0.00055\ \mathrm{A}=0.55\ \mathrm{mA}
$$

$$
I_{\mathrm{pulse}} \approx \frac{6.6}{160}=0.0413\ \mathrm{A}=41.3\ \mathrm{mA}.
$$

The approximate powers would be 3.63 mW (base) and 272 mW (pulse). Actual current varies as cell voltage changes, and the test papers' load settings cannot be rescaled into a qualification claim for an entirely different 75 W rover motor. The practical lesson is to keep **energy capacity**, **long-term self-discharge**, **allowable current**, and **pulse-power capability** as distinct parameters.

The cited 2023 paper also describes orientation, electrical feedthrough, ceramic insulation and electrolyte-migration problems. These become mechanical and interconnect requirements for ASTARTE V2 [S1].

## 5. Nominal stack voltage — first mathematical sizing

For $N_s$ cells connected in series:

$$
V_{\mathrm{stack}}(t,I,T) = \sum_{i=1}^{N_s} V_i(t,I,T).
$$

If the published 1.32 V plateau is used **temporarily** for each cell:

| Series cells, $N_s$ | Estimated plateau stack voltage |
|---:|---:|
| 17 | 22.44 V |
| 18 | 23.76 V |
| 19 | 25.08 V |
| 20 | 26.40 V |

**Initial comparison:** 19 cells in series give approximately 25.08 V *at the assumed plateau*. A regulated 24 V bus is therefore worth investigating, but it needs a validated input-voltage range and appropriate converter topology. In particular, the 17-cell endurance unit fell below 19 V near the end of its reported run [S1]; fixed voltage throughout 60 days must not be assumed.

NASA's LLISSE work refers to **positive and negative supply rails** around ±25 V [S1, S2]. Our illustrative single 24 V distribution bus from `01-mission-requirements.md` is a separate **ASTARTE design assumption**. We will not equate those two electrical architectures.

## 6. Energy sizing against the mission profiles

The mission-requirements document defines a 60-day stationary delivered-load demand of 570 Wh and a limited-mobility demand of 1,320 Wh. With a deliberately assumed distribution efficiency of $\eta_d=0.85$ and end-of-mission inventory reserve $r=0.20$, the *zero-self-discharge* energy inventory is:

$$
E_{0,\mathrm{req}}=\frac{E_{60}}{\eta_d(1-r)}.
$$

| Case | Delivered energy | Assumed initial battery energy |
|---|---:|---:|
| S — stationary | 570 Wh | **838 Wh** |
| M — limited mobility | 1,320 Wh | **1,941 Wh** |

These values are **energy requirements**, not demonstrated ATB battery capacities.

### Illustrative ampere-hour requirement

At a nominal **24 V** bus-equivalent energy basis, the Scenario M initial inventory of 1,941 Wh corresponds to:

$$
Q_{\mathrm{eq}} \approx \frac{1941.2\ \mathrm{Wh}}{24\ \mathrm{V}} = 80.9\ \mathrm{Ah}.
$$

For the candidate **19S** electrochemical stack at the assumed 1.32 V plateau, the equivalent charge is approximately **77.4 Ah** ($1941.2/25.08$). The different numbers arise because the voltage bases are different. Neither is a measured cell ampere-hour rating.

### A deliberately hypothetical cell-count example

Suppose, **for calculation only**, an individually qualified 465°C cell had:

- representative plateau voltage = 1.32 V;
- usable charge capacity = **20 Ah** at the *relevant 60-day load profile*;
- required current and lifetime capability confirmed by test (currently **unknown**).

A **19S4P** arrangement would contain 76 such cells:

$$
E_{\mathrm{illustrative}} = 19\times4\times1.32\ \mathrm{V}\times20\ \mathrm{Ah} = 2006.4\ \mathrm{Wh}.
$$

Under the *zero-self-discharge, constant-voltage approximation*, energy remaining after the specified distribution loss and 20% reserve would allow **1,364 Wh** at loads, slightly above Scenario M's 1,320 Wh. This margin is narrow and disappears under even modest self-discharge or an unfavorable voltage curve. **The 20 Ah capacity and this configuration are not supported by a cell data sheet.** They exist solely to illustrate the sizing equations.

The outer **60 triangular faces** are an architectural/mechanical design feature. Their number is not equivalent to the number of electrochemical cells. Future CAD work will determine where physically grouped cell stacks can fit within an enclosure.

## 7. Self-discharge changes the required pack size

The 60-day daily-time-step model in AST-ENG-001 is:

$$
E_{d+1}=E_d(1-s)-\frac{E_{\mathrm{day}}}{\eta_d},
$$

where $s$ is the **assumed fractional energy lost per day** and the end reserve is $E_{60}\geq0.2E_0$.

For Scenario M:

| Assumed self-discharge | Starting energy required | Added inventory vs zero-loss case |
|---:|---:|---:|
| 0%/day | 1,941 Wh | baseline |
| 0.1%/day | 2,033 Wh | +92 Wh |
| 0.5%/day | 2,489 Wh | +548 Wh |
| 1.0%/day | 3,376 Wh | +1,435 Wh |

The percentages above are **parameter sweeps**, not rates measured for ATB cells. Real battery aging may depend on electrolyte migration, stack pressure, voltage history, cell orientation, temperature and load. A cell-specific model will replace this simplified energy-loss model if reliable data become available.

## 8. Peak-power and interconnect checks

Scenario M has a scheduled peak load of **75.25 W** (drive plus housekeeping), or **87.25 W** if all listed loads overlap. At an ideal 24 V bus, 87.25 W corresponds to **3.64 A delivered to loads**.

With the *assumed* whole-path efficiency $\eta_d=0.85$, a simplified battery-side current estimate at $V_{\mathrm{bat}}=25.08$ V is:

$$
I_{\mathrm{bat}}\approx\frac{87.25\ \mathrm W}{0.85\times25.08\ \mathrm V}=4.09\ \mathrm A.
$$

At an illustrative 19 V battery input it becomes **5.40 A**. If current were evenly shared by four parallel strings, each would deliver approximately **1.02–1.35 A** across those two example voltages. These numbers are **requirements imposed by our assumed rover load**, not measured cell capabilities.

Electrical loss should also be included explicitly:

$$
P_{\mathrm{ohmic}} = I^2 R_{\mathrm{path}},
\qquad
\Delta V = I R_{\mathrm{path}}.
$$

We need measured or defensibly bounded cell internal resistance, interconnect resistance, terminal contact resistance and switching losses as functions of temperature and age. Uniform current sharing cannot be assumed in real parallel stacks.

### Architectural alternatives to test

| Architecture | Potential benefit | Main validation problem |
|---|---|---|
| More parallel long-life cell strings | Lower peak current per string | Added mass, interstring imbalance, fault isolation, thermal interfaces |
| Dedicated high-temperature pulse-power branch | Decouples routine science power from motor surges | Identify a qualified pulse device and high-temperature control/switching electronics |
| Shorter/slower traverses | Reduces peak current and/or total energy | Mobility performance and science productivity |
| Stationary-first platform | Most direct near-term evidence path | Does not yet demonstrate the full mobile rover mission |

**Working decision:** use a stationary science power architecture as the testable baseline; retain limited mobility as a quantified stretch objective. The defining experiment is whether a high-temperature energy source can supply the prescribed pulse profile without violating lifetime and voltage limits.

## 9. Design validation gates before dimensioned CAD

| Gate | Evidence required | Status |
|---|---|---|
| CELL-01 | Discharge voltage curve at ~465°C over relevant load and 60-day period | OPEN |
| CELL-02 | Cell usable capacity (Ah / Wh) and mass under the same test conditions | OPEN |
| CELL-03 | Continuous and pulsed current limits, transient voltage drop and impedance | OPEN |
| CELL-04 | Self-discharge and cell-to-cell leakage versus time and orientation | OPEN |
| CELL-05 | Electrical feedthrough, ceramic separator, seal and interconnect compatibility | OPEN |
| CELL-06 | Stack input-voltage envelope and efficient regulation at 465°C | OPEN |
| CELL-07 | High-temperature switch/controller component feasibility for Mechanoron | OPEN |
| CELL-08 | Pack integration, external pressure shell and 60-day environmental qualification | OPEN |

Until these gates have defensible inputs, *precise* active-cell dimensions, nominal capacity, a 19S4P production layout and final pack mass cannot be claimed. CAD can begin with clearly marked **parametric placeholders**, but geometry should not be presented as qualified hardware.

## 10. Next engineering actions

1. Add source-specific rows to the research evidence register for 1.32 V, 152/117 days, the 12 kΩ / 160 Ω test loads, and the 0.2 A / 12 A LLISSE power specifications. Mark each by *experimental observation* or *development requirement*.
2. Create a parameterized Python battery model with swappable voltage curves and self-discharge assumptions; start from the analytical checks here and in AST-ENG-001.
3. Evaluate stationary mission survival for worst-case energy inventory, then add motion events and test failure scenarios.
4. Develop a preliminary circuit/network abstraction for Mechanoron that includes switching losses, current sharing and stuck-open/stuck-closed failures.
5. Fix an electrical architecture only after a compatible cell/performance dataset and high-temperature electronics path have been identified.

## References

**[S1]** Scherzberg, E., & Miller, T. (2023, 27 June). *Long Life Molten Salt Battery for NASA Venus Application.* 49th Power Sources Conference. NASA NTRS ID 20230009302. [NTRS record](https://ntrs.nasa.gov/citations/20230009302) · [Paper PDF](https://ntrs.nasa.gov/api/citations/20230009302/downloads/Long%20Life%20Molten%20Salt%20Battery%20for%20NASA%20Venus%20Application.pdf).

**[S2]** NASA Science (2023, 21 February). *Providing Power on Earth's Evil Twin.* [NASA article](https://science.nasa.gov/science-research/science-enabling-technology/providing-power-on-earth-s-evil-twin/).

**[S3]** Hunter, G. W. (2023, 26 September). *A Brief Overview of High Temperature Technologies for a Venus Long Lived Lander.* NASA Glenn, IMAPS presentation, “LLISSE Power” slide. [NASA presentation PDF](https://ntrs.nasa.gov/api/citations/20230013176/downloads/IMAPS%20Venus%20Overview%20Hunter%20fin%202.pdf).

**[S4]** Glass, D. E., et al. (2020). *High temperature primary battery for Venus surface missions.* *Journal of Power Sources.* DOI: [10.1016/j.jpowsour.2019.227492](https://doi.org/10.1016/j.jpowsour.2019.227492). See also [abstract](https://www.sciencedirect.com/science/article/abs/pii/S0378775319314855).

**[S5]** JPL (2017). *Energy Storage Technologies for Future Planetary Science Missions.* JPL D-101146, Section 4.2.7 (high-temperature batteries). [NASA-hosted report](https://solarsystem.nasa.gov/system/downloadable_items/716_Energy_Storage_Tech_Report_FINAL.PDF).

**[S6]** NASA TechPort (record updated 22 January 2026). *High Temperature All Solid-State LiAl-CO₂ Batteries for Venus Missions.* Project 113270. [NASA project record](https://techport.nasa.gov/projects/113270).

---

**Revision note:** The numbers in Section 6 are analytical examples, deliberately labelled as assumptions. Future revisions will replace these assumptions with source-supported cell specifications or measured laboratory data, and will report failed design cases alongside successful ones.
