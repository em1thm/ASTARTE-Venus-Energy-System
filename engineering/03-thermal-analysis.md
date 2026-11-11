# ASTARTE V2 — Thermal Architecture and First-Principles Analysis

**Document ID:** AST-ENG-003  
**Revision:** 0.1 — analytical feasibility model  
**Date:** 11 November 2026  
**Project:** ASTARTE Venus Energy System  
**Related documents:** [`01-mission-requirements.md`](01-mission-requirements.md) · [`02-battery-chemistry.md`](02-battery-chemistry.md)  
**Status:** Concept-stage engineering analysis; all numerical results below are calculated estimates, not performance tests of ASTARTE hardware.

## 1. Engineering objective

The thermal architecture must maintain the electrochemical cells, interconnects, seals, power-control electronics, and structural components within their **individual allowable temperature ranges** for a 60-Earth-day mission. The operating environment is approximately 464–465 °C and 92 bar at the mean Venus surface [T1]. NASA's HOTTech programme uses **500 °C for at least 60 days** as a technology-development target [T2]. This is a design comparison target, not a demonstrated ASTARTE capability.

The original 2022 concept included a 6 cm titanium outer layer, 8 cm aerogel layer and 2 cm carbon-fibre inner layer [T3]. This document examines that configuration against a *hot-operating* molten-salt battery reference and identifies the thermal requirements that remain unresolved.

Two architectures are compared:

- **C — Cold core:** Maintain a conventional temperature-sensitive subsystem near 25 °C while the exterior remains near 465 °C.
- **H — Hot-operating core:** Use an electrochemistry and associated components intended to operate near Venus surface temperature. Temperature uniformity, dissipated electrical power and material compatibility become the leading questions.

**Provisional preference:** Architecture H, conditional on cell/electronic component evidence. NASA/ATB research has demonstrated a long-lived molten-salt battery at Venus-like temperatures, while high-temperature SiC circuits have shown operation in simulated Venus surface conditions [T4, T5]. Neither result qualifies an integrated ASTARTE rover.

## 2. Evidence and model inputs

| Input or result | Value | Classification | Source / interpretation |
|---|---:|---|---|
| Mean Venus surface temperature | 464 °C (737 K) | Planetary reference | NASA NSSDC [T1] |
| Analysis ambient temperature | **465 °C (738.15 K)** | Rounded modelling assumption | Approximately the above reference |
| Mean external atmospheric pressure | **92 bar (9.2 MPa)** | Planetary reference | NASA NSSDC [T1] |
| HOTTech qualification ambition | **500 °C, ≥60 days** | Research-programme objective | NASA [T2] |
| Mission duration | **60 days = 1,440 h** | ASTARTE requirement | AST-ENG-001 |
| Original reported volume | **530,604 cm³ = 0.530604 m³** | Historical unverified design statement | NASA Space Apps archive [T3] |
| Original titanium / aerogel / carbon-fibre thickness | **60 / 80 / 20 mm** | Historical design statement | NASA Space Apps archive [T3] |
| Hot-composite-aerogel conductivity | **0.051 W/(m·K) at 500 °C** | *Measured for a particular 2023 composite* | Wu et al. [T6] |
| Comparison silica-fibre aerogel conductivity | **0.076 W/(m·K) at 500 °C** | *Measured for another 2023 composite* | Wu et al. [T6] |
| Additional high-temperature composite example | **0.0489 W/(m·K) at 500 °C** | *Measured for a 2019 composite* | Shang et al. [T7] |
| Titanium-alloy density for demonstration | **4,430 kg/m³** | Typical handbook value | Nippon Steel [T8]; actual alloy not selected |
| Titanium-alloy expansion coefficient | **8.8 × 10⁻⁶ K⁻¹** | Typical reference value | Nippon Steel [T8]; assumed constant solely for first-pass calculation |

**Important transfer limitation:** The reported aerogel values were measured on specific composite samples under the authors' conditions. Their effective conductivity inside a **92 bar, hot CO₂-rich** assembly, under a large through-thickness temperature gradient and over 60 days, has not been established here. Values from 500 °C tests are used in *sensitivity calculations*, not as qualified ASTARTE material properties. Radiation through porous insulation, gas conduction, compression, chemical stability and thermal contact resistances require separate investigation [T6, T7].

## 3. Geometric surrogate for the 2022 shell

