# ARINC Characteristic 745 & RTCA DO-258A Engineering Specification

## Automatic Dependent Surveillance (ADS-C) Airborne & Ground Subsystem Architecture

**Document Version:** 1.0.0 • **Status:** Approved for Implementation • **Standard Baseline:** ARINC 745, RTCA DO-258A / EUROCAE ED-100A, ICAO Doc 9705 / Doc 9880, FAA AC 20-140C

---

### 1\. Executive Summary

ARINC Characteristic 745 defines the design guidance and standard avionics provisions for Automatic Dependent Surveillance (ADS-C) operational over oceanic, polar, and remote airspace. ADS-C establishes digital point-to-point contracts between the airborne Flight Management Computer (FMC) / Communications Management Unit (CMU) and Air Traffic Services (ATS) ground automation systems (such as Shanwick EGGX, Gander CZQX, Oakland KZAK, and Fukuoka RJJJ).

ARINC745Forge Pro provides an avionics-grade reference implementation of the ADS-C contract state machine, FANS 1/A surveillance report encodings, discrete ARINC 429 glass-cockpit bus interface, and a 10-point normative compliance audit suite.

---

### 2\. Normative Industry Standards Reference Architecture

1. **ARINC Characteristic 745**: *Automatic Dependent Surveillance (ADS)* — Architectural definition of airborne ADS equipment, CMU interfaces, contract parameters, and glass-cockpit discrete status words.  
2. **RTCA DO-258A / EUROCAE ED-100A**: *Interoperability Requirements for ATS Applications Using ARINC 622 Data Communications* — Normative definition of FANS 1/A ADS-C contract management and ASN.1 message bitstream formatting.  
3. **ICAO Doc 9705 / Doc 9880**: *Manual on Technical Provisions for the Aeronautical Telecommunication Network (ATN)* — Datalink application protocols for oceanic and remote air traffic management.  
4. **FAA AC 20-140C**: *Guidelines for Design Approval of Aircraft Data Link Communication Systems Supporting Air Traffic Services (ATS)* — Airworthiness compliance for oceanic surveillance and RNP-based reduced lateral/longitudinal separation (e.g., 30/30 NM and 23 NM Oceanic Tracks).

---

### 3\. FANS 1/A ADS-C Contract State Machine & Contract Types

An aircraft can maintain simultaneous contracts with up to four ground facilities (e.g., controlling FIR and adjacent downstream FIR for automated handoff):

| Contract Type | Operating Principle | Uplink Parameters / Trigger Criteria | Downlink Report Frequency |
| :---- | :---- | :---- | :---- |
| **Periodic Contract** | Ground station specifies reporting time interval. | Reporting interval \$T\_{interval} \\in \[1, 4095\\text{ seconds}\]\$. Default oceanic standard is 600 seconds (10 min) or 300 seconds (5 min). | Downlinked at regular scheduled timestamps with countdown timer. |
| **Event Contract** | Airborne CMU monitors aircraft trajectory and downlinks an event report upon parameter threshold exceedance. | • Waypoint Change: Overflight of active waypoint. • Altitude Deviation: Excursion exceeds \$\\pm 200\\text{ ft}\$ from cleared level. • Lateral Deviation: Cross-track error (XTK) exceeds \$1.0\\text{ NM}\$. • Vertical Rate: Rate of climb/descent exceeds \$500\\text{ fpm}\$. | Downlinked immediately upon triggering event. Does not reset periodic timer. |
| **Demand Contract** | One-time interrogation report requested by ATC controller. | Downlink report requested immediately for immediate conflict probe or radar correlation. | Single immediate downlink report transmission. |
| **Emergency Contract** | Airborne crew initiates emergency mode via cockpit discrete or FMS MAYDAY prompt. | Automatically overrides periodic interval and broadcasts high-priority emergency bursts. | High-frequency burst downlinks every 60 seconds until cancelled by flight crew. |

---

### 4\. Downlink ADS-C Message Payload Structure (DO-258A)

