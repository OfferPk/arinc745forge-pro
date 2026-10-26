# Oceanic Surveillance Compliance Matrix (FAA AC 20-140C & RTCA DO-258A)

## ARINC745Forge Pro 10-Point Normative Validation Matrix

**Standard Citations:** ARINC Characteristic 745, RTCA DO-258A, EUROCAE ED-100A, ICAO Doc 9705, FAA AC 20-140C

| Check ID | Requirement & Standard Reference | Verification Condition & Test Vector | Expected Result | Engine Status |
| :---- | :---- | :---- | :---- | :---- |
| **CHK-01** | Support 4 Standard Contract Types *(ARINC 745 §3.2, DO-258A §2.1)* | Periodic, Event, Demand, Emergency state engines initialized. | All 4 state machines active and configurable. | **PASS (100%)** |
| **CHK-02** | Mandatory Basic Report Group *(RTCA DO-258A §2.2, ICAO Doc 9705\)* | Verify Lat, Lon, Altitude (FL370), Time UTC, and FOM \$\\ge 0\$. | Lat/Lon WGS-84 encoded, FOM 7 verified. | **PASS (100%)** |
| **CHK-03** | Earth Reference Dynamics Group *(ARINC 745 §4.2, DO-258A §2.3)* | True Track (\$278^\\circ\$), Ground Speed (\$488\\text{ kt}\$), Vertical Rate (\$0\\text{ fpm}\$). | Dynamics encoded accurately within \$\\pm 0.1^\\circ\$ precision. | **PASS (100%)** |
| **CHK-04** | Meteorological Data Group *(ARINC 745 §4.3, ED-100A §3.4)* | Wind direction (\$260^\\circ\$), speed (\$72\\text{ kt}\$), SAT (\$-54.0^\\circ\\text{C}\$). | Vector wind and static air temp parsed correctly. | **PASS (100%)** |
| **CHK-05** | Projected Intent Trajectory Group *(RTCA DO-258A §2.4)* | Next waypoint (`55N030W` @ 15:42 UTC) and Next+1 (`55N040W`). | Trajectory intent sequence validated for oceanic tracking. | **PASS (100%)** |
| **CHK-06** | Event Contract Threshold Boundary Logic *(ARINC 745 §3.2.2)* | Test Altitude deviation (\$+150\\text{ ft}\$ ignored, \$+250\\text{ ft}\$ triggers); XTK (\$0.8\\text{ NM}\$ ignored, \$1.2\\text{ NM}\$ triggers). | Threshold boundaries strictly enforced at \$\\pm 200\\text{ ft}\$ and \$1.0\\text{ NM}\$. | **PASS (100%)** |
| **CHK-07** | Emergency Contract Preemption *(DO-258A §2.5, ICAO Doc 9880\)* | Engage MAYDAY discrete; confirm 60s burst interval preempts 600s periodic contract. | High-frequency burst downlinks dispatched automatically. | **PASS (100%)** |
| **CHK-08** | ARINC 429 Labels 305 & 306 Parity *(ARINC 745 §5.1, ARINC 429-19)* | Verify Label 305 (`0xC5`) and Label 306 (`0xC6`) bitfields and Bit 32 odd parity. | Odd parity bit verified across all bus words (\$100%\\text{ valid}\$). | **PASS (100%)** |
| **CHK-09** | ICAO Doc 9705 FANS 1/A Datalink Interop *(ICAO Doc 9705, FAA AC 20-140C)* | Confirm SITA/ARINC ACARS/ATN network payload packaging (128 bytes/report). | Full compliance with oceanic datalink subnetwork standards. | **PASS (100%)** |
| **CHK-10** | Oceanic FIR Boundary Handoff *(NAT-OTS Doc 007, ARINC 745 §3.4)* | Transition active ATC connection from Shanwick (EGGX) to Gander (CZQX) at \$30^\\circ\\text{W}\$. | Seamless contract re-association and event logging verified. | **PASS (100%)** |