The 2022 specification does not establish whether 530,604 cm³ is the *outer displacement volume*, active battery volume or an internal design volume. **For this numerical check only**, treat it as the outer volume and replace the sixty-faced solid with an equal-volume sphere. Real facets and attachment bosses will be modelled later.

The equivalent sphere radius is

$$
R_0=\left(\frac{3V}{4\pi}\right)^{1/3}=0.50222\ \mathrm{m}.
$$

Using the original thicknesses from the **outside inward**:

| Boundary | Radius | Description |
|---|---:|---|
| $R_0$ | 0.50222 m | External surface |
| $R_1=R_0-0.060$ | 0.44222 m | Titanium / aerogel interface |
| $R_2=R_1-0.080$ | 0.36222 m | Aerogel / inner-layer interface |
| $R_3=R_2-0.020$ | 0.34222 m | Inner layer / battery-cavity interface |

For titanium alone, assuming a uniform 60 mm solid shell and 4,430 kg/m³ density:

$$
V_{\mathrm{Ti}}=\frac{4\pi}{3}(R_0^3-R_1^3)=0.16836\ \mathrm{m^3},
$$

$$
m_{\mathrm{Ti}}=\rho_{\mathrm{Ti}}V_{\mathrm{Ti}}\approx\mathbf{746\ kg}.
$$

The corresponding 80 mm aerogel region occupies approximately **0.16318 m³**. Using the **particular** 2023 paper-composite density of 186 kg/m³ [T6] would give approximately **30.4 kg** in this ideal volume-fill illustration; a fabricated three-dimensional insulating system needs its own material density and assembly specification.

The original 450 kg total-mass statement is therefore inconsistent with this **specific interpretation** of the original volume and layers. The geometry and meaning of the reported volume must be resolved before quoting a corrected design mass.

## 4. Steady-state heat leakage to a cold core

For radial conduction through a homogeneous spherical layer with constant conductivity $k$:

$$
R_{\mathrm{th},a}=\frac{1}{4\pi k}\left(\frac{1}{R_2}-\frac{1}{R_1}\right),\qquad
\dot Q=\frac{T_{\mathrm{out}}-T_{\mathrm{in}}}{R_{\mathrm{th},a}}.
$$

Use $T_{\mathrm{out}}=465\ ^\circ\mathrm C$ and $T_{\mathrm{in}}=25\ ^\circ\mathrm C$, so $\Delta T=440$ K. These temperatures are **prescribed at the two aerogel interfaces**, rather than solved from convection and radiation at the true external surface. The metal shells, contacts, seals, penetrations, heat generation and transient effects are omitted from this isolated-layer diagnostic.

| Assigned aerogel $k$, W/(m·K) | Aerogel $R_{\mathrm{th}}$, K/W | Inward heat flow, W | Heat carried over 1,440 h, kWh |
|---:|---:|---:|---:|
| 0.0300 — hypothetical low-conductivity case | 1.325 | **332.1** | 478.3 |
| 0.0489 — measured example at 500 °C [T7] | 0.813 | **541.4** | 779.6 |
| 0.0510 — measured example at 500 °C [T6] | 0.779 | **564.6** | 813.0 |
| 0.0760 — measured comparison at 500 °C [T6] | 0.523 | **841.4** | 1,211.6 |

The kWh column is **thermal energy transferred if the temperature difference is held constant for 60 days**. It is not stored battery energy and does not imply that a passive, finite-heat-capacity cold core could remain at 25 °C for that period. These heat rates would change when boundary temperatures, material properties and coupling to the external atmosphere are modelled.

### Cooling requirement: a thermodynamic floor

If active refrigeration removes heat $\dot Q_c$ at a 25 °C cold reservoir and rejects it to a 465 °C hot reservoir, its ideal reversible coefficient of performance is

$$
\mathrm{COP}_{\mathrm{Carnot}}=\frac{T_c}{T_h-T_c}
=\frac{298.15}{738.15-298.15}=0.6776.
$$

Thus **even an ideal heat pump** would need at least

$$
\dot W_{\min}=\frac{\dot Q_c}{\mathrm{COP}_{\mathrm{Carnot}}}.
$$

For the 0.030 W/(m·K) illustrative case, this is **490 W** of continuous cooling power, or **706 kWh over 60 days**. At $k=0.051$, the ideal minimum is approximately **833 W**, or **1,200 kWh** over 60 days. Real machines would require more energy. This first-pass comparison explains why a 25 °C protected battery compartment is an unattractive baseline for the current low-power ASTARTE mission model, whose electrical delivered-load budgets are 570 Wh (stationary) and 1,320 Wh (limited mobility) [AST-ENG-001].

