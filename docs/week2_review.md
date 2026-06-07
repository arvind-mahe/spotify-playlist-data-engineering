# Week 2 Review — Bronze and Silver Pipeline

## Week 2 Goal

The goal of Week 2 was to implement the Bronze layer, validate it, and build the normalized Silver layer from nested Spotify playlist data.

---

## Completed Work

### 1. Bronze Ingestion Job Built

Bronze ingestion script:

```text
src/ingestion/bronze_ingestion.py
```

Run command:

```bash
python src/ingestion/bronze_ingestion.py
```

Input:

```text
data/raw/mpd.slice.0-999.json
```

Output:

```text
data/bronze/playlists/
```

Bronze format:

```text
Parquet
```

Bronze grain:

```text
One row per playlist
```

Bronze output includes:

```text
playlist_id
playlist_name
collaborative
modified_at
num_tracks
num_albums
num_followers
num_edits
playlist_duration_ms
tracks
ingestion_timestamp
source_file
```

---

### 2. Bronze Validation Job Built

Bronze validation script:

```text
src/quality/validate_bronze.py
```

Run command:

```bash
python src/quality/validate_bronze.py
```

Validation checks:

1. Required columns exist.
2. Bronze row count is greater than zero.
3. Playlist IDs are not null.
4. Playlist IDs are not duplicated.
5. Tracks array is not null or empty.
6. `num_tracks` matches the size of the nested tracks array.
7. Basic null counts are displayed.

---

### 3. Silver Playlists Table Created

Silver playlists script:

```text
src/transformation/silver_playlists.py
```

Run command:

```bash
python src/transformation/silver_playlists.py
```

Input:

```text
data/bronze/playlists/
```

Output:

```text
data/silver/playlists/
```

Table grain:

```text
One row per playlist
```

This table removes the nested `tracks` array and keeps only playlist-level metadata.

---

### 4. Silver Playlist Tracks Bridge Table Created

Silver playlist tracks script:

```text
src/transformation/silver_playlist_tracks.py
```

Run command:

```bash
python src/transformation/silver_playlist_tracks.py
```

Input:

```text
data/bronze/playlists/
```

Output:

```text
data/silver/playlist_tracks/
```

Table grain:

```text
One row per track inside a playlist
```

Columns:

```text
playlist_id
track_id
position
ingestion_timestamp
source_file
```

This table represents the many-to-many relationship between playlists and tracks.

---

### 5. Silver Tracks Table Created

Silver tracks script:

```text
src/transformation/silver_tracks.py
```

Run command:

```bash
python src/transformation/silver_tracks.py
```

Input:

```text
data/bronze/playlists/
```

Output:

```text
data/silver/tracks/
```

Table grain:

```text
One row per unique track
```

Columns:

```text
track_id
track_name
artist_id
artist_name
album_id
album_name
track_duration_ms
ingestion_timestamp
source_file
```

Tracks are deduplicated using `track_id`.

---

### 6. Silver Artists and Albums Tables Created

Silver artists and albums script:

```text
src/transformation/silver_artists_albums.py
```

Run command:

```bash
python src/transformation/silver_artists_albums.py
```

Outputs:

```text
data/silver/artists/
data/silver/albums/
```

Artists table grain:

```text
One row per unique artist
```

Albums table grain:

```text
One row per unique album
```

---

### 7. Silver Layer Validation Built

Silver validation script:

```text
src/quality/validate_silver.py
```

Run command:

```bash
python src/quality/validate_silver.py
```

Validation checks:

1. All Silver tables are readable.
2. All Silver tables are non-empty.
3. Primary IDs are not null.
4. Dimension tables do not contain duplicate IDs.
5. `playlist_tracks.playlist_id` values exist in `playlists`.
6. `playlist_tracks.track_id` values exist in `tracks`.
7. Summary counts are printed.

---

## Final Silver Model

Week 2 completed the normalized Silver model:

```text
data/silver/playlists/
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
data/silver/albums/
```

Relationship model:

```text
playlists
    playlist_id
        ↓
playlist_tracks
    playlist_id
    track_id
        ↓
tracks
    track_id
    artist_id
    album_id
        ↓
artists
albums
```

---

## Week 2 Architecture Progress

Completed architecture stage:

```text
Raw JSON
   ↓
Bronze Parquet
   ↓
Silver Normalized Tables
```

---

## Key Week 2 Learning Outcomes

By the end of Week 2, the project demonstrated:

1. PySpark JSON-to-Parquet processing.
2. Bronze layer creation.
3. Bronze validation.
4. Nested array flattening using `explode`.
5. Normalized Silver data modeling.
6. Dimension table creation.
7. Bridge table creation.
8. Silver layer validation and referential checks.

---

## Week 2 Conclusion

Week 2 completed the core data modeling phase of the project. The raw nested Spotify JSON was converted into a validated Bronze layer and then transformed into normalized Silver tables.

The next step is to design and build the Gold analytics layer.
