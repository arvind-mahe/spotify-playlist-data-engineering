from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, size


def create_spark_session():
    """
    Create and return a Spark session for Bronze validation.
    """
    return SparkSession.builder \
        .appName("ValidateSpotifyBronzeLayer") \
        .master("local[*]") \
        .getOrCreate()


def validate_required_columns(df, required_columns):
    """
    Check whether all required columns exist in the Bronze DataFrame.
    """
    print("\nValidating required columns...")

    actual_columns = df.columns
    missing_columns = [column for column in required_columns if column not in actual_columns]

    if missing_columns:
        print("FAILED: Missing required columns:")
        for column in missing_columns:
            print(f"- {column}")
    else:
        print("PASSED: All required columns exist.")


def validate_row_count(df):
    """
    Check whether Bronze table has records.
    """
    print("\nValidating row count...")

    row_count = df.count()
    print(f"Bronze row count: {row_count}")

    if row_count > 0:
        print("PASSED: Bronze table has records.")
    else:
        print("FAILED: Bronze table is empty.")


def validate_null_playlist_ids(df):
    """
    Check for null playlist IDs.
    """
    print("\nValidating null playlist IDs...")

    null_count = df.filter(col("playlist_id").isNull()).count()
    print(f"Null playlist_id count: {null_count}")

    if null_count == 0:
        print("PASSED: No null playlist IDs.")
    else:
        print("FAILED: Null playlist IDs found.")


def validate_duplicate_playlist_ids(df):
    """
    Check for duplicate playlist IDs.
    """
    print("\nValidating duplicate playlist IDs...")

    duplicate_df = df.groupBy("playlist_id") \
        .count() \
        .filter(col("count") > 1)

    duplicate_count = duplicate_df.count()
    print(f"Duplicate playlist_id count: {duplicate_count}")

    if duplicate_count == 0:
        print("PASSED: No duplicate playlist IDs.")
    else:
        print("FAILED: Duplicate playlist IDs found.")
        duplicate_df.show(10, truncate=False)


def validate_tracks_array(df):
    """
    Check whether tracks array exists and is not empty.
    """
    print("\nValidating tracks array...")

    null_tracks_count = df.filter(col("tracks").isNull()).count()
    empty_tracks_count = df.filter(size(col("tracks")) == 0).count()

    print(f"Null tracks array count: {null_tracks_count}")
    print(f"Empty tracks array count: {empty_tracks_count}")

    if null_tracks_count == 0 and empty_tracks_count == 0:
        print("PASSED: Tracks array exists and is not empty.")
    else:
        print("FAILED: Some playlists have null or empty tracks arrays.")


def validate_num_tracks_matches_array_size(df):
    """
    Check whether num_tracks matches the actual number of tracks in the tracks array.
    """
    print("\nValidating num_tracks against tracks array size...")

    mismatch_df = df.filter(col("num_tracks") != size(col("tracks")))
    mismatch_count = mismatch_df.count()

    print(f"num_tracks mismatch count: {mismatch_count}")

    if mismatch_count == 0:
        print("PASSED: num_tracks matches tracks array size.")
    else:
        print("FAILED: num_tracks does not match tracks array size for some playlists.")
        mismatch_df.select(
            "playlist_id",
            "playlist_name",
            "num_tracks"
        ).show(10, truncate=False)


def show_basic_null_counts(df):
    """
    Show null counts for important Bronze columns.
    """
    print("\nBasic null counts:")

    important_columns = [
        "playlist_id",
        "playlist_name",
        "collaborative",
        "modified_at",
        "num_tracks",
        "num_albums",
        "num_followers",
        "num_edits",
        "playlist_duration_ms",
        "tracks",
        "ingestion_timestamp",
        "source_file"
    ]

    null_counts_df = df.select([
        count(when(col(column).isNull(), column)).alias(column)
        for column in important_columns
    ])

    null_counts_df.show(truncate=False)


def main():
    spark = create_spark_session()

    bronze_path = "data/bronze/playlists/"

    print("Bronze validation job started.")
    print(f"Bronze input path: {bronze_path}")

    bronze_df = spark.read.parquet(bronze_path)

    print("\nBronze Schema:")
    bronze_df.printSchema()

    required_columns = [
        "playlist_id",
        "playlist_name",
        "collaborative",
        "modified_at",
        "num_tracks",
        "num_albums",
        "num_followers",
        "num_edits",
        "playlist_duration_ms",
        "tracks",
        "ingestion_timestamp",
        "source_file"
    ]

    validate_required_columns(bronze_df, required_columns)
    validate_row_count(bronze_df)
    validate_null_playlist_ids(bronze_df)
    validate_duplicate_playlist_ids(bronze_df)
    validate_tracks_array(bronze_df)
    validate_num_tracks_matches_array_size(bronze_df)
    show_basic_null_counts(bronze_df)

    spark.stop()

    print("\nBronze validation job completed.")


if __name__ == "__main__":
    main()