A cold design might still be necessary for a limited specialist instrument. Its heat load, duration, size and duty cycle would need independent sizing.

## 5. Illustrative transient warm-up, without cooling

A single thermal-capacitance surrogate provides a quick test of the statement that insulation *alone* could preserve a cold interior for 60 days:

$$
C_{\mathrm{th}}\frac{dT_c}{dt}=\frac{T_a-T_c}{R_{\mathrm{th}}}+\dot Q_{\mathrm{internal}}-\dot Q_{\mathrm{cool}},
$$

where $C_{\mathrm{th}}$ is the effective lumped heat capacity in J/K. With constant $T_a$, $\dot Q_{\mathrm{internal}}=\dot Q_{\mathrm{cool}}=0$ and initial $T_c(0)=25\ ^\circ\mathrm C$,

$$
T_c(t)=T_a+(25-T_a)e^{-t/(R_{\mathrm{th}}C_{\mathrm{th}})}.
$$

For **$k=0.051$**, $R_{\mathrm{th}}=0.779$ K/W:

| Hypothetical effective heat capacity | Model time constant | Model time for 25 → 100 °C |
|---:|---:|---:|
| 20 kJ/K | 4.33 h | 0.81 h |
| 100 kJ/K | 21.65 h | 4.05 h |

The table is a **lumped-parameter sensitivity illustration**, not an ASTARTE warm-up prediction. Actual layer-dependent heat capacities, internal conduction, heat transfer from the Venus atmosphere, thermal bridges, phase changes, and surface radiation would determine the real temperature history. The model nevertheless makes the duration issue explicit: reducing heat flow with insulation slows heating; it does not by itself set a permanent cold-core temperature.

## 6. Hot-operating core: heat must also escape

The LiSi/FeS reference has a different thermal design problem. NASA's long-life molten-salt battery development addresses electrochemistry that operates efficiently above approximately **330 °C** and has been demonstrated at Venus-like temperature [T4]. Exact cell temperature limits, permitted gradients and storage/launch conditions remain **open**.

For a hot-operating system, steady-state conservation is

$$
\dot Q_{\mathrm{out}}-\dot Q_{\mathrm{in}}=\dot Q_{\mathrm{generated}},
$$

with the sign and direction depending on core temperature relative to the environment. Heat generation includes cell overpotential/resistive losses, parasitic reactions and nearby power-control electronics; the required measurements are currently unavailable.

A deliberately simple example treats the 80 mm aerogel layer as the **only thermal resistance** and uses $k=0.051$ W/(m·K). For a core *hotter than ambient*, the excess core temperature approximately satisfies

$$
\Delta T_{\mathrm{core}}\simeq \dot Q_{\mathrm{generated}} R_{\mathrm{th}}.
$$

| Sustained internally dissipated heat | Approximate core temperature above 465 °C ambient |
|---:|---:|
| 1 W | +0.8 °C |
| 5 W | +3.9 °C |
| 15.4 W | +12.0 °C |
| 30 W | +23.4 °C |

The **15.4 W case** corresponds to the aggregate 87.25 W delivered-load example in AST-ENG-002 with an assumed 85% electrical distribution efficiency, *if all distribution losses were located inside the insulating core*. In practice, those losses occur across converters, contacts, wires and other subsystems; their actual physical locations must be modelled. Short pulses are transient and should not be treated as steady heating without duration and heat-capacity analysis.

**Design implication:** Retaining the 8 cm insulating layer around a high-temperature battery may increase peak internal temperature by impeding heat rejection. Hot-operating architecture H will therefore compare a thermally coupled, corrosion-protected stack against selectively insulated subsystems. We will not carry the 2022 layer stack unchanged into the final design.

## 7. Convection, radiation and contact interfaces

A Venus surface thermal model should eventually couple the core and outer surface by conduction, and the outer surface and surrounding atmosphere/terrain by convection and radiation:

$$
\dot Q_{\mathrm{conv}}=hA(T_{\mathrm{gas}}-T_{\mathrm{surface}}),
$$

$$
\dot Q_{\mathrm{rad}}=\varepsilon\sigma A(T_{\mathrm{surroundings}}^4-T_{\mathrm{surface}}^4),
$$

