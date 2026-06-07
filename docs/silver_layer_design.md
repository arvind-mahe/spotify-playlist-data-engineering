# Silver Layer Design — Spotify Million Playlist Dataset

## Purpose

The Silver layer contains cleaned, normalized, and SQL-friendly tables created from the Bronze playlist data.

The Bronze layer keeps one row per playlist with a nested `tracks` array. The Silver layer separates that nested structure into multiple relational-style tables.

The Silver layer prepares the data for Gold-level aggregations and Athena SQL analytics.

---

## Input

Silver transformations use the Bronze playlist Parquet table as input:

```text
data/bronze/playlists/
```

In AWS, the equivalent input path will be:

```text
s3://your-bucket/spotify/bronze/playlists/
```

---

## Output

Silver tables will be written locally under:

```text
data/silver/
```

Expected Silver outputs:

```text
data/silver/playlists/
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
data/silver/albums/
```

In AWS, the equivalent output paths will be:

```text
s3://your-bucket/spotify/silver/playlists/
s3://your-bucket/spotify/silver/playlist_tracks/
s3://your-bucket/spotify/silver/tracks/
s3://your-bucket/spotify/silver/artists/
s3://your-bucket/spotify/silver/albums/
```

Output format:

```text
Parquet
```

---

## Silver Layer Data Model

The Silver layer uses a normalized structure:

```text
playlists
playlist_tracks
tracks
artists
albums
```

Relationship model:

```text
playlists.playlist_id
        ↓
playlist_tracks.playlist_id

tracks.track_id
        ↓
playlist_tracks.track_id
```

The `playlist_tracks` table is the bridge table between playlists and tracks.

This is needed because:

```text
One playlist can contain many tracks.
One track can appear in many playlists.
```

---

# Silver Table 1: Playlists

## Purpose

The `playlists` table stores playlist-level metadata.

It removes the nested `tracks` array from the Bronze table and keeps only playlist attributes.

## Output Path

```text
data/silver/playlists/
```

## Grain

```text
One row per playlist
```

## Columns

| Column | Description |
|---|---|
| `playlist_id` | Unique playlist identifier |
| `playlist_name` | Playlist name |
| `collaborative` | Whether the playlist is collaborative |
| `modified_at` | Last modified timestamp |
| `num_tracks` | Number of tracks in the playlist |
| `num_albums` | Number of albums in the playlist |
| `num_followers` | Number of playlist followers |
| `num_edits` | Number of playlist edits |
| `playlist_duration_ms` | Total playlist duration in milliseconds |
| `ingestion_timestamp` | Timestamp from Bronze ingestion |
| `source_file` | Source file from Bronze ingestion |

## Transformation Rules

1. Read Bronze playlist table.
2. Select playlist-level fields.
3. Trim `playlist_name`.
4. Cast numeric fields to `long`.
5. Exclude the nested `tracks` array.
6. Write output as Parquet.

## Script

```text
src/transformation/silver_playlists.py
```

Run command:

```bash
python src/transformation/silver_playlists.py
```

---

# Silver Table 2: Playlist Tracks

## Purpose

The `playlist_tracks` table stores the relationship between playlists and tracks.

This table is created by exploding the nested `tracks` array from the Bronze table.

## Output Path

```text
data/silver/playlist_tracks/
```

## Grain

```text
One row per track inside a playlist
```

## Columns

| Column | Description |
|---|---|
| `playlist_id` | Playlist identifier |
| `track_id` | Track identifier from `track_uri` |
| `position` | Track position inside the playlist |
| `ingestion_timestamp` | Timestamp from Bronze ingestion |
| `source_file` | Source file from Bronze ingestion |

## Transformation Rules

1. Read Bronze playlist table.
2. Explode the nested `tracks` array.
3. Extract `playlist_id` from the playlist record.
4. Extract `track_uri` as `track_id`.
5. Extract `pos` as `position`.
6. Write output as Parquet.

## Script

```text
src/transformation/silver_playlist_tracks.py
```

Run command:

```bash
python src/transformation/silver_playlist_tracks.py
```

---

# Silver Table 3: Tracks

## Purpose

The `tracks` table stores one row per unique track.

It contains track metadata such as track name, artist, album, and duration.

## Output Path

```text
data/silver/tracks/
```

## Grain

```text
One row per unique track
```

## Columns

