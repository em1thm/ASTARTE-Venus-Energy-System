# ASTARTE — Project History and 2026 Redesign

**Project:** ASTARTE Venus Energy System  
**Original team:** Team Aldebaran, NASA International Space Apps Challenge 2022  
**Challenge:** Exploring Venus Together  
**2026 continuation:** Independent engineering redesign of the original team concept  
**Document status:** Working draft — 11 November 2026

## Where the project began (2022)

ASTARTE began as Team Aldebaran's response to the 2022 NASA Space Apps *Exploring Venus Together* challenge. The challenge asked teams to design an energy storage system capable of powering a surface lander or rover on Venus for at least 60 Earth days.

I served as the team leader. Our team proposed a battery assembly with a 60-triangle external geometry, a layered protective enclosure and an electrical network inspired by the connections between neurons. We called its proposed connection nodes **Mechanorons**. The intention was to make the energy system modular and preserve an alternative electrical path when an individual battery module failed.

The original design described three protective layers: a 6 cm titanium exterior, an 8 cm aerogel insulation layer and a 2 cm carbon-fiber interior. It also proposed lithium-sulfide-based battery elements. These choices documented our design reasoning in 2022; their ability to operate together on Venus had not been established through a full engineering validation program.

The original submission reported a total mass of 450 kg, a volume of 530,604 cm³ and a capacity value of 219 kW. The capacity figure uses a unit of power rather than stored energy, and the geometry, material quantities and electrochemical assumptions require re-evaluation. These values are kept here as **historical claims**, not adopted 2026 specifications.

The official archived Space Apps team page records the team as a **Global Nominee**. Any separate evidence for a Global Finalist designation will be assessed before the recognition is described differently in application materials.

## Why I am revisiting ASTARTE (2026)

I am returning to the concept to test how far it can be developed as an engineering system. The main question is whether a modular, fault-tolerant battery architecture could support a long-duration Venus surface mission when the electrochemistry, thermal environment, mechanical loads and power electronics are modelled together.

The redesign will first examine the battery as a subsystem, then consider its integration into a rover. It will retain the 60-face geometry and the biological inspiration as candidate design features, while allowing their electrical and mechanical implementations to change when calculations indicate a better solution.

## Engineering work planned for ASTARTE V2

1. **Mission and electrical requirements:** Define realistic science, communications, standby and mobility load profiles; calculate usable energy and reserve margins for 60 Earth days.
2. **Cell chemistry and architecture:** Evaluate high-temperature lithium-alloy/metal-sulfide molten-salt technology against other candidates using published test conditions and limitations.
3. **Thermal and structural analysis:** Estimate heat transfer, enclosure mass and pressure-related failure risks using temperature-dependent properties and explicitly stated assumptions.
4. **Mechanoron network:** Formalize the connection graph, fault-isolation strategy, losses and load-shedding rules; compare performance with a conventional battery arrangement.
5. **Design and validation:** Produce parametric Fusion 360 models, reproducible Python simulations, sensitivity analyses and—if practical—a safe low-temperature demonstration of the control concept.

## Evidence and status

As of the date of this document, **ASTARTE V2 is at the feasibility and concept-development stage**. Published NASA research establishes relevant technology demonstrations; it does not yet establish that this proposed integrated rover power system can complete a 60-day Venus mission. Numerical values developed in future documents will be labelled as reported measurements, engineering assumptions, calculated estimates or experimental results.

The 2022 project was created collaboratively by Team Aldebaran. This repository is intended to document my subsequent independent technical work. Original team contributions and new analysis will be attributed separately throughout.

## Starting references

- [NASA Space Apps 2022 — Team Aldebaran, original project](https://2022.spaceappschallenge.org/challenges/2022-challenges/exploring-venus/teams/team-aldebaran/)
- [NASA Space Apps 2022 — Team Aldebaran, team members](https://2022.spaceappschallenge.org/challenges/2022-challenges/exploring-venus/teams/team-aldebaran/members/)
- [NASA NSSDC — Venus Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html)
- [NASA Science — Providing Power on Earth's Evil Twin](https://science.nasa.gov/science-research/science-enabling-technology/providing-power-on-earth-s-evil-twin/)
- [NASA NTRS — Progress Towards SiC ASICs for Extreme Temperature and Radiation Environments](https://ntrs.nasa.gov/citations/20240015144)

*Next document: `research/evidence-register.csv`, with claim-level references and verification status.*
