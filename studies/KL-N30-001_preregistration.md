# Karmic Ledger: Pre-Registration, N=30 Held-Out Study

> Fill every remaining `TODO` field, commit, tag, and only then touch held-out data.
> The commit hash of this file is the registration timestamp. Edits after the tag go in section 12 (Deviations), never in place.
>
> **Status note:** `DECIDE` fields below are filled with proposed freeze values grounded in current `main` (`core/*`). Human-only gates remain `TODO`. Status stays **DRAFT** until section 13 is complete and the freeze tag exists.

## 0. Metadata

| Field | Value |
|---|---|
| Study ID | `KL-N30-001` |
| Registered on (UTC) | `TODO` (set to commit UTC at freeze) |
| Registration commit / tag | `TODO` → tag `study/KL-N30-001-prereg` |
| Engine freeze tag | `TODO` → tag `study/KL-N30-001-engine-freeze` (see section 4) |
| Analyst | `TODO` |
| Event extractor (must differ from analyst, or be blind to chart outputs) | `TODO` |
| Status | **DRAFT** |

**Statement:** No held-out chart has been computed, scored, or viewed by anyone involved in rule design before the freeze tag.

**Order of operations (do not reorder):**

1. Commit this file as **DRAFT** (no tag) — design history before any held-out data.
2. Land VCS cap + dasha-year patches with tests; tag `study/KL-N30-001-engine-freeze`.
3. Clear Astro-Databank terms gate (section 2).
4. Clear remaining `TODO`s that do not require held-out data; commit + tag `study/KL-N30-001-prereg`; **only then** draw the cohort with the registered seed.
5. Blind event extraction → hash event file → paste registry + `swe.version`.
6. Score once.

**Pre-freeze code changes required (must land on the engine-freeze tag, not after):**

1. Normalize VCS component caps to sum to 100 (section 5): Mahadasha 40 + Antardasha 40 + Transit 20. Drop dual-bonus and void-multiplier from the primary path (see section 5). Current `core/confluence.py` uses 40+40+25 with +12 dual bonus and ×0.55 void.
2. Freeze Vimshottari year length to **365.25 days** (section 4). Current `core/dasha.py` uses civil 365/366 via day-of-year. Add a golden-master test against Jagannatha Hora reference boundaries (section 4).
3. Pre-scoring **discrimination audit** (section 5): confirm the primary score has non-trivial spread on random dates under classical-only rules; abort freeze if nearly flat.
4. Scoring entrypoint `studies/kl_n30_001/score_heldout.py` must exist and pin all section-4 settings.

## 1. Hypotheses

- **H1 (primary, one only):** Mean subject-level excess VCS at eligible life-event dates (real chart, real events, window in section 5) is greater than zero relative to the matched random-date null (null model 1), and this excess is not reproduced by the wrong-chart control (null model 3).
- **H0:** Real-chart scores at event dates are indistinguishable from the null distributions in section 6.
- **Exploratory (not tested, descriptive only):**
  - Per-domain breakdown (marriage, childbirth, career start/end, relocation, parental bereavement)
  - Per-component contribution (MD / AD / transit)
  - Discrimination margin under random-chart offsets (null model 2) as a sensitivity diagnostic, not a success criterion
  - Time-to-flip flags (section 7) prevalence

Prior note: the published literature (e.g. Carlson, *Nature* 1985) makes a null outcome the expected result. A null is reported with the same prominence as a positive.

## 2. Cohort

| Item | Rule |
|---|---|
| Source | Astro-Databank, Rodden rating **AA** only |
| Terms-of-use gate | **Must be ticked before extraction:** [ ] terms read, [ ] permission obtained or use confirmed allowed, [ ] storage and redistribution rules recorded here: `TODO` (paste Astro-Databank license URL + allowed uses; if redistribution of birth data is forbidden, publish only hashed IDs + aggregate stats) |
| Sampling frame | All Astro-Databank AA entries with: (a) birthplace coordinates resolvable, (b) birth time present to the minute, (c) ≥ 4 dated public events of eligible types (section 3), (d) birth year in **1800–1975** inclusive (enough adult lifespan for career/marriage/bereavement events; avoids minors-heavy contemporary entries), (e) not in the exclusion list below |
| Selection | Random draw without replacement from the frame, seed `0x4B4C4E30` (`KLN0`), performed by script `studies/kl_n30_001/select_cohort.py`, output list hash `TODO` (SHA-256 of sorted subject IDs file) |
| N | 30 |
| Excluded | Any subject used in rule design, tuning, or earlier benchmarks — including all of `benchmarks/cohort/` (`01_indira_gandhi` … `15_synthetic_beta`), `benchmarks/historical_indira_gandhi.json`, and any profile under `profiles/` used for UI demos; subjects with missing or ambiguous birthplace; duplicates; Rodden A/B/C/DD/X |
| Time-zone / DST handling | Single documented rule: IANA tzdata version `TODO` (record `tzdata` package / OS zoneinfo version on freeze machine); convert civil local birth time → UT via zone history for that place. Historical LMT (pre-zone adoption) and wartime DST handled by Astro-Databank’s stated zone when present; if missing, use `timezonefinder` + IANA for the coordinates at the birth date. Manual overrides allowed only with a source citation, logged in section 12 |
| Replacement policy | If a drawn subject fails inclusion (terms, missing day-precision events, unresolved TZ), take the next from the seeded list, and log the failure reason in `studies/kl_n30_001/cohort_replacements.log` |

