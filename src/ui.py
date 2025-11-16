from collections.abc import Callable
import tkinter as tk

from tkinterdnd2 import TkinterDnD

import config

class UIManager:

    def __init__(self, root: TkinterDnD.Tk) -> None:
        self.root = root
        self.root.geometry(config.WINDOW_SIZE)

        self.drop_area: tk.Listbox

        self.move_up_button: tk.Button
        self.move_down_button: tk.Button
        self.add_files_button: tk.Button
        self.remove_files_button: tk.Button
        self.clear_list_button: tk.Button
        self.merge_button: tk.Button

        self._setup_ui()

    def _setup_ui(self) -> None:
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._setup_drag_and_drop_area(main_frame)
        self._setup_button_frame(main_frame)

    def _setup_drag_and_drop_area(self, parent: tk.Frame) -> None:
        self.drop_area = tk.Listbox(
            parent,
            selectmode=tk.EXTENDED,
            height=15,
            width=35
        )
        self.drop_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _setup_button_frame(self, parent: tk.Frame) -> None:
        button_frame = tk.Frame(parent)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self._setup_arrow_buttons(button_frame)
        self._setup_action_buttons(button_frame)
        self._setup_merge_button(button_frame)
    
    def _setup_arrow_buttons(self, parent: tk.Frame) -> None:
        arrow_frame = tk.Frame(parent)
        arrow_frame.pack(side=tk.LEFT, padx=5)

        self.move_up_button = tk.Button(
            arrow_frame,
            text="↑",
            width=config.ARROW_BUTTON_SIZE,
            height=config.ARROW_BUTTON_SIZE
        )
        self.move_up_button.pack(pady=(40, 5))

        self.move_down_button = tk.Button(
            arrow_frame,
            text="↓",
            width=config.ARROW_BUTTON_SIZE,
            height=config.ARROW_BUTTON_SIZE
        )
        self.move_down_button.pack(pady=(5, 40))

    def _setup_action_buttons(self, parent: tk.Frame) -> None:
        self.add_files_button = tk.Button(
            parent,
            text="Add File(s)",
            width=config.BUTTON_WIDTH
        )
        self.add_files_button.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

        # Define Remove File(s) and Clear buttons
        self.remove_files_button = tk.Button(
            parent,
            text="Remove File(s)",
            width=config.BUTTON_WIDTH
        )
        self.remove_files_button.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

        self.clear_list_button = tk.Button(
            parent,
            text="Clear All",
            width=config.BUTTON_WIDTH
        )
        self.clear_list_button.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    def _setup_merge_button(self, parent: tk.Frame) -> None:        
        self.merge_button = tk.Button(
            parent,
            text="Merge",
            bg="green",
            fg="white",
            font=config.MERGE_BUTTON_FONT,
            width=20,
            height=2
        )
        self.merge_button.pack(side=tk.BOTTOM, pady=20)

    def add_title(self, title: str) -> None:
        self.root.title(title)

    def bind(self, pattern: str, func: Callable) -> None:
        self.drop_area.bind(pattern, func)
    
    def dnd_bind(self, pattern: str, func: Callable) -> None:
        self.drop_area.dnd_bind(pattern, func)

    def drop_target_register(self, drop_target: str) -> None:
        self.drop_area.drop_target_register(drop_target)

    def add_button_action(self, label: str, action: Callable) -> None:
        button: tk.Button = getattr(self, f"{label}_button")
        button.config(command=action)
