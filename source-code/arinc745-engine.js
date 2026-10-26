/**
 * ARINC745Forge Pro — Core Engine
 * Automatic Dependent Surveillance (ADS-C, ARINC 745 & RTCA DO-258A)
 * Standard References: ARINC Characteristic 745, RTCA DO-258A, EUROCAE ED-100A, ICAO Doc 9705, FAA AC 20-140C
 */

class ARINC745Engine {
  constructor() {
    this.groundFacilities = {
      'EGGX': { name: 'Shanwick Oceanic FIR (Prestwick, UK)', network: 'FANS_1A_SATCOM', active: true },
      'CZQX': { name: 'Gander Oceanic FIR (Newfoundland, Canada)', network: 'FANS_1A_SATCOM', active: true },
      'KZAK': { name: 'Oakland Oceanic FIR (FAA Pacific)', network: 'FANS_1A_SATCOM', active: false },
      'RJJJ': { name: 'Fukuoka Oceanic FIR (Japan JCAB)', network: 'FANS_1A_SATCOM', active: false }
    };
    this.activeFacility = 'EGGX';

    // FANS 1/A ADS-C Contracts (ARINC 745 §3.2 / RTCA DO-258A)
    this.contracts = {
      periodic: { enabled: true, intervalSeconds: 600, secondsUntilNext: 240 },
      event: {
        enabled: true,
        waypointChange: true,
        altitudeRangeThresholdFt: 200,
        lateralDeviationThresholdNm: 1.0,
        verticalRateThresholdFpm: 500
      },
      demand: { pendingRequests: 0 },
      emergency: { active: false, burstIntervalSeconds: 60 }
    };

    // Aircraft State & Telemetry
    this.flightState = {
      callsign: 'UAL745',
      tailNumber: 'N745AG',
      airframe: 'Boeing 787-9',
      lat: 55.0,
      lon: -25.4,
      altFt: 37000,
      clearedAltFt: 37000,
      trueTrackDeg: 278.0,
      groundSpeedKt: 488,
      verticalRateFpm: 0,
      crossTrackErrorNm: 0.1,
      fom: 7, // Figure of Merit: 7 = RNP 1.0/0.3, GPS integrity verified
      windDirDeg: 260,
      windSpeedKt: 72,
      satDegC: -54.0,
      nextWaypoint: { id: '55N030W', lat: 55.0, lon: -30.0, etaUtc: '15:42', altFt: 37000 },
      nextPlusOneWaypoint: { id: '55N040W', lat: 55.0, lon: -40.0, etaUtc: '16:55', altFt: 37000 }
    };

    // Transmission History & Statistics
    this.transmittedReports = [];
    this.stats = {
      periodicReportsSent: 0,
      eventReportsSent: 0,
      demandReportsSent: 0,
      emergencyReportsSent: 0,
      totalDownlinkBytes: 0
    };

    // Generate initial report
    this.generateADSReport('PERIODIC_REPORT');
  }