where radiative temperatures are expressed in kelvin. $h$ and $\varepsilon$ are **not yet assigned** because their values depend on the rover geometry, local gas composition/properties, wind, surface finish, nearby ground and orientation. A component may also conduct heat through the chassis, cables or structural mounts. Pressure-dependent gas transport and radiation within porous insulation are additional concerns [T6].

The next model should use a thermal-resistance network or finite-volume representation with separate nodes for atmosphere, external structural skin, insulation (if present), pressure shell, battery module, feedthroughs and control electronics. A time-dependent model will include heat capacity and power pulses.

## 8. Thermal expansion and mechanical interfaces

As a first illustration, take a Ti-6Al-4V-like shell of outer radius 0.50222 m and use a **constant** representative coefficient $\alpha=8.8\times10^{-6}\ \mathrm{K^{-1}}$ [T8] from 25 to 465 °C:

$$
\Delta R \simeq \alpha R\Delta T
=8.8\times10^{-6}\times0.50222\times440
=\mathbf{1.94\ mm}.
$$

The corresponding diameter change is approximately **3.89 mm**. This is a free-expansion illustration, not a constrained thermomechanical stress calculation. The coefficient, strength and creep response at 465 °C must be selected for a specified alloy and heat-treatment condition; dissimilar ceramic-to-metal joints can accumulate thermal mismatch stress.

A 2026 peer-reviewed Venus exposure study tested wrought and additively manufactured Ti-6Al-4V under approximately 467 °C and 92.7 bar conditions for **10 days**. It observed surface reaction layers and measured post-exposure high-temperature mechanical properties [T9]. This offers directly relevant material evidence, with 60-day durability, creep, joint and seal behaviour still requiring investigation. Earlier NASA GEER work examined a wider set of metallic alloys and ceramics in a chemically representative Venus atmosphere [T10].

**Pressure/thermal coupling:** A pressure-equalised architecture and a sealed pressure-vessel architecture impose different loads and chemical-isolation needs. Whether battery modules can be safely pressure-balanced while isolating electrochemical contents is an **open design gate**. Structural pressure-vessel sizing belongs in `04-mechanical-analysis.md` and must use temperature-dependent properties and realistic buckling imperfections.

## 9. Preliminary thermal architecture decision matrix

| Subsystem | Preferred study direction | Technical rationale | Open verification |
|---|---|---|---|
| Main electrochemical stack | **Hot-operating LiSi/FeS reference** | Direct NASA long-life high-temperature research basis [T4] | Cell-specific permitted $T$, gradients, self-heating, 60-day loss characteristics |
| High-temperature control | SiC with ceramic / metal packaging | 60-day simulated-Venus circuit results [T5] | Switching functionality, power budget, lifetime and interconnects of *our* design |
| Battery exterior | Corrosion-compatible, structurally separate enclosure | Allows tailored thermal and chemical protection | Pressure differential, permeability, shock, creep, corrosion |
| Insulation | **Selective, requirement-driven** | Full-system 8 cm insulation may hinder heat rejection from hot cells | Correct $k(T,P)$, gas infiltration, radiative transport, thermal bridges |
| Mechanoron nodes | Local thermal dissipation and interfaces modelled explicitly | Electrical switching and contact resistances can produce local hotspots | Available high-temperature devices and experimental heat measurements |
| Low-temperature auxiliary payload | Individual insulated enclosure only if required | Limits refrigeration burden to defined loads and durations | Device duty cycle and complete thermal budget |

**Concept gate decision:** Continue developing a **nominally hot-operating battery architecture**. Treat full-scale cold-core preservation as a rejected *baseline for this low-power mission profile*, pending any new evidence of a practical alternate system. The final architecture remains contingent on cell, packaging and 92-bar external-pressure feasibility.

## 10. Next verification actions and CAD parameters

1. **Resolve the 2022 volume definition.** Confirm whether 530,604 cm³ was outer, usable internal or material-specific volume; identify actual polyhedral geometry.
2. **Obtain the permitted thermal window** of the selected long-life battery chemistry, including storage/activation, heat generation, thermal gradient and cycling limitations.
3. **Measure/estimate true hot-stack dissipations.** Use cell $I$–$V$ curves and internal resistance from AST-ENG-002, plus separately located converter and contact losses.
4. **Create a time-stepped Python thermal model.** Validate constant-$k$ spherical formulas above; then introduce $k(T,P)$, thermal capacity, varying heat loads and geometric thermal bridges.
5. **Build a candidate enclosure property table.** Alloy, ceramic, gasket, coating, feedthrough and fastener: $\rho$, $k(T)$, $c_p(T)$, $\alpha(T)$, creep and Venus-atmosphere compatibility.
6. **Translate to Fusion 360 placeholders.** Until pressure and temperature compliance are established, model `outer_radius`, `shell_thickness`, `insulation_thickness` and `module_clearance` as **parameters to sweep**, not fixed flight dimensions.

