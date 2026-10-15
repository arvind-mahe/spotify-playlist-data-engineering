
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select playlist_count
from "spotify_analytics"."main"."top_tracks"
where playlist_count is null



  
  
      
    ) dbt_internal_test