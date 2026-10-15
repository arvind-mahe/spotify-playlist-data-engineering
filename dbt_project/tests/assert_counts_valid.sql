select * from {{ ref('top_tracks') }}
where playlist_count < 1 or total_appearances < playlist_count
