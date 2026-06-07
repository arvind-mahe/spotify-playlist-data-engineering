# Logging and Error Handling

## Purpose

The pipeline uses a reusable logger to track pipeline execution, step completion, and failures.

Logging helps make the project easier to debug and closer to production-style data engineering workflows.

## Logger File

```text
src/utils/logger.py
Log Output

Logs are written to both:

Console
logs/pipeline_YYYYMMDD.log
Main Pipeline Logging

The main pipeline runner logs each pipeline step:

Bronze ingestion
Silver playlists transformation
Silver playlist_tracks transformation
Silver tracks transformation
Silver artists and albums transformation
Gold top_tracks aggregation
Gold top_artists and top_albums aggregation
Gold playlist_summary aggregation
Error Handling

Each pipeline step is wrapped in a try/except block.

If a step fails, the logger records the error and stops the pipeline.

This prevents later steps from running on incomplete or invalid upstream data.

Run Command
python -m src.main