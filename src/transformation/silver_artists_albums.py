from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, trim


def create_spark_session():
    """
    Create and return a Spark session for Silver artists and albums transformations.
    """
    return SparkSession.builder \
        .appName("SpotifySilverArtistsAlbums") \
        .master("local[*]") \
        .getOrCreate()


def read_bronze_playlists(spark, bronze_path):
    """
    Read Bronze playlist Parquet data.
    """
    print(f"Reading Bronze playlists from: {bronze_path}")
    return spark.read.parquet(bronze_path)


def explode_tracks(bronze_df):
    """
    Explode nested tracks from Bronze playlists.
    """
    return bronze_df.select(
        explode(col("tracks")).alias("track"),
        col("ingestion_timestamp"),
        col("source_file")
    )


def transform_to_silver_artists(exploded_tracks_df):
    """
    Create deduplicated Silver artists table.

    Grain:
    One row per unique artist.
    """
    artists_df = exploded_tracks_df.select(
        col("track.artist_uri").alias("artist_id"),
        trim(col("track.artist_name")).alias("artist_name"),
        col("ingestion_timestamp"),
        col("source_file")
    )

    silver_artists_df = artists_df.dropDuplicates(["artist_id"])

    return silver_artists_df


def transform_to_silver_albums(exploded_tracks_df):
    """
    Create deduplicated Silver albums table.

    Grain:
    One row per unique album.
    """
    albums_df = exploded_tracks_df.select(
        col("track.album_uri").alias("album_id"),
        trim(col("track.album_name")).alias("album_name"),
        col("track.artist_uri").alias("artist_id"),
        trim(col("track.artist_name")).alias("artist_name"),
        col("ingestion_timestamp"),
        col("source_file")
    )

    silver_albums_df = albums_df.dropDuplicates(["album_id"])

    return silver_albums_df


def write_parquet(df, output_path, table_name):
    """
    Write a DataFrame as Parquet.
    """
    print(f"Writing Silver {table_name} to: {output_path}")

    df.write \
        .mode("overwrite") \
        .parquet(output_path)


def validate_table(spark, output_path, table_name, id_column):
    """
    Read back a Silver table and perform basic validation.
    """
    print(f"\nValidating Silver {table_name} output...")

    check_df = spark.read.parquet(output_path)

    print(f"\nSilver {table_name} Schema:")
    check_df.printSchema()

    print(f"\nSilver {table_name} Sample:")
    check_df.show(10, truncate=False)

    row_count = check_df.count()
    distinct_id_count = check_df.select(id_column).distinct().count()
    null_id_count = check_df.filter(col(id_column).isNull()).count()

    print(f"\nSilver {table_name} Row Count:")
    print(row_count)

    print(f"\nDistinct {id_column} Count:")
    print(distinct_id_count)

    print(f"\nNull {id_column} Count:")
    print(null_id_count)


def main():
    spark = create_spark_session()

    bronze_path = "data/bronze/playlists/"
    artists_output_path = "data/silver/artists/"
    albums_output_path = "data/silver/albums/"

    print("Silver artists and albums transformation started.")
    print(f"Bronze input path: {bronze_path}")
    print(f"Artists output path: {artists_output_path}")
    print(f"Albums output path: {albums_output_path}")

    bronze_df = read_bronze_playlists(spark, bronze_path)

    exploded_tracks_df = explode_tracks(bronze_df)

    silver_artists_df = transform_to_silver_artists(exploded_tracks_df)
    silver_albums_df = transform_to_silver_albums(exploded_tracks_df)

    print("\nTransformed Silver Artists Preview:")
    silver_artists_df.show(10, truncate=False)

    print("\nTransformed Silver Albums Preview:")
    silver_albums_df.show(10, truncate=False)

    write_parquet(silver_artists_df, artists_output_path, "artists")
    write_parquet(silver_albums_df, albums_output_path, "albums")

    validate_table(spark, artists_output_path, "artists", "artist_id")
    validate_table(spark, albums_output_path, "albums", "album_id")

    spark.stop()

    print("\nSilver artists and albums transformation completed successfully.")


if __name__ == "__main__":
    main()