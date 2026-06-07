from src.ingestion.bronze_ingestion import main as run_bronze_ingestion

from src.transformation.silver_playlists import main as run_silver_playlists
from src.transformation.silver_playlist_tracks import main as run_silver_playlist_tracks
from src.transformation.silver_tracks import main as run_silver_tracks
from src.transformation.silver_artists_albums import main as run_silver_artists_albums

from src.transformation.gold_top_tracks import main as run_gold_top_tracks
from src.transformation.gold_top_artists_albums import main as run_gold_top_artists_albums
from src.transformation.gold_playlist_summary import main as run_gold_playlist_summary

from src.utils.logger import get_logger


logger = get_logger(__name__)


def run_step(step_number, total_steps, step_name, step_function):
    """
    Run a single pipeline step with logging and error handling.
    """

    logger.info("=" * 80)
    logger.info(f"[{step_number}/{total_steps}] STARTED: {step_name}")

    try:
        step_function()
        logger.info(f"[{step_number}/{total_steps}] COMPLETED: {step_name}")
    except Exception as error:
        logger.exception(f"[{step_number}/{total_steps}] FAILED: {step_name}")
        raise error


def run_pipeline():
    """
    Run the full Spotify Million Playlist data pipeline.

    Pipeline order:
    1. Bronze ingestion
    2. Silver transformations
    3. Gold aggregations
    """

    logger.info("=" * 80)
    logger.info("Spotify Million Playlist Data Pipeline Started")
    logger.info("=" * 80)

    pipeline_steps = [
        ("Bronze ingestion", run_bronze_ingestion),
        ("Silver playlists transformation", run_silver_playlists),
        ("Silver playlist_tracks transformation", run_silver_playlist_tracks),
        ("Silver tracks transformation", run_silver_tracks),
        ("Silver artists and albums transformation", run_silver_artists_albums),
        ("Gold top_tracks aggregation", run_gold_top_tracks),
        ("Gold top_artists and top_albums aggregation", run_gold_top_artists_albums),
        ("Gold playlist_summary aggregation", run_gold_playlist_summary),
    ]

    total_steps = len(pipeline_steps)

    for index, (step_name, step_function) in enumerate(pipeline_steps, start=1):
        run_step(index, total_steps, step_name, step_function)

    logger.info("=" * 80)
    logger.info("Spotify Million Playlist Data Pipeline Completed Successfully")
    logger.info("=" * 80)


if __name__ == "__main__":
    run_pipeline()