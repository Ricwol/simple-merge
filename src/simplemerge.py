from pathlib import Path
import tkinter as tk

from tkinterdnd2 import TkinterDnD, DND_FILES


class SimpleMerge:

    def __init__(self, root: TkinterDnD.Tk) -> None:
        self.root = root
        self.root.title("Simple Merge")
        self.pdf_files: list[str] = []

        self.drop_area: tk.Listbox = tk.Listbox(
            root,
            selectmode=tk.EXTENDED,
            height=10,
            width=50
        )
        self.drop_area.pack(pady=20)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

    def on_drop(self, event: tk.Event) -> None:
        files: list[str] = self.root.tk.splitlist(event.data)
        for file in files:
            file_path = Path(file)
            if file_path.suffix.lower() == ".pdf":
                self.pdf_files.append(file)
                self.drop_area.insert(tk.END, file_path.name)
