# ASTARTE V2 — Mission and Power Requirements

**Document ID:** AST-ENG-001  
**Revision:** 0.1 — feasibility baseline  
**Date:** 11 November 2026  
**Project:** ASTARTE Venus Energy System  
**Status:** Working engineering assumptions; not a verified flight design

## 1. Purpose and design question

The 2022 ASTARTE proposal developed by Team Aldebaran imagined a modular energy storage system for long-duration operation on Venus. I am revisiting its engineering assumptions to answer a more specific question: **what energy, peak-power, thermal, and mechanical requirements must a fault-tolerant battery system meet to support a 60-Earth-day Venus surface mission?**

The first design covers the **energy subsystem**. Rover mobility is modelled as an additional, explicitly defined power load; the mechanical rover architecture will be developed after the energy and peak-power limits have been evaluated.

This document is an initial requirements baseline. The calculations are reproducible estimates based on the assumptions shown below. No ASTARTE V2 hardware has yet been qualified for operation on Venus.

## 2. Mission concept

Two operating profiles will be compared.

- **Scenario S — Stationary science platform:** 60 days of basic control, environmental measurements and scheduled communication. This provides a lower-power reference system.
- **Scenario M — Limited-mobility exploration:** Scenario S plus ten minutes of rover motion per Earth day. This tests the energy and peak-power cost of mobility before a drivetrain is selected.

Both profiles assume operation on the Venus surface with no credit for wind or solar power in the baseline energy budget. Energy harvesting can be investigated later as a sensitivity case. The surface-to-orbiter communications link, measurement payload and motion capability remain conceptual.

## 3. Environmental design inputs

| ID | Parameter | Baseline value | Evidence / interpretation |
|---|---|---:|---|
| ENV-01 | Mean Venus surface temperature | 464 °C (737 K) | NASA planetary reference [R1] |
| ENV-02 | Mean surface pressure | 92 bar (9.2 MPa) | NASA planetary reference [R1] |
| ENV-03 | Surface gravity | 8.87 m/s² | NASA planetary reference [R1] |
| ENV-04 | Near-surface CO₂ fraction | 96.5% by volume | NASA planetary reference [R1] |
| ENV-05 | Technology development temperature | 500 °C | NASA HOTTech programme goal; target, not a measurement of ASTARTE [R2] |
| ENV-06 | Design operating period | 60 Earth days = 1,440 h | ASTARTE mission requirement; related to LLISSE [R3] |

The external atmosphere contains reactive minor species as well as CO₂. Thermal expansion, electrical insulation, corrosion, creep and pressure-related buckling must be checked with temperature-dependent material data. The mean values above are not a complete pressure/temperature envelope for a specific landing site.

## 4. Literature basis for the power architecture

NASA's 2021 *Venus Surface Platform Study* identifies **7–10 W for short communication periods** in the LLISSE context and discusses the significantly higher power needed by mobile platforms. The report treats approximately **25 W** as a useful division between lower-power instrument/communication systems and higher-power mobility or cooling applications. These figures provide scale and context for this preliminary model; they do not specify ASTARTE's component-level loads [R4].

NASA and Advanced Thermal Batteries reported a 17-cell high-temperature battery that operated for **118 days** at Venus temperatures. NASA also states that pressure containment, packaging, shock and vibration remained engineering development tasks. That demonstration supports a long-life electrochemical research direction but does not establish that a cell stack can supply the motion profile defined here [R3].

NASA's SiC electronics experiments show promising high-temperature control technology. The power draw and qualification of a complete ASTARTE controller, switches and power converter remain unverified [R5].

## 5. Preliminary load schedule

**Modelling convention:** The housekeeping load is always on. The instrument, radio and drive loads are *incremental* loads; their energy is added to housekeeping energy. Loads are assumed scheduled without overlap for the primary peak estimate. All entries in this table are **engineering assumptions awaiting hardware evidence**.

| Load | Power while active | Activity per Earth day | Energy per day | Included in |
|---|---:|---:|---:|---|
| Housekeeping: control, timing, monitoring | 0.25 W | 24 h | 6.00 Wh | S and M |
| Environmental science payload | 2.00 W | 0.50 h (30 min) | 1.00 Wh | S and M |
| Orbiter communications session | 10.00 W | 0.25 h (15 min) | 2.50 Wh | S and M |
| Rover drive and local navigation | 75.00 W | 1/6 h (10 min) | 12.50 Wh | M only |

**Notional schedule:** one science measurement block, one communication window and (for M) one short traverse per day. The scheduling feasibility depends on the eventual science and relay operations concept. The housekeeping power assumption also requires validation against available 465 °C control electronics.

### Calculations

Energy per load over a day:

\[
E_{i,\mathrm{day}} = P_i\,t_{i,\mathrm{day}}
\]

Total daily energy delivered to loads:

\[
E_{\mathrm{day}} = \sum_i E_{i,\mathrm{day}}
\]

