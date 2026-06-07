# Bronze Layer Design — Spotify Million Playlist Dataset

## Purpose

The Bronze layer is the first processed layer of the Spotify Million Playlist data lake pipeline.

It converts raw nested Spotify playlist JSON files into Parquet format while preserving the original playlist structure as much as possible.

The Bronze layer is used as the stable input for downstream Silver transformations.

---

## Input

Raw files are stored locally under:

```text
data/raw/
```

Example:

```text
data/raw/mpd.slice.0-999.json
```

In AWS, the equivalent location will be:

```text
s3://your-bucket/spotify/raw/
```

---

## Output

Bronze data will be written locally to:

```text
data/bronze/playlists/
```

In AWS, the equivalent location will be:

```text
s3://your-bucket/spotify/bronze/playlists/
```

Output format:

```text
Parquet
```

---

## Data Grain

The Bronze playlist table will have:

```text
One row per playlist
```

The nested `tracks` array will remain inside each playlist row.

Tracks will not be flattened until the Silver layer.

---

## Bronze Fields

| Bronze Field | Source Field | Description |
|---|---|---|
| `playlist_id` | `pid` | Unique playlist identifier |
| `playlist_name` | `name` | Name of the playlist |
| `collaborative` | `collaborative` | Whether the playlist is collaborative |
| `modified_at` | `modified_at` | Last modified timestamp |
| `num_tracks` | `num_tracks` | Number of tracks in the playlist |
| `num_albums` | `num_albums` | Number of albums in the playlist |
| `num_followers` | `num_followers` | Number of playlist followers |
| `num_edits` | `num_edits` | Number of playlist edits |
| `playlist_duration_ms` | `duration_ms` | Total playlist duration in milliseconds |
| `tracks` | `tracks` | Nested array of track records |
| `ingestion_timestamp` | System generated | Timestamp when the record was ingested |
| `source_file` | Input file name | Raw source file path |

---

## Transformations Applied

The Bronze ingestion job will:

1. Read raw JSON files from `data/raw/`.
2. Explode the top-level `playlists` array.
3. Select and rename playlist-level fields.
4. Keep the nested `tracks` array unchanged.
5. Add an ingestion timestamp.
6. Add the input source file path.
7. Write the output as Parquet.

---

## Transformations Not Applied

The Bronze layer will not:

1. Deduplicate tracks.
2. Flatten the nested tracks array.
3. Create artists or albums tables.
4. Build business-level metrics.
5. Create aggregations.

These transformations will happen in the Silver and Gold layers.

---

## Bronze Layer Output Example

Expected output folder:

```text
data/bronze/playlists/
```

Expected file format:

```text
.parquet
```

Expected table structure:

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

## Bronze Validation Rules

After the Bronze ingestion job runs, the following checks should be performed:

1. Bronze output path exists.
2. Bronze table row count is greater than zero.
3. Required columns are present.
4. `playlist_id` is not null.
5. `playlist_id` has no duplicates within the processed slice.
6. `tracks` array is not null.
7. `tracks` array is not empty.
8. `num_tracks` matches the actual size of the `tracks` array.

---

## Bronze Layer Script

Bronze ingestion script:

```text
src/ingestion/bronze_ingestion.py
```

Run command:

```bash
python src/ingestion/bronze_ingestion.py
```

Bronze validation script:

```text
src/quality/validate_bronze.py
```

Run command:

```bash
python src/quality/validate_bronze.py
```

---

## Design Decision

The Bronze layer should remain close to the raw source data.

It should improve storage and processing efficiency by converting JSON to Parquet, but it should not perform heavy cleaning, normalization, or aggregation.

The main purpose of Bronze is to create a reliable, reusable, source-preserved dataset for the Silver layer.

---

## Conclusion

The Bronze layer converts raw Spotify JSON playlist data into playlist-level Parquet data while preserving the nested track structure.

This creates the foundation for the Silver layer, where the nested data will be flattened and normalized into analytical tables.
