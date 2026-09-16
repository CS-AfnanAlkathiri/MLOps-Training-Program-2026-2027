import logging
from pathlib import Path

from src.config import PROJECT_ROOT, load_config


def setup_logging():
    """Configure logging to both console and file."""
    config = load_config()

    log_level = config["logging"]["level"]
    log_file = PROJECT_ROOT / config["logging"]["file"]

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
        force=True,
    )
