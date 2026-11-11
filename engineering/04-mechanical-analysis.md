# ASTARTE V2 — Mechanical Architecture, External-Pressure Screening and Materials

**Document ID:** AST-ENG-004  
**Revision:** 0.1 — analytical screening, not a qualified structure  
**Date:** 12 November 2026  
**Project:** ASTARTE Venus Energy System  
**Related work:** [Mission requirements](01-mission-requirements.md) · [Battery chemistry](02-battery-chemistry.md) · [Thermal analysis](03-thermal-analysis.md)  
**Reproducibility:** `calculations/mechanical-screening.csv` (upload the companion CSV to that path)

## 1. Design problem and scope

The 2022 Team Aldebaran submission described a 60-triangle outer geometry with 60 mm titanium, 80 mm aerogel and 20 mm carbon-fibre layers, a stated 530,604 cm³ volume and a 450 kg total mass [M1]. ASTARTE V2 examines the *structural* consequences of those claims and develops a candidate enclosure for a 60-Earth-day high-temperature battery mission.

The mechanical architecture must address (i) a surface temperature near 465 °C; (ii) ambient pressure near 92 bar; (iii) oxidation/sulfidation and high-temperature creep over 1,440 hours; (iv) cell confinement, electrical insulation, feedthroughs and seals; and (v) shock, launch and landing loads not yet specified [M2, M3]. A full load case and flight-grade safety factors are not yet defined.

Two distinct enclosure concepts must be investigated:

- **Architecture P — sealed low-internal-pressure vessel:** pressure difference can approach 9.2 MPa inward. Stability against external-pressure buckling becomes a primary structural requirement.
- **Architecture B — pressure-compensated / pressure-balanced enclosure:** internal and external pressures may be close, but a separate barrier must still prevent Venus gases and moisture/sulfur species from contaminating the molten-salt electrochemistry. A credible pressure-compensation mechanism, temperature-compatible barrier, and leak/failure model have **not been designed**. This is a research hypothesis, not a validated shortcut.

**Working mechanical direction:** separate a *continuous, sealable inner enclosure* from the *60-face external protective carrier*. The faceted structure can support module placement and wiring; the smooth inner shell can be evaluated with classical pressure-vessel equations. These are independent subsystems until their connections and loads are analysed.

## 2. Evidence table: environmental and material inputs

| Quantity / evidence | Value or result | Classification | Source / transfer limitation |
|---|---|---|---|
| Mean Venus surface temperature | 464 °C | Planetary reference | NASA NSSDC [M2]; landing-site range TBD |
| Mean Venus surface pressure | 92 bar = 9.2 MPa absolute | Planetary reference | NASA NSSDC [M2]; *differential* pressure depends on internal design |
| Exposure of Ti-6Al-4V / 304 SS | 10 days at 467 °C, 92.7 bar | Experimental literature | Kane et al. (2026), GEER; material coupons, not a complete 60-day pressure vessel [M4] |
| GEER exposure of steels, Ni alloys, ceramics | 10 and 42 days at 467 °C, 92 bar and Venus gas mixture | Experimental literature | NASA Glenn; corrosion products depend on alloy/coating [M5] |
| GEER 60-day campaign | 60-day Venus-atmosphere experiment, geological samples | Experimental literature | Supports test-environment capability, **not** a 60-day Ti structural qualification [M6] |
| Ti-6Al-4V density | 4,430 kg/m³ | Supplier typical | Nippon Steel [M7]; nominal room-temperature value used for mass illustration |
| Stainless steel 304 density | 7,900 kg/m³ | Nominal reference | 18–8 stainless reference [M7]; grade and processing need definition |
| Alloy 625 density | 8,440 kg/m³ | Supplier reference | Haynes International [M8]; no Venus-specific qualification implied |
| Ti-6Al-4V high-temperature modulus used here | **80 GPa** | **Screening assumption** | Consistent in scale with temperature-dependent FEM input tables (76 GPa at 500 °C) [M9]; not a measured ASTARTE value |
| Poisson ratio used here | **0.36** | Screening assumption | Near elevated-temperature tabulated value in [M9] |
| Imperfection multiplier / knockdown | **0.20** for a single illustrative case | **Sensitivity only** | Spherical shell studies show strong imperfection sensitivity; no project-specific approved factor [M10, M11] |

The published 2026 Ti-6Al-4V study reports oxide/oxygen-enriched surface layers after 10-day exposure and no broad loss of tensile properties over that particular interval [M4]. Its outcome informs candidate selection. The material's 60-day creep behavior, welded-joint properties, seal integrity and impact performance remain unresolved.

## 3. Reconstructing the 2022 geometric envelope

