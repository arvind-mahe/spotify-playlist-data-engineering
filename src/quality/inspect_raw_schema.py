from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col


def create_spark_session():
    return SparkSession.builder \
        .appName("InspectRawSpotifySchema") \
        .master("local[*]") \
        .getOrCreate()


def main():
    spark = create_spark_session()

    raw_path = "data/raw/mpd.slice.0-999.json"

    print("Reading raw Spotify JSON...")
    df = spark.read.option("multiline", "true").json(raw_path)

    print("\n=== Raw Root Schema ===")
    df.printSchema()

    playlists_df = df.select(explode(col("playlists")).alias("playlist"))

    print("\n=== Playlist Schema ===")
    playlists_df.printSchema()

    playlist_columns_df = playlists_df.select(
        col("playlist.pid").alias("playlist_id"),
        col("playlist.name").alias("playlist_name"),
        col("playlist.collaborative").alias("collaborative"),
        col("playlist.modified_at").alias("modified_at"),
        col("playlist.num_tracks").alias("num_tracks"),
        col("playlist.num_albums").alias("num_albums"),
        col("playlist.num_followers").alias("num_followers"),
        col("playlist.num_edits").alias("num_edits"),
        col("playlist.duration_ms").alias("playlist_duration_ms")
    )

    print("\n=== Playlist-Level Sample ===")
    playlist_columns_df.show(10, truncate=False)

    tracks_df = playlists_df.select(
        col("playlist.pid").alias("playlist_id"),
        explode(col("playlist.tracks")).alias("track")
    )

    track_columns_df = tracks_df.select(
        col("playlist_id"),
        col("track.pos").alias("position"),
        col("track.track_uri").alias("track_id"),
        col("track.track_name").alias("track_name"),
        col("track.artist_uri").alias("artist_id"),
        col("track.artist_name").alias("artist_name"),
        col("track.album_uri").alias("album_id"),
        col("track.album_name").alias("album_name"),
        col("track.duration_ms").alias("track_duration_ms")
    )

    print("\n=== Track-Level Sample ===")
    track_columns_df.show(10, truncate=False)

    print("\n=== Basic Counts ===")
    print(f"Number of playlists: {playlist_columns_df.count()}")
    print(f"Number of playlist-track rows: {track_columns_df.count()}")
    print(f"Number of unique tracks: {track_columns_df.select('track_id').distinct().count()}")
    print(f"Number of unique artists: {track_columns_df.select('artist_id').distinct().count()}")
    print(f"Number of unique albums: {track_columns_df.select('album_id').distinct().count()}")

    spark.stop()


if __name__ == "__main__":
    main()