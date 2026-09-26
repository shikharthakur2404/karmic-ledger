# KARMIC LEDGER // FUTURE UPDATES & DEVELOPMENT ROADMAP
**Master Engineering Plan: `v2.1.0` to `v2.4.0` // Canonical Reference for Planned Subsystem Upgrades**

---

## 1. System Generational Timeline

```
[CURRENT: v2.0.0] ──► [v2.1.0: SPRINT 2] ──► [v2.2.0: SPRINT 3] ──► [v2.3.0: SPRINT 4] ──► [v2.4.0: SPRINT 5]
• 8 Engines Versioned • Multi-Profession     • Ashtakavarga Damping  • 7-Day Rolling Graph   • ENGINE 09: HELLENISTIC
• Kuro-Washi HUD      • Software/Trades     • Gandanta Voids        • 1-Click Micro-Logger  • Zodiacal Releasing
• Retina Vector SVGs  • Geocoding Cache Exp • N=30 Held-Out Study   • SQLite Calibration    • Dual-Civilization VCS
```

---

## 2. Sprint 2 (`v2.1.0`): Multi-Profession Incident Radar Expansion

### Objective
Expand the 24-Hour Daily Incident Radar from generic bodily/mental alerts to **environment-specific friction vectors** based on the user's active professional exposure.

### Key Milestones
1. **Profession Archetype Enum (`core/daily.py`):**
   * `SOFTWARE_ARCHITECT`: Specialized in logic flaws, concurrency bugs, and deployment failures.
   * `EXECUTIVE_FOUNDER`: Specialized in boardroom resistance, capital overextension, and term-sheet freezes.
   * `TRADES_CONSTRUCTION`: Specialized in mechanical impact, power tool jams, and reflex fatigue.
   * `CREATIVE_MEDIA`: Specialized in aesthetic scope creep, visual dissociation, and creative blocks.
   * `HEALTHCARE_CLINICAL`: Specialized in triage fatigue, circadian desync, and fine-motor tremor.
2. **Specialized Algorithmic Detectors:**
   * **Heisenbug / Silent Logic Corruption:** Ketu-Mercury transits crossing the natal Rahu/Ketu axis.
   * **Production Deployment Crash:** Mars transiting House 8 or aspecting House 10 with afflicted Moon.
   * **Mechanical Impact / Tool Failure:** Mars-Saturn exact opposition or conjunction in House 3 or 6.
