"""Inspect actual Silver Parquet record counts and input/output byte sizes."""
from pathlib import Path
import duckdb

base = Path('data/silver')
con = duckdb.connect()
for name in ('playlists', 'playlist_tracks', 'tracks', 'artists', 'albums'):
    folder = base / name
    files = list(folder.rglob('*.parquet'))
    if not files:
        print(f'{name}: missing Silver data')
        continue
    n = con.execute('SELECT COUNT(*) FROM read_parquet(?)', [str(folder / '**/*.parquet')]).fetchone()[0]
    size = sum(f.stat().st_size for f in files)
    print(f'{name}: rows={n:,}, parquet_bytes={size:,}, files={len(files)}')
raw = Path('data/raw')
raw_bytes = sum(p.stat().st_size for p in raw.rglob('*.json')) if raw.exists() else 0
silver_bytes = sum(p.stat().st_size for p in base.rglob('*.parquet')) if base.exists() else 0
print(f'Raw JSON bytes={raw_bytes:,}; Silver Parquet bytes={silver_bytes:,}')
print('NOTE: These are not comparable storage-savings metrics unless equivalent records and table scopes are compared.')
