# 🪐 KARMIC LEDGER // DEVELOPMENT & SYSTEM REFERENCE MANUAL
### *Analytical Jyotish Telemetry, Algorithmic Sensitivity Engine, & Classical Sastra Retrieval*

> **Current Epoch:** 2026-09-21 // Production Build  
> **Repository:** `karmic-ledger`  
> **Status:** Active Daemon running at `http://127.0.0.1:8080`  
> **Primary Active Theme:** CRT Retro Terminal (Green Phosphor on Cathode Black)  
> **Epistemic Standard:** Ground-Truth Fact Primacy (Carlson, *Nature*, 1985)

---

## 1. Executive Directive & Epistemic Boundaries

### The Foundational Rule of Primacy
* **Stated human biographical facts are ground truth.**
* **Astrological rules are symbolic heuristics and pattern-matching models.**
* The engine makes **zero physical celestial causation claims** and asserts **no real-world facts** (no unprompted declarations of job loss, visa revocation, medical conditions, or marital delays).
* Evaluation metrics measure **internal algorithmic sensitivity to input parameter perturbations** (testing that corrupted inputs collapse heuristic scores rather than generating confirmation bias), not proof of cosmic determinism.

---

## 2. Codebase Architecture & File Registry

```
karmic-ledger/
├── core/
│   ├── ephemeris.py        # Swiss Ephemeris (pyswisseph) Lahiri sidereal calculations
│   ├── dasha.py            # 120-Year Vimshottari Mahadasha / Antardasha / Pratyantardasha compiler
│   ├── ashtakavarga.py     # Classical BPHS Sarvashtakavarga (SAV) & Bhinna Ashtakavarga (BAV)
│   ├── confluence.py       # Confluence scoring engine with ±3°20' Navamsha Pada orb lock
│   ├── consent.py          # Subject Consent & Privacy Enforcement Gate (Mandatory pre-flight check)
│   ├── transits.py         # Real-time planetary transits & double-transit aspect evaluator
│   ├── frictions.py        # Symbolic transit strain indices (Option B: zero real-world assertions)
│   ├── soul.py             # Jaimini Ātmakāraka, Soul Antiquity Index (0.0–5.0), 7 Archetypes
│   ├── adversarial.py      # 4-vector adversarial stress test harness (sensitivity engine)
│   ├── battery_runner.py   # 15-profile x 11-corruption cohort evaluation battery (165 runs)
│   ├── visuals.py          # Vector SVG Diamond Kundli & Vimshottari Dasha progress bar
│   ├── verifier.py         # Profile milestone backtester & VCS generator
│   ├── shastra.py          # Classical Sanskrit rule lookup (BPHS, Phaladeepika, Saravali)
│   ├── primer.py           # Systems-architecture plain-English planet placement translator
│   └── mantras.py          # Classical remedial Upayas (Sastra Shanti) mapped to active dasha
├── benchmarks/
│   ├── historical_indira_gandhi.json   # Public historical benchmark (Ground Truth baseline)
│   ├── cohort/                         # 15 de-identified public/synthetic calibration cases
│   ├── results/                        # Adversarial simulation evaluations & summary logs
│   │   ├── cohort_adversarial_summary.json
│   │   └── PERFORMANCE_GAP_REPORT.md  # 3-gap architectural audit
│   └── generate_cohort.py             # Benchmark generator script
├── templates/
│   └── index.html          # Interactive CRT Retro Terminal UI (BIOS boot, scanlines, CRT flicker)
├── profiles/               # Local sovereign profile storage (STRICTLY GITIGNORED // ZERO PII)
│   ├── example_anonymous.json         # Consented de-identified synthetic archetype
│   └── .unconsented_quarantine/       # Quarantined unconsented profiles (execution_locked: true)
├── main.py                 # CLI execution entrypoint
├── server.py               # FastAPI web server and REST API
├── THEME.md                # Multi-theme design system catalog (CRT, Swiss, Observatory, Vedic)
├── PROJECT_MANIFESTO.md    # Philosophical & architectural core principles
├── ARCHITECTURE.md         # Mermaid topology graph & node hardening matrix
└── DEVELOPMENT.md          # Comprehensive development manual (this document)
```

---

## 3. Core Engine Mechanics & Algorithms

