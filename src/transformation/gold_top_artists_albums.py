from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct, desc


def create_spark_session():
    """
    Create and return a Spark session for Gold artist and album aggregations.
    """
    return SparkSession.builder \
        .appName("SpotifyGoldTopArtistsAlbums") \
        .master("local[*]") \
        .getOrCreate()


def read_silver_table(spark, path, table_name):
    """
    Read a Silver Parquet table.
    """
    print(f"Reading {table_name} from: {path}")
    return spark.read.parquet(path)


def build_track_playlist_fact(playlist_tracks_df, tracks_df):
    """
    Join playlist-track relationships with track metadata.

    Grain:
    One row per track placement inside a playlist.
    """
    fact_df = playlist_tracks_df.join(
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
    )

    return fact_df


def build_top_artists(fact_df):
    """
    Build Gold top_artists table.

    Grain:
    One row per artist.
    """
    top_artists_df = fact_df.groupBy(
        "artist_id",
        "artist_name"
    ).agg(
        countDistinct("playlist_id").alias("playlist_count"),
        count("*").alias("track_appearance_count"),
        countDistinct("track_id").alias("unique_track_count")
    ).orderBy(
        desc("playlist_count"),
        desc("track_appearance_count"),
        col("artist_name")
    )

    return top_artists_df


def build_top_albums(fact_df):
    """
    Build Gold top_albums table.

    Grain:
    One row per album.
    """
    top_albums_df = fact_df.groupBy(
        "album_id",
        "album_name",
        "artist_id",
        "artist_name"
    ).agg(
        countDistinct("playlist_id").alias("playlist_count"),
        count("*").alias("track_appearance_count"),
        countDistinct("track_id").alias("unique_track_count")
    ).orderBy(
        desc("playlist_count"),
        desc("track_appearance_count"),
        col("album_name")
    )

    return top_albums_df


def write_gold_table(df, output_path, table_name):
    """
    Write Gold table as Parquet.
    """
    print(f"Writing Gold {table_name} to: {output_path}")

    df.write \
        .mode("overwrite") \
        .parquet(output_path)


def validate_gold_table(spark, output_path, table_name, id_column):
    """
    Read back a Gold table and perform validation.
    """
    print(f"\nValidating Gold {table_name} output...")

    check_df = spark.read.parquet(output_path)

    print(f"\nGold {table_name} Schema:")
    check_df.printSchema()

    print(f"\nTop 20 rows from {table_name}:")
    check_df.show(20, truncate=False)

    print(f"\nGold {table_name} Row Count:")
    print(check_df.count())

    print(f"\nNull {id_column} Count:")
    print(check_df.filter(col(id_column).isNull()).count())


def main():
    spark = create_spark_session()

    playlist_tracks_path = "data/silver/playlist_tracks/"
    tracks_path = "data/silver/tracks/"

    top_artists_output_path = "data/gold/top_artists/"
    top_albums_output_path = "data/gold/top_albums/"

    print("Gold top artists and albums transformation started.")
    print(f"Playlist tracks input path: {playlist_tracks_path}")
    print(f"Tracks input path: {tracks_path}")
    print(f"Top artists output path: {top_artists_output_path}")
    print(f"Top albums output path: {top_albums_output_path}")

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

    fact_df = build_track_playlist_fact(playlist_tracks_df, tracks_df)

    top_artists_df = build_top_artists(fact_df)
    top_albums_df = build_top_albums(fact_df)

    print("\nGold Top Artists Preview:")
    top_artists_df.show(20, truncate=False)

    print("\nGold Top Albums Preview:")
    top_albums_df.show(20, truncate=False)

    write_gold_table(top_artists_df, top_artists_output_path, "top_artists")
    write_gold_table(top_albums_df, top_albums_output_path, "top_albums")

    validate_gold_table(
        spark,
        top_artists_output_path,
        "top_artists",
        "artist_id"
    )

    validate_gold_table(
        spark,
        top_albums_output_path,
        "top_albums",
        "album_id"
    )

    spark.stop()

    print("\nGold top artists and albums transformation completed successfully.")


if __name__ == "__main__":
    main()