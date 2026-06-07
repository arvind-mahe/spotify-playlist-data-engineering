from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode


def create_spark_session():
    """
    Create and return a Spark session for Silver playlist_tracks transformation.
    """
    return SparkSession.builder \
        .appName("SpotifySilverPlaylistTracks") \
        .master("local[*]") \
        .getOrCreate()


def read_bronze_playlists(spark, bronze_path):
    """
    Read Bronze playlist Parquet data.
    """
    print(f"Reading Bronze playlists from: {bronze_path}")
    return spark.read.parquet(bronze_path)


def transform_to_silver_playlist_tracks(bronze_df):
    """
    Transform Bronze nested tracks into Silver playlist_tracks bridge table.

    Silver playlist_tracks grain:
    One row per track inside a playlist.
    """

    exploded_tracks_df = bronze_df.select(
        col("playlist_id"),
        explode(col("tracks")).alias("track"),
        col("ingestion_timestamp"),
        col("source_file")
    )

    silver_playlist_tracks_df = exploded_tracks_df.select(
        col("playlist_id").cast("long").alias("playlist_id"),
        col("track.track_uri").alias("track_id"),
        col("track.pos").cast("long").alias("position"),
        col("ingestion_timestamp"),
        col("source_file")
    )

    return silver_playlist_tracks_df


def write_silver_playlist_tracks(silver_df, silver_output_path):
    """
    Write Silver playlist_tracks table as Parquet.
    """
    print(f"Writing Silver playlist_tracks to: {silver_output_path}")

    silver_df.write \
        .mode("overwrite") \
        .parquet(silver_output_path)


def validate_silver_playlist_tracks(spark, silver_output_path):
    """
    Read back Silver playlist_tracks output and perform basic validation.
    """
    print("\nValidating Silver playlist_tracks output...")

    silver_check_df = spark.read.parquet(silver_output_path)

    print("\nSilver Playlist Tracks Schema:")
    silver_check_df.printSchema()

    print("\nSilver Playlist Tracks Sample:")
    silver_check_df.show(10, truncate=False)

    print("\nSilver Playlist Tracks Row Count:")
    print(silver_check_df.count())

    print("\nDistinct Playlists in playlist_tracks:")
    print(silver_check_df.select("playlist_id").distinct().count())

    print("\nDistinct Tracks in playlist_tracks:")
    print(silver_check_df.select("track_id").distinct().count())


def main():
    spark = create_spark_session()

    bronze_path = "data/bronze/playlists/"
    silver_output_path = "data/silver/playlist_tracks/"

    print("Silver playlist_tracks transformation started.")
    print(f"Bronze input path: {bronze_path}")
    print(f"Silver output path: {silver_output_path}")

    bronze_df = read_bronze_playlists(spark, bronze_path)

    silver_playlist_tracks_df = transform_to_silver_playlist_tracks(bronze_df)

    print("\nTransformed Silver Playlist Tracks Preview:")
    silver_playlist_tracks_df.show(10, truncate=False)

    write_silver_playlist_tracks(silver_playlist_tracks_df, silver_output_path)

    validate_silver_playlist_tracks(spark, silver_output_path)

    spark.stop()

    print("\nSilver playlist_tracks transformation completed successfully.")


if __name__ == "__main__":
    main()