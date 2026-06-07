# Gold Layer Design — Spotify Million Playlist Dataset

## Purpose

The Gold layer contains business-ready analytics tables created from the normalized Silver layer.

The goal of the Gold layer is to make the Spotify Million Playlist Dataset easy to query using SQL and AWS Athena. Instead of asking users to repeatedly write complex joins and aggregations, the Gold layer stores pre-aggregated Parquet datasets that directly answer common analytics questions.

---

## Position in the Architecture

```text
Raw JSON
   ↓
Bronze Parquet
   ↓
Silver Normalized Tables
   ↓
Gold Analytics Tables
   ↓
Athena SQL Analytics
```

---

## Gold Layer Input

The Gold layer uses the cleaned and normalized Silver tables as input.

```text
data/silver/playlists/
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
data/silver/albums/
```

---

## Gold Layer Output

Gold tables will be written under:

```text
data/gold/
```

Expected outputs:

```text
data/gold/top_tracks/
data/gold/top_artists/
data/gold/top_albums/
data/gold/playlist_summary/
data/gold/common_playlist_names/
```

All Gold outputs will be stored in Parquet format.

---

## Gold Table 1: Top Tracks

### Purpose

Identify tracks that appear in the most playlists.

### Input Tables

```text
data/silver/playlist_tracks/
data/silver/tracks/
```

### Output Path

```text
data/gold/top_tracks/
```

### Table Grain

```text
One row per track
```

### Columns

| Column | Description |
|---|---|
| `track_id` | Unique Spotify track URI |
| `track_name` | Track name |
| `artist_id` | Unique Spotify artist URI |
| `artist_name` | Artist name |
| `album_id` | Unique Spotify album URI |
| `album_name` | Album name |
| `playlist_count` | Number of distinct playlists containing the track |
| `total_appearances` | Total number of playlist-track appearances |

### Business Question

Which tracks appear in the most playlists?

### Example SQL Logic

```sql
SELECT
    t.track_id,
    t.track_name,
    t.artist_id,
    t.artist_name,
    t.album_id,
    t.album_name,
    COUNT(DISTINCT pt.playlist_id) AS playlist_count,
    COUNT(*) AS total_appearances
FROM playlist_tracks pt
JOIN tracks t
    ON pt.track_id = t.track_id
GROUP BY
    t.track_id,
    t.track_name,
    t.artist_id,
    t.artist_name,
    t.album_id,
    t.album_name;
```

---

## Gold Table 2: Top Artists

### Purpose

Identify artists that appear across the highest number of playlists.

### Input Tables

```text
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
```

### Output Path

```text
data/gold/top_artists/
```

### Table Grain

```text
One row per artist
```

### Columns

| Column | Description |
|---|---|
| `artist_id` | Unique Spotify artist URI |
| `artist_name` | Artist name |
| `playlist_count` | Number of distinct playlists containing tracks by the artist |
| `track_appearance_count` | Total number of artist track appearances across playlists |
| `unique_track_count` | Number of unique tracks by the artist in the dataset |

### Business Question

Which artists are most represented across playlists?

### Example SQL Logic

```sql
SELECT
    t.artist_id,
    t.artist_name,
    COUNT(DISTINCT pt.playlist_id) AS playlist_count,
    COUNT(*) AS track_appearance_count,
    COUNT(DISTINCT t.track_id) AS unique_track_count
FROM playlist_tracks pt
JOIN tracks t
    ON pt.track_id = t.track_id
GROUP BY
    t.artist_id,
    t.artist_name;
```

---

## Gold Table 3: Top Albums

### Purpose

Identify albums that appear across the highest number of playlists.

### Input Tables

```text
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/albums/
```

### Output Path

```text
data/gold/top_albums/
```

### Table Grain

```text
One row per album
```

### Columns

| Column | Description |
|---|---|
| `album_id` | Unique Spotify album URI |
| `album_name` | Album name |
| `artist_id` | Artist URI associated with the album |
| `artist_name` | Artist name associated with the album |
| `playlist_count` | Number of distinct playlists containing tracks from the album |
| `track_appearance_count` | Total number of album track appearances across playlists |
| `unique_track_count` | Number of unique tracks from the album in the dataset |