  generateADSReport(triggerType, eventDetails = null) {
    const timestamp = new Date().toISOString();
    const reportID = `ADSC-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

    const report = {
      reportID: reportID,
      timestamp: timestamp,
      facility: this.activeFacility,
      triggerType: triggerType,
      eventDetails: eventDetails,
      basicReport: {
        lat: parseFloat(this.flightState.lat.toFixed(4)),
        lon: parseFloat(this.flightState.lon.toFixed(4)),
        altitudeFt: this.flightState.altFt,
        timeUtc: timestamp.substring(11, 19),
        figureOfMerit: this.flightState.fom
      },
      earthRefGroup: {
        trueTrackDeg: this.flightState.trueTrackDeg,
        groundSpeedKt: this.flightState.groundSpeedKt,
        verticalRateFpm: this.flightState.verticalRateFpm
      },
      metGroup: {
        windSpeedKt: this.flightState.windSpeedKt,
        windDirDeg: this.flightState.windDirDeg,
        satDegC: this.flightState.satDegC
      },
      projectedIntent: {
        nextWaypoint: { ...this.flightState.nextWaypoint },
        nextPlusOne: { ...this.flightState.nextPlusOneWaypoint }
      },
      emergency: this.contracts.emergency.active,
      payloadBytes: 128
    };

    this.transmittedReports.unshift(report);
    if (this.transmittedReports.length > 25) this.transmittedReports.pop();

    if (triggerType === 'PERIODIC_REPORT') this.stats.periodicReportsSent++;
    else if (triggerType === 'EVENT_REPORT') this.stats.eventReportsSent++;
    else if (triggerType === 'DEMAND_REPORT') this.stats.demandReportsSent++;
    else if (triggerType === 'EMERGENCY_REPORT') this.stats.emergencyReportsSent++;

    this.stats.totalDownlinkBytes += report.payloadBytes;
    return report;
  }

  stepTimer(secondsElapsed = 60) {
    if (this.contracts.emergency.active) {
      this.generateADSReport('EMERGENCY_REPORT', 'Emergency 60s burst downlink');
      return;
    }

    if (this.contracts.periodic.enabled) {
      this.contracts.periodic.secondsUntilNext -= secondsElapsed;
      if (this.contracts.periodic.secondsUntilNext <= 0) {
        this.contracts.periodic.secondsUntilNext = this.contracts.periodic.intervalSeconds;
        this.generateADSReport('PERIODIC_REPORT');
      }
    }
  }

  triggerWaypointChange(waypointId) {
    const details = `Waypoint overflight event: ${waypointId}`;
    return this.generateADSReport('EVENT_REPORT', details);
  }

  triggerAltitudeExcursion(deviationFt) {
    this.flightState.altFt = this.flightState.clearedAltFt + deviationFt;
    if (Math.abs(deviationFt) >= this.contracts.event.altitudeRangeThresholdFt) {
      return this.generateADSReport('EVENT_REPORT', `Altitude excursion: ${deviationFt > 0 ? '+' : ''}${deviationFt} ft (Threshold: ±200 ft)`);
    }
    return null;
  }

  triggerLateralDeviation(xtkNm) {
    this.flightState.crossTrackErrorNm = xtkNm;
    if (xtkNm >= this.contracts.event.lateralDeviationThresholdNm) {
      return this.generateADSReport('EVENT_REPORT', `Lateral deviation: ${xtkNm} NM (Threshold: 1.0 NM)`);
    }
    return null;
  }

  triggerEmergency(active = true) {
    this.contracts.emergency.active = active;
    if (active) {
      return this.generateADSReport('EMERGENCY_REPORT', 'MAYDAY Emergency Broadcast Initiated');
    }
    return null;
  }

  generateARINC429BusWords() {
    // ARINC 429 Label 305 (Octal): ADS-C Status, Facility & FOM
    const label305 = 0xC5; // Label 305 representation
    let data305 = 0;

    const facMap = { EGGX: 1, CZQX: 2, KZAK: 3, RJJJ: 4 };
    const facVal = facMap[this.activeFacility] || 0;
    const emergBit = this.contracts.emergency.active ? 1 : 0;
    const periodicBit = this.contracts.periodic.enabled ? 1 : 0;
    const eventBit = this.contracts.event.enabled ? 1 : 0;

    data305 |= (facVal & 0x07) << 10; // Bits 11-13 Facility code
    data305 |= (this.flightState.fom & 0x07) << 13; // Bits 14-16 FOM (0-7)
    data305 |= (emergBit & 0x01) << 16; // Bit 17 Emergency State
    data305 |= (periodicBit & 0x01) << 17; // Bit 18 Periodic Contract Active
    data305 |= (eventBit & 0x01) << 18; // Bit 19 Event Contract Active
    data305 |= 0x03 << 28; // Bits 29-30 SSM (Normal Operation)

    let word305 = (data305 & 0x7FFFFF00) | (label305 & 0xFF);
    word305 = this.applyOddParity(word305);

    // Label 306 (Octal): Time to Next Report (sec) & Event Trigger Code
    const label306 = 0xC6;
    let data306 = 0;
    const secVal = Math.min(1023, Math.max(0, this.contracts.periodic.secondsUntilNext));

    data306 |= (secVal & 0x3FF) << 10; // Bits 11-20: Seconds to next report (0-1023s)
    data306 |= (Math.min(15, this.stats.eventReportsSent) & 0x0F) << 20; // Bits 21-24: Event count
    data306 |= 0x03 << 28; // Bits 29-30 SSM

    let word306 = (data306 & 0x7FFFFF00) | (label306 & 0xFF);
    word306 = this.applyOddParity(word306);

    return {
      label305: { hex: '0x' + (word305 >>> 0).toString(16).toUpperCase().padStart(8, '0'), parityValid: this.verifyOddParity(word305) },
      label306: { hex: '0x' + (word306 >>> 0).toString(16).toUpperCase().padStart(8, '0'), parityValid: this.verifyOddParity(word306) }
    };
  }

  applyOddParity(word32) {
    let bits = word32 & 0x7FFFFFFF;
    let count = 0;
    for (let i = 0; i < 31; i++) {
      if ((bits >> i) & 1) count++;
    }
    if (count % 2 === 0) {
      bits |= (1 << 31);
    }
    return bits >>> 0;
  }

  verifyOddParity(word32) {
    let count = 0;
    for (let i = 0; i < 32; i++) {
      if ((word32 >>> i) & 1) count++;
    }
    return count % 2 === 1;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ARINC745Engine };
}
