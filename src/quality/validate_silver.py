from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def create_spark_session():
    """
    Create and return a Spark session for Silver validation.
    """
    return SparkSession.builder \
        .appName("ValidateSpotifySilverLayer") \
        .master("local[*]") \
        .getOrCreate()


def read_table(spark, path, table_name):
    """
    Read a Parquet table and print basic info.
    """
    print(f"\nReading {table_name} from: {path}")
    df = spark.read.parquet(path)

    print(f"{table_name} schema:")
    df.printSchema()

    print(f"{table_name} sample:")
    df.show(5, truncate=False)

    print(f"{table_name} row count: {df.count()}")

    return df


def validate_non_empty(df, table_name):
    """
    Check whether a table has at least one row.
    """
    print(f"\nValidating {table_name} is not empty...")

    row_count = df.count()

    if row_count > 0:
        print(f"PASSED: {table_name} has {row_count} rows.")
    else:
        print(f"FAILED: {table_name} is empty.")


def validate_null_id(df, table_name, id_column):
    """
    Check whether an ID column has null values.
    """
    print(f"\nValidating null IDs for {table_name}.{id_column}...")

    null_count = df.filter(col(id_column).isNull()).count()

    if null_count == 0:
        print(f"PASSED: No null values in {table_name}.{id_column}.")
    else:
        print(f"FAILED: {table_name}.{id_column} has {null_count} null values.")


def validate_duplicate_id(df, table_name, id_column):
    """
    Check whether a dimension table has duplicate IDs.
    """
    print(f"\nValidating duplicate IDs for {table_name}.{id_column}...")

    duplicate_df = df.groupBy(id_column).count().filter(col("count") > 1)
    duplicate_count = duplicate_df.count()

    if duplicate_count == 0:
        print(f"PASSED: No duplicate IDs in {table_name}.{id_column}.")
    else:
        print(f"FAILED: Found {duplicate_count} duplicate IDs in {table_name}.{id_column}.")
        duplicate_df.show(10, truncate=False)


def validate_playlist_track_references(playlists_df, playlist_tracks_df):
    """
    Check whether all playlist_tracks playlist_id values exist in playlists.
    """
    print("\nValidating playlist_tracks → playlists relationship...")

    missing_playlists_df = playlist_tracks_df.select("playlist_id").distinct() \
        .join(
            playlists_df.select("playlist_id").distinct(),
            on="playlist_id",
            how="left_anti"
        )

    missing_count = missing_playlists_df.count()

    if missing_count == 0:
        print("PASSED: All playlist_tracks.playlist_id values exist in playlists.")
    else:
        print(f"FAILED: {missing_count} playlist_id values in playlist_tracks are missing from playlists.")
        missing_playlists_df.show(10, truncate=False)


def validate_track_references(tracks_df, playlist_tracks_df):
    """
    Check whether all playlist_tracks track_id values exist in tracks.
    """
    print("\nValidating playlist_tracks → tracks relationship...")

    missing_tracks_df = playlist_tracks_df.select("track_id").distinct() \
        .join(
            tracks_df.select("track_id").distinct(),
            on="track_id",
            how="left_anti"
        )

    missing_count = missing_tracks_df.count()

    if missing_count == 0:
        print("PASSED: All playlist_tracks.track_id values exist in tracks.")
    else:
        print(f"FAILED: {missing_count} track_id values in playlist_tracks are missing from tracks.")
        missing_tracks_df.show(10, truncate=False)


def validate_summary_counts(playlists_df, playlist_tracks_df, tracks_df, artists_df, albums_df):
    """
    Print useful Silver layer summary counts.
    """
    print("\n=== Silver Layer Summary Counts ===")

    print(f"Playlists row count: {playlists_df.count()}")
    print(f"Playlist-track row count: {playlist_tracks_df.count()}")
    print(f"Tracks row count: {tracks_df.count()}")
    print(f"Artists row count: {artists_df.count()}")
    print(f"Albums row count: {albums_df.count()}")

    print(f"Distinct playlist IDs in playlists: {playlists_df.select('playlist_id').distinct().count()}")
    print(f"Distinct playlist IDs in playlist_tracks: {playlist_tracks_df.select('playlist_id').distinct().count()}")
    print(f"Distinct track IDs in playlist_tracks: {playlist_tracks_df.select('track_id').distinct().count()}")
    print(f"Distinct track IDs in tracks: {tracks_df.select('track_id').distinct().count()}")


def main():
    spark = create_spark_session()

    playlists_path = "data/silver/playlists/"
    playlist_tracks_path = "data/silver/playlist_tracks/"
    tracks_path = "data/silver/tracks/"
    artists_path = "data/silver/artists/"
    albums_path = "data/silver/albums/"

    print("Silver validation job started.")

    playlists_df = read_table(spark, playlists_path, "silver_playlists")
    playlist_tracks_df = read_table(spark, playlist_tracks_path, "silver_playlist_tracks")
    tracks_df = read_table(spark, tracks_path, "silver_tracks")
    artists_df = read_table(spark, artists_path, "silver_artists")
    albums_df = read_table(spark, albums_path, "silver_albums")

    validate_non_empty(playlists_df, "silver_playlists")
    validate_non_empty(playlist_tracks_df, "silver_playlist_tracks")
    validate_non_empty(tracks_df, "silver_tracks")
    validate_non_empty(artists_df, "silver_artists")
    validate_non_empty(albums_df, "silver_albums")

    validate_null_id(playlists_df, "silver_playlists", "playlist_id")
    validate_null_id(playlist_tracks_df, "silver_playlist_tracks", "playlist_id")
    validate_null_id(playlist_tracks_df, "silver_playlist_tracks", "track_id")
    validate_null_id(tracks_df, "silver_tracks", "track_id")
    validate_null_id(artists_df, "silver_artists", "artist_id")
    validate_null_id(albums_df, "silver_albums", "album_id")

    validate_duplicate_id(playlists_df, "silver_playlists", "playlist_id")
    validate_duplicate_id(tracks_df, "silver_tracks", "track_id")
    validate_duplicate_id(artists_df, "silver_artists", "artist_id")
    validate_duplicate_id(albums_df, "silver_albums", "album_id")

    validate_playlist_track_references(playlists_df, playlist_tracks_df)
    validate_track_references(tracks_df, playlist_tracks_df)

    validate_summary_counts(
        playlists_df,
        playlist_tracks_df,
        tracks_df,
        artists_df,
        albums_df
    )

    spark.stop()

    print("\nSilver validation job completed.")


if __name__ == "__main__":
    main()