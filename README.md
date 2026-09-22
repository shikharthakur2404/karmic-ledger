# 🪐 Karmic Ledger
 
> **Analytical Jyotish Telemetry, Classical Sastra Retrieval, & Algorithmic Sensitivity Engine**
 
`karmic-ledger` is an analytical platform that calculates sidereal planetary coordinates, compiles Vimshottari dasha cycles, tests biographical milestone alignment against classical double-transit rules, and retrieves verified verses from ancient Sanskrit texts (*Brihat Parashara Hora Shastra*, *Phaladeepika*, *Saravali*) to generate manuscript-grade karmic dossiers.
 
---
 
## Architecture Overview
 
```
karmic-ledger/
├── core/
│   ├── ephemeris.py       # Swiss Ephemeris sidereal Lahiri calculations
│   ├── dasha.py           # Vimshottari Mahadasha / Antardasha / Pratyantardasha compiler
│   ├── transits.py        # Double-Transit (Jupiter + Saturn) event backtesting engine
│   ├── ashtakavarga.py    # Classical BPHS Sarvashtakavarga & Bhinna Ashtakavarga matrix
│   ├── confluence.py      # Confluence scoring with ±3°20' Navamsha Pada orb lock
│   ├── numerology.py      # Mulank, Bhagyank, and composite axis calculator
│   └── correlation.py     # Vedic Correlation Score (VCS) generator
├── data/
│   ├── classics/          # Vectorized classical Sanskrit texts with shloka citations
│   │   ├── bphs/          # Brihat Parashara Hora Shastra
│   │   ├── phaladeepika/  # Phaladeepika
│   │   └── saravali/      # Saravali
│   └── history/           # Historical timelines & geopolitical datasets (1900–2026)
├── templates/             # Swiss Grid Minimal HTML/CSS templates
├── THEME.md               # Swiss Grid Minimal UI prompt & design system specification
├── profiles/              # Local private profiles (strictly gitignored, zero PII tracked)
│   └── example_anonymous.json
├── benchmarks/            # Public historical & synthetic benchmark datasets (15 cohorts)
│   └── results/           # Adversarial stress-test logs & performance gap analysis
└── tests/                 # Unit tests for astronomical precision & transit alignment
```
 
---
 
## Core Principles
 
1. **Epistemic Primacy & Ground Truth:** Stated human biographical facts are ground truth; astrological rules are symbolic heuristics. The engine tests internal mathematical consistency, not physical celestial causation (acknowledging Carlson, *Nature*, 1985).
2. **No Fortune-Cookie Boilerplate:** Every planetary interpretation cites its source verse (e.g. `[BPHS 24:14]`).
3. **Parametric Sensitivity Testing:** Verifies engine sensitivity through adversarial input perturbation (+3Y, -3Y, +6H, 12H inversion), confirming that corrupted inputs collapse heuristic scores rather than generating confirmation bias.
4. **Swiss Grid Minimal Aesthetic:** Zero decorative clutter, 1px architectural gridlines, pure white background, and a single Swiss Red accent (`#eb0028`).
5. **Zero-PII Local Architecture:** All private subject profiles remain local and quarantined from version control.

