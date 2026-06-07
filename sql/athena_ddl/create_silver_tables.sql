USE spotify_analytics;

CREATE EXTERNAL TABLE IF NOT EXISTS silver_playlists (
    playlist_id BIGINT,
    playlist_name STRING,
    collaborative STRING,
    modified_at BIGINT,
    num_tracks BIGINT,
    num_albums BIGINT,
    num_followers BIGINT,
    num_edits BIGINT,
    playlist_duration_ms BIGINT,
    ingestion_timestamp TIMESTAMP,
    source_file STRING
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/silver/playlists/';

CREATE EXTERNAL TABLE IF NOT EXISTS silver_playlist_tracks (
    playlist_id BIGINT,
    track_id STRING,
    position BIGINT,
    ingestion_timestamp TIMESTAMP,
    source_file STRING
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/silver/playlist_tracks/';

CREATE EXTERNAL TABLE IF NOT EXISTS silver_tracks (
    track_id STRING,
    track_name STRING,
    artist_id STRING,
    artist_name STRING,
    album_id STRING,
    album_name STRING,
    track_duration_ms BIGINT,
    ingestion_timestamp TIMESTAMP,
    source_file STRING
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/silver/tracks/';

CREATE EXTERNAL TABLE IF NOT EXISTS silver_artists (
    artist_id STRING,
    artist_name STRING,
    ingestion_timestamp TIMESTAMP,
    source_file STRING
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/silver/artists/';

CREATE EXTERNAL TABLE IF NOT EXISTS silver_albums (
    album_id STRING,
    album_name STRING,
    artist_id STRING,
    artist_name STRING,
    ingestion_timestamp TIMESTAMP,
    source_file STRING
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/silver/albums/';