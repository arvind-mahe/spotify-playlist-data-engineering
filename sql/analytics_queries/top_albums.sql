USE spotify_analytics;

SELECT
    album_name,
    artist_name,
    playlist_count,
    track_appearance_count,
    unique_track_count
FROM gold_top_albums
ORDER BY playlist_count DESC, track_appearance_count DESC
LIMIT 20;