**First CAD sketch parameters (historical diagnostic geometry only):** `R0 = 502.22 mm`, `t_Ti = 60 mm`, `t_aerogel = 80 mm`, `t_inner = 20 mm`. These reproduce a hypothetical interpretation of the *2022* claim and **must not** be labelled as approved ASTARTE V2 dimensions.

## 11. Limitations and evidence classification

- **Measured in sources:** planetary reference conditions; thermal conductivities and densities for *specified published samples*; published battery/SiC tests; 10-day Ti-alloy exposure results.
- **Historical statements:** original 60-faced shape, thicknesses, mass and volume.
- **Calculated here:** equivalent sphere radii, shell material mass, spherical heat-leak rates, reversible refrigeration energy floor, lumped warm-up examples, thermal expansion estimate.
- **Assumed here:** outer-volume interpretation; 25 °C cold core; 465 °C constant thermal reservoir; homogeneous and constant-$k$ spherical insulation; example thermal capacities and internally dissipated powers; free thermal expansion.
- **Open:** true material performance at 92 bar and 465 °C for 60 days, pressure differentials, full transient temperature map, chemical integrity of the pack and cell-specific electrothermal limits.

**The analysis supports architectural screening, not operational certification.** Future revisions will report numeric source values alongside their test conditions and replace assumptions only when traceable evidence is available.

## References

**[T1]** NASA NSSDC. *Venus Fact Sheet.* https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html

**[T2]** NASA Science, PESTO. *Hot Operating Temperature Technology (HOTTech).* https://science.nasa.gov/planetary-science/programs/pesto/hottech/

**[T3]** NASA Space Apps 2022. *Team Aldebaran — original ASTARTE concept.* https://2022.spaceappschallenge.org/challenges/2022-challenges/exploring-venus/teams/team-aldebaran/

**[T4]** Scherzberg, E. & Miller, T. (2023). *Long Life Molten Salt Battery for NASA Venus Application.* NASA NTRS 20230009302. https://ntrs.nasa.gov/citations/20230009302 ; NASA Science (2023), *Providing Power on Earth's Evil Twin*: https://science.nasa.gov/science-research/science-enabling-technology/providing-power-on-earth-s-evil-twin/

**[T5]** NASA NTRS (2024). *Progress Towards SiC ASICs for Extreme Temperature and Radiation Environments.* https://ntrs.nasa.gov/citations/20240015144

**[T6]** Wu, Q., et al. (2023). *A flexible silica aerogel paper with temperature-switch opacifier for thermal insulation.* *Journal of Materials Research and Technology*, 24, 4037–4046. https://doi.org/10.1016/j.jmrt.2023.04.022

**[T7]** Shang, L., Lyu, Y. & Han, W. (2019). *Microstructure and Thermal Insulation Property of Silica Composite Aerogel.* *Materials*, 12(6), 993. https://doi.org/10.3390/ma12060993

**[T8]** Nippon Steel. *Titanium and titanium alloy technical data — physical properties.* https://www.nipponsteel.com/en/product/titan/feature/pdf/T001en_16-23.pdf

**[T9]** Kane, K. A., Costa, G., Park, S., et al. (2026, 8 September). *Corrosion and mechanical performance of wrought and additively manufactured Ti-6Al-4V under supercritical carbon dioxide Venus atmospheric conditions.* *npj Materials Degradation.* https://doi.org/10.1038/s41529-026-00877-7

**[T10]** NASA NTRS (2017). *Chemical and Microstructural Changes in Metallic and Ceramic Materials Exposed to Venusian Surface Conditions.* https://ntrs.nasa.gov/citations/20170006025

---

*Next planned document: `04-mechanical-analysis.md` — pressure-vessel architecture, high-temperature material selection, ideal versus imperfection-sensitive shell buckling, mass and expansion compatibility. The 03 analysis will also be translated into a reproducible Python thermal parameter sweep after the baseline geometry decision.*
