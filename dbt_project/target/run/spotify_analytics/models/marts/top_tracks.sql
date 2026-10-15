
    

    create  table
      "spotify_analytics"."main"."top_tracks__dbt_tmp"
  
    
    as (
      with counts as (
    select track_id, count(distinct playlist_id) as playlist_count,
           count(*) as total_appearances
    from "spotify_analytics"."main"."stg_playlist_tracks"
    group by track_id
)
select c.track_id, t.track_name, t.artist_name,
       c.playlist_count, c.total_appearances
from counts c
left join "spotify_analytics"."main"."stg_tracks" t on c.track_id = t.track_id
    );
    
  