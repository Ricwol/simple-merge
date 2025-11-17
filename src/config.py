"""
Provide statically defined configuration values
used across the application.
"""

from typing import Final

APP_TITLE: Final[str] = "Simple PDF Merge"
DEFAULT_OUTPUT_FILENAME: Final[str] = "merged.pdf"

ARROW_BUTTON_SIZE: Final[int] = 1
BUTTON_WIDTH: Final[int] = 12
MERGE_BUTTON_FONT: Final[tuple[str, int, str]] = ("Helvetica", 14, "bold")
WINDOW_SIZE: Final[str] = "600x400"

BINDINGS: Final[dict[str, str]] = {
    "on_press": "<ButtonPress-1>",
    "on_drag": "<B1-Motion>",
    "on_delete": "<Delete>",
}
BUTTON_LABELS: Final[list[str]] = [
    "move_up",
    "move_down",
    "add_files",
    "remove_files",
    "clear_list",
    "merge",
]

# Logging configuration
LOG_FORMAT: Final[str] = "%(asctime)s %(levelname)s %(name)s: %(message)s"
LOG_DATEFMT: Final[str] = "%Y-%m-%d %H:%M:%S"

# Log file and rotation: rotate after 1MB and keep 3 backups
LOG_FILE: Final[str] = "simple_merge.log"
LOG_ROTATE_WHEN: Final[str] = "midnight"
LOG_ROTATE_INTERVAL: Final[int] = 1
LOG_BACKUP_COUNT: Final[int] = 3

# Optional: size based rotation fallback
LOG_MAX_BYTES: Final[int] = 1_000_000
LOG_BACKUP_COUNT_BYTES: Final[int] = 3
