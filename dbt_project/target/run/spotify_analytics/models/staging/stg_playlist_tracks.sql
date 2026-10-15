
  
  create view "spotify_analytics"."main"."stg_playlist_tracks__dbt_tmp" as (
    select playlist_id, track_id, position
from read_parquet('data/silver/playlist_tracks/*.parquet')
where playlist_id is not null and track_id is not null
  );
