USE spotify_analytics;

SELECT
    artist_name,
    playlist_count,
    track_appearance_count,
    unique_track_count
FROM gold_top_artists
ORDER BY playlist_count DESC, track_appearance_count DESC
LIMIT 20;