**Power (fill before freeze):** Run `studies/kl_n30_001/power_sim.py` over a range of effect sizes and register the **minimum detectable effect (MDE) as a finding**, not as an assumed plausible effect.

- Unit of analysis: subject (N=30). Paired excess-VCS vs random-date null.
- Two-sided α = 0.05. Report power at \(d_z \in \{0.2, 0.3, 0.5, 0.8\}\) under the empirical null variance from section 6 (pilot on excluded tuning cohort or synthetic charts — **not** held-out AA subjects).
- **Analytic detection floor (not an effect-size claim):** a paired test at N=30, α=0.05, 80% power detects about \(d_z \approx 0.53\). That number describes what the design can see, not what astrology should produce. Do not treat it as the registered MDE.
- **Registered MDE:** `TODO` (output of `power_sim.py`). If only large effects are detectable, say so explicitly in the report: N=30 is underpowered for small/medium effects; a null is unsurprising.

## 3. Events

- **Eligible types (closed list):**
  1. `MARRIAGE` — civil or religious marriage ceremony date (not engagement, not cohabitation)
  2. `CHILDBIRTH` — birth of a child of the native (first or any; date of birth)
  3. `CAREER_START` — first assumption of a major named office, first professional appointment, company founding with a dated public record
  4. `CAREER_END` — loss of that office, resignation, firing, electoral defeat ending the role
  5. `RELOCATION_ABROAD` — permanent move across an international border (departure or arrival date; pick the one with a primary record; document which)
  6. `PARENT_BEREAVEMENT` — death of a parent
- **Excluded types:** health events of the native; assassination/own death; vague events ("rose to fame", "became successful"); engagement/romance; incarceration; anything without a day-precision date; month-only or year-only dates
- **Source rule:** date supported by ≥ 2 independent published sources, **or** one primary record (civil registry, official gazette, autobiography with explicit date). URLs/citations stored in the event file.
- **Cap:** max **5** events per subject (if more eligible, keep the chronologically earliest 5 after applying the closed list; log dropped events)
- **Extraction:** done blind to chart outputs; event file `studies/kl_n30_001/events.jsonl`; file hash `TODO` (SHA-256); the file is frozen before any scoring
- **Date precision:** day. Month-only dates are excluded, not rounded
- **Domain mapping for VCS:** extractor labels use the closed list above; `classify_event_domain` in `core/confluence.py` is **not** used for primary scoring (keyword classifier is too loose). Mapping table is fixed in `studies/kl_n30_001/domain_map.py` at freeze

## 4. Engine Freeze

All computation uses one tagged commit. Fill registry paste at freeze from `python -c "from core.registry import get_system_manifest; …"`.

