# Raw Schema Notes — Spotify Million Playlist Dataset

## Purpose

This document describes the raw structure of the Spotify Million Playlist Dataset and identifies how the raw JSON fields will be used in the Bronze, Silver, and Gold layers of the data engineering pipeline.

The dataset is semi-structured JSON. Each file contains a top-level `playlists` array, and each playlist contains playlist-level metadata along with a nested `tracks` array.

---

## Raw File Location

Local raw data path:

```text
data/raw/
```

Example file:

```text
data/raw/mpd.slice.0-999.json
```

Future AWS S3 raw path:

```text
s3://your-bucket/spotify/raw/
```

---

## Raw JSON Structure

Each raw JSON file contains a root object with a `playlists` array.

```text
root
 └── playlists
      ├── playlist 1
      ├── playlist 2
      ├── playlist 3
      └── ...
```

Each playlist contains metadata and a nested `tracks` array.

```text
playlist
 ├── pid
 ├── name
 ├── collaborative
 ├── modified_at
 ├── num_tracks
 ├── num_albums
 ├── num_followers
 ├── num_edits
 ├── duration_ms
 └── tracks
      ├── track 1
      ├── track 2
      └── ...
```

---

## Playlist-Level Fields

| Raw Field | Meaning | Target Name |
|---|---|---|
| `pid` | Unique playlist identifier | `playlist_id` |
| `name` | Playlist name | `playlist_name` |
| `collaborative` | Whether playlist is collaborative | `collaborative` |
| `modified_at` | Last modified timestamp | `modified_at` |
| `num_tracks` | Number of tracks in the playlist | `num_tracks` |
| `num_albums` | Number of albums in the playlist | `num_albums` |
| `num_followers` | Number of playlist followers | `num_followers` |
| `num_edits` | Number of playlist edits | `num_edits` |
| `duration_ms` | Total playlist duration in milliseconds | `playlist_duration_ms` |

---

## Track-Level Fields

Each playlist contains a nested `tracks` array.

| Raw Field | Meaning | Target Name |
|---|---|---|
| `pos` | Track position inside playlist | `position` |
| `track_uri` | Unique Spotify track URI | `track_id` |
| `track_name` | Track name | `track_name` |
| `artist_uri` | Unique Spotify artist URI | `artist_id` |
| `artist_name` | Artist name | `artist_name` |
| `album_uri` | Unique Spotify album URI | `album_id` |
| `album_name` | Album name | `album_name` |
| `duration_ms` | Track duration in milliseconds | `track_duration_ms` |

---

## Raw Data Observations

1. The raw dataset is nested JSON.
2. The top-level object contains a `playlists` array.
3. Each playlist contains playlist metadata.
4. Each playlist contains a nested `tracks` array.
5. The same track can appear in multiple playlists.
6. The same artist can appear across many tracks and playlists.
7. The same album can appear across many tracks and playlists.
8. The raw data needs to be flattened before SQL analytics.

---

## Data Grain in Raw JSON

The raw file itself has this structure:

```text
One file contains many playlists.
One playlist contains many tracks.
```

For processing, the first useful grain is:

```text
One row per playlist
```

This becomes the Bronze layer grain.

For Silver, the nested tracks array is flattened into:

```text
One row per track inside a playlist
```

This becomes the `playlist_tracks` bridge table.

---

## Data Modeling Decision

The raw nested JSON will be normalized into separate Silver tables.

Expected Silver tables:

```text
data/silver/playlists/
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
data/silver/albums/
```

---

## Relationship Between Silver Tables

```text
playlists
    playlist_id

playlist_tracks
    playlist_id
    track_id
    position

tracks
    track_id
    track_name
    artist_id
    album_id
    track_duration_ms

artists
    artist_id
    artist_name

albums
    album_id
    album_name
    artist_id
    artist_name
```

The `playlist_tracks` table is the bridge table between playlists and tracks.

This is needed because:

```text
One playlist can contain many tracks.
One track can appear in many playlists.
```

---

## Bronze Layer Decision

The Bronze layer will preserve the playlist-level structure and keep the `tracks` array nested.

Bronze output path:

```text
data/bronze/playlists/
```

Bronze grain:

```text
One row per playlist
```

Bronze format:

```text
Parquet
```

Bronze transformations:

1. Read raw JSON.
2. Explode the top-level `playlists` array.
3. Rename playlist-level fields.
4. Keep `tracks` nested.
5. Add ingestion metadata.
6. Write as Parquet.

---

## Silver Layer Decision

The Silver layer will flatten and normalize the Bronze data into clean tables.

Silver outputs:

```text
data/silver/playlists/
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
data/silver/albums/
```

Silver transformations:

1. Remove nested `tracks` from the playlist table.
2. Explode nested `tracks` into playlist-track rows.
3. Deduplicate tracks by `track_id`.
4. Deduplicate artists by `artist_id`.
5. Deduplicate albums by `album_id`.
6. Validate null IDs, duplicate IDs, and referential consistency.

---

## Gold Layer Decision

The Gold layer will create analytics-ready aggregated tables.

Expected Gold outputs:

```text
data/gold/top_tracks/
data/gold/top_artists/
data/gold/top_albums/
data/gold/playlist_summary/
data/gold/common_playlist_names/
```

Gold will answer questions such as:

1. What are the most common tracks?
2. Which artists appear in the most playlists?
3. Which albums appear most often?
4. What are the most common playlist names?
5. What is the average number of tracks per playlist?
6. How many unique tracks, artists, and albums are in the dataset?

---

## Raw Schema Inspection Script

Raw schema inspection script:

```text
src/quality/inspect_raw_schema.py
```

Run command:

```bash
python src/quality/inspect_raw_schema.py
```

The script prints:

1. Raw root schema.
2. Playlist-level schema.
3. Playlist sample records.
4. Track-level sample records.
5. Basic counts.

---

## Conclusion

The Spotify Million Playlist Dataset starts as nested JSON. The project converts this raw semi-structured data into a layered data lake architecture:

```text
Raw JSON → Bronze Parquet → Silver Normalized Tables → Gold Analytics Tables
```

Understanding the raw schema is the foundation for building the Bronze, Silver, and Gold layers correctly.