### Business Question

Which albums appear most frequently across playlists?

### Example SQL Logic

```sql
SELECT
    t.album_id,
    t.album_name,
    t.artist_id,
    t.artist_name,
    COUNT(DISTINCT pt.playlist_id) AS playlist_count,
    COUNT(*) AS track_appearance_count,
    COUNT(DISTINCT t.track_id) AS unique_track_count
FROM playlist_tracks pt
JOIN tracks t
    ON pt.track_id = t.track_id
GROUP BY
    t.album_id,
    t.album_name,
    t.artist_id,
    t.artist_name;
```

---

## Gold Table 4: Playlist Summary

### Purpose

Create a single dataset-level summary table.

This table gives quick high-level metrics about the processed Spotify playlist dataset.

### Input Tables

```text
data/silver/playlists/
data/silver/playlist_tracks/
data/silver/tracks/
data/silver/artists/
data/silver/albums/
```

### Output Path

```text
data/gold/playlist_summary/
```

### Table Grain

```text
One row for the dataset summary
```

### Columns

| Column | Description |
|---|---|
| `total_playlists` | Total number of playlists |
| `total_playlist_track_rows` | Total number of playlist-track records |
| `unique_tracks` | Total number of unique tracks |
| `unique_artists` | Total number of unique artists |
| `unique_albums` | Total number of unique albums |
| `average_tracks_per_playlist` | Average number of tracks per playlist |
| `average_followers_per_playlist` | Average playlist follower count |
| `max_tracks_in_playlist` | Maximum track count in a playlist |
| `min_tracks_in_playlist` | Minimum track count in a playlist |

### Business Question

What is the overall summary of the playlist dataset?

---

## Gold Table 5: Common Playlist Names

### Purpose

Identify the most common playlist names and their average playlist characteristics.

### Input Table

```text
data/silver/playlists/
```

### Output Path

```text
data/gold/common_playlist_names/
```

### Table Grain

```text
One row per playlist name
```

### Columns

| Column | Description |
|---|---|
| `playlist_name` | Playlist name |
| `playlist_name_count` | Number of playlists with that name |
| `average_num_tracks` | Average number of tracks for playlists with that name |
| `average_num_followers` | Average follower count for playlists with that name |

### Business Question

What are the most common playlist names?

### Example SQL Logic

```sql
SELECT
    playlist_name,
    COUNT(*) AS playlist_name_count,
    AVG(num_tracks) AS average_num_tracks,
    AVG(num_followers) AS average_num_followers
FROM playlists
GROUP BY playlist_name;
```

---

## Gold Layer Design Decisions

1. Gold tables are built from Silver tables, not directly from Bronze.
2. Gold tables are stored as Parquet for efficient Athena and Spark querying.
3. Gold tables are pre-aggregated to reduce repeated computation.
4. Gold tables are designed around business questions, not raw source structure.
5. The Gold layer supports SQL analytics, dashboards, and resume-ready project insights.

---

## Validation Expectations

Gold validation should check:

1. Each Gold table is readable.
2. Each Gold table has records.
3. Ranking tables have valid count columns.
4. Playlist counts are not negative or null.
5. Summary table contains exactly one row.
6. Gold outputs can be queried using Athena.

---

## Final Gold Layer Outcome

After the Gold layer is complete, the project will support direct analytics such as:

```sql
SELECT *
FROM gold_top_tracks
ORDER BY playlist_count DESC
LIMIT 10;
```

```sql
SELECT *
FROM gold_top_artists
ORDER BY playlist_count DESC
LIMIT 10;
```

```sql
SELECT *
FROM gold_playlist_summary;
```

---

## Conclusion

The Gold layer transforms the normalized Silver data model into analytics-ready business datasets. This makes the Spotify Million Playlist Dataset easier to analyze using SQL and prepares the project for AWS S3 and Athena integration.
