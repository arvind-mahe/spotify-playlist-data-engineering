
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select * from "spotify_analytics"."main"."top_tracks"
where playlist_count < 1 or total_appearances < playlist_count
  
  
      
    ) dbt_internal_test