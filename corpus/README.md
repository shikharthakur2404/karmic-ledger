# Sacred / natal rule corpus

Runtime store is **SQLite FTS5** (`corpus/db/shastra.fts.sqlite`), not PDFs.

## What we ingested so far

| Source | Path | Notes |
|---|---|---|
| Existing engine citations | `core/shastra.py` | Tagged `MODERN_PRACTITIONER` until verses are pinned to a named edition |
| BPHS ch. 1–10 (Sanskrit, ITRANS) | `sources/bphs_01_10.itx` | From [sanskritdocuments.org](https://sanskritdocuments.org/) — **personal study / research only**; not for commercial repost without their permission |

## What we deliberately did **not** bulk-download

Modern English / Hindi print editions of BPHS (Ranjan, etc.) on Archive.org are often still under publisher copyright even when a scan is free to browse. We do **not** dump those into the repo. Prefer:

1. Volunteer Sanskrit encodings with explicit study terms  
2. Editions you personally own / license  
3. Rule rows you pin yourself (`edition`, `provenance`)

## Build

```bash
python3 scripts/build_corpus.py
```

## Query

```bash
python3 -c "from core.corpus_store import search_corpus; print(search_corpus('dashA', limit=5))"
```
