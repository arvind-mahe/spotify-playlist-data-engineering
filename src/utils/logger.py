import logging
import os
from datetime import datetime


def get_logger(name: str):
    """
    Create and return a reusable logger.

    Logs are written to:
    1. Console
    2. logs/pipeline_YYYYMMDD.log
    """

    os.makedirs("logs", exist_ok=True)

    log_date = datetime.now().strftime("%Y%m%d")
    log_file = f"logs/pipeline_{log_date}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger