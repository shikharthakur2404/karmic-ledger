# Sacred / natal rule corpus

Runtime store is **SQLite FTS5** (`corpus/db/shastra.fts.sqlite`), not PDFs.

## Sources (Sanskrit Documents — study / research terms)

ITRANS packs under `sources/par*.itx` covering BPHS chapter ranges roughly **1–97**:

`par0110`, `par1120`, `par2130`, `par3140`, `par4145`, `par4650`, `par5160`, `par6170`, `par7180`, `par8190`, `par9197`

From [sanskritdocuments.org](https://sanskritdocuments.org/) — **personal study / research only**; not for commercial repost without their permission.

Also: engine citation rows from `core/shastra.py` (tagged `MODERN_PRACTITIONER` until pinned).

## Build

```bash
python3 scripts/build_corpus.py
```

## Query / RAG

```bash
python3 -c "from core.rag import generate_shastra_rag_card; print(generate_shastra_rag_card('maitreya', allow_llm=False)['card'][:400])"
```

UI: Sector 08 on the main page · API: `POST /api/shastra/rag`

## What we do not bulk-commit

Modern copyrighted English/Hindi print editions (even if scanned on Archive.org).