| Setting | Value |
|---|---|
| Git tag | `TODO` (`study/KL-N30-001-engine-freeze`) |
| Engine versions | **Snapshot at draft time (re-paste at freeze):** system `2.2.0`; 01 ephemeris `1.2.0`; 02 chronology `1.1.0`; 03 ayurdaya `1.2.0`; 04 soul `1.2.0`; 05 daily `1.0.0` (**excluded from primary score**); 06 confluence `1.1.0` (**primary**); 07 adversarial `1.1.0` (**not used as null**); 08 visuals `2.0.0` (N/A); 09 hellenistic `1.0.0-planned` (**excluded**); 10 medini `1.0.0` (**excluded**); 11 samskara `1.0.0` (**excluded**) |
| Ayanamsha | Lahiri (`swe.SIDM_LAHIRI`) |
| Node | **true** (`swe.TRUE_NODE`; Ketu = Rahu + 180°) |
| House system | **Whole Sign** (house = sign count from Lagna; `swe.houses_ex(..., b"W", …)` for Asc only) |
| Dasha year length | **365.25 days** (must be implemented before freeze; replaces current civil 365/366 approximation in `core/dasha.py`) |
| Chara Karaka scheme | **7** (Sun–Saturn only; Rahu excluded). Note: Soul Antiquity weights are **not** in the primary score |
| Ephemeris files | Swiss Ephemeris via `pyswisseph` binding version **2.10.03** at draft; confirm SE file path and reject Moshier fallback (`FLG_SWIEPH` required; abort if ephemeris file missing). Freeze value: `TODO` (re-check `swe.version` + installed `*.se1` path on freeze machine) |
| Dasha golden-master | After the 365.25 patch: compare Mahadasha/Antardasha boundary dates for **4–5 reference charts** against **Jagannatha Hora** exports you produce yourself (same Lahiri, true node, 365.25-year setting). Store expected boundaries in `tests/fixtures/jh_vimshottari_golden.json`. **Do not** fill expected dates from this engine’s own output (circular). Until `populated: true` and ≥4 charts are present, the JH test skips and the engine-freeze tag must not be cut. |

Any bug fix after the freeze is a deviation (section 12). The study is re-run from scratch on the fixed tag.

## 5. Score and Hit Definition

- **VCS formula (primary):** Mahadasha **40** + Antardasha **40** + Transit **20** = **100**. No other additives.
  - Internal point awards inside MD/AD keep current structure (ownership / placement / aspect / karaka / sambandha) but are capped at 40 each.
  - Transit Saturn+Jupiter contribution capped at **20** (was 25).
  - **Hard cap only:** \(\mathrm{VCS} = \mathrm{round}(\min(\mathrm{md}+\mathrm{ad}+\mathrm{transit},\,100),\,1)\). No production floor of 15 and no ceiling of 98 on the study path (those compress variance).
  - Dasha error sentinel: force score **0.0** (was 5.0) so failures do not inflate the floor.
- **Excluded from primary (explicit):** the following stay in production code if desired, but are **off** for `KL-N30-001` primary scoring and must not be re-enabled post-hoc:
  | Rule ID | Current behaviour | Provenance | Study use |
  |---|---|---|---|
  | `VCS.MOD.DUAL_DASHA_BONUS` | +12 (draft had proposed +10) | `ORIGINAL_HEURISTIC` — no pinned verse | Excluded (would push raw total above 100) |
  | `VCS.MOD.PRIMARY_VOID` | ×0.55, cap 38 | `ORIGINAL_HEURISTIC` — no pinned verse | Excluded |
  | `VCS.MOD.FLOOR_15` / `VCS.MOD.CEIL_98` | clip to [15, 98] | `ORIGINAL_HEURISTIC` | Excluded on study path |
