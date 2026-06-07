# Local data paths

RAW_DATA_PATH = "data/raw/mpd.slice.0-999.json"

BRONZE_PLAYLISTS_PATH = "data/bronze/playlists/"

SILVER_PLAYLISTS_PATH = "data/silver/playlists/"
SILVER_PLAYLIST_TRACKS_PATH = "data/silver/playlist_tracks/"
SILVER_TRACKS_PATH = "data/silver/tracks/"
SILVER_ARTISTS_PATH = "data/silver/artists/"
SILVER_ALBUMS_PATH = "data/silver/albums/"

GOLD_TOP_TRACKS_PATH = "data/gold/top_tracks/"
GOLD_TOP_ARTISTS_PATH = "data/gold/top_artists/"
GOLD_TOP_ALBUMS_PATH = "data/gold/top_albums/"
GOLD_PLAYLIST_SUMMARY_PATH = "data/gold/playlist_summary/"


# AWS S3 paths

S3_BUCKET = "spotify-million-playlist-data-lake-arvind-2026"
S3_BASE_PATH = f"s3://{S3_BUCKET}/spotify"

S3_RAW_PATH = f"{S3_BASE_PATH}/raw/"
S3_BRONZE_PATH = f"{S3_BASE_PATH}/bronze/"
S3_SILVER_PATH = f"{S3_BASE_PATH}/silver/"
S3_GOLD_PATH = f"{S3_BASE_PATH}/gold/"

S3_BRONZE_PLAYLISTS_PATH = f"{S3_BRONZE_PATH}playlists/"

S3_SILVER_PLAYLISTS_PATH = f"{S3_SILVER_PATH}playlists/"
S3_SILVER_PLAYLIST_TRACKS_PATH = f"{S3_SILVER_PATH}playlist_tracks/"
S3_SILVER_TRACKS_PATH = f"{S3_SILVER_PATH}tracks/"
S3_SILVER_ARTISTS_PATH = f"{S3_SILVER_PATH}artists/"
S3_SILVER_ALBUMS_PATH = f"{S3_SILVER_PATH}albums/"

S3_GOLD_TOP_TRACKS_PATH = f"{S3_GOLD_PATH}top_tracks/"
S3_GOLD_TOP_ARTISTS_PATH = f"{S3_GOLD_PATH}top_artists/"
S3_GOLD_TOP_ALBUMS_PATH = f"{S3_GOLD_PATH}top_albums/"
S3_GOLD_PLAYLIST_SUMMARY_PATH = f"{S3_GOLD_PATH}playlist_summary/"