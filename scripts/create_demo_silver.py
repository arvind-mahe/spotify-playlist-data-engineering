"""Generate a tiny SYNTHETIC Silver dataset, only for checking dbt setup.
Run from repository root: python scripts/create_demo_silver.py
Do NOT use demo statistics as project or resume metrics.
"""
from pathlib import Path
import duckdb

out = Path("data/silver")
for name in ("tracks", "playlist_tracks"):
    folder = out / name
    folder.mkdir(parents=True, exist_ok=True)
    if list(folder.glob("*.parquet")):
        raise SystemExit(f"Refusing to overwrite existing data: {folder}")
con = duckdb.connect()
con.execute("""COPY (SELECT * FROM (VALUES
    ('spotify:track:1','Demo Track A','a1','Demo Artist','b1','Demo Album'),
    ('spotify:track:2','Demo Track B','a2','Demo Artist 2','b2','Demo Album 2'))
    AS t(track_id,track_name,artist_id,artist_name,album_id,album_name))
    TO 'data/silver/tracks/demo.parquet' (FORMAT PARQUET)""")
con.execute("""COPY (SELECT * FROM (VALUES
    (1,'spotify:track:1',0),(1,'spotify:track:2',1),
    (2,'spotify:track:1',0))
    AS t(playlist_id,track_id,position))
    TO 'data/silver/playlist_tracks/demo.parquet' (FORMAT PARQUET)""")
print("Generated SYNTHETIC data; replace demo files with your real PySpark Silver outputs before claiming results.")
