from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder \
        .appName("SpotifyMillionPlaylistPipeline") \
        .master("local[*]") \
        .getOrCreate()

    print("Spark session created successfully.")
    print(f"Spark version: {spark.version}")

    sample_data = [
        (1, "workout playlist", 50),
        (2, "chill playlist", 80),
        (3, "study playlist", 35)
    ]

    columns = ["playlist_id", "playlist_name", "num_tracks"]

    df = spark.createDataFrame(sample_data, columns)

    print("Sample DataFrame:")
    df.show()

    spark.stop()


if __name__ == "__main__":
    main()