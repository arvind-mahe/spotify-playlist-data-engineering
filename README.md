# Spotify Million Playlist Data Pipeline

A batch data-engineering pipeline that turns nested Spotify Million Playlist Dataset (MPD) JSON into a
Bronze / Silver / Gold Parquet data lake with PySpark, loads it to AWS S3, and exposes it to SQL through
Athena external tables and the Glue Data Catalog.

> **Scope:** developed and validated on one MPD slice (`mpd.slice.0-999.json`, **1,000 playlists**; the full
> dataset has 1,000,000 playlists across 1,000 slice files). All figures below come from that slice.

## Verified results

| Metric | Value | Evidence |
|---|---|---|
| Playlists | 1,000 | `docs/query_outputs/athena_raw_results/` |
| Playlist-track rows | 67,503 | same |
| Unique tracks / artists / albums | 34,443 / 9,754 / 19,261 | same |
| Avg tracks per playlist | 67.5 (min 5, max 245) | same |
| Raw JSON to Bronze Parquet | 32.54 MB to 3.74 MB (**88.5% smaller**) | `docs/storage_report.md`, `docs/storage_proof.txt` |
| All three layers vs raw JSON | 14.77 MB (**54.6% smaller**) | same |
| Silver / Gold tables | 5 / 4 | `sql/athena_ddl/` |

The 88.5% figure compares raw JSON to the Bronze layer only. Silver and Gold are additional derived copies, so
the whole lake is 54.6% smaller than the raw file. See [`docs/storage_report.md`](docs/storage_report.md).

The Athena outputs were captured during the June 2026 run. They are raw Athena result files (one per query),
so they can be checked against the queries in `sql/analytics_queries/`.

## Architecture

```text
Raw JSON (nested)
   |  PySpark: read, parse, add ingestion metadata
   v
Bronze   playlists (nested tracks kept)                        Parquet
   |  PySpark: flatten + normalize
   v
Silver   playlists, playlist_tracks, tracks, artists, albums   Parquet (5 tables)
   |  PySpark: aggregate
   v
Gold     top_tracks, top_artists, top_albums, playlist_summary Parquet (4 tables)
   |  aws s3 sync
   v
AWS S3  ->  Glue Data Catalog / Athena external tables  ->  SQL analytics
```

| Layer | Grain | Purpose |
|---|---|---|
| Bronze | one row per playlist | Close to source; Parquet for storage and read efficiency |
| Silver | normalized entities plus a `playlist_tracks` bridge table | Clean, queryable model |
| Gold | one row per track / artist / album, plus a dataset summary | Pre-aggregated business metrics |

## Example output (Gold `top_tracks`)

| Track | Artist | Playlists |
|---|---|---|
| HUMBLE. | Kendrick Lamar | 52 |
| One Dance | Drake | 50 |
| Broccoli (feat. Lil Yachty) | DRAM | 49 |
| Closer | The Chainsmokers | 45 |
| Congratulations | Post Malone | 44 |

Most-appearing artist: Drake (202 playlists, 130 unique tracks). Most-appearing album: *Stoney* by Post Malone
(88 playlists).

## Tech stack

Python, PySpark, Parquet, AWS S3, AWS Athena, AWS Glue Data Catalog, SQL. Local development on WSL (Ubuntu).

## Project structure

```text
src/
  ingestion/       bronze_ingestion.py, read_raw_json.py
  transformation/  silver_*.py, gold_*.py
  quality/         validate_bronze.py, validate_silver.py, inspect_raw_schema.py
  utils/           config.py, logger.py, spark_test.py
  main.py          sequential pipeline runner (8 steps)
sql/
  athena_ddl/         create_database.sql, create_silver_tables.sql, create_gold_tables.sql
  analytics_queries/  top_tracks.sql, top_artists.sql, top_albums.sql, playlist_summary.sql, ...
scripts/           storage_proof.sh
docs/              design notes, storage_report.md, storage_proof.txt, query_outputs/athena_raw_results/
```

## Run it locally

Requires Python 3 and Java 11 or 17 (for PySpark).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.utils.spark_test           # confirm Spark works

# put mpd.slice.0-999.json in data/raw/ (Spotify Million Playlist Dataset)
python -m src.main                       # Bronze -> Silver -> Gold, 8 steps
python -m src.quality.validate_bronze
python -m src.quality.validate_silver
```

The runner logs every step to the console and to `logs/pipeline_YYYYMMDD.log`, and stops if a step fails.

### Reproduce the storage measurement

```bash
bash scripts/storage_proof.sh            # writes docs/storage_proof.txt
```

### Load to AWS and query with Athena

```bash
aws s3 sync data/bronze/ s3://<your-bucket>/spotify/bronze/
aws s3 sync data/silver/ s3://<your-bucket>/spotify/silver/
aws s3 sync data/gold/   s3://<your-bucket>/spotify/gold/
```

Then run, in order, `sql/athena_ddl/create_database.sql`, `create_silver_tables.sql`, `create_gold_tables.sql`,
and the queries in `sql/analytics_queries/`. Update the bucket name in `src/utils/config.py` and the DDL files.

## Data quality

- Bronze and Silver validation scripts check non-empty tables, null IDs, and row counts.
- Athena validation queries (`sql/analytics_queries/athena_validation_checks.sql`) cross-check Silver and Gold
  counts; saved results show 1,000 playlists, 67,503 playlist-track rows, and 34,443 Gold top-track rows,
  consistent across layers.

## Known limitations and roadmap

- The validation scripts print PASSED/FAILED but do not raise an error, so they cannot yet stop a run.
- `src/main.py` is a sequential runner, not a scheduler or orchestrator.
- Only one 1,000-playlist slice has been processed.
- The AWS account used for the original deployment is currently suspended; the saved Athena outputs document
  the run.

Planned: fail-loud data-quality checks, Airflow DAG for orchestration, dbt models and tests on the Gold layer,
GitHub Actions CI, and processing additional MPD slices.