The original reported volume **may refer to an external envelope, free internal volume, or another design quantity**. To make the earlier mass discrepancy reproducible, use the **external-volume interpretation** as an explicit conditional example:

$$V_{\mathrm{historical}}=530,604\ {\rm cm^3}=0.530604\ {\rm m^3}.$$

An equal-volume sphere has external radius:

$$R_o=\left(\frac{3V}{4\pi}\right)^{1/3}=0.502220\ {\rm m}.$$

For a uniform spherical shell of thickness $t$, its exact geometric volume and illustrative mass are:

$$V_{\rm shell}=\frac{4\pi}{3}\left[R_o^3-(R_o-t)^3\right],\qquad m=\rho V_{\rm shell}.$$

At $t=60$ mm, a 4,430 kg/m³ Ti-6Al-4V surrogate gives approximately **745.8 kg** for this shell alone, exceeding the historical 450 kg **under this explicit volume interpretation**. This does not establish the original project's actual as-built dimensions or mass.

### Exact-volume material comparison (same geometry and wall thickness)

| Thickness (mm) | Ti-6Al-4V (kg) | 304 SS (kg) | Alloy 625 (kg) |
|---:|---:|---:|---:|
| 10 | 137.6 | 245.4 | 262.2 |
| 15 | 204.4 | 364.5 | 389.4 |
| 20 | 269.8 | 481.1 | 514.0 |

The table deliberately holds thickness constant for comparison. Different materials require **independent** high-temperature structural sizing, so a lighter number at a common thickness does not establish which material yields the lightest safe enclosure.

## 4. Elastic buckling under external pressure — a screening model

For a **complete, perfect, homogeneous, thin elastic spherical shell** under uniform external differential pressure, the classical Zoelly buckling expression is [M10, M11]:

$$p_{\mathrm{cr,ideal}}=\frac{2E}{\sqrt{3(1-\nu^2)}}\left(\frac{t}{R_m}\right)^2,$$

where $R_m=R_o-t/2$ is the mean shell radius. The corresponding simple membrane-compression magnitude is:

$$\sigma_{\mathrm{mem}}\approx \frac{\Delta p\,R_m}{2t}.$$

**Illustrative inputs:** $E=80$ GPa, $\nu=0.36$, $R_o=0.502220$ m and $\Delta p=9.2$ MPa (almost no internal pressure). Constant $E$ and $\nu$ ignore long-term creep and temperature variations. Do not apply this thin-shell buckling approximation to the original 60 mm shell as though it were a thin wall: $t/R_m$ is much larger there.

| Wall thickness (mm) | Ti-6Al-4V shell mass (kg) | Ideal buckling pressure (MPa) | 0.20 × ideal (MPa) | Membrane compression (MPa) |
|---:|---:|---:|---:|---:|
| 5 | 69.5 | 9.91 | 1.98 | 459.7 |
| 8 | 110.5 | 25.53 | 5.11 | 286.5 |
| 10 | 137.6 | 40.05 | 8.01 | 228.7 |
| 12 | 164.5 | 57.90 | 11.58 | 190.2 |
| 15 | 204.4 | 91.03 | 18.21 | 151.7 |
| 20 | 269.8 | 163.47 | 32.69 | 113.2 |

The column `0.20 × ideal` is an **arbitrary knockdown-factor sensitivity**, illustrating the effect of imperfection sensitivity. Research on external-pressure spherical shells reports substantial reductions compared with perfect-shell predictions [M10]. The factor 0.20 is **not** a verified knockdown factor for ASTARTE, a material allowable, an ASME rule or a certified design margin.

For comparison, taking an **illustrative pressure load factor** of 1.5 gives $p_{\rm study}=13.8$ MPa. The 15 mm idealized titanium case has $0.2p_{\rm cr,ideal}\approx18.2$ MPa, above that assumed study load. Actual acceptance requires a relevant design standard, measured imperfections, geometric nonlinearity, yielding and **time-dependent creep buckling**. A 15 mm design has **not** been approved.

**Pressure equalization effect:** external buckling is controlled by $\Delta p=p_{\rm outside}-p_{\rm inside}$, rather than Venus' absolute atmospheric pressure by itself. Maintaining a credible internal counter-pressure throughout heating, cooling, charging/handling, entry, landing, and a 60-day mission requires a separate design. We have not assumed this can be achieved safely with a molten-salt cell assembly.

## 5. Structural hazards beyond ideal buckling

