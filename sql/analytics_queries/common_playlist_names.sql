USE spotify_analytics;

SELECT
    LOWER(TRIM(playlist_name)) AS playlist_name,
    COUNT(*) AS playlist_name_count,
    ROUND(AVG(num_tracks), 2) AS average_num_tracks,
    ROUND(AVG(num_followers), 2) AS average_num_followers
FROM silver_playlists
WHERE playlist_name IS NOT NULL
GROUP BY LOWER(TRIM(playlist_name))
ORDER BY playlist_name_count DESC, average_num_tracks DESC
LIMIT 20;