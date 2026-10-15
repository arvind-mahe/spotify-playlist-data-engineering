select track_id, track_name, artist_id, artist_name, album_id, album_name
from read_parquet('data/silver/tracks/*.parquet')
where track_id is not null
