# Storage report

Measured locally (WSL Ubuntu) on the 1,000-playlist slice behind the Athena results in
`docs/query_outputs/athena_raw_results/`. Raw evidence: `docs/storage_proof.txt`.

| Layer | Size | vs raw JSON |
|---|---|---|
| Raw JSON (`mpd.slice.0-999.json`, 34,119,368 bytes) | 32.54 MB | baseline |
| Bronze (Parquet) | 3.74 MB | **88.5% smaller** |
| Silver (5 tables, Parquet) | 6.28 MB | 80.7% smaller |
| Gold (4 tables, Parquet) | 4.75 MB | 85.4% smaller |
| **All three layers combined** | **14.77 MB** | **54.6% smaller** |

The 88.5% figure is the format change from raw nested JSON to Bronze Parquet. Silver and Gold are additional
derived copies, so storing every layer saves 54.6% versus the raw JSON. Always state which comparison a number
refers to.

Reproduce: `bash scripts/storage_proof.sh`