### A. Ephemeris & Coordinate Precision (`core/ephemeris.py`)
* Computes exact topocentric and sidereal positions via `pyswisseph` utilizing the **Lahiri Ayanamsha** (`SE_SIDM_LAHIRI`).
* Calculates exact degree progress across 27 Nakshatras and 108 Nakshatra Padas (3°20' per pada).
* Houses calculated under Whole Sign and Equal House systems with strict timezone offset parsing (`timezone_offset` parameter from birth data, replacing legacy hardcoded offsets).

### B. Classical Ashtakavarga Engine (`core/ashtakavarga.py`)
* Computes complete **Bhinna Ashtakavarga (BAV)** for 7 planets (Sun through Saturn) and Lagna across all 12 signs following *Brihat Parashara Hora Shastra* (Ch. 66–72).
* Calculates cumulative **Sarvashtakavarga (SAV)** point distribution per house (theoretical max 337 bindus, average 28 per house).
* Provides dynamic transit multipliers (`get_ashtakavarga_house_multiplier`):
  * $< 25$ Bindus: $0.65\times$ attenuation (transit lacks structural support).
  * $25 - 31$ Bindus: $1.00\times$ nominal baseline.
  * $\ge 32$ Bindus: $1.20\times$ amplification (transit operating in high-receptivity zone).

### C. Confluence Engine, Orb Lock & Safety Interceptor (`core/confluence.py`)
* **$\pm 3^\circ 20'$ Navamsha Pada Orb Lock**: Transit Saturn and Jupiter scores scale continuously as a function of proximity to target natal degrees:
  $$\text{Orb Multiplier} = \max\left(0.15, 1.0 - \frac{\Delta^\circ}{3.333^\circ} \times 0.85\right) \quad \text{for } \Delta^\circ \le 3.333^\circ$$
  Drops to $0.15\times$ outside the pada boundary, eliminating multi-year false positives.
* **Aspectual Primary Mandate (Drishti Crediting)**: Mahadasha and Antardasha lords receive full primary status if they cast classical Parashari aspects on house significators (resolving false negatives for historical charts like Churchill and Mandela).
* **Mortality & Incarceration Hard-Lock**:
  * `MORTALITY_CRISIS` (Maraka timing) and `INCARCERATION_OR_BANDHANA` (jail) are **strictly confined to closed retrospective historical validation archives** (`is_historical_benchmark=True`, e.g. Lincoln, Gandhi).
  * For all live, current, or unverified subjects (`is_historical_benchmark=False`), mortality keywords are intercepted and re-mapped to `TRANSFORMATIVE_CROSSING_WINDOW`, and imprisonment keywords are re-mapped to `STRUCTURAL_CONFINEMENT_OR_DISCIPLINE` (abstract endurance/discipline). Zero mortality or incarceration scoring touches a living individual.

### D. Symbolic Transit Strain Indices (`core/frictions.py` — Option B)
Strictly purged of all concrete real-world diagnoses. Computes abstract geometric friction indices:
1. `H10_SATURN_TRANSIT_TENSION`: *Structural Vocational Re-evaluation & Accountability Phase* (Saturnian transit over vocational axis).
2. `H12_RAHU_DISPERSION`: *Foreign-Domain Adaptation & Boundary Fluidity Theme* (Nodal transit across unfamiliar territory).
3. `LUNAR_SATURN_PRESSURE_CYCLE`: *Psychological Maturation, Introspection & Endurance Theme* (Sade Sati / Janma Shani).
4. `H4_DOMESTIC_RESTRUCTURING_CYCLE`: *Domestic Foundation & Spatial Recalibration Theme* (Internal roots and sanctuary).
5. `H8_TRANSIT_INTENSITY_WINDOW`: *Deep Introspection & Unforeseen Variable Management Theme* (Navigating complexity).
6. `H7_RELATIONAL_TRANSIT_FRICTION`: *Commitment Boundary Testing & Relational Restructuring Theme* (Interpersonal contract re-evaluation).
7. **Astronomical Cycle Horizons**: Outputs purely celestial sign/ingress dates (e.g. *Rahu transit over H12 concludes: January 2027*).

### E. Adversarial Sensitivity Engine (`core/adversarial.py`)
Applies deliberate data corruption to measure heuristic discrimination:
1. `SHIFT_PLUS_3Y`: Shifts birth year $+3$ years ($+1,095$ days Dasha desync).
2. `SHIFT_MINUS_3Y`: Shifts birth year $-3$ years.
3. `LAGNA_ROTATION_6H`: Advances birth time $+6$ hours ($90^\circ$ Bhavachakra scramble).
4. `INVERSION_12H`: Reverses diurnal/nocturnal hemisphere ($180^\circ$ Bhavachakra flip).
* **Verdict Metric**: `INPUT_DISCRIMINATING // HEURISTIC_SENSITIVE` when mean discrimination margin $\Delta \ge 20\%$.

---

## 4. UI System & Themes (`THEME.md` & `templates/index.html`)

### Active Theme: CRT Retro Terminal
* **Cathode Ray Aesthetic**: Deep phosphor black (`#030803`), intense P31 green phosphor (`#00ff66` / `#33ff77`), glowing amber reticles (`#ffb000`), and crimson alerts (`#ff3333`).
* **Hardware Emulations**:
  * **Scanlines Raster Overlay**: Fixed repeating linear gradient simulating phosphor scanlines.
  * **Curvature Vignette**: Radial barrel distortion vignette with cathode edge dropoff.
  * **Phosphor Flicker**: Subtle 140ms CSS `@keyframes crt-flicker` animation.
  * **Boot-Sequence Intro**: Animated BIOS POST sequence typing memory checks, Swiss Ephemeris subsystem mounting, and shastra matrix initialization with instant-skip on click/keypress.
  * **Terminal Cursor**: Monospace typography (`Share Tech Mono`, `VT323`) with blinking `_` / `█` cursor.
* **Vector Graphics (`core/visuals.py`)**:
  * `generate_diamond_kundli_svg`: Procedural North Indian Kundli in glowing phosphor green with amber focal reticle on `#040a04` cathode canvas.
  * `generate_dasha_progress_bar_svg`: Segmented phosphor timeline with glowing amber `[T+ {age}Y]` cursor beam.

### Cataloged Backup Themes (Specifications in `THEME.md`):
* **Swiss Grid Minimal**: Architectural 1px black grid, RAL 9016 pure white canvas, single Swiss Red accent (`#eb0028`), zero rounded corners.
* **Observatory Dark Mode**: Deep navy (`#030712`), celestial cyan (`#38bdf8`), interactive parallax starfield canvas with constellation connect.
* **Vedic Temple Carving**: Sandstone relief, bas-relief borders, deep maroon/gold palette, chisel-cut serif typography.

---

## 5. Security, Subject Consent & Zero-PII Quarantine Protocol

1. **Mandatory Subject Consent Gate (`core/consent.py`)**:
   * Prior to ingesting any local profile for backtesting or telemetry, `verify_subject_consent` inspects the record for explicit affirmative consent (`"subject_consent": {"status": "EXPLICIT_CONSENT_GRANTED"}`).
   * Profiles lacking verified consent are immediately halted with `PROCESSING_HALTED // CONSENT_GATE_LOCKED`. The engine refuses to process or evaluate private persons without verified authorization.
2. **Quarantine of Unconsented Private Profiles**:
   * All unconsented private records are relocated to `profiles/.unconsented_quarantine/` with `"execution_locked": true`.
   * Active profiles in `profiles/` are replaced with locked tombstones, preventing unauthorized automated evaluation.
3. **Public Historical Benchmarks & De-Identified Synthetic Archetypes**:
   * The public REST API (`/api/demo/{name}`) strictly serves public retrospective historical records (`indira`) or synthetic de-identified calibration cases (`anonymous`).
   * Mortality crisis and incarceration domains are hard-locked strictly to deceased historical benchmarks.
4. **Copy & Translation Hygiene (`core/primer.py` & `core/reporter.py`)**:
   * Downstream reporting modules are purged of concrete real-world claims (no assertions of visa loss, job termination, or relationship status).
   * All reports include explicit scholarly methodology notes citing Carlson (*Nature*, 1985), defining metrics as symbolic heuristic alignment rather than physical celestial determinism.
5. **`.gitignore` Isolation**: The directory `profiles/` and all private cohort data are strictly quarantined and gitignored.

---

## 6. Execution & Testing Runbook

### Starting the Server Daemon
```bash
# From workspace root:
.venv/bin/uvicorn server:app --host 127.0.0.1 --port 8080 --reload
```

### Running Adversarial Falsification on Historical Baseline
```bash
.venv/bin/python -c '
from core.adversarial import run_adversarial_stress_test
res = run_adversarial_stress_test("benchmarks/historical_indira_gandhi.json")
print("Baseline VCS:", res["baseline_vcs"])
print("Corrupted VCS:", res["average_corrupted_vcs"])
print("Discrimination Margin:", res["discrimination_margin"])
print("Verdict:", res["resilience_verdict"])
'
```

### Running Full 15-Cohort Evaluation Battery (165 Simulations)
```bash
.venv/bin/python core/battery_runner.py
```

### Testing Ephemeris & Confluence Integrity
```bash
.venv/bin/python -c '
from datetime import datetime
from core.ephemeris import compute_natal_chart
from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.transits import get_planet_transit_positions
from core.frictions import audit_live_frictions

natal = compute_natal_chart(1917, 11, 19, 23, 11, 0, 25.4358, 81.8463, tz_offset_hours=5.5)
timeline = compute_vimshottari_timeline(datetime(1917, 11, 19, 23, 11), natal["planets"]["Moon"]["nakshatra"]["lord"], natal["planets"]["Moon"]["nakshatra"]["fraction_elapsed"])
frictions = audit_live_frictions(natal, timeline)
print("Frictions Status:", frictions["status"])
print("Active Strain Indices:", len(frictions["active_strain_indices"]))
'
```

---

## 7. Known Improvement Areas & Engineering Roadmap

1. **Micro-Jitter Sensitivity Gap ($\pm 15$ min)**:
   * Whole-sign D-1 houses remain static over $30^\circ$ ($\approx 2$ hours).
   * **Fix**: Ingest Divisional Charts **D-9 (Navamsha, shifts every ~50 min)** and **D-60 (Shashtiamsha, shifts every ~2 min)** into the scoring matrix.
2. **Layer-3 Vector Shastra RAG**:
   * Migrate curated dictionary in `core/shastra.py` to SQLite + ChromaDB embeddings covering the complete Sanskrit text of *BPHS* (2,000+ verses), *Jaimini Upadesha Sutras*, and *Saravali*.
3. **Divisional Chart Graphics**:
   * Add modular SVG generators for South Indian box charts and East Indian charts alongside the North Indian Diamond chart.

---

## 8. Name Telemetry, Forward Namakaran, & Numerology Firewalls

If name-derived telemetry is introduced into Karmic Ledger, it is bound by three structural firewalls:

### A. Directionality Lock (Forward Namakaran Only)
* **Ephemeris to Syllable ($\text{Chart} \to \text{Phoneme}$):** Classical *Namakaran* maps the Moon's natal Nakshatra-pada ($27 \times 4 = 108$ padas) forward to a traditional starting syllable.
* **Invertibility Barred ($\text{Name} \not\to \text{Chart}$):** The engine strictly forbids reverse-engineering birth coordinates, Moon signs, or Lagna from names. Phonetic collision, modern chosen names, and regional conventions break mathematical invertibility.

### B. Metric Quarantine (Numerology Decoupling)
* **Firewall from VCS & $\Delta$:** Divinatory letter-to-number heuristics (Chaldean/Pythagorean) are completely decoupled from the astronomical ephemeris. They are strictly barred from contaminating the Vedic Correlation Score (VCS), perturbation margins ($\Delta$), or transit strain indices.
* **Isolated Container:** If surfaced, numerology must sit in an independent, explicitly labeled heuristic container.

### C. Epistemic Claim Suppression & Deficit-Framing Guardrail
* **Zero Outcome Claims:** Strict ban on "lucky numbers", "name destiny", or deterministic outcome assertions.
* **Non-Judgment Framing (Deficit-Framing Firewall):** Mandatory disclosure:
  > *"Naming conventions vary widely by region, era, and family tradition — this shows the classical prescription only, not a judgment on your actual name."*
  Bars framing any mismatch between a querent's actual name and their Moon Nakshatra-pada syllable as an energetic deficit, spiritual misalignment, or karmic defect.

