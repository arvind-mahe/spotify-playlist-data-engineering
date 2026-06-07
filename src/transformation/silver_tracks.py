from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, trim


def create_spark_session():
    """
    Create and return a Spark session for Silver tracks transformation.
    """
    return SparkSession.builder \
        .appName("SpotifySilverTracks") \
        .master("local[*]") \
        .getOrCreate()


def read_bronze_playlists(spark, bronze_path):
    """
    Read Bronze playlist Parquet data.
    """
    print(f"Reading Bronze playlists from: {bronze_path}")
    return spark.read.parquet(bronze_path)


def transform_to_silver_tracks(bronze_df):
    """
    Transform Bronze nested tracks into a deduplicated Silver tracks table.

    Silver tracks grain:
    One row per unique track.
    """

    exploded_tracks_df = bronze_df.select(
        explode(col("tracks")).alias("track"),
        col("ingestion_timestamp"),
        col("source_file")
    )

    tracks_df = exploded_tracks_df.select(
        col("track.track_uri").alias("track_id"),
        trim(col("track.track_name")).alias("track_name"),
        col("track.artist_uri").alias("artist_id"),
        trim(col("track.artist_name")).alias("artist_name"),
        col("track.album_uri").alias("album_id"),
        trim(col("track.album_name")).alias("album_name"),
        col("track.duration_ms").cast("long").alias("track_duration_ms"),
        col("ingestion_timestamp"),
        col("source_file")
    )

    silver_tracks_df = tracks_df.dropDuplicates(["track_id"])

    return silver_tracks_df


def write_silver_tracks(silver_df, silver_output_path):
    """
    Write Silver tracks table as Parquet.
    """
    print(f"Writing Silver tracks to: {silver_output_path}")

    silver_df.write \
        .mode("overwrite") \
        .parquet(silver_output_path)


def validate_silver_tracks(spark, silver_output_path):
    """
    Read back Silver tracks output and perform basic validation.
    """
    print("\nValidating Silver tracks output...")

    silver_check_df = spark.read.parquet(silver_output_path)

    print("\nSilver Tracks Schema:")
    silver_check_df.printSchema()

    print("\nSilver Tracks Sample:")
    silver_check_df.show(10, truncate=False)

    print("\nSilver Tracks Row Count:")
    print(silver_check_df.count())

    print("\nDistinct Track IDs:")
    print(silver_check_df.select("track_id").distinct().count())

    print("\nNull Track ID Count:")
    print(silver_check_df.filter(col("track_id").isNull()).count())


def main():
    spark = create_spark_session()

    bronze_path = "data/bronze/playlists/"
    silver_output_path = "data/silver/tracks/"

    print("Silver tracks transformation started.")
    print(f"Bronze input path: {bronze_path}")
    print(f"Silver output path: {silver_output_path}")

    bronze_df = read_bronze_playlists(spark, bronze_path)

    silver_tracks_df = transform_to_silver_tracks(bronze_df)

    print("\nTransformed Silver Tracks Preview:")
    silver_tracks_df.show(10, truncate=False)

    write_silver_tracks(silver_tracks_df, silver_output_path)

    validate_silver_tracks(spark, silver_output_path)

    spark.stop()

    print("\nSilver tracks transformation completed successfully.")


if __name__ == "__main__":
    main()