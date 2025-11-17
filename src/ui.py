"""
Provide the UI layer for the Simple Merge application.

This module builds and organizes all widgets used by the
application. It exposes a UI class that constructs layout
and allows the App layer to bind callbacks and interact
with the visual components.
"""

from collections.abc import Callable
import tkinter as tk

from tkinterdnd2 import TkinterDnD

import config
from logger import logger


class UI:
    """
    The `UI` builds and organizes visual components
    and delegates actions to the controlling instance.
    """

    def __init__(self, root: TkinterDnD.Tk) -> None:
        logger.info("build: ui start")
        self.root = root
        self.root.geometry(config.WINDOW_SIZE)

        self.drop_area: tk.Listbox
        self.buttons: dict[str, tk.Button] = {}

        self._setup_ui()
        logger.info("build: ui done")

    def _setup_ui(self) -> None:
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._setup_drag_and_drop_area(main_frame)
        self._setup_button_frame(main_frame)

    def _setup_drag_and_drop_area(self, parent: tk.Frame) -> None:
        """
        Create and place the listbox used for displaying dropped files.
        """
        self.drop_area = tk.Listbox(
            parent,
            selectmode=tk.EXTENDED,
            height=15,
            width=35
        )
        self.drop_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        logger.info("build: drop area")

    def _setup_button_frame(self, parent: tk.Frame) -> None:
        """Build the button frame and initialize action buttons."""
        button_frame = tk.Frame(parent)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self._setup_arrow_buttons(button_frame)
        self._setup_action_buttons(button_frame)
        self._setup_merge_button(button_frame)
        logger.info("build: button window")

    def _setup_arrow_buttons(self, parent: tk.Frame) -> None:
        """Create and place arrow action buttons."""
        arrow_frame = tk.Frame(parent)
        arrow_frame.pack(side=tk.LEFT, padx=5)

        self.buttons["move_up"] = tk.Button(
            arrow_frame,
            text="↑",
            width=config.ARROW_BUTTON_SIZE,
            height=config.ARROW_BUTTON_SIZE
        )
        self.buttons["move_up"].pack(pady=(40, 5))

        self.buttons["move_down"] = tk.Button(
            arrow_frame,
            text="↓",
            width=config.ARROW_BUTTON_SIZE,
            height=config.ARROW_BUTTON_SIZE
        )
        self.buttons["move_down"].pack(pady=(5, 40))
        logger.info("build: arrow buttons")

    def _setup_action_buttons(self, parent: tk.Frame) -> None:
        """Create and place file handling action buttons."""
        self.buttons["add_files"] = tk.Button(
            parent,
            text="Add File(s)",
            width=config.BUTTON_WIDTH
        )
        self.buttons["add_files"].place(relx=0.6, rely=0.4, anchor=tk.CENTER)

        # Define Remove File(s) and Clear buttons
        self.buttons["remove_files"] = tk.Button(
            parent,
            text="Remove File(s)",
            width=config.BUTTON_WIDTH
        )
        self.buttons["remove_files"].place(relx=0.6, rely=0.5, anchor=tk.CENTER)

        self.buttons["clear_list"] = tk.Button(
            parent,
            text="Clear All",
            width=config.BUTTON_WIDTH
        )
        self.buttons["clear_list"].place(relx=0.6, rely=0.6, anchor=tk.CENTER)
        logger.info("build: action buttons")

    def _setup_merge_button(self, parent: tk.Frame) -> None:
        """Create and place the merge action button."""     
        self.buttons["merge"] = tk.Button(
            parent,
            text="Merge",
            bg="green",
            fg="white",
            font=config.MERGE_BUTTON_FONT,
            width=20,
            height=2
        )
        self.buttons["merge"].pack(side=tk.BOTTOM, pady=20)
        logger.info("build: merge button")

    def add_title(self, title: str) -> None:
        """Apply a title to the UI's title label."""
        self.root.title(title)

    def bind(self, pattern: str, func: Callable) -> None:
        """Bind an event pattern to the drop area."""
        self.drop_area.bind(pattern, func)

    def dnd_bind(self, pattern: str, func: Callable) -> None:
        """Bind drag-and-drop event to the drop area."""
        self.drop_area.dnd_bind(pattern, func)

    def drop_target_register(self, drop_target: str) -> None:
        """Register the drop area as an active drag-and-drop target."""
        self.drop_area.drop_target_register(drop_target)

    def add_button_action(self, name: str, action: Callable) -> None:
        """Attach a callback to a button identified by its name."""
        button: tk.Button | None = self.buttons.get(name)
        if button:
            button.config(command=action)
