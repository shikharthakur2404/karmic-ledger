# Karmic Ledger: Architecture & Epistemic Upgrades

This document serves as the historical record of structural improvements made to the Karmic Ledger engine. The overarching engineering philosophy applied here was **"Structural over Cosmetic"** — fixing flaws in the data model, validation layers, and algorithmic core rather than patching UI text or relying on legal Terms of Service disclaimers.

## 1. Epistemic Hygiene & The "Real-World Claim" Purge
The engine initially functioned as an unconstrained oracle, capable of outputting literal, fatalistic claims (e.g., "visa cancellation," "job loss," "divorce") to living users.
*   **Symbolic Abstraction:** All 12 House definitions and planetary frictions were rewritten to output abstract, psychological strain indices (e.g., `H12_RAHU_DISPERSION`, `H10_SATURN_TRANSIT_TENSION`).
*   **Domain Interceptor:** Downstream rendering pipelines (like `primer.py`) were sanitized to prevent abstract tags from being re-translated into concrete real-world claims on the UI.
*   **Scientific Modesty:** Introduced baseline disclaimers explicitly citing the Carlson (1985) *Nature* study, defining the engine as a "heuristic sensitivity index" rather than a deterministic predictive model.

## 2. Consent Gating & The Historical Allowlist
Certain classical astrological combinations evaluate biological mortality (Maraka) and legal incarceration (Bandhana). Exposing these on living individuals without out-of-band consent poses severe epistemic and ethical risks.
*   **Domain Quarantine:** `MORTALITY_CRISIS` and `INCARCERATION_OR_BANDHANA` were hard-locked in `core/confluence.py`.
*   **Strict Allowlist:** Instead of a self-declared `is_historical_benchmark` flag (which could be trivially spoofed), the system now uses a hardcoded, immutable allowlist of deceased historical figures (e.g., Indira Gandhi, Abraham Lincoln).
*   **Graceful Remapping:** If a living profile triggers these algorithms, the domains are safely remapped to `TRANSFORMATIVE_CROSSING_WINDOW` and `STRUCTURAL_CONFINEMENT_OR_DISCIPLINE` to evaluate psychological resilience instead of physical outcomes.

## 3. Data Integrity & Input Robustness
Garbage input previously led to either server crashes (500 errors) or, worse, "garbage-in-looks-valid-out" silent assumptions.
*   **Pydantic API Bounds:** Enforced strict mathematical bounds on geography (Latitudes `-90.0` to `90.0`) and caught calendar edge cases (e.g., Leap Year errors like Feb 29 vs Feb 30) returning clean `422 Unprocessable Entity` rejections.
*   **Ephemeris Crash Protection:** Added protective `try/except` wrappers around the `pyswisseph` integration. If the Swiss Ephemeris mathematically fails (e.g., circumpolar ecliptic misses), it safely degrades instead of panicking the runtime.
*   **No Silent Guessing:** If a birth time is missing, the engine gracefully falls back to a `"12:00:00"` noon chart—but injects a strict `"birth_time_confidence": "unknown_defaulted"` flag. This flag cascades through the pipeline, explicitly suppressing Lagna (Ascendant) and House-dependent claims, preventing the engine from asserting confidence on guessed data.

## 4. Live Telemetry Stream Optimization
The WebSocket-based live transit dashboard originally computed full ephemeris updates every 2 seconds, which was computationally wasteful and prone to memory leaks upon client disconnect.
*   **Cost-Sane Polling:** Shifted the backend payload generation to a 60-second sleep loop, offloading the granular "ticking" to a cosmetic JavaScript interval on the frontend to maintain the CRT aesthetic cheaply.
*   **Leak Prevention:** Wrapped the WebSocket daemon in `WebSocketDisconnect` and `asyncio.CancelledError` catches to cleanly kill zombie tasks when a user closes the browser tab.

