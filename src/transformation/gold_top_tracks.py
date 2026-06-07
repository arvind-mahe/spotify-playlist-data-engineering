from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct, desc


def create_spark_session():
    """
    Create and return a Spark session for Gold top tracks aggregation.
    """
    return SparkSession.builder \
        .appName("SpotifyGoldTopTracks") \
        .master("local[*]") \
        .getOrCreate()


def read_silver_table(spark, path, table_name):
    """
    Read a Silver Parquet table.
    """
    print(f"Reading {table_name} from: {path}")
    return spark.read.parquet(path)


def build_top_tracks(playlist_tracks_df, tracks_df):
    """
    Build Gold top_tracks table.

    Grain:
    One row per track.
    """

    track_counts_df = playlist_tracks_df.groupBy("track_id").agg(
        countDistinct("playlist_id").alias("playlist_count"),
        count("*").alias("total_appearances")
    )

    top_tracks_df = track_counts_df.join(
        tracks_df.select(
            "track_id",
            "track_name",
            "artist_id",
            "artist_name",
            "album_id",
            "album_name"
        ),
        on="track_id",
        how="left"
    ).select(
        col("track_id"),
        col("track_name"),
        col("artist_id"),
        col("artist_name"),
        col("album_id"),
        col("album_name"),
        col("playlist_count"),
        col("total_appearances")
    ).orderBy(
        desc("playlist_count"),
        desc("total_appearances"),
        col("track_name")
    )

    return top_tracks_df


def write_gold_table(df, output_path):
    """
    Write Gold table as Parquet.
    """
    print(f"Writing Gold top_tracks to: {output_path}")

    df.write \
        .mode("overwrite") \
        .parquet(output_path)


def validate_gold_top_tracks(spark, output_path):
    """
    Read back Gold top_tracks output and perform validation.
    """
    print("\nValidating Gold top_tracks output...")

    check_df = spark.read.parquet(output_path)

    print("\nGold Top Tracks Schema:")
    check_df.printSchema()

    print("\nTop 20 Tracks:")
    check_df.show(20, truncate=False)

    print("\nGold Top Tracks Row Count:")
    print(check_df.count())

    print("\nNull Track ID Count:")
    print(check_df.filter(col("track_id").isNull()).count())

    print("\nNull Track Name Count:")
    print(check_df.filter(col("track_name").isNull()).count())


def main():
    spark = create_spark_session()

    playlist_tracks_path = "data/silver/playlist_tracks/"
    tracks_path = "data/silver/tracks/"
    output_path = "data/gold/top_tracks/"

    print("Gold top_tracks transformation started.")
    print(f"Playlist tracks input path: {playlist_tracks_path}")
    print(f"Tracks input path: {tracks_path}")
    print(f"Gold output path: {output_path}")

    playlist_tracks_df = read_silver_table(
        spark,
        playlist_tracks_path,
        "silver_playlist_tracks"
    )

    tracks_df = read_silver_table(
        spark,
        tracks_path,
        "silver_tracks"
    )

    top_tracks_df = build_top_tracks(playlist_tracks_df, tracks_df)

    print("\nGold Top Tracks Preview:")
    top_tracks_df.show(20, truncate=False)

    write_gold_table(top_tracks_df, output_path)

    validate_gold_top_tracks(spark, output_path)

    spark.stop()

    print("\nGold top_tracks transformation completed successfully.")


if __name__ == "__main__":
    main()