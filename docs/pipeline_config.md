# Pipeline Configuration

## Purpose

This project uses a central configuration file to store local and S3 data paths.

Configuration file:

```text
src/utils/config.py
Why This Is Useful

Centralized configuration avoids hardcoding file paths across multiple pipeline scripts.

If a local folder or S3 bucket changes, the path can be updated once in config.py.

Local Paths
RAW_DATA_PATH
BRONZE_PLAYLISTS_PATH
SILVER_PLAYLISTS_PATH
SILVER_PLAYLIST_TRACKS_PATH
SILVER_TRACKS_PATH
SILVER_ARTISTS_PATH
SILVER_ALBUMS_PATH
GOLD_TOP_TRACKS_PATH
GOLD_TOP_ARTISTS_PATH
GOLD_TOP_ALBUMS_PATH
GOLD_PLAYLIST_SUMMARY_PATH
S3 Paths
S3_BUCKET
S3_BASE_PATH
S3_RAW_PATH
S3_BRONZE_PATH
S3_SILVER_PATH
S3_GOLD_PATH
Current S3 Bucket
s3://spotify-million-playlist-data-lake-arvind-2026/

---

# 7. Update README

Add this section after the Week 3 / Athena section:

```markdown
## Pipeline Configuration

Project paths are centralized in:

```text
src/utils/config.py

This file stores local paths and S3 paths for Raw, Bronze, Silver, and Gold layers.

This makes the pipeline easier to maintain because data paths are not hardcoded repeatedly across every script.