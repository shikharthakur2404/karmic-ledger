"""
karmic-ledger: Engine Version Registry & Subsystem Topology
Canonical registry assigning semantic version numbers (SemVer) to all 8
analytical sub-engines, providing runtime metadata, telemetry boundaries,
and tracking generational Before-vs-After upgrades.
"""

from typing import Any

SYSTEM_VERSION = "2.2.0"

ENGINE_REGISTRY: dict[str, dict[str, Any]] = {
    "engine_01_ephemeris": {
        "engine_id": "01",
        "name": "Swiss Ephemeris & Geocoding Ingestion",
        "version": "1.2.1",
        "status": "STABLE",
        "files": ["core/ephemeris.py", "core/geocoding.py"],
        "description": "High-precision Lahiri sidereal planetary coordinates and intelligent offline/online village geocoder.",
        "before_state": "Manual latitude/longitude decimal entry required; user had to open external map apps or guess coordinates. Ephemeris had unhandled exceptions on extreme latitudes.",
        "after_state": "Geocoding + circumpolar guards; natal planets expose speed_deg_per_day / speed_deg_per_hour (FLG_SPEED) for KL-N30-001 window propagation.",
    },
    "engine_02_chronology": {
        "engine_id": "02",
        "name": "120-Year Vimshottari Chronology Engine",
        "version": "1.3.0",
        "status": "STABLE",
        "files": ["core/dasha.py"],
        "description": "Vimshottari chronology with fixed 365.25-day years and birth-Moon-speed event windows.",
        "before_state": "Civil 365/366 day-of-year scaling (pre-1.2) then mean-Moon 0.55°/h window (1.2.x). Every profile's dasha calendar dates change under 365.25.",
        "after_state": "DASHA_YEAR_DAYS=365.25 for all timelines (production and study). KL-N30-001 window uses birth Moon nakshatra lord + ephemeris Moon speed at birth; math.ceil rounding registered. JH golden-master required before freeze tag.",
    },
    "engine_03_ayurdaya": {
        "engine_id": "03",
        "name": "Ayurdaya & Constitutional Vitality Engine",
        "version": "1.2.0",
        "status": "STABLE",
        "files": ["core/ayurdaya.py"],
        "description": "Classical 3-Pair Parashari Longevity Model with Kendra buffers, Kakshya Vriddhi/Hrasa, and Vitality Quotient (0-100).",
        "before_state": "Fatalistic single-number lifespan estimates or cryptic Sanskrit terms (Alpayu/Madhyayu) without context, risking user anxiety.",
        "after_state": "Non-medical Fun Kundli vitality index (0-100 score), semantic status badges (ROBUST ENDURANCE / BALANCED BASELINE), and plain-English explanatory cards.",
    },
    "engine_04_soul": {
        "engine_id": "04",
        "name": "Soul Antiquity & Ātmakāraka Engine",
        "version": "1.2.0",
        "status": "STABLE",
        "files": ["core/soul.py"],
        "description": "Jaimini Chara Karaka sorting, continuous Antiquity Index (0.0-5.0), and 4-tier visual gauge track.",
        "before_state": "Binary classification or raw decimal score without polarity, leaving users uncertain whether a high score was positive or negative.",
        "after_state": "4-stage interactive visual gauge track (Nascent, Developing, Mature, Transcendent), semantic status pills (ADVANCED MATURITY), and clear archetypal calling descriptions.",
    },
    "engine_05_daily_radar": {
        "engine_id": "05",
        "name": "24-Hour Micro-Transit Incident Radar",
        "version": "1.0.0",
        "status": "ACTIVE_BETA",
        "files": ["core/daily.py", "DAILY_INCIDENT_RADAR.md"],
        "description": "Short-horizon turbulence detector: Chandrāṣṭama, H6 Lagnesha somatic strain, and Mercury Sandhi dead-zones.",
        "before_state": "Zero short-term tactical telemetry. The engine only answered 120-year macro questions, leaving daily sudden disruptions unexplained.",
        "after_state": "Real-time 24-48h turbulence radar flagging Moon 8th-house mental fatigue, H6 joint strain (knees), and Mercury Sandhi communication dead-zones, with multi-profession roadmap.",
    },
    "engine_06_confluence": {
        "engine_id": "06",
        "name": "Confluence & Live Friction Audit Engine",
        "version": "1.2.0",
        "status": "STABLE",
        "files": ["core/confluence.py", "core/frictions.py"],
        "description": "Vedic Correlation Score (VCS) with production and KL-N30-001 study profiles.",
        "before_state": "Single path with Mahadasha 40 + Antardasha 40 + Transit 25 (=105) plus dual-bonus/void heuristics and [15,98] clipping.",
        "after_state": "vcs_profile=production keeps legacy heuristics; vcs_profile=kl_n30_001 uses registered 40+40+20 hard-capped at 100 with whole-sign transit only (no dual bonus, void, or floor-15).",
    },
    "engine_07_adversarial": {
        "engine_id": "07",
        "name": "Adversarial Falsification Battery",
        "version": "1.1.1",
        "status": "STABLE",
        "files": ["core/adversarial.py", "core/battery_runner.py"],
        "description": "Fixed-mutation sensitivity smoke test (+3y, -3y, +6h, 12h inversion).",
        "before_state": "Unfalsifiable astrological claims prone to confirmation bias and subjective validation (Barnum effect).",
        "after_state": "Fixed-mutation sensitivity smoke test only — not a Monte Carlo null and not evidence of predictive validity. Held-out validation is KL-N30-001.",
    },
    "engine_08_visuals": {
        "engine_id": "08",
        "name": "Kuro-Washi Zen Vector Visualizer",
        "version": "2.0.0",
        "status": "STABLE",
        "files": ["core/visuals.py", "templates/index.html", "static/images/"],
        "description": "Retina vector SVG glyphs, Ensō calligraphic watermark, Top 3 Hero Triad, and Observatory Visualizer Lightbox.",
        "before_state": "Monochrome text tables and raw unicode characters without visual hierarchy or aesthetic presence.",
        "after_state": "Kuro-Washi paper aesthetic with gold wireframe reticles, Top 3 Essential Highlights Triad, 9 Graha custom vector SVGs, and Observatory Visualizer Hero Card with lightbox modal.",
    },
    "engine_09_hellenistic": {
        "engine_id": "09",
        "name": "Hellenistic Chronometry & Zodiacal Releasing",
        "version": "1.0.0-planned",
        "status": "PLANNED",
        "files": ["core/hellenistic.py"],
        "description": "Zodiacal Releasing (Aphesis from Spirit), Hermetic Lots (Fortune/Spirit), Planetary Sect physics, and Annual Profections.",
        "before_state": "Single-tradition system reliant strictly on Vedic Nakshatra Dasha clocks without cross-civilizational validation.",
        "after_state": "Dual-civilization chronometry engine combining Indian Vimshottari karmic execution with Alexandrian career peak & narrative pivot detectors.",
    },
    "engine_10_medini": {
        "engine_id": "10",
        "name": "Medini Geopolitical & Mundane Chronometry Engine",
        "version": "1.0.0",
        "status": "STABLE",
        "files": ["core/medini.py"],
        "description": "Macroeconomic, territorial conflict, and geopolitical stress indices using national foundation charts, Gochar angularity, and Vimshottari national timelines.",
        "before_state": "System was strictly micro-natal (individual querents only), with zero capacity to model macro geopolitical cycles, sovereign boundaries, or historical nation crises.",
        "after_state": "Sovereign nation inception database (India 1947, USA 1776), Geopolitical Stress Index (GSI 0-100), automated historical backtesting (1962, 1971, 1999, 2008, 2020), and 2024-2035 forward projection.",
    },
    "engine_11_samskara": {
        "engine_id": "11",
        "name": "Saṃskāra & Karmic Trace Engine (Karma-Trace)",
        "version": "1.0.0",
        "status": "STABLE",
        "files": ["core/samskara.py"],
        "description": "Text-grounded Sanskrit karmic continuity engine based on Yoga Sūtra 3.18, BPHS Pūrva Janma Loka (D3/D60), and UVA DOPS academic case comparison.",
        "before_state": "System had only continuous soul antiquity scores without scriptural verse provenance, Pūrva Janma Loka decanate classification, or Saṃskāra behavioral feature extraction.",
        "after_state": "Auditable 3-layer epistemic karmic trace engine combining deterministic Jyotiṣa (D3 Drekkāṇa Loka, D60, 9th/5th Pūrva Puṇya), Yoga Sūtra 3.18 latent impression profiling, and verifiable scriptural citations.",
    },
}


def get_system_manifest() -> dict[str, Any]:
    """Returns the unified system architecture and engine version manifest."""
    return {
        "system_name": "Karmic Ledger // Fun Kundli",
        "system_version": SYSTEM_VERSION,
        "engine_count": len(ENGINE_REGISTRY),
        "engines": ENGINE_REGISTRY,
    }
