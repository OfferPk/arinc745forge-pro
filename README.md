# ARINC745Forge Pro (v1.0.0)

## Commercial Avionics Automatic Dependent Surveillance (ADS-C) Contract Engine, Oceanic Tracking Studio & 10-Point Normative Auditor

**Target Standards:** [ARINC Characteristic 745](https://en.wikipedia.org/wiki/ARINC), [RTCA DO-258A](https://standards.globalspec.com/std/1018597/rtca-do-258a), [EUROCAE ED-100A](https://www.eurocae.net/), [ICAO Doc 9705 / Doc 9880](https://store.icao.int/), [FAA AC 20-140C](https://www.faa.gov/regulations_policies/advisory_circulars/)

---

### Overview

**ARINC745Forge Pro** is an avionics-grade reference implementation and simulation suite for **Automatic Dependent Surveillance \- Contract (ADS-C)** operational across the North Atlantic Organised Track System (NAT-OTS), Pacific Oceanic FIRs, and remote airspace.

Built to address the strict surveillance certification mandates of **FAA AC 20-140C** and **ICAO Performance-Based Longitudinal Separation (30/30 NM & 23 NM RNP tracks)**, ARINC745Forge Pro empowers avionics manufacturers, datalink software engineers, and airline flight operations teams to model, test, and audit ADS-C contract lifecycles and ARINC 429 cockpit bus telemetry.

---

### Key Capabilities

- **Four Standard ADS-C Contract Engines**: Full lifecycle modeling for **Periodic Contracts** (1–4095s interval), **Event Contracts** (Waypoint overflight, Altitude deviation ±200 ft, Lateral deviation 1.0 NM, Vertical rate), **Demand Contracts** (ATC one-time interrogation), and **Emergency Contracts** (60s burst preemption).  
- **Complete FANS 1/A Downlink Report Groups**: Assembles standard Basic Position Reports, Earth Reference Dynamics Groups (True Track, GS, VS), Meteorological Groups (Wind vector, SAT), and Projected Intent Trajectory Groups.  
- **Glass-Cockpit ARINC 429 Discrete Bus Monitor**: Generates and verifies **Label 305** (ADS-C Status & FOM) and **Label 306** (Time to Next Report & Event Count) with hardware-accurate **Bit 32 Odd Parity** verification.  
- **Interactive Oceanic Radar Studio (`index.html`)**: Interactive dark aviation HUD featuring the Shanwick (EGGX) and Gander (CZQX) North Atlantic Track (NAT-OTS Oscar), real-time trajectory extrapolations, manual ATC interrogation triggers, and downlink log streams.  
- **10-Point Normative Compliance Auditor**: Automated verification suite validating DO-258A, ARINC 745, and AC 20-140C requirements with 100% pass criteria.  
- **Python 3 CLI & Automated Test Suite**: Zero-dependency standalone CLI tool (`arinc745-cli.py`) and 10-point test runner (`test_runner.py`).

---

### Standards References

- [ARINC Characteristic 745 — Automatic Dependent Surveillance (ADS)](https://en.wikipedia.org/wiki/ARINC)  
- [RTCA DO-258A / EUROCAE ED-100A — Interoperability Requirements for ATS Applications](https://standards.globalspec.com/std/1018597/rtca-do-258a)  
- [FAA Advisory Circular AC 20-140C — Design Approval of Aircraft Data Link Systems](https://www.faa.gov/regulations_policies/advisory_circulars/)  
- [ICAO Doc 9705 / Doc 9880 — Aeronautical Telecommunication Network (ATN)](https://store.icao.int/)