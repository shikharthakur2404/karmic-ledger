# EMPIRICAL ADVERSARIAL FALSIFICATION REPORT & ARCHITECTURAL GAP AUDIT

> **Diagnostic Target:** Parashari Astrological Confluence Engine (`karmic-ledger`)  
> **Execution Epoch:** `2026-09-21T12:40:18.311529`  
> **Benchmark Scale:** 15 Historical Profiles // 165 Total Simulations // 11 Adversarial Perturbation Vectors  

---

## 1. Executive Telemetry Summary

```text
OVERALL FALSIFICATION PASS RATE:  26.1% (43/165)
COHORT RESILIENCE SCORE:          0/15 Subjects Fully Ground-Truth Locked
MEAN BASELINE GROUND TRUTH VCS:   62.9%
MEAN CORRUPTED VCS:               56.6%
AVERAGE DISCRIMINATION MARGIN:    +6.3% (Δ)
TOTAL DETECTED COLLUSIONS:        42 / 165 (25.5%)
```

---

## 2. Cohort Subject Performance Matrix

| Subject ID | Profile Name | Baseline VCS | Mean Corrupted VCS | Margin (Δ) | Pass Rate | Collusions | Engine Verdict |
|---|---|---|---|---|---|---|---|
| `01_indira_gandhi` | Indira Gandhi (Historical Benchmark) | **74.0%** | 59.0% | **+15.0%** | 6/11 | 3 | *VULNERABLE* |
| `02_abraham_lincoln` | Abraham Lincoln (Historical Benchmark) | **80.6%** | 60.8% | **+19.8%** | 6/11 | 5 | *VULNERABLE* |
| `03_queen_elizabeth_ii` | Queen Elizabeth II (Historical Benchmark) | **72.5%** | 56.0% | **+16.5%** | 7/11 | 3 | *VULNERABLE* |
| `04_albert_einstein` | Albert Einstein (Historical Benchmark) | **47.6%** | 54.1% | **+-6.5%** | 0/11 | 1 | *VULNERABLE* |
| `05_mahatma_gandhi` | Mahatma Gandhi (Historical Benchmark) | **51.1%** | 50.8% | **+0.3%** | 0/11 | 0 | *VULNERABLE* |
| `06_steve_jobs` | Steve Jobs (Historical Benchmark) | **70.3%** | 57.6% | **+12.7%** | 5/11 | 4 | *VULNERABLE* |
| `07_john_f_kennedy` | John F. Kennedy (Historical Benchmark) | **50.9%** | 51.8% | **+-0.9%** | 0/11 | 0 | *VULNERABLE* |
| `08_martin_luther_king` | Martin Luther King Jr. (Historical Benchmark) | **61.3%** | 59.3% | **+2.0%** | 1/11 | 4 | *VULNERABLE* |
| `09_winston_churchill` | Winston Churchill (Historical Benchmark) | **40.1%** | 42.5% | **+-2.4%** | 0/11 | 0 | *VULNERABLE* |
| `10_nelson_mandela` | Nelson Mandela (Historical Benchmark) | **51.8%** | 50.3% | **+1.5%** | 0/11 | 1 | *VULNERABLE* |
| `11_marie_curie` | Marie Curie (Historical Benchmark) | **60.6%** | 62.3% | **+-1.7%** | 1/11 | 5 | *VULNERABLE* |
| `12_franklin_d_roosevelt` | Franklin D. Roosevelt (Historical Benchmark) | **62.4%** | 59.6% | **+2.8%** | 1/11 | 3 | *VULNERABLE* |
| `13_swami_vivekananda` | Swami Vivekananda (Historical Benchmark) | **84.3%** | 68.4% | **+15.9%** | 7/11 | 7 | *VULNERABLE* |
| `14_synthetic_alpha` | Synthetic Subject Alpha (De-Identified Archetype) | **73.3%** | 55.3% | **+18.0%** | 7/11 | 3 | *VULNERABLE* |
| `15_synthetic_beta` | Synthetic Subject Beta (De-Identified Archetype) | **62.6%** | 60.5% | **+2.1%** | 2/11 | 3 | *VULNERABLE* |

---

## 3. Degradation Gradient by Mutation Vector

