
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select playlist_id
from "spotify_analytics"."main"."stg_playlist_tracks"
where playlist_id is null



  
  
      
    ) dbt_internal_test