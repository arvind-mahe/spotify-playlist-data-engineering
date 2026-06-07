from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col


def create_spark_session():
    return SparkSession.builder \
        .appName("ReadRawSpotifyJSON") \
        .master("local[*]") \
        .getOrCreate()


def main():
    spark = create_spark_session()

    raw_path = "data/raw/mpd.slice.0-999.json"

    print("Reading raw Spotify playlist JSON file...")
    df = spark.read.option("multiline", "true").json(raw_path)

    print("\nRaw DataFrame Schema:")
    df.printSchema()

    print("\nTop-level preview:")
    df.show(5, truncate=False)

    print("\nExploding playlists array...")
    playlists_df = df.select(explode(col("playlists")).alias("playlist"))

    print("\nPlaylist-level schema:")
    playlists_df.printSchema()

    print("\nSample playlist records:")
    playlists_df.select(
        col("playlist.pid").alias("playlist_id"),
        col("playlist.name").alias("playlist_name"),
        col("playlist.num_tracks").alias("num_tracks"),
        col("playlist.num_followers").alias("num_followers")
    ).show(10, truncate=False)

    print("\nSample nested tracks from playlists:")
    playlists_df.select(
        col("playlist.pid").alias("playlist_id"),
        explode(col("playlist.tracks")).alias("track")
    ).select(
        col("playlist_id"),
        col("track.pos").alias("position"),
        col("track.track_uri").alias("track_uri"),
        col("track.track_name").alias("track_name"),
        col("track.artist_name").alias("artist_name"),
        col("track.album_name").alias("album_name")
    ).show(10, truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()