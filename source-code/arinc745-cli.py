#!/usr/bin/env python3
"""
ARINC745Forge Pro — Standalone Python 3 CLI Runner & ADS-C Report Parser
Automatic Dependent Surveillance (ADS-C) Oceanic Tracking Suite
Standards: ARINC Characteristic 745, RTCA DO-258A, EUROCAE ED-100A
"""

import sys
import json
import time

class ARINC745Simulator:
    def __init__(self):
        self.callsign = "UAL745"
        self.facility = "EGGX" # Shanwick Oceanic
        self.periodic_interval_sec = 600
        self.seconds_to_next = 240
        self.emergency = False
        
        self.telemetry = {
            "lat": 55.0,
            "lon": -25.4,
            "alt": 37000,
            "cleared_alt": 37000,
            "true_track": 278.0,
            "ground_speed": 488,
            "vert_rate": 0,
            "xtk_nm": 0.1,
            "fom": 7,
            "wind_dir": 260,
            "wind_spd": 72,
            "sat": -54.0,
            "next_wpt": "55N030W",
            "next_eta": "15:42"
        }
        
        self.events_sent = 0

    def generate_report(self, trigger="PERIODIC"):
        if trigger == "EVENT":
            self.events_sent += 1
        return {
            "callsign": self.callsign,
            "facility": self.facility,
            "trigger": trigger,
            "emergency": self.emergency,
            "basic": {
                "lat": self.telemetry["lat"],
                "lon": self.telemetry["lon"],
                "alt": self.telemetry["alt"],
                "fom": self.telemetry["fom"]
            },
            "earth_ref": {
                "track": self.telemetry["true_track"],
                "gs": self.telemetry["ground_speed"],
                "vs": self.telemetry["vert_rate"]
            },
            "met": {
                "wind": f"{self.telemetry['wind_dir']}° / {self.telemetry['wind_spd']} kt",
                "sat": f"{self.telemetry['sat']}°C"
            },
            "intent": {
                "next": self.telemetry["next_wpt"],
                "eta": self.telemetry["next_eta"]
            }
        }

    def trigger_waypoint(self, wpt_name):
        self.telemetry["next_wpt"] = wpt_name
        return self.generate_report("EVENT")

    def trigger_altitude_excursion(self, dev_ft):
        self.telemetry["alt"] = self.telemetry["cleared_alt"] + dev_ft
        if abs(dev_ft) >= 200:
            return self.generate_report("EVENT")
        return None

    def trigger_lateral_deviation(self, xtk):
        self.telemetry["xtk_nm"] = xtk
        if xtk >= 1.0:
            return self.generate_report("EVENT")
        return None

    def generate_arinc429_words(self):
        # Label 305 (Octal): ADS-C Status & FOM
        label305 = 0xC5
        fac_map = {"EGGX": 1, "CZQX": 2, "KZAK": 3, "RJJJ": 4}
        fac_val = fac_map.get(self.facility, 1)
        emerg_bit = 1 if self.emergency else 0

        data305 = ((fac_val & 0x07) << 10) | \
                  ((self.telemetry["fom"] & 0x07) << 13) | \
                  (emerg_bit << 16) | \
                  (1 << 17) | (1 << 18) | \
                  (0x03 << 28)
        word305 = (data305 & 0x7FFFFF00) | label305
        word305 = self.apply_odd_parity(word305)

        # Label 306 (Octal): Seconds to Next Report & Event Count
        label306 = 0xC6
        sec_val = min(1023, max(0, self.seconds_to_next))
        data306 = ((sec_val & 0x3FF) << 10) | \
                  ((min(15, self.events_sent) & 0x0F) << 20) | \
                  (0x03 << 28)
        word306 = (data306 & 0x7FFFFF00) | label306
        word306 = self.apply_odd_parity(word306)

        return {
            "label305": hex(word305),
            "label306": hex(word306),
            "odd_parity_valid": self.verify_odd_parity(word305) and self.verify_odd_parity(word306)
        }

    def apply_odd_parity(self, word):
        bits = word & 0x7FFFFFFF
        count = bin(bits).count('1')
        if count % 2 == 0:
            bits |= (1 << 31)
        return bits

    def verify_odd_parity(self, word):
        return bin(word).count('1') % 2 == 1

def run_cli():
    sim = ARINC745Simulator()
    print("=" * 70)
    print("ARINC745Forge Pro — FANS 1/A ADS-C Surveillance CLI")
    print("Standards: ARINC Characteristic 745, RTCA DO-258A, EUROCAE ED-100A")
    print("=" * 70)

    rep = sim.generate_report("PERIODIC")
    print(f"\n[ACTIVE ADS-C CONTRACT WITH {sim.facility} (SHANWICK OCEANIC)]")
    print(f"  Callsign         : {rep['callsign']}")
    print(f"  Position         : {rep['basic']['lat']}°N, {abs(rep['basic']['lon'])}°W (FL{rep['basic']['alt']//100})")
    print(f"  Figure of Merit  : FOM {rep['basic']['fom']} (RNP 1.0/0.3 Navigation Verified)")
    print(f"  Earth Dynamics   : Track {rep['earth_ref']['track']}° | Ground Speed {rep['earth_ref']['gs']} kt")
    print(f"  Meteorological   : Winds {rep['met']['wind']} | Temp {rep['met']['sat']}")
    print(f"  Next Waypoint    : {rep['intent']['next']} @ {rep['intent']['eta']} UTC")

    # Simulate Event Trigger
    print("\n[SIMULATING EVENT CONTRACT: ALTITUDE EXCURSION +300 FT]")
    ev_rep = sim.trigger_altitude_excursion(300)
    if ev_rep:
        print(f"  Automatic Downlink Triggered: Event Report Generated ({ev_rep['trigger']})")

    bus = sim.generate_arinc429_words()
    print("\n" + "-" * 70)
    print("ARINC 429 Glass-Cockpit Discrete Bus Output:")
    print(f"  Label 305 (ADS-C Status & FOM)       : {bus['label305']}")
    print(f"  Label 306 (Seconds to Next & Events) : {bus['label306']}")
    print(f"  Bit 32 Odd Parity Status             : {'VALID (PASS)' if bus['odd_parity_valid'] else 'INVALID (FAIL)'}")
    print("=" * 70)

if __name__ == "__main__":
    run_cli()