1. **Geometric imperfections:** out-of-roundness, weld distortions, unsupported openings and manufacturing tolerances reduce buckling capacity; numerical eigenvalue buckling alone can overpredict strength [M10, M11].
2. **Temperature-dependent plasticity:** elastic modulus and yield behavior change near 465–500 °C; static stresses must be compared with *actual temperature-dependent* material properties and relevant allowables [M4, M9].
3. **Creep and time-dependent instability:** 1,440 hours under pressure at 465 °C creates a long-duration load case. ASME has published a specialist report on external pressure design in the creep regime [M12]. It does not provide a ready-made qualification of this enclosure.
4. **Chemical attack:** Venus includes CO₂ and reactive sulfur-containing trace gases. NASA's GEER tests found oxide/sulfide scales on a range of steels and Ni alloys, with different behavior for some coatings and ceramics [M5].
5. **Penetrations and joining:** signal feedthroughs, cell terminals, ceramic-metal seals, inspection joints and mechanical supports create localized loads and possible leakage paths.
6. **Dynamic loads:** the launch, entry, landing, rover motion and drop/shock cases need a separate acceleration and fatigue envelope before detailed sizing.

## 6. Candidate materials and role separation

| Role / candidate | Benefits motivating study | Evidence and design concerns | Initial status |
|---|---|---|---|
| **Ti-6Al-4V inner shell** | Low nominal density; direct 2026 Venus-like coupon study | Oxide/alpha-case; 60-day creep, welding, seal and wall-strength data missing [M4] | **Candidate A** |
| **304/316 stainless inner shell** | Manufacturing/joining experience; GEER vessel uses stainless interior [M6] | Higher mass at same thickness; oxide/sulfide scales and potential local corrosion over long exposure [M5, M6] | **Candidate B** |
| **Alloy 625 / similar Ni alloy** | High-temperature alloy reference and supplier property data [M8] | Higher density; NASA GEER exposure has observed nickel sulfide in Alloy 625 samples [M5] | **Candidate C** |
| **Al₂O₃ / SiC / Si₃N₄ ceramics** | Corrosion-compatible candidate for stand-offs, bushings and insulation, based on NASA GEER tests [M5] | Brittle fracture, thermal expansion mismatch, feedthrough manufacturing | **Auxiliary components** |
| **Carbon-fibre composite** | Historical lightweight structure idea | Polymer matrix rating, high-temperature oxidation/atmosphere and joint performance must be specified | **Historical option only** |

A multi-material structure may be worthwhile, but **each mating interface needs its own expansion and sealing calculation**. As a basic diagnostic, a 1.0 m member with two nominal expansion coefficients $\alpha_1=8.8\times10^{-6}$ K⁻¹ and $\alpha_2=17\times10^{-6}$ K⁻¹ accumulates about **3.61 mm** *difference in free expansion* from 25 °C to 465 °C. These are typical coefficients, not a validated joint model [M7].

## 7. How to preserve the 60-face ASTARTE identity

A **pentakis dodecahedron** offers a geometric starting point with **60 triangular faces, 90 edges and 32 vertices**; 20 vertices have degree six and 12 have degree five [M13]. It is a candidate geometry for the external module carrier, *not yet a pressure-rated hull*.

Separate CAD bodies are proposed:

1. **Pressure/chemical isolation shell:** smooth spherical reference with defined inner volume and feedthroughs.
2. **Modular battery subassemblies:** conceptual cell-stack bounding boxes with thermal/electrical clearances.
3. **Outer 60-face carrier:** supports panels, mounting, Mechanoron routing and replaceable protective features; load paths to the inner shell remain to be evaluated.
4. **Stand-offs / seals / feedthroughs:** interface geometry, expansion gaps and material selection to be established.

**Important:** the 60 faces are a mechanical and routing layout, not an assertion of 60 electrochemical cells. The provisional `19S4P` configuration in AST-ENG-002 is a *hypothetical electrical case* and should not be forced into a 60-face mechanical partition.

## 8. Fusion 360 parameter draft (NOT final manufacturing dimensions)

| User parameter | First-pass value | Meaning and status |
|---|---:|---|
| `R_outer_hist` | 502.22 mm | Historical-volume-equivalent sphere radius |
| `t_shell_trial` | 10 mm | Editable sensitivity value; evaluate 5–20 mm range |
| `R_inner_trial` | `R_outer_hist - t_shell_trial` | Derived cavity radius |
| `t_cage_trial` | 5 mm | **Pure CAD placeholder**, not structural sizing |
| `carrier_gap` | 10 mm | **Pure CAD placeholder**, no high-temperature clearance validation |
| `face_count` | 60 | Historical geometric design feature |
| `service_temperature` | 465 °C | Rounded Venus reference |
| `external_pressure` | 9.2 MPa | Nominal external pressure; internal pressure TBD |

**Model stage:** create a smooth, parametric reference shell and a separate faceted carrier. Use Fusion 360 for geometry and mass-property comparison where available. An actual buckling assessment may need a suitable solver outside the user's Fusion 360 license; a static stress contour alone is insufficient to quantify collapse pressure.