Mission energy at the loads:

\[
E_{60} = 60\,E_{\mathrm{day}}
\]

| Result | Scenario S | Scenario M |
|---|---:|---:|
| Delivered load energy per day | 9.50 Wh | 22.00 Wh |
| Average delivered load power | 0.396 W | 0.917 W |
| Delivered load energy over 60 days | **570 Wh** | **1,320 Wh** |
| Largest scheduled incremental load | 10 W | 75 W |
| Peak, largest scheduled load + housekeeping | 10.25 W | 75.25 W |
| Bound if all loads overlap | 12.25 W | 87.25 W |

The simultaneous-load bound includes housekeeping, science and communications, plus mobility in Scenario M. It is a conservative *load-scheduling bound* for this example, not an experimentally measured surge. Motor starting current and radio transmission transients could create additional short-duration peaks.

## 6. Initial energy storage sizing

The initial model distinguishes electricity delivered to loads from the energy initially available in the battery.

| Model variable | Value | Status |
|---|---:|---|
| Distribution efficiency, \(\eta_d\) | 0.85 | Design assumption; includes aggregate power-path loss |
| End-of-mission state-of-charge reserve, \(r\) | 0.20 | Design assumption |
| Daily self-discharge, \(s\) | 0 initially | Ideal baseline; sensitivity analysis below |
| Calendar degradation and high-temperature capacity fade | TBD | Not yet quantified |
| Battery specific energy at **system** level | 40, 100, 150 Wh/kg | Hypothetical sensitivity values, not measured ASTARTE values |

For the ideal **zero self-discharge** case, the lower-bound initial energy inventory is

\[
E_{0,\mathrm{req}} = \frac{E_{60}}{\eta_d(1-r)}.
\]

Therefore:

- Scenario S: \(570/(0.85\times0.8) = \mathbf{838.2\ Wh}\).
- Scenario M: \(1320/(0.85\times0.8) = \mathbf{1941.2\ Wh}\).

These are energy-sizing *estimates*, not cell-stack specifications. An actual pack must also sustain the peak currents at operating temperature and voltage throughout the discharge period.

### Specific-energy sensitivity

| Assumed system-level specific energy | Scenario S pack mass | Scenario M pack mass |
|---|---:|---:|
| 40 Wh/kg | 21.0 kg | 48.5 kg |
| 100 Wh/kg | 8.4 kg | 19.4 kg |
| 150 Wh/kg | 5.6 kg | 12.9 kg |

These masses use \(m_{\mathrm{pack}} = E_{0,\mathrm{req}}/e_{\mathrm{specific}}\). The denominator must ultimately be established for a complete high-temperature pack including the relevant cell and packaging masses. The structural shell, rover chassis, electronics and instruments are not included here unless they are already represented in an eventual measured pack-level specific energy figure.

### Self-discharge sensitivity

A long-lived high-temperature battery requires special attention to internal self-discharge. To make this effect explicit, use a one-day time step:

\[
E_{d+1}=E_d(1-s)-\frac{E_{\mathrm{day}}}{\eta_d},\qquad d=0,\ldots,59.
\]

Choose the initial energy such that \(E_{60}\geq r E_0\). For constant daily load and fixed \(s\),

\[
E_{0,\mathrm{req}} =
\frac{(E_{\mathrm{day}}/\eta_d)\sum_{j=0}^{59}(1-s)^j}
{(1-s)^{60}-r}.
\]

| Assumed self-discharge | Scenario S initial energy | Scenario M initial energy |
|---|---:|---:|
| 0% / day | 838 Wh | 1,941 Wh |
| 0.1% / day | 878 Wh | 2,033 Wh |
| 0.5% / day | 1,075 Wh | 2,489 Wh |
| 1.0% / day | 1,458 Wh | 3,376 Wh |

Self-discharge percentages here are **test cases**, not published rates for NASA's battery. Battery aging, voltage limits and time-varying load behavior will be modelled separately when suitable data become available.

## 7. Preliminary bus and current constraints

A **24 V nominal** distribution bus is used provisionally to illustrate current levels. The final bus voltage will be selected using high-temperature cell discharge curves, converter feasibility, switching losses and cable mass. NASA's LLISSE battery development discussed a ±25 V bus, which provides a comparison point but is not an ASTARTE design commitment [R3].

For a constant-power load, \(I\simeq P/V\):

| Load case | Power | Illustrative current at 24 V |
|---|---:|---:|
| Stationary peak with housekeeping | 10.25 W | 0.427 A |
| Mobile peak with housekeeping | 75.25 W | 3.135 A |
| Mobile bound: all loads overlap | 87.25 W | 3.635 A |

These are **nominal-voltage estimates**. Lower end-of-discharge voltage increases current. Motor start-up, controller faults, protection-device ratings and high-temperature cable derating must be evaluated before hardware sizing.

## 8. Engineering requirements and acceptance methods

