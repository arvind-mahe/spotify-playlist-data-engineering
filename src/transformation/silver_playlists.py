from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim


def create_spark_session():
    """
    Create and return a Spark session for Silver playlist transformation.
    """
    return SparkSession.builder \
        .appName("SpotifySilverPlaylists") \
        .master("local[*]") \
        .getOrCreate()


def read_bronze_playlists(spark, bronze_path):
    """
    Read Bronze playlist Parquet data.
    """
    print(f"Reading Bronze playlists from: {bronze_path}")
    return spark.read.parquet(bronze_path)


def transform_to_silver_playlists(bronze_df):
    """
    Transform Bronze playlist data into a clean Silver playlists table.

    Silver playlists grain:
    One row per playlist.
    """

    silver_playlists_df = bronze_df.select(
        col("playlist_id").cast("long").alias("playlist_id"),
        trim(col("playlist_name")).alias("playlist_name"),
        col("collaborative").alias("collaborative"),
        col("modified_at").cast("long").alias("modified_at"),
        col("num_tracks").cast("long").alias("num_tracks"),
        col("num_albums").cast("long").alias("num_albums"),
        col("num_followers").cast("long").alias("num_followers"),
        col("num_edits").cast("long").alias("num_edits"),
        col("playlist_duration_ms").cast("long").alias("playlist_duration_ms"),
        col("ingestion_timestamp"),
        col("source_file")
    )

    return silver_playlists_df


def write_silver_playlists(silver_df, silver_output_path):
    """
    Write Silver playlists table as Parquet.
    """
    print(f"Writing Silver playlists to: {silver_output_path}")

    silver_df.write \
        .mode("overwrite") \
        .parquet(silver_output_path)


def validate_silver_playlists(spark, silver_output_path):
    """
    Read back Silver playlists output and perform basic validation.
    """
    print("\nValidating Silver playlists output...")

    silver_check_df = spark.read.parquet(silver_output_path)

    print("\nSilver Playlists Schema:")
    silver_check_df.printSchema()

    print("\nSilver Playlists Sample:")
    silver_check_df.show(10, truncate=False)

    print("\nSilver Playlists Row Count:")
    print(silver_check_df.count())


def main():
    spark = create_spark_session()

    bronze_path = "data/bronze/playlists/"
    silver_output_path = "data/silver/playlists/"

    print("Silver playlists transformation started.")
    print(f"Bronze input path: {bronze_path}")
    print(f"Silver output path: {silver_output_path}")

    bronze_df = read_bronze_playlists(spark, bronze_path)

    silver_playlists_df = transform_to_silver_playlists(bronze_df)

    print("\nTransformed Silver Playlists Preview:")
    silver_playlists_df.show(10, truncate=False)

    write_silver_playlists(silver_playlists_df, silver_output_path)

    validate_silver_playlists(spark, silver_output_path)

    spark.stop()

    print("\nSilver playlists transformation completed successfully.")


if __name__ == "__main__":
    main()