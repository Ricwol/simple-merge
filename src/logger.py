"""
Configure a basic application-wide logger.

Modules import `logger` from here to produce structured logs.
Adjust logging behavior centrally if needed.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import (
    LOG_BACKUP_COUNT,
    LOG_DATEFMT,
    LOG_FILE,
    LOG_FORMAT,
    LOG_MAX_BYTES,
)

# Ensure logs directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / LOG_FILE

formatter = logging.Formatter(LOG_FORMAT, LOG_DATEFMT)

# file handler for logs with backups
file_handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=LOG_MAX_BYTES,
    backupCount=LOG_BACKUP_COUNT,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# console handler for development
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# configure global logger
logger = logging.getLogger("simplemerge")
logger.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
