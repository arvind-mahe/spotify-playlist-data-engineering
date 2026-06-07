# Week 3 Review — Gold Layer, S3, and Athena

## Week 3 Goal

The goal of Week 3 was to build business-ready Gold analytics tables, upload the data lake outputs to AWS S3, and create Athena external tables for SQL-based analytics.

---

## Completed Work

### 1. Gold Layer Design

Gold design document:

```text
docs/gold_layer_design.md
```

The Gold layer was designed to create pre-aggregated analytics tables from the normalized Silver tables.

Gold outputs:

```text
data/gold/top_tracks/
data/gold/top_artists/
data/gold/top_albums/
data/gold/playlist_summary/
```

---

### 2. Gold Top Tracks Table

Script:

```text
src/transformation/gold_top_tracks.py
```

Input tables:

```text
data/silver/playlist_tracks/
data/silver/tracks/
```

Output:

```text
data/gold/top_tracks/
```

Business question answered:

```text
Which tracks appear in the most playlists?
```

---

### 3. Gold Top Artists and Top Albums Tables

Script:

```text
src/transformation/gold_top_artists_albums.py
```

Input tables:

```text
data/silver/playlist_tracks/
data/silver/tracks/
```

Outputs:

```text
data/gold/top_artists/
data/gold/top_albums/
```

Business questions answered:

```text
Which artists are most represented across playlists?
Which albums appear most frequently across playlists?
```

Metrics created:

```text
playlist_count
track_appearance_count
unique_track_count
```

---

### 4. Gold Playlist Summary Table

Script:

```text
src/transformation/gold_playlist_summary.py
```

Input tables:

```text
data/silver/playlists/
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
data/silver/albums/
```

Output:

```text
data/gold/playlist_summary/
```

Business question answered:

```text
What is the overall summary of the playlist dataset?
```

Summary metrics include:

```text
total_playlists
total_playlist_track_rows
unique_tracks
unique_artists
unique_albums
average_tracks_per_playlist
average_followers_per_playlist
max_tracks_in_playlist
min_tracks_in_playlist
```

---

### 5. AWS S3 Data Lake Setup

S3 bucket:

```text
s3://spotify-million-playlist-data-lake-arvind-2026/
```

S3 data lake structure:

```text
s3://spotify-million-playlist-data-lake-arvind-2026/spotify/
├── raw/
├── bronze/
├── silver/
└── gold/
```

The local Raw, Bronze, Silver, and Gold outputs were uploaded to S3.

---

### 6. Athena External Tables

Athena database:

```text
spotify_analytics
```

DDL files:

```text
sql/athena_ddl/create_database.sql
sql/athena_ddl/create_silver_tables.sql
sql/athena_ddl/create_gold_tables.sql
```

Athena external tables were created on top of the Silver and Gold Parquet data stored in S3.

Created Athena tables:

```text
silver_playlists
silver_playlist_tracks
silver_tracks
silver_artists
silver_albums
gold_top_tracks
gold_top_artists
gold_top_albums
gold_playlist_summary
```

---

### 7. Athena Analytics Queries

Reusable analytics queries were created under:

```text
sql/analytics_queries/
```

Query files:

```text
top_tracks.sql
top_artists.sql
top_albums.sql
playlist_summary.sql
common_playlist_names.sql
athena_validation_checks.sql
```

These queries answer business questions such as:

```text
Which tracks appear in the most playlists?
Which artists are most represented across playlists?
Which albums appear most frequently?
What are the most common playlist names?
What are the overall dataset summary metrics?
```

The `common_playlist_names.sql` query currently uses the Silver playlists table directly.

---

## Week 3 Architecture Completed

By the end of Week 3, the project architecture reached:

```text
Raw JSON
   ↓
Bronze Parquet
   ↓
Silver Normalized Tables
   ↓
Gold Analytics Tables
   ↓
AWS S3 Data Lake
   ↓
Athena SQL Queries
```

---

## Key Week 3 Learning Outcomes

Week 3 demonstrated:

1. Business-oriented aggregation design.
2. Gold layer development.
3. SQL-friendly analytics modeling.
4. Parquet outputs for query engines.
5. AWS S3 data lake organization.
6. Athena external table creation.
7. Serverless SQL analytics over S3 data.

---

## Week 3 Conclusion

Week 3 moved the project from local data processing into cloud-based analytics. The project now has Gold analytics tables stored in S3 and queryable through Athena, making the Spotify dataset ready for SQL-based business analysis.
