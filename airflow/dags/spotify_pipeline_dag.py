
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

from airflow.sdk import dag, task

# Project folder: Spotify_IBM_Day1_Ready
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Use the existing Linux environment for PySpark and dbt
PYTHON = PROJECT_ROOT / ".venv_linux" / "bin" / "python"
DBT = PROJECT_ROOT / ".venv_linux" / "bin" / "dbt"

RAW_FILE = PROJECT_ROOT / "data/raw/mpd.slice.0-999.json"


def run_command(command, timeout=1800):
    """Run a command and fail the Airflow task if it fails."""
    subprocess.run(
        [str(part) for part in command],
        cwd=str(PROJECT_ROOT),
        check=True,
        timeout=timeout,
    )


@dag(
    dag_id="spotify_analytics_pipeline",
    description="Spotify PySpark and dbt analytics pipeline",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["spotify", "pyspark", "dbt", "ibm"],
)
def spotify_analytics_pipeline():

    @task
    def validate_input():
        import json

        if not RAW_FILE.is_file():
            raise FileNotFoundError(f"Missing dataset: {RAW_FILE}")

        with RAW_FILE.open(encoding="utf-8") as f:
            data = json.load(f)

        playlists = data["playlists"]
        count = len(playlists)
        occurrences = sum(len(p["tracks"]) for p in playlists)

        if count == 0 or occurrences == 0:
            raise ValueError("Spotify input dataset is empty")

        print(f"Playlists: {count}")
        print(f"Track occurrences: {occurrences}")

    @task
    def run_pyspark():
        run_command(
            [PYTHON, "-m", "src.main"],
            timeout=3600,
        )
        print("PySpark pipeline completed")

    @task
    def run_dbt():
        run_command(
            [
                DBT,
                "build",
                "--project-dir",
                "dbt_project",
                "--profiles-dir",
                "dbt_project",
            ]
        )
        print("dbt models and data-quality tests passed")

    @task
    def verify_outputs():
        for table in ["playlists", "playlist_tracks", "tracks"]:
            folder = PROJECT_ROOT / "data" / "silver" / table

            if not folder.is_dir() or not list(folder.rglob("*.parquet")):
                raise FileNotFoundError(
                    f"Missing Silver Parquet data: {folder}"
                )

        run_command(
            [PYTHON, "scripts/inspect_silver_metrics.py"]
        )

        print("Silver outputs verified")

    input_task = validate_input()
    spark_task = run_pyspark()
    dbt_task = run_dbt()
    verification_task = verify_outputs()

    input_task >> spark_task >> dbt_task >> verification_task


spotify_analytics_pipeline()
