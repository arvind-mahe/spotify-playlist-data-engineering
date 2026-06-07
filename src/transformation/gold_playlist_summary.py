from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    count,
    countDistinct,
    lit,
    max,
    min,
    round
)


def create_spark_session():
    """
    Create and return a Spark session for Gold playlist summary aggregation.
    """
    return SparkSession.builder \
        .appName("SpotifyGoldPlaylistSummary") \
        .master("local[*]") \
        .getOrCreate()


def read_silver_table(spark, path, table_name):
    """
    Read a Silver Parquet table.
    """
    print(f"Reading {table_name} from: {path}")
    return spark.read.parquet(path)


def build_playlist_summary(
    playlists_df,
    playlist_tracks_df,
    tracks_df,
    artists_df,
    albums_df
):
    """
    Build one-row Gold playlist summary table.
    """

    playlist_metrics_df = playlists_df.agg(
        count("*").alias("total_playlists"),
        round(avg("num_tracks"), 2).alias("average_tracks_per_playlist"),
        round(avg("num_followers"), 2).alias("average_followers_per_playlist"),
        max("num_tracks").alias("max_tracks_in_playlist"),
        min("num_tracks").alias("min_tracks_in_playlist")
    )

    playlist_track_metrics_df = playlist_tracks_df.agg(
        count("*").alias("total_playlist_track_rows"),
        countDistinct("track_id").alias("unique_tracks_from_playlist_tracks")
    )

    tracks_metrics_df = tracks_df.agg(
        countDistinct("track_id").alias("unique_tracks")
    )

    artists_metrics_df = artists_df.agg(
        countDistinct("artist_id").alias("unique_artists")
    )

    albums_metrics_df = albums_df.agg(
        countDistinct("album_id").alias("unique_albums")
    )

    summary_df = playlist_metrics_df \
        .crossJoin(playlist_track_metrics_df) \
        .crossJoin(tracks_metrics_df) \
        .crossJoin(artists_metrics_df) \
        .crossJoin(albums_metrics_df) \
        .withColumn("summary_level", lit("dataset"))

    summary_df = summary_df.select(
        "summary_level",
        "total_playlists",
        "total_playlist_track_rows",
        "unique_tracks",
        "unique_artists",
        "unique_albums",
        "average_tracks_per_playlist",
        "average_followers_per_playlist",
        "max_tracks_in_playlist",
        "min_tracks_in_playlist"
    )

    return summary_df


def write_gold_table(df, output_path):
    """
    Write Gold playlist_summary table as Parquet.
    """
    print(f"Writing Gold playlist_summary to: {output_path}")

    df.write \
        .mode("overwrite") \
        .parquet(output_path)


def validate_playlist_summary(spark, output_path):
    """
    Read back Gold playlist_summary output and validate it.
    """
    print("\nValidating Gold playlist_summary output...")

    check_df = spark.read.parquet(output_path)

    print("\nGold Playlist Summary Schema:")
    check_df.printSchema()

    print("\nGold Playlist Summary:")
    check_df.show(truncate=False)

    print("\nGold Playlist Summary Row Count:")
    print(check_df.count())


def main():
    spark = create_spark_session()

    playlists_path = "data/silver/playlists/"
    playlist_tracks_path = "data/silver/playlist_tracks/"
    tracks_path = "data/silver/tracks/"
    artists_path = "data/silver/artists/"
    albums_path = "data/silver/albums/"
    output_path = "data/gold/playlist_summary/"

    print("Gold playlist_summary transformation started.")

    playlists_df = read_silver_table(
        spark,
        playlists_path,
        "silver_playlists"
    )

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

    artists_df = read_silver_table(
        spark,
        artists_path,
        "silver_artists"
    )

    albums_df = read_silver_table(
        spark,
        albums_path,
        "silver_albums"
    )

    playlist_summary_df = build_playlist_summary(
        playlists_df,
        playlist_tracks_df,
        tracks_df,
        artists_df,
        albums_df
    )

    print("\nGold Playlist Summary Preview:")
    playlist_summary_df.show(truncate=False)

    write_gold_table(playlist_summary_df, output_path)

    validate_playlist_summary(spark, output_path)

    spark.stop()

    print("\nGold playlist_summary transformation completed successfully.")


if __name__ == "__main__":
    main()