## 9. Evidence and verification gates

| Gate | Required evidence / check | Status |
|---|---|---|
| MECH-01 | Meaning of original 530,604 cm³ volume and historical dimensions | OPEN |
| MECH-02 | Inner pressure scenario, pressure differential, leakage and pressure balancing feasibility | OPEN |
| MECH-03 | Specific alloy grade/temper and $E(T),\nu(T),\sigma_y(T)$ | OPEN |
| MECH-04 | 1,440 h creep and material degradation at 465–500 °C | OPEN |
| MECH-05 | Imperfection-calibrated nonlinear buckling and verified design factor | OPEN |
| MECH-06 | Coatings, metals, ceramics and seals in relevant gas mixture | OPEN |
| MECH-07 | Cell containment and high-temperature electrical feedthrough design | OPEN |
| MECH-08 | Landing/mobility vibration, impact and supported masses | OPEN |
| MECH-09 | CAD mass roll-up and geometry audit | PLANNED |
| MECH-10 | Independent verification of formulas and numerical results | CALCULATION ONLY |

## 10. Decision at this checkpoint

Carry forward **two enclosure configurations**: (P) a sealed spherical reference shell for conservative external-pressure screening; (B) pressure-compensated containment as a higher-uncertainty research alternative. Use the original 60-triangle shape as a **separate, non-pressure-rated carrier** for now. This decoupling preserves the project's geometric identity and allows conventional pressure-shell analysis to proceed without claiming the 60-faced object is already suitable for 92-bar differential pressure.

**Next document:** `05-mechanoron-network.md` can define the graph topology, node failure behavior and electrical losses. Structural and battery choices remain preliminary until the gates above are addressed. A small Python test should independently regenerate the table in Sections 3 and 4 before CAD results are presented in the portfolio.

## References

**[M1]** NASA Space Apps Challenge 2022. *Team Aldebaran — Exploring Venus Together.* https://2022.spaceappschallenge.org/challenges/2022-challenges/exploring-venus/teams/team-aldebaran/

**[M2]** NASA NSSDC. *Venus Fact Sheet.* https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html

**[M3]** NASA Science (2023). *Providing Power on Earth's Evil Twin.* https://science.nasa.gov/science-research/science-enabling-technology/providing-power-on-earth-s-evil-twin/

**[M4]** Kane, K. A., et al. (2026). *Corrosion and mechanical performance of wrought and additively manufactured Ti-6Al-4V under supercritical carbon dioxide Venus atmospheric conditions.* *npj Materials Degradation.* https://doi.org/10.1038/s41529-026-00877-7

**[M5]** Costa, G. C. C., et al. (2017). *Chemical and Microstructural Changes in Metallic and Ceramic Materials Exposed to Venusian Surface Conditions.* NASA/TM-2017-219437. https://ntrs.nasa.gov/citations/20170006025

**[M6]** Gilmore, M. S., et al. (2025). *Overview of the MMT 60-Day GEER Experiment on Geologic Samples at Venus Surface Conditions.* *Journal of Geophysical Research: Planets.* https://doi.org/10.1029/2025JE009237

**[M7]** Nippon Steel. *Titanium and titanium alloy technical data* (densities and thermal expansion reference). https://www.nipponsteel.com/en/product/titan/feature/pdf/T001en_16-23.pdf

**[M8]** Haynes International. *HAYNES® 625 alloy — Physical Properties.* https://haynesintl.com/en/alloys/alloy-portfolio/high-temperature-alloys/haynes-625/

**[M9]** Palmeri, D., et al. (2023). *Finite Element Method in L-PBF of Ti-6Al-4V: Influence of Laser Power and Scan Speed on Residual Stress and Part Distortion.* *Metals*, 13(11), 1907. Table 1 (modelling parameters). https://doi.org/10.3390/met13111907

**[M10]** *Geometric imperfection and lower-bound analysis of spherical shells under external pressure* (2019). *Thin-Walled Structures.* https://www.sciencedirect.com/science/article/pii/S0263823118312771

**[M11]** *Localization in spherical shell buckling* (2020). *Journal of the Mechanics and Physics of Solids.* https://www.sciencedirect.com/science/article/pii/S0022509619306052

**[M12]** ASME. *External Pressure Design in Creep Range*, STP-PT-029-1. https://www.asme.org/codes-standards/find-codes-standards/external-pressure-design-in-creep-range

**[M13]** Wolfram MathWorld. *Pentakis Dodecahedron.* https://mathworld.wolfram.com/PentakisDodecahedron.html

---

*Evidence labels: published measurements and sourced reference values are distinct from numerical assumptions, sensitivity factors, analytical results, and open validation gates. This document is a feasibility-study output, not pressure-vessel certification.*
