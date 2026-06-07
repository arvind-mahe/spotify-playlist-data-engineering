USE spotify_analytics;

-- Check Silver playlist count
SELECT COUNT(*) AS silver_playlist_count
FROM silver_playlists;

-- Check Silver playlist-track rows
SELECT COUNT(*) AS silver_playlist_track_rows
FROM silver_playlist_tracks;

-- Check Gold top tracks count
SELECT COUNT(*) AS gold_top_tracks_count
FROM gold_top_tracks;

-- Check Gold summary table
SELECT *
FROM gold_playlist_summary;

-- Check that Gold top tracks table is queryable
SELECT
    track_name,
    artist_name,
    playlist_count
FROM gold_top_tracks
ORDER BY playlist_count DESC
LIMIT 10;