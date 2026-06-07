# Main Pipeline Runner

## Purpose

The main pipeline runner provides a single entry point for running the Spotify Million Playlist data pipeline.

Instead of running each ingestion and transformation script manually, the full pipeline can be executed with one command.

## Command

```bash
python -m src.main
Pipeline Order
1. Bronze ingestion
2. Silver playlists transformation
3. Silver playlist_tracks transformation
4. Silver tracks transformation
5. Silver artists and albums transformation
6. Gold top_tracks aggregation
7. Gold top_artists and top_albums aggregation
8. Gold playlist_summary aggregation
Main File
src/main.py
Notes

The pipeline currently runs in batch mode and overwrites local Parquet outputs on each execution.

This is acceptable for the current project because the input dataset is static. In a production system, this could be extended with incremental processing, partitioning, and orchestration.