## 5. Birth Time Rectification & The "Winner's Curse" Trap
Built a mathematically constrained Birth Time Rectification module (`POST /api/rectify`).
*   **Minimum Milestone Floor:** Hard-crashes if fed fewer than 5 verified life events.
*   **Time-Window Clustering:** Returns probability windows (e.g., `18:30 - 21:10`) rather than a single hallucinated "exact minute".
*   **Anti-Noise / Multi-Hypothesis Defense:** Through rigorous adversarial testing, we proved that feeding vague milestones (like "Saw a cloud") artificially inflated scores due to broad hit-boxes, and that scanning 288 daily slots guarantees a false-positive local maximum (the Winner's Curse). We structurally blocked vague milestones (`GENERAL_SIGNIFICANT_EVENT`), demanding strict categorized domains (Marriage, Relocation, etc.) before the engine is legally allowed to compute a baseline.
*   **Empirical Suspension & False Precision:** Further statistical analysis revealed that the Z-score separation between true historical data and randomized noise was ~0.04 SD. The 288 scanning slots are heavily autocorrelated into ~12 effective independent draws (the Lagnas). Thus, a peak Z-score of ~2.2 is the expected mathematical maximum of the null distribution, meaning the engine currently possesses zero proven discriminative power. 
*   **Action Taken:** The feature is formally suspended ("Insufficient evidence"). Additionally, the false precision of returning minute-level time windows has been purged; the output granularity is now honestly restricted to the implied Lagna block (e.g., "Capricorn Ascendant") pending a large-scale (N=30) separation study.
*   **Data Contamination & Held-Out Set Requirement:** The upcoming separation study (N=30) must be run on an entirely *held-out* test set. Profiles like Indira Gandhi, Abraham Lincoln, Winston Churchill, and Nelson Mandela were used to historically tune the `confluence.py` scoring weights. Evaluating them in the separation study would measure training error, not generalization error, causing a contaminated go/no-go threshold. All tuning benchmarks will be strictly isolated to an "in-sample" column.
*   **Payload Anti-Leakage:** To prevent false precision and UX contradiction (where decimal scores override text disclaimers in human perception), the Rectification API is now hard-blocked by default. It returns an empty candidate list and `FEATURE_SUSPENDED_PENDING_VALIDATION` unless a `debug=true` flag is explicitly passed for internal iteration.

## 6. Pre-Registered Validation Study Design (Pending)
To prevent second-order data contamination (tuning the study design to fit the desired output), the empirical separation study for the Rectification Engine is pre-registered below. 

*   **The Unseen Corpus (N=30):** The dataset will consist of 30 documented historical figures exclusively from the Astro-Databank "AA" rated archive (birth times confirmed via birth certificate). **Exclusion Rule:** Any figure previously used to manually tune or eyeball the `confluence.py` engine (Gandhi, Lincoln, Churchill, Mandela) is strictly excluded and quarantined to an "in-sample" tracking column.
*   **Milestone Selection & The Muhurta Exclusion:** We use the first 5 chronological life events from the figure's Wikipedia intro that map to strict domains. **Crucial Exclusion (Circularity Risk):** Events subject to deliberate cultural timing (e.g., weddings, coronations) are strictly excluded in favor of exogenous events (sudden job loss, illness, bereavement). 
    *   *Procedural Resolution:* If a chronological event is blacklisted, skip to the next qualifying event in strict chronological order; never skip backward or select non-adjacent events.
    *   *Corpus Substitution:* If a figure yields fewer than 5 qualifying events from the Wikipedia intro, expand to the full article in chronological order; if still fewer than 5, exclude the figure and replace with the next name on the pre-registered corpus list, logged as a substitution.
*   **Success Threshold (The "Clears Zero" Mark):** The statistical bar is locked as follows:
    *   **Stabilized Null Formulation:** The "Fake Dates" score for each figure cannot be a single noisy random draw. It must be generated as the median peak VCS over 50 repeated random date permutations per figure, stabilizing the null side of the comparison.
    *   **Effect Size:** A **Paired Cohen's $d_z$ > 1.0** (true-vs-stabilized-random computed *within* the exact same figure and milestone mix, eliminating between-figure variance).
    *   **Null Baseline:** The median True Z-score must exceed **+3.0**, computed explicitly against the empirical permutation null distribution (Monte Carlo simulated for that specific N and domain-mix bucket).
    *   **Binary Verdict Protocol:** Outcome is strictly logged as **PASS** or **FAIL**. Any result missing either threshold (e.g., $d_z = 0.92$ or $Z = 2.8$) is an unqualified **FAIL**. Zero qualitative reframing ("promising separation", "trend toward significance") is permitted; on FAIL, the feature stays permanently parked.
