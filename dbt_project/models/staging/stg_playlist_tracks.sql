select playlist_id, track_id, position
from read_parquet('data/silver/playlist_tracks/*.parquet')
where playlist_id is not null and track_id is not null
