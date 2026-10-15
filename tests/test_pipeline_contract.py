from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_modules_have_valid_python_syntax():
    for source in (ROOT / 'src').rglob('*.py'):
        ast.parse(source.read_text(encoding='utf-8'), filename=str(source))


def test_expected_pipeline_layers_present():
    required = [
        'src/ingestion/bronze_ingestion.py',
        'src/transformation/silver_tracks.py',
        'src/transformation/silver_playlist_tracks.py',
        'src/transformation/gold_top_tracks.py',
    ]
    for name in required:
        assert (ROOT / name).is_file(), f'Missing pipeline module: {name}'