3. **Offline Geocoding Database Expansion:**
   * Expand cached Indian city/village catalog from 5,000 to 25,000 regional tehsils, mandals, and taluks in [`core/geocoding.py`](file:///Users/shikharthakur/GitHub/karmic-ledger/core/geocoding.py).

---

## 3. Sprint 3 (`v2.2.0`): Ashtakavarga Damping & Gandanta Void Matrix

### Objective
Eliminate false-alarm variance by grounding raw transit friction into the user's native structural capacity (*Bindu distribution*).

### Key Milestones
1. **Ashtakavarga Damping Math ([`core/ashtakavarga.py`](file:///Users/shikharthakur/GitHub/karmic-ledger/core/ashtakavarga.py)):**
   * Scale raw transit incident scores against sign Sarvashtakavarga (SAV, baseline 28) and Bhinnashtakavarga (BAV, baseline 4):
     $$R_{\text{damped}} = R_{\text{raw}} \times \left(1.0 - \left[\frac{B_{\text{SAV}} - 28}{28} \times 0.50 + \frac{B_{\text{BAV}} - 4}{8} \times 0.50\right]\right)$$
   * Prevents high-bindu houses from over-reporting minor transient friction.
2. **Tīvra Gandanta Boundary Voids:**
   * Flag high-entropy water-to-fire cuspal crossings (Cancer $\rightarrow$ Leo, Scorpio $\rightarrow$ Sagittarius, Pisces $\rightarrow$ Aries) where zero earth/air stabilization exists.
3. **Pre-Registered N=30 Held-Out Empirical Study:**
   * Execute statistical validation test across 30 Astro-Databank "AA" rated profiles quarantined from previous tuning sets, measuring Paired Cohen's $d_z > 1.0$ against Monte Carlo permutation nulls.

---

## 4. Sprint 4 (`v2.3.0`): 7-Day Rolling Incident Horizon & Empirical Micro-Logger

### Objective
Provide forward-looking weekly tactical visibility and close the feedback loop through user-logged lived events.

### Key Milestones
1. **7-Day Rolling Predictive Curve:**
   * Compute rolling 7-day transit trajectory in 6-hour increments, rendering an interactive SVG sparkline on the web HUD.
2. **Interactive 1-Click Micro-Logging Drawer:**
   * Low-friction modal on the HUD: *"Log Today's Micro-Incident"* (takes 5 seconds: select tag [Bug / Stalled Email / Knee Strain / Clear Day] + Severity 1–5).
3. **Calibration Feedback Loop (`incident_logs.db`):**
   * SQLite persistence tracking predicted vector alerts vs. user-confirmed friction.
   * Auto-tighten or loosen orb boundaries (e.g. Mercury Sandhi $1.25^\circ \rightarrow 0.85^\circ$) via gradient adjustment to maximize precision.

---

## 5. Sprint 5 (`v2.4.0`): Engine 09 — Hellenistic Chronometry & Zodiacal Releasing

### Objective
Deploy a complete parallel Western ancient chronometry engine (`core/hellenistic.py`), establishing a **Dual-Civilization Telemetry Stack**.

```
                       [DUAL-CIVILIZATION CONFLUENCE STACK]
                                        │
      ┌─────────────────────────────────┴─────────────────────────────────┐
      ▼                                                                   ▼
[VEDIC ENGINE 02: VIMSHOTTARI]                              [HELLENISTIC ENGINE 09: RELEASING]
Source: Moon Ecliptic Longitude                             Source: Lot of Spirit (Asc + Sun - Moon)
Scale: 120-Year Lunar Nakshatras                            Scale: Sign-by-Sign Planetary Periods
Answers: "What karmic thread is executing?"                 Answers: "When does career peak & reboot?"
      │                                                                   │
      └─────────────────────────────────┬─────────────────────────────────┘
                                        │
                                        ▼
                         [CROSS-TRADITION CONFLUENCE]
          "Both Vimshottari & Zodiacal Releasing converge on Q4 2024
           for international relocation and major architectural launch."
```

### Key Milestones
1. **Planetary Sect Engine (Diurnal vs. Nocturnal Physics):**
   * Determine diurnal status via solar altitude: $h_{\odot} \ge 0^\circ \implies \text{Day Sect}$; $h_{\odot} < 0^\circ \implies \text{Night Sect}$.
   * Identify Team Leaders (Day: Sun, Jupiter, Saturn; Night: Moon, Venus, Mars).
   * Flag the *Malefic Contrary to Sect* (Day: Mars; Night: Saturn) as the primary life stressor.
2. **Hermetic Lots Calculation:**
   * **Lot of Fortune (*Tychē*):** Material circumstances, physical health, and events beyond conscious control.
   * **Lot of Spirit (*Daimon*):** Mind, career trajectory, agency, intellectual output, and architecture.
3. **Zodiacal Releasing (Aphesis from Spirit):**
   * Releasing through sign planetary periods: Aries (15y), Taurus (8y), Gemini (20y), Cancer (25y), Leo (19y), Virgo (20y), Libra (8y), Scorpio (15y), Sagittarius (12y), Capricorn (27y), Aquarius (30y), Pisces (12y).
   * 4-tier fractal subdivision: Level I (Decades) down to Level IV (Days).
4. **Angular Peak & "Loosing of the Helm" Detectors:**
   * **Angular Peak Detector:** Identifies when releasing enters signs angular to Fortune (1st, 10th, 7th, 4th from Fortune), signaling career zenith and peak public prominence.
   * **Loosing of the Helm Alert:** Flags when releasing reaches the boundary limit and jumps to the polar opposite sign, alerting to radical career reboots, sudden identity shifts, or structural life pivots.
5. **Annual Profections & "Lord of the Year" (Chronocrator):**
   * $\text{Active House} = (\text{Age} \pmod{12}) + 1$.
   * Activates the annual time-lord planet to arbitrate solar return transits.
6. **Dual-Tradition Confluence Multiplier:**
   * If both Vedic Vimshottari and Hellenistic Zodiacal Releasing identify the same milestone window, confidence weighting scales from $1.0\times$ to $1.65\times$.

---

### Canonical References
* Comprehensive sub-engine version ledger: [ARCHITECTURE_UPGRADES.md](file:///Users/shikharthakur/GitHub/karmic-ledger/ARCHITECTURE_UPGRADES.md)
* Short-horizon radar specification: [DAILY_INCIDENT_RADAR.md](file:///Users/shikharthakur/GitHub/karmic-ledger/DAILY_INCIDENT_RADAR.md)
* System node topology: [ARCHITECTURE.md](file:///Users/shikharthakur/GitHub/karmic-ledger/ARCHITECTURE.md)
