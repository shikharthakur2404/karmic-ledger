"""
karmic-ledger: Engine Version Registry & Subsystem Topology
Canonical registry assigning semantic version numbers (SemVer) to all 8
analytical sub-engines, providing runtime metadata, telemetry boundaries,
and tracking generational Before-vs-After upgrades.
"""

from typing import Any

SYSTEM_VERSION = "2.0.0"

ENGINE_REGISTRY: dict[str, dict[str, Any]] = {
    "engine_01_ephemeris": {
        "engine_id": "01",
        "name": "Swiss Ephemeris & Geocoding Ingestion",
        "version": "1.2.0",
        "status": "STABLE",
        "files": ["core/ephemeris.py", "core/geocoding.py"],
        "description": "High-precision Lahiri sidereal planetary coordinates and intelligent offline/online village geocoder.",
        "before_state": "Manual latitude/longitude decimal entry required; user had to open external map apps or guess coordinates. Ephemeris had unhandled exceptions on extreme latitudes.",
        "after_state": "Single search box with smart debounce auto-geocoding (Photon/Nominatim + 5,000+ cached Indian cities/villages). Circumpolar error protection and topocentric refraction correction.",
    },
    "engine_02_chronology": {
        "engine_id": "02",
        "name": "120-Year Vimshottari Chronology Engine",
        "version": "1.1.0",
        "status": "STABLE",
        "files": ["core/dasha.py"],
        "description": "Fractal 3-tier Mahadasha/Antardasha life chapter timeline with age reticle.",
        "before_state": "Text-only dasha printouts with static lists. No visual timeline or proportional representation of planetary period spans.",
        "after_state": "Dynamic Zen Paper SVG Mahadasha timeline with millimeter-accurate current-age needle, duration tooltips, and fractal Antardasha milestone lookup.",
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
        "version": "1.1.0",
        "status": "STABLE",
        "files": ["core/confluence.py", "core/frictions.py"],
        "description": "Vedic Correlation Score (VCS 0-100), Saturn 10th-aspect stoppage transit, and Sade Sati shocks.",
        "before_state": "Fragmented astrological rules firing independently without cross-validation, generating conflicting predictions.",
        "after_state": "Synthesized Confluence Scoring (VCS) weighting Mahadasha (40 pts), Antardasha (40 pts), and Gochar Transits (25 pts) with double-transit activation rules.",
    },
    "engine_07_adversarial": {
        "engine_id": "07",
        "name": "Adversarial Falsification Battery",
        "version": "1.1.0",
        "status": "STABLE",
        "files": ["core/adversarial.py", "core/battery_runner.py"],
        "description": "Data corruption suite (+3y date shift, 6h lagna rotation, 12h polarity inversion) for empirical sensitivity verification.",
        "before_state": "Unfalsifiable astrological claims prone to confirmation bias and subjective validation (Barnum effect).",
        "after_state": "Automated Monte Carlo perturbation testing proving +25.7% discriminative separation between authentic birth data and scrambled noise on historical benchmarks.",
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
}


def get_system_manifest() -> dict[str, Any]:
    """Returns the unified system architecture and engine version manifest."""
    return {
        "system_name": "Karmic Ledger // Fun Kundli",
        "system_version": SYSTEM_VERSION,
        "engine_count": len(ENGINE_REGISTRY),
        "engines": ENGINE_REGISTRY,
    }