| ID | Requirement or development objective | Initial criterion | Planned verification | Status |
|---|---|---|---|---|
| REQ-01 | Mission duration | 60 Earth days | Time-stepped energy balance | Open |
| REQ-02 | Environmental temperature | 464 °C reference; assess 500 °C target | Literature + thermal model | Open |
| REQ-03 | External pressure | 92 bar nominal; design envelope TBD | Structural calculation and later FEA | Open |
| REQ-04 | Baseline energy | S: 570 Wh; M: 1320 Wh at loads | Recalculate from schedule | Preliminary |
| REQ-05 | Reserve at mission end | >=20% initial energy in simplified model | 60-day model with losses | Assumed |
| REQ-06 | Distribution losses | Baseline \(\eta_d=85\%\); sensitivity required | Power-path model | Assumed |
| REQ-07 | Peak delivered power | >=87.25 W if simultaneous M loads are permitted, plus transients | High-temp cell I–V and load tests | Unverified feasibility |
| REQ-08 | Fault tolerance | Isolate one module fault while maintaining explicitly prioritised critical loads | Graph/network simulation | Proposed |
| REQ-09 | Chemical compatibility | Cell, seal, interconnect and shell viable at target environment | Compatibility database + test plan | Open |
| REQ-10 | Mass budget | Document energy pack, shell, electronics and mobility masses separately | CAD/analytical mass roll-up | Open |
| REQ-11 | Reproducibility | Every computed value traceable to input and formula | Version-controlled inputs and Python tests | Planned |
| REQ-12 | Evidence classification | Distinguish source measurements, historical claims, assumptions and model results | Review against research/evidence-register.csv | Active |

**Major feasibility gate:** The published 118-day battery demonstration establishes a promising long-life chemistry, but the continuous/peak power, cell energy, self-discharge and packaging requirements of the proposed mobile system must still be matched to published or tested high-temperature cell performance. In particular, Scenario M may require a different configuration or power architecture if long-life cells cannot deliver the pulse load.

## 9. Architecture dependencies

Before finalising the battery module count or drawing a dimensioned CAD enclosure, the following quantities need evidence or explicit design decisions:

1. Cell output voltage as a function of temperature, state of charge, current and time.
2. Cell nominal capacity and total available watt-hours under the expected discharge profile.
3. Permissible continuous and pulse current at approximately 465 °C.
4. Measured self-discharge rate and long-duration voltage stability.
5. Energy consumed by 465 °C-qualified power management, sensing and switching hardware.
6. Temperature-dependent mechanical properties and chemically compatible seals/interconnects.
7. Rover traverse requirements (mass, slope, rolling resistance, wheel radius, speed and drivetrain efficiency).
8. Communications duty cycle and achievable link/data budget with an orbiter.

The historical 60-triangle shell and Mechanoron concept are retained as **candidate architectures**. Their physical dimensions and graph connectivity will be evaluated against these requirements, rather than assumed in advance.

## 10. Development boundaries and next decision

**Current deliverable:** a reproducible 60-day energy sizing baseline with stationary and limited-mobility mission scenarios.

**Next engineering task:** source and compare measured LiSi/FeS cell-level discharge data and chemistry-dependent limits, then build a traceable cell-stack-sizing model. If those data do not support Scenario M's pulse requirement, investigate a separate high-temperature peak-power subsystem or adjust the operational schedule.

The proposed low-voltage demonstrator, if built, will test energy-routing algorithms and module fault isolation at ordinary laboratory conditions. It will not constitute a 465 °C / 92 bar qualification test.

## References

**[R1]** NASA National Space Science Data Center. *Venus Fact Sheet.* https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html

**[R2]** NASA Planetary Exploration Science Technology Office. *Hot Operating Temperature Technology (HOTTech).* https://science.nasa.gov/planetary-science/programs/pesto/hottech/

**[R3]** NASA Science (21 February 2023). *Providing Power on Earth's Evil Twin.* https://science.nasa.gov/science-research/science-enabling-technology/providing-power-on-earth-s-evil-twin/

**[R4]** NASA (2021). *Venus Surface Platform Study Final Report*, Sections 4.1 and 5.1–5.2. https://ntrs.nasa.gov/api/citations/20210023723/downloads/Venus%20Surface%20Platform%20Study%20Final%2011-4-21.pdf

**[R5]** NASA Science (15 January 2020). *Integrated Circuits to Enable Exploration of the Harshest Environments in the Solar System.* https://science.nasa.gov/science-research/science-enabling-technology/technology-highlights/integrated-circuits-to-enable-exploration-of-the-harshest-environments-in-solar-system/

**[R6]** NASA Space Apps 2022. *Team Aldebaran — Exploring Venus Together.* https://2022.spaceappschallenge.org/challenges/2022-challenges/exploring-venus/teams/team-aldebaran/

*Evidence classification and source metadata: `research/evidence-register.csv`. This document will be revised after the cell chemistry comparison and first numerical simulation.*