Each ADS-C downlink packet is assembled into discrete normative report groups:

#### 4.1 Group 1: Basic Report Group (Mandatory)

Every transmitted ADS-C packet must contain Group 1:

- **Latitude / Longitude**: WGS-84 coordinates encoded to 0.0001° resolution.  
- **Altitude**: Pressure altitude in 1-foot increments (e.g., FL370 \= 37,000 ft).  
- **Time UTC**: Hours, minutes, and seconds of position fix.  
- **Figure of Merit (FOM)**: Navigation accuracy and integrity indicator:  
  - `FOM 7`: RNP 1.0 / 0.3 NM accuracy with GPS RAIM integrity confirmed.  
  - `FOM 6`: RNP 2.0 NM accuracy.  
  - `FOM 5`: RNP 4.0 NM accuracy.  
  - `FOM 4`: RNP 10.0 NM accuracy.

#### 4.2 Group 2: Earth Reference Dynamics Group (Optional / Negotiated)

- **True Track**: Aerodynamic ground track angle in degrees (\$0.0^\\circ\$ to \$360.0^\\circ\$).  
- **Ground Speed**: True ground speed in knots (0 to 1023 kt).  
- **Vertical Rate**: Instantaneous vertical velocity in feet per minute (\$\\pm 6000\\text{ fpm}\$).

#### 4.3 Group 3: Meteorological Data Group

- **Wind Direction & Speed**: Ambient wind vector measured by air data computer (e.g., \$260^\\circ / 72\\text{ kt}\$).  
- **Static Air Temperature (SAT)**: Outside ambient temperature encoded in degrees Celsius (e.g., \$-54.0^\\circ\\text{C}\$).

#### 4.4 Group 4 & 5: Projected Intent Groups

- **Next Waypoint Fix**: Waypoint identifier, latitude, longitude, and estimated time of arrival (ETA UTC).  
- **Next+1 Waypoint Fix**: Downstream flight plan waypoint for multi-sector automated trajectory prediction.

---

### 5\. ARINC 429 Glass-Cockpit Discrete Bus Architecture

ARINC 745 specifies two dedicated ARINC 429 digital words transmitted on the flight deck avionics bus at high speed (100 kbps) or low speed (12.5 kbps):

#### Label 305 (Octal 305 / Hex 0xC5): ADS-C Status & FOM

- **Bits 1–8**: ARINC 429 Label `305` (Hex `C5`, transmitted LSB first).  
- **Bits 9–10**: SDI (Source/Destination Identifier: `00` for Omnidirectional).  
- **Bits 11–13**: Active ATC Ground Facility Code (`001` \= Shanwick, `010` \= Gander, `011` \= Oakland, `100` \= Fukuoka).  
- **Bits 14–16**: Figure of Merit (`000` to `111` for FOM 0–7).  
- **Bit 17**: Emergency Contract Active Flag (`0` \= Normal, `1` \= Emergency).  
- **Bit 18**: Periodic Contract Active Flag (`1` \= Armed/Active).  
- **Bit 19**: Event Contract Active Flag (`1` \= Armed/Active).  
- **Bits 20–28**: Reserved / Datalink Subsystem Status.  
- **Bits 29–30**: SSM (Sign/Status Matrix: `11` \= Normal Operation).  
- **Bit 32**: Odd Parity bit (computed across Bits 1–31 to ensure total number of '1' bits is odd).

#### Label 306 (Octal 306 / Hex 0xC6): ADS-C Time to Next & Event Count

- **Bits 1–8**: ARINC 429 Label `306` (Hex `C6`).  
- **Bits 9–10**: SDI (`00`).  
- **Bits 11–20**: Seconds Remaining to Next Periodic Report (\$0\$ to \$1023\\text{ seconds}\$).  
- **Bits 21–24**: Cumulative Event Report Trigger Count (\$0\$ to \$15\$).  
- **Bits 25–28**: Reserved.  
- **Bits 29–30**: SSM (`11` \= Normal Operation).  
- **Bit 32**: Odd Parity bit.