# Sacred Corpus Vision (Apauruṣeya-first)

> Intent note linked from the Everything vault:  
> `/Users/shikharthakur/Desktop/Everything/vedic-mantras-and-epistemology.md`

## Goal

Build Kundli interpretation from **chart astronomy + classical / traditionally attributed śāstra**, stored for fast local fetch (JSON / SQLite FTS), **not** from developer biography, demo JSON profiles, or generic Barnum text.

## Source priority (epistemic)

1. **Apauruṣeya / Śruti layer** — Veda Saṃhitās as heard tradition (Rishis as *draṣṭā*, not authors). Example seer lineage named in the vault note: Maharishi Vasiṣṭha (e.g. RV 7.59.12).
2. **Hora / Jyotiṣa layer used for natal charts** — primarily texts traditionally attributed to Parāśara and Jaimini (and later digests). Note: historians treat sage attributions as traditional; natal technique is **not** mainly from Yoga Vāsiṣṭha (philosophy) or ritual-calendar Vedāṅga Jyotiṣa alone.
3. **Commentarial / practitioner heuristics** — allowed only if tagged `COMMENTARIAL` / `MODERN_PRACTITIONER` / `ORIGINAL_HEURISTIC` and never silently mixed into “classical” claims.

## Storage shape (planned)

- One row/doc per **rule** or **verse fragment**: Sanskrit, pinned edition, provenance tag, base rate, engine IDs that may cite it.
- Fast path: SQLite FTS5 or JSONL + hash index (not PDF page scans at query time).
- PDFs/Word are **ingest sources**, not the runtime store.

## Hard product rule

Demo profiles (Shikhar, friends, historical benchmarks) are for **calibration UI only**. Live readings must never inherit their affinities, milestones, or narrative defaults.

## Status

- Bias fix for Engine 11 personal defaults: done (`core/samskara.py` v1.1.0).
- Local FTS corpus started: `corpus/` + `core/corpus_store.py` (SQLite FTS5).
  - 10 engine citations + **324** BPHS ch.1–10 Sanskrit verses from sanskritdocuments.org ITX.
  - Rebuild: `python3 scripts/build_corpus.py`
- RAG slice v1: `core/rag.py` + `POST /api/shastra/rag` (FTS retrieve → grounded card; optional Gemini paraphrase, never invents verses).
- Full remaining chapters / Jaimini / UI plain-language pass: next.
