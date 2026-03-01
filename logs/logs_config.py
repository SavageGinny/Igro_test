import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).parent.absolute()
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


LOG_FILE = LOG_DIR / f"database_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"


def setup_logging() -> logging.Logger:
    log: logging.Logger = logging.getLogger("database")
    log.setLevel(logging.INFO)

    handler: RotatingFileHandler = RotatingFileHandler(
        LOG_FILE,
        mode='a',
        maxBytes=5 * 1024 * 1024 * 100,
        backupCount=3
    )

    formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log


logger: logging.Logger = setup_logging()
