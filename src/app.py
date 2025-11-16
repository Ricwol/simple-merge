"""
Coordinate interactions between the UI and PDF merger logic.

The `App` class binds events, handles file operations, updates
the UI state, and controls the merge workflow.
"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES

from config import (
    BINDINGS,
    BUTTON_LABELS,
    DEFAULT_OUTPUT_FILENAME
)
from logger import logger
from pdfmerger import PDFMerger
from ui import UI


class App:
    """
    Control overall application behavior, connect UI callbacks,
    and synchronize UI state with the PDFMerger model.
    """
    title = "Simple Merge"

    def __init__(self, ui: UI, merger: PDFMerger) -> None:
        logger.info("init: app")
        self.ui = ui
        self.merger = merger

        self.ui.add_title(self.title)

        logger.info("bind: events")
        self.ui.drop_target_register(DND_FILES)
        self.ui.dnd_bind("<<Drop>>", self.on_drop)

        for func_name, pattern in BINDINGS.items():
            self.ui.bind(pattern, getattr(self, func_name))

        for label in BUTTON_LABELS:
            self.ui.add_button_action(label, action=getattr(self, label))

    def on_drop(self, event: tk.Event) -> None:
        """Handle files dropped into the listbox via drag-and-drop."""
        files = self.ui.root.tk.splitlist(event.data)
        logger.info(f"drop: received {len(files)} file(s)")
        self.merger.add_files(files)
        logger.info(f"add: accepted {len(self.merger)} file(s)")
        self._update_drop_area()

    def add_files(self) -> None:
        """Open a selection dialog to choose PDF files."""
        logger.info("open: file dialog")
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not files:
            logger.info("open: file dialog cancelled")
            return
        
        self.merger.add_files(files)
        logger.info(f"add: accepted {len(self.merger)} file(s) from dialog")
        self._update_drop_area()

    def move_up(self) -> None:
        """Move the selected file one position up."""
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices or selected_indices[0] == 0:
            return
        
        index = selected_indices[0]
        self.merger.swap_files(index, index - 1)
        logger.info(f"move: up index {index}")
        self._update_drop_area()
        self.ui.drop_area.select_set(index - 1)

    def move_down(self) -> None:
        """Move the selected file one position down."""
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices or selected_indices[0] == len(self.merger) - 1:
            return
        
        index = selected_indices[0]
        self.merger.swap_files(index, index + 1)
        logger.info(f"move: down index {index}")
        self._update_drop_area()
        self.ui.drop_area.select_set(index + 1)

    def remove_files(self) -> None:
        """Remove the selected file entries from the list."""
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices:
            return
        
        self.merger.remove_files(selected_indices)
        logger.info(f"remove: indices {selected_indices}")
        self._update_drop_area()

    def clear_list(self) -> None:
        """Clear all files from the list."""
        logger.info(f"clear: files")
        self.merger.clear_files()
        self._update_drop_area()

    def merge(self) -> None:
        """Perform merge operation and prompt user to save output."""
        if not self.merger._pdf_files:
            messagebox.showerror(title="Error", message="No PDFs selected!")
            return
        
        if len(self.merger) == 1:
            messagebox.showerror(
                title="Error",
                message="Can't merge only one PDF file!"
            )
            return

        output_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=DEFAULT_OUTPUT_FILENAME,
            title="Save merged PDF as..."
        )
        if not output_filename:
            return
        
        self.ui.merge_button.config(state=tk.DISABLED)
        logger.info(f"merge: start {len(self.merger)} file(s)")
        self.merger.merge_pdfs(output_filename)
        logger.info(f"merge: success {output_filename}")

        messagebox.showinfo(
            title="Success",
            message=f"PDFs merged to {output_filename}"
        )
        self.merger.clear_files()
        self._update_drop_area()
        self.ui.merge_button.config(state=tk.NORMAL)

    def on_press(self, event: tk.Event) -> None:
        """Record the starting index for drag-based reordering."""
        logger.info("drag: press")
        self.merger.drag_index = self.ui.drop_area.nearest(event.y)

    def on_drag(self, event: tk.Event) -> None:
        """Reorder files dynamically based on drag position."""
        new_index = self.ui.drop_area.nearest(event.y)
        logger.info(f"drag: move to {new_index}")
        self.merger.move_file(new_index)
        self._update_drop_area()

    def _update_drop_area(self) -> None:
        """Refresh the listbox to reflect current merger state."""
        self.ui.drop_area.delete(0, tk.END)
        for file in self.merger:
            self.ui.drop_area.insert(tk.END, Path(file).name)

    def on_delete(self, _: tk.Event) -> None:
        """Remove file entries using the Delete key."""
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices:
            return

        self.merger.remove_files(selected_indices)
        logger.info(f"delete: indices {selected_indices}")
        self._update_drop_area()
