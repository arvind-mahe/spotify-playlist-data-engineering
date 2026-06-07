USE spotify_analytics;

CREATE EXTERNAL TABLE IF NOT EXISTS gold_top_tracks (
    track_id STRING,
    track_name STRING,
    artist_id STRING,
    artist_name STRING,
    album_id STRING,
    album_name STRING,
    playlist_count BIGINT,
    total_appearances BIGINT
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/gold/top_tracks/';

CREATE EXTERNAL TABLE IF NOT EXISTS gold_top_artists (
    artist_id STRING,
    artist_name STRING,
    playlist_count BIGINT,
    track_appearance_count BIGINT,
    unique_track_count BIGINT
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/gold/top_artists/';

CREATE EXTERNAL TABLE IF NOT EXISTS gold_top_albums (
    album_id STRING,
    album_name STRING,
    artist_id STRING,
    artist_name STRING,
    playlist_count BIGINT,
    track_appearance_count BIGINT,
    unique_track_count BIGINT
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/gold/top_albums/';

CREATE EXTERNAL TABLE IF NOT EXISTS gold_playlist_summary (
    summary_level STRING,
    total_playlists BIGINT,
    total_playlist_track_rows BIGINT,
    unique_tracks BIGINT,
    unique_artists BIGINT,
    unique_albums BIGINT,
    average_tracks_per_playlist DOUBLE,
    average_followers_per_playlist DOUBLE,
    max_tracks_in_playlist BIGINT,
    min_tracks_in_playlist BIGINT
)
STORED AS PARQUET
LOCATION 's3://spotify-million-playlist-data-lake-arvind-2026/spotify/gold/playlist_summary/';