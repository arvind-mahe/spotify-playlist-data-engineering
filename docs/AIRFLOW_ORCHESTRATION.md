# Spotify Analytics Pipeline — Airflow Orchestration

## Overview
Implemented Apache Airflow orchestration to automate a
Spotify data engineering pipeline using PySpark, dbt, and DuckDB.

## Pipeline Architecture

Spotify JSON
    |
    v
PySpark Bronze → Silver → Gold
    |
    v
dbt SQL Transformations
    |
    v
Automated Data Quality Tests
    |
    v
Validated Analytics Outputs

## Airflow DAG Tasks

1. validate_input
   - Confirms Spotify JSON exists.
   - Validates playlist and track counts.

2. run_pyspark
   - Executes the Bronze-Silver-Gold pipeline.
   - Produces Parquet datasets.

3. run_dbt
   - Executes dbt models.
   - Runs automated SQL data-quality tests.

4. verify_outputs
   - Verifies Silver Parquet outputs.
   - Reports dataset metrics.

## Verified Results

- 1,000 Spotify playlists processed
- 67,503 track occurrences
- 34,443 unique tracks
- 9,754 unique artists
- 19,261 unique albums
- 3 dbt SQL models built successfully
- 8 dbt data-quality tests passed
- 4 Airflow tasks completed successfully

## Engineering Practices

- DAG-based workflow orchestration
- Task dependencies
- Automatic retries
- Failure propagation
- Automated data-quality validation
- Reproducible analytical transformations

## Future Enhancements

- Incremental data ingestion
- Scheduled execution
- Failure notifications
- Additional data-quality tests
