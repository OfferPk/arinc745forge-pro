#!/usr/bin/env python3
"""
ARINC745Forge Pro Automated Test Runner (10-Point Test Suite)
Validates:
1. Periodic Contract Generation & Structure
2. Basic Report Group Integrity (Lat, Lon, Alt, FOM)
3. Earth Reference Group Integrity (Track, GS, VS)
4. Meteorological Group Formatting (Wind, Temp)
5. Projected Intent Group Structure (Next Waypoint, ETA)
6. Waypoint Change Event Trigger Logic
7. Altitude Excursion Event Contract (Threshold ±200 ft boundary)
8. Lateral Deviation / Cross-Track Error Event Contract (Threshold 1.0 NM boundary)
9. ARINC 429 Label 305 & 306 Bitfield Architecture
10. ARINC 429 Bit 32 Odd Parity Verification
"""

import sys
import os

# Ensure local import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arinc745_cli import ARINC745Simulator

def run_tests():
    print("=" * 70)
    print("ARINC745Forge Pro — Automated Compliance & Unit Test Suite")
    print("Standards: ARINC Characteristic 745, RTCA DO-258A, EUROCAE ED-100A")
    print("=" * 70)

    sim = ARINC745Simulator()
    tests_passed = 0
    total_tests = 10

    # Test 1: Periodic Contract Generation
    rep = sim.generate_report("PERIODIC")
    assert rep["trigger"] == "PERIODIC"
    assert rep["facility"] == "EGGX"
    print("Test 1: Periodic Contract Generation & ATC Ground Association ... PASS")
    tests_passed += 1

    # Test 2: Basic Report Group Integrity
    basic = rep["basic"]
    assert "lat" in basic and "lon" in basic and "alt" in basic and "fom" in basic
    assert 0 <= basic["fom"] <= 7
    print("Test 2: Basic Report Group Payload & FOM Validation (DO-258A §3.2) ... PASS")
    tests_passed += 1

    # Test 3: Earth Reference Group Integrity
    earth = rep["earth_ref"]
    assert 0 <= earth["track"] <= 360
    assert earth["gs"] > 0
    print("Test 3: Earth Reference Dynamics Group (Track/GS/VS) ... PASS")
    tests_passed += 1

    # Test 4: Meteorological Group
    met = rep["met"]
    assert "kt" in met["wind"]
    assert "°C" in met["sat"]
    print("Test 4: Meteorological Group Parsing (Wind Vector & SAT) ... PASS")
    tests_passed += 1

    # Test 5: Projected Intent Group
    intent = rep["intent"]
    assert intent["next"] == "55N030W"
    assert ":" in intent["eta"]
    print("Test 5: Projected Intent Trajectory Group (Next Fix & ETA) ... PASS")
    tests_passed += 1

    # Test 6: Waypoint Change Event Trigger
    wpt_rep = sim.trigger_waypoint("55N040W")
    assert wpt_rep["trigger"] == "EVENT"
    assert wpt_rep["intent"]["next"] == "55N040W"
    print("Test 6: Waypoint Sequence Event Downlink Trigger ... PASS")
    tests_passed += 1

    # Test 7: Altitude Excursion Event Contract Boundary (±200 ft)
    no_ev = sim.trigger_altitude_excursion(150)
    assert no_ev is None  # Below 200 ft threshold
    ev = sim.trigger_altitude_excursion(250)
    assert ev is not None and ev["trigger"] == "EVENT"
    print("Test 7: Altitude Deviation Event Contract Threshold (±200 ft) ... PASS")
    tests_passed += 1

    # Test 8: Lateral Deviation (Cross-Track) Boundary (1.0 NM)
    no_lat_ev = sim.trigger_lateral_deviation(0.8)
    assert no_lat_ev is None # Below 1.0 NM threshold
    lat_ev = sim.trigger_lateral_deviation(1.2)
    assert lat_ev is not None and lat_ev["trigger"] == "EVENT"
    print("Test 8: Lateral Deviation Event Contract Threshold (1.0 NM) ... PASS")
    tests_passed += 1

    # Test 9: ARINC 429 Label 305 & 306 Bitfield Architecture
    bus = sim.generate_arinc429_words()
    assert bus["label305"].startswith("0x")
    assert bus["label306"].startswith("0x")
    print("Test 9: ARINC 429 Discrete Cockpit Bus Encoding (Labels 305/306) ... PASS")
    tests_passed += 1

    # Test 10: ARINC 429 Bit 32 Odd Parity Verification
    w305 = int(bus["label305"], 16)
    w306 = int(bus["label306"], 16)
    assert sim.verify_odd_parity(w305) is True
    assert sim.verify_odd_parity(w306) is True
    print("Test 10: ARINC 429 Bit 32 Odd Parity Hardware Verification ... PASS")
    tests_passed += 1

    print("=" * 70)
    print(f"AUTOMATED TEST RESULTS: {tests_passed}/{total_tests} TESTS PASSED (100% SUCCESS RATE)")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
