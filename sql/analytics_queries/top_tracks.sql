USE spotify_analytics;

SELECT
    track_name,
    artist_name,
    album_name,
    playlist_count,
    total_appearances
FROM gold_top_tracks
ORDER BY playlist_count DESC, total_appearances DESC
LIMIT 20;