| Mutation Vector | Category | Mean Corrupted VCS | Mean Drop (Δ) | Pass Rate | Collusion Rate |
|---|---|---|---|---|---|
| `JITTER_PLUS_15M` (Micro Cusp Jitter (+15 Min)) | temporal_jitter | 60.5% | **-2.4%** | 1/15 (6.7%) | 6/15 (40.0%) |
| `JITTER_MINUS_15M` (Micro Cusp Jitter (-15 Min)) | temporal_jitter | 62.9% | **--0.0%** | 0/15 (0.0%) | 8/15 (53.3%) |
| `SHIFT_PLUS_2H` (Lagna Advance (+2 Hours)) | bhava_rotation | 53.7% | **-9.2%** | 5/15 (33.3%) | 3/15 (20.0%) |
| `SHIFT_MINUS_2H` (Lagna Regression (-2 Hours)) | bhava_rotation | 56.1% | **-6.8%** | 4/15 (26.7%) | 2/15 (13.3%) |
| `LAGNA_ROTATION_6H` (Bhavachakra Scramble (+6 Hours)) | bhava_rotation | 53.4% | **-9.5%** | 6/15 (40.0%) | 3/15 (20.0%) |
| `INVERSION_12H` (Polarity Inversion (12-Hour AM/PM Flip)) | diurnal_inversion | 56.3% | **-6.6%** | 6/15 (40.0%) | 2/15 (13.3%) |
| `DESYNC_PLUS_1Y` (Dasha Desynchronization (+1 Year)) | dasha_desync | 52.7% | **-10.2%** | 4/15 (26.7%) | 4/15 (26.7%) |
| `DESYNC_PLUS_3Y` (Severe Dasha Desynchronization (+3 Years)) | dasha_desync | 56.0% | **-6.9%** | 5/15 (33.3%) | 2/15 (13.3%) |
| `DESYNC_MINUS_3Y` (Severe Dasha Desynchronization (-3 Years)) | dasha_desync | 56.3% | **-6.6%** | 5/15 (33.3%) | 4/15 (26.7%) |
| `GEO_DRIFT_ARBITRARY` (Hemispheric Geo-Drift (+35° Lat, -75° Lon)) | geographic_distortion | 53.5% | **-9.4%** | 6/15 (40.0%) | 3/15 (20.0%) |
| `SCRAMBLED_EVENT_DATES` (Milestone Chronology Inversion (Fake Events)) | event_scramble | 60.7% | **-2.2%** | 1/15 (6.7%) | 5/15 (33.3%) |

---

## 4. Deep-Dive Failure Modes & Identified Vulnerabilities

### A. The Micro-Jitter Insensitivity Gap (±15 Minutes)
Across several charts, shifting birth time by only **±15 minutes** produces very mild degradation (Δ: 5% to 12%).
- **Root Cause:** The engine currently evaluates D-1 (Rashi) house positions, where a sign spans ~2 hours. If a ±15m shift does not cross the Ascendant border (e.g. middle of Gemini 19°), the D-1 houses remain completely unchanged!
- **Vulnerability:** Birth time precision cannot be validated down to the exact minute using D-1 alone.
- **Remedy:** Integrate **Navamsha (D-9)** and **Shashtiamsha (D-60)** harmonic division check into the confluence engine. D-9 shifts every 13°20' (~50 mins) and D-60 shifts every 30 arcminutes (~2 minutes).

### B. Collusion Risks & Broad Transit Overlap (False Positives)
A total of **42 collusion instances** were detected where a corrupted chart still scored $\ge 65\%$ VCS.
- **Root Cause:** Saturn and Jupiter Gochar (transits) stay in a single sign for 2.5 years and 1 year respectively. The current transit scoring awards up to 25 points based simply on transit house lordship or 3rd/7th/10th aspect.
- **Vulnerability:** When a birth chart is rotated by +2 hours, transit Saturn and Jupiter may still casually aspect a secondary house, giving free points to a falsified chart.
- **Remedy:** Multiply Gochar transit scores by the **Ashtakavarga Bindu strength** of the transit sign, and require transit triggers to be orb-locked within $\pm 3°$ rather than whole-sign broad aspect.

### C. Natural Karaka Dilution
- **Root Cause:** In `core/confluence.py`, if an active Dasha lord is a natural Karaka (e.g., Sun for power, Saturn for death, Venus for marriage), it receives +6 points even if its natal house position and house ownership are completely irrelevant.
- **Vulnerability:** In desynchronized charts, landing on Sun during an election event still grabs partial credit purely on archetypal name match.
- **Remedy:** Karaka bonus must be conditioned on house rulership or sambandha; an unconnected natural Karaka in a Dusthana (6, 8, 12) should receive a penalty rather than a bonus.

---

## 5. Concrete Engineering Improvement Roadmap

1. **Node 1 (`core/confluence.py`): Implement Orb-Based Degree Confluence**
   - Replace categorical whole-sign transit scoring with exact planetary orb proximity (within 3°20' Navamsha Pada).
2. **Node 2 (`core/dasha.py`): Integrate Pratyantardasha (Sub-Sub Period)**
   - Current resolution stops at Mahadasha-Antardasha (~months to years). Integrating Level 3 Pratyantardasha (~days to weeks) will instantly penalize any temporal shift $> 1$ week.
3. **Node 3 (`core/varga.py`): Add D-9 Navamsha and D-10 Dashamsha Validation**
   - Cross-verify career elevations against D-10 and marriages against D-9 to eliminate ±15m micro-jitter indifference.
4. **Node 4 (`core/ashtakavarga.py`): Samudaya Ashtakavarga Multiplier**
   - Weight house activations by Sarvashtakavarga bindu counts (points < 25 reduce score; points > 30 amplify).
