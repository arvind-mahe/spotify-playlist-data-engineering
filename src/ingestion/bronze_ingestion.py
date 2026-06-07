from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, current_timestamp, input_file_name
from src.utils.config import RAW_DATA_PATH, BRONZE_PLAYLISTS_PATH

def create_spark_session():
    """
    Create and return a Spark session for the Spotify Bronze ingestion job.
    """
    return SparkSession.builder \
        .appName("SpotifyBronzeIngestion") \
        .master("local[*]") \
        .getOrCreate()


def read_raw_json(spark, raw_path):
    """
    Read raw Spotify Million Playlist JSON file.
    """
    print(f"Reading raw JSON from: {raw_path}")

    raw_df = spark.read \
        .option("multiline", "true") \
        .json(raw_path)

    return raw_df


def transform_to_bronze(raw_df):
    """
    Convert raw nested JSON into Bronze playlist-level DataFrame.

    Bronze grain:
    One row per playlist.

    The tracks array remains nested.
    """

    playlists_df = raw_df.select(
        explode(col("playlists")).alias("playlist")
    )

    bronze_df = playlists_df.select(
        col("playlist.pid").alias("playlist_id"),
        col("playlist.name").alias("playlist_name"),
        col("playlist.collaborative").alias("collaborative"),
        col("playlist.modified_at").alias("modified_at"),
        col("playlist.num_tracks").alias("num_tracks"),
        col("playlist.num_albums").alias("num_albums"),
        col("playlist.num_followers").alias("num_followers"),
        col("playlist.num_edits").alias("num_edits"),
        col("playlist.duration_ms").alias("playlist_duration_ms"),
        col("playlist.tracks").alias("tracks"),
        current_timestamp().alias("ingestion_timestamp"),
        input_file_name().alias("source_file")
    )

    return bronze_df


def write_bronze_parquet(bronze_df, bronze_output_path):
    """
    Write Bronze DataFrame to Parquet.
    """
    print(f"Writing Bronze Parquet to: {bronze_output_path}")

    bronze_df.write \
        .mode("overwrite") \
        .parquet(bronze_output_path)


def validate_bronze_output(spark, bronze_output_path):
    """
    Read Bronze Parquet output and perform basic validation.
    """
    print("\nValidating Bronze output...")

    bronze_check_df = spark.read.parquet(bronze_output_path)

    print("\nBronze Schema:")
    bronze_check_df.printSchema()

    print("\nBronze Sample Records:")
    bronze_check_df.select(
        "playlist_id",
        "playlist_name",
        "num_tracks",
        "num_followers",
        "ingestion_timestamp"
    ).show(10, truncate=False)

    print("\nBronze Row Count:")
    print(bronze_check_df.count())


def main():
    spark = create_spark_session()

    raw_path = RAW_DATA_PATH
    bronze_output_path = BRONZE_PLAYLISTS_PATH

    print("Bronze ingestion job started.")
    print(f"Raw input path: {raw_path}")
    print(f"Bronze output path: {bronze_output_path}")

    raw_df = read_raw_json(spark, raw_path)

    bronze_df = transform_to_bronze(raw_df)

    print("\nTransformed Bronze DataFrame Preview:")
    bronze_df.select(
        "playlist_id",
        "playlist_name",
        "num_tracks",
        "num_followers"
    ).show(10, truncate=False)

    write_bronze_parquet(bronze_df, bronze_output_path)

    validate_bronze_output(spark, bronze_output_path)

    spark.stop()

    print("\nBronze ingestion job completed successfully.")


if __name__ == "__main__":
    main()