- **Components included in the primary score:**
  - **Included (rule IDs):**
    - `VCS.MD.OWN_PRIMARY` / `VCS.MD.OWN_SECONDARY` / `VCS.MD.OCCUPY_PRIMARY` / `VCS.MD.ASPECT_PRIMARY` / `VCS.MD.KARAKA`
    - `VCS.AD.*` (same structure) + `VCS.AD.SAMBANDHA_MD`
    - `VCS.TR.SATURN_PRIMARY` / `VCS.TR.JUPITER_PRIMARY`
  - **Transit sub-options for primary:** whole-sign house hit only (orb weight = 1.0 if transit/aspect house matches primary domain houses, else 0). **Pada-orb ladder and SAV bindu multiplier are `MODERN_PRACTITIONER` and are excluded from primary** (they remain available for secondary endpoint 2’s contrast / exploratory rescore — secondary #2 is redefined as “full modern transit weighting on” vs this classical primary).
  - **Provenance tags for primary block:** house-lordship, dasha lord evaluation, and whole-sign gochar house contact = `CLASSICAL` technique with `MODERN_PRACTITIONER` numeric point tables (24/14/9/… awards are not verse-literal). Point tables stay frozen as implemented at the engine-freeze tag.
  - **Also excluded from primary:**
    - `DOUBLE_TRANSIT` (`MODERN_PRACTITIONER`)
    - Mercury-sandhi daily detectors (`ORIGINAL_HEURISTIC`)
    - Soul Antiquity index & weights (`ORIGINAL_HEURISTIC`)
    - Any `1.65×` Hellenistic confluence multiplier (not implemented; remains excluded)
    - Numerology / Mulank / Bhagyank
    - Daily Radar, Medini, Saṃskāra, Ayurdaya vitality
- **Discrimination audit (pre-scoring, before freeze tag):** **This audit runs only on the excluded tuning cohort and/or synthetic charts. It must never be run on, tuned against, or informed by the held-out AA cohort.** Score ≥ 500 random dates per chart under the primary formula. Record SD and IQR of VCS. **Abort freeze** if SD < 5.0 points or if ≥ 80% of mass sits in a single 5-point bin — a near-flat classical score makes the study underpowered by design. Audit output hash: `TODO`.
- **Window (per subject, formula — not a free parameter):** For subject \(i\) with birth-nakshatra lord \(L\) and Mahadasha span \(Y_L\) years,
  \[
  w_i = \left\lceil\, t_{\mathrm{AA}} \cdot Y_L \cdot 365.25 \cdot \frac{0.55/60}{360/27}\,\right\rceil
  \]
  days, where \(t_{\mathrm{AA}} = 2\) (section 7). An event on civil date \(D\) (birth timezone) is scored if any calendar day in \([D - w_i,\ D + w_i]\) is evaluated; the study uses the **max VCS inside that window** (same rule for all subjects). Implemented by `core.dasha.event_window_half_width_days`.
  - **Computed consequence of the AA assumption (locked before any held-out score):** Moon ≈ 0.55°/h ⇒ ≈ 0.00917°/min. One minute of birth-time error shifts the Vimshottari balance by \(Y_L \times 365.25 \times (0.00917 / 13.\overline{3})\) days ≈ **1.5–5 days/min** by lord. With \(t_{\mathrm{AA}}=2\), \(w_i\) is therefore about **±3 to ±10 days** (Ketu/Mars/Sun at the low end; Venus/Saturn/Rahu/Mercury at the high end). A flat ±3 would under-cover long-lord charts; the formula removes that free parameter. Half/double of \(w_i\) are sensitivity only (section 9) and must not replace \(w_i\) after seeing scores.
  - Approximate table at \(t_{\mathrm{AA}}=2\) (ceil): Ketu/Mars 4; Sun 3; Moon 5; Rahu 9; Jupiter 8; Saturn 9; Mercury 8; Venus 10.
- **Primary statistic (subject level):** For subject \(i\) with \(n_i\) events,
  \[
  \Delta_i = \overline{\mathrm{VCS}}_{i,\mathrm{events}} - \overline{\mathrm{VCS}}_{i,\mathrm{random\ dates}}
  \]
  where the random-date mean is the mean over the null sets’ per-set means (null model 1). Cohort primary statistic: \(\bar\Delta = \frac{1}{30}\sum_i \Delta_i\). Subject is the unit of analysis; events are clustered within subjects.
- **No post-hoc rule selection:** the rule set is fixed at section 4.

## 6. Null Models (all three are run; seeds fixed)

1. **Random-date null.** For each subject, **2,000** sets of random dates (same count as the subject's events) drawn uniformly from the subject's life span \([ \mathrm{birth}+16\mathrm{y},\ \min(\mathrm{death\ or\ 2020{-}12{-}31}) ]\), scored with the real chart. Tests whether event dates are special.
2. **Random-chart (offset) null.** For each subject, **2,000** perturbed charts: birth **date** offset uniform on \([-5\,\mathrm{y},\,+5\,\mathrm{y}]\) excluding \([-30,\,+30]\) days (avoid near-identical charts); birth **time** offset uniform on \([0,\,86400)\) seconds. Scored against the real events. Tests dependence on the exact inputs. The four fixed mutations in `core/adversarial.py` are **not** part of the null.
3. **Wrong-chart control.** Each subject's events scored against every other subject's chart (all 29 others). Plus **20,000** cohort-level permutations that re-assign entire charts to event-sets without replacement.

Seeds:

| Stream | Seed |
|---|---|
| Cohort selection | `0x4B4C4E30` |
| Random-date null | `0x4B4C4E31` |
| Random-chart null | `0x4B4C4E32` |
| Wrong-chart permutations | `0x4B4C4E33` |
| Bootstrap CI (section 8) | `0x4B4C4E34` |

All nulls use the identical scoring script and window.

## 7. Birth-Time Uncertainty Policy

- AA rating means time certified to the minute. Uncertainty used: **± 2 min** (allows 1-minute certification plus 1-minute transcription/clock error).
- Dasha boundary uncertainty is propagated: ~1.5–5 days per minute (depends on the birth-nakshatra lord). With ±2 min, Antardasha boundaries carry roughly ±3–10 days; Pratyantardasha is not used in the primary score.
- Pratyantardasha-level (or finer) hits are **out of scope** for primary scoring (score stops at Antardasha + transit). If any exploratory PD layer is added later, it counts only if the boundary is further from the event than the propagated uncertainty.
- Report time-to-flip for Lagna sign, Moon nakshatra and Atmakaraka (7-planet) per subject at ±1 min steps out to ±30 min. Subjects whose Lagna flips within ±2 min are flagged `LAGNA_UNSTABLE`. They stay in the primary analysis, and are dropped in the sensitivity analysis.

## 8. Primary Endpoint and Decision Rule

- **Primary test:** One-sided-in-spirit but **two-sided** permutation test of \(\bar\Delta\) against the subject-level permutation distribution formed by sign-flipping / null-draw re-centring under null model 1 (10,000 permutations, seed `0x4B4C4E34`), α = 0.05. (Two-sided because either systematic anti-correlation or correlation is scientifically informative; “Supported” still requires positive direction.)
- **Effect size:** mean \(\bar\Delta\) with 95% CI from a subject-level bootstrap (≥ 10,000 resamples, seed `0x4B4C4E34`).
- **Supported** if p < 0.05 **and** the CI lower bound > 0 **and** the wrong-chart control does not reproduce the effect (wrong-chart mean excess CI includes values ≥ the real-chart \(\bar\Delta\), or wrong-chart \(\bar\Delta_{wrong}\) is within 50% of real \(\bar\Delta\) with overlapping CIs — exact predicate: real \(\bar\Delta\) exceeds the 97.5th percentile of the wrong-chart permutation distribution). **Otherwise: null.**
- **Secondary endpoints** (max **2**, Holm-corrected):
  1. Mean discrimination margin under random-chart null (null model 2): real baseline VCS vs mean offset-chart VCS at the same events
  2. Modern-transit rescore: primary formula **plus** Pada-orb ladder and SAV bindu multiplier (still no dual-bonus / void / floor-15)

Everything else is exploratory.

## 9. Sensitivity Analyses (pre-declared, not decision-bearing)

- Drop flagged subjects (`LAGNA_UNSTABLE`, section 7)
- Re-enable `VCS.MOD.DUAL_DASHA_BONUS` (+10) and/or `VCS.MOD.PRIMARY_VOID` (×0.55) with hard cap 100 — exploratory only; tagged `ORIGINAL_HEURISTIC`
- Window \(\pm \lceil w_i/2\rceil\) and \(\pm 2w_i\) (half / double of the per-subject formula width)
- Leave-one-subject-out
- Alternative dasha year length: **360-day** Savana year (recompute timelines only; same weights)

## 10. Analysis Plan and Stop Rules

- Scores computed **once**, by script `studies/kl_n30_001/score_heldout.py` at the freeze tag, with output hash recorded (`studies/kl_n30_001/outputs/primary.json` SHA-256 → `TODO`).
- No interim looks and no peeking at partial scores. The analyst does not see per-subject results before the analysis script is final.
- Permitted pre-scoring stops: data error discovered in cohort or events (log it, fix, restart from section 2 with the same seed).
- No stopping or extending on the basis of results. N stays 30.

## 11. Reporting Commitments

- Report all of sections 6, 8 and 9 outputs, positive or null.
- Publish the cohort IDs, event file, scripts, tags and hashes (subject to the section 2 terms gate).
- UI and README wording follows the result. A null means "no evidence the engine predicts event timing" language, not "sensitivity verified".
- Engine 07 changelog / registry `after_state` must be rewritten to drop “Monte Carlo” / “proving … discriminative separation” claims unless this study’s Supported criteria are met. Until then, describe Engine 07 as a **fixed-mutation sensitivity smoke test**, not a validation.

## 12. Deviations Log

| Date | Section | What changed | Why | Impact |
|---|---|---|---|---|
| | | | | |

## 13. Sign-Off Checklist

- [ ] Terms gate (section 2) ticked
- [ ] VCS weights sum to 100; dual-bonus / void / floor-15 **off** on study path
- [ ] Dasha year length frozen to 365.25 in code
- [ ] Jagannatha Hora golden-master test green
- [ ] Discrimination audit passed (SD ≥ 5.0; hash recorded)
- [ ] Power simulation recorded; MDE registered as a finding
- [ ] All `TODO` cleared (except those that require post-score hashes)
- [ ] Event file extracted blind and hashed
- [ ] Engine freeze tag created, registry output pasted
- [ ] DRAFT committed untagged first; prereg tag only after terms + freeze + pre-cohort TODOs
- [ ] Cohort drawn **after** prereg tag
- [ ] Analyst ≠ event extractor (or extractor attested blind)
- [ ] Engine 07 public wording downgraded pending result (section 11)