| Column | Description |
|---|---|
| `track_id` | Unique track identifier from `track_uri` |
| `track_name` | Track name |
| `artist_id` | Artist identifier from `artist_uri` |
| `artist_name` | Artist name |
| `album_id` | Album identifier from `album_uri` |
| `album_name` | Album name |
| `track_duration_ms` | Track duration in milliseconds |
| `ingestion_timestamp` | Timestamp from Bronze ingestion |
| `source_file` | Source file from Bronze ingestion |

## Transformation Rules

1. Read Bronze playlist table.
2. Explode the nested `tracks` array.
3. Select track-level fields.
4. Trim string fields such as `track_name`, `artist_name`, and `album_name`.
5. Cast duration fields to `long`.
6. Deduplicate using `track_id`.
7. Write output as Parquet.

## Script

```text
src/transformation/silver_tracks.py
```

Run command:

```bash
python src/transformation/silver_tracks.py
```

---

# Silver Table 4: Artists

## Purpose

The `artists` table stores one row per unique artist.

This avoids repeating artist metadata across many track rows.

## Output Path

```text
data/silver/artists/
```

## Grain

```text
One row per unique artist
```

## Columns

| Column | Description |
|---|---|
| `artist_id` | Unique artist identifier from `artist_uri` |
| `artist_name` | Artist name |
| `ingestion_timestamp` | Timestamp from Bronze ingestion |
| `source_file` | Source file from Bronze ingestion |

## Transformation Rules

1. Read Bronze playlist table.
2. Explode the nested `tracks` array.
3. Select `artist_uri` as `artist_id`.
4. Select and trim `artist_name`.
5. Deduplicate using `artist_id`.
6. Write output as Parquet.

## Script

```text
src/transformation/silver_artists_albums.py
```

Run command:

```bash
python src/transformation/silver_artists_albums.py
```

---

# Silver Table 5: Albums

## Purpose

The `albums` table stores one row per unique album.

It contains album metadata and the associated artist fields available in the source data.

## Output Path

```text
data/silver/albums/
```

## Grain

```text
One row per unique album
```

## Columns

| Column | Description |
|---|---|
| `album_id` | Unique album identifier from `album_uri` |
| `album_name` | Album name |
| `artist_id` | Artist identifier from `artist_uri` |
| `artist_name` | Artist name |
| `ingestion_timestamp` | Timestamp from Bronze ingestion |
| `source_file` | Source file from Bronze ingestion |

## Transformation Rules

1. Read Bronze playlist table.
2. Explode the nested `tracks` array.
3. Select `album_uri` as `album_id`.
4. Select and trim `album_name`.
5. Select artist fields associated with the album record.
6. Deduplicate using `album_id`.
7. Write output as Parquet.

## Script

```text
src/transformation/silver_artists_albums.py
```

Run command:

```bash
python src/transformation/silver_artists_albums.py
```

---

## Silver Validation Rules

The Silver validation job should check all Silver tables together.

Validation checks include:

1. All Silver tables can be read.
2. Each table has more than zero rows.
3. Required ID columns are not null.
4. Dimension tables do not have duplicate IDs.
5. Every `playlist_tracks.playlist_id` exists in `playlists.playlist_id`.
6. Every `playlist_tracks.track_id` exists in `tracks.track_id`.
7. Summary counts make sense.

Expected count relationships:

```text
playlists row count = 1000 for one Spotify slice
playlist_tracks row count > playlists row count
tracks row count <= playlist_tracks row count
artists row count <= tracks row count
albums row count <= tracks row count
```

---

## Silver Validation Script

Validation script:

```text
src/quality/validate_silver.py
```

Run command:

```bash
python src/quality/validate_silver.py
```

---

## Silver Layer Scripts Summary

| Script | Purpose |
|---|---|
| `src/transformation/silver_playlists.py` | Creates Silver playlists table |
| `src/transformation/silver_playlist_tracks.py` | Creates Silver playlist-track bridge table |
| `src/transformation/silver_tracks.py` | Creates Silver tracks dimension table |
| `src/transformation/silver_artists_albums.py` | Creates Silver artists and albums dimension tables |
| `src/quality/validate_silver.py` | Validates the full Silver layer |

---

## Design Decision

The Silver layer should be cleaned and normalized, but not heavily aggregated.

Aggregations such as top tracks, top artists, top albums, and playlist summary metrics belong to the Gold layer.

The Silver layer focuses on making the raw nested JSON structure queryable and reliable.

---

## Conclusion

The Silver layer transforms the Bronze playlist data into normalized Parquet tables.

This creates a SQL-friendly data model that can be used for Gold analytics, Athena queries, dashboards, and portfolio project demonstrations.
