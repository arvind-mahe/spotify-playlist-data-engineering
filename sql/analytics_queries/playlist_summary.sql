USE spotify_analytics;

SELECT
    summary_level,
    total_playlists,
    total_playlist_track_rows,
    unique_tracks,
    unique_artists,
    unique_albums,
    average_tracks_per_playlist,
    average_followers_per_playlist,
    max_tracks_in_playlist,
    min_tracks_in_playlist
FROM gold_playlist_summary;