from typing import Final

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