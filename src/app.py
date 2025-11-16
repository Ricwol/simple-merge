from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES

from config import BINDINGS, BUTTON_LABELS
from pdfmerger import PDFMerger
from ui import UIManager

class App:

    title = "Simple Merge"

    def __init__(self, ui: UIManager, merger: PDFMerger) -> None:
        self.ui = ui
        self.merger = merger

        self.ui.add_title(self.title)

        self.ui.drop_target_register(DND_FILES)
        self.ui.dnd_bind("<<Drop>>", self.on_drop)

        for func_name, pattern in BINDINGS.items():
            self.ui.bind(pattern, getattr(self, func_name))

        for label in BUTTON_LABELS:
            self.ui.add_button_action(label, action=getattr(self, label))

    def on_drop(self, event: tk.Event) -> None:
        files = self.ui.root.tk.splitlist(event.data)
        self.merger.add_files(files)

        for file in files:
            file_path = Path(file)
            if file in self.merger:
                self.ui.drop_area.insert(tk.END, file_path.name)

    def add_files(self) -> None:
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        self.merger.add_files(files)
        for file in files:
            file_path = Path(file)
            if file in self.merger:
                self.ui.drop_area.insert(tk.END, file_path.name)

    def move_up(self) -> None:
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices or selected_indices[0] == 0:
            return
        
        index = selected_indices[0]
        self.merger.swap_files(index, index - 1)
        self._update_drop_area()
        self.ui.drop_area.select_set(index - 1)

    def move_down(self) -> None:
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices or selected_indices[0] == len(self.merger) - 1:
            return
        
        index = selected_indices[0]
        self.merger.swap_files(index, index + 1)
        self._update_drop_area()
        self.ui.drop_area.select_set(index + 1)

    def remove_files(self) -> None:
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices:
            return
        
        self.merger.remove_files(selected_indices)
        self._update_drop_area()

    def clear_list(self) -> None:
        self.merger.clear_files()
        self.ui.drop_area.delete(0, tk.END)

    def merge(self) -> None:
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
            title="Save merged PDF as..."
        )
        if not output_filename:
            return
        
        self.ui.merge_button.config(state=tk.DISABLED)
        self.merger.merge_pdfs(output_filename)
        messagebox.showinfo(
            title="Success",
            message=f"PDFs merged to {output_filename}"
        )
        self.ui.merge_button.config(state=tk.NORMAL)

    def on_press(self, event: tk.Event) -> None:
        self.merger.drag_index = self.ui.drop_area.nearest(event.y)

    def on_drag(self, event: tk.Event) -> None:
        new_index = self.ui.drop_area.nearest(event.y)
        self.merger.move_file(new_index)
        self._update_drop_area()

    def _update_drop_area(self) -> None:
        self.ui.drop_area.delete(0, tk.END)
        for file in self.merger:
            self.ui.drop_area.insert(tk.END, Path(file).name)

    def on_delete(self, _: tk.Event) -> None:
        selected_indices = self.ui.drop_area.curselection()
        if not selected_indices:
            return

        self.merger.remove_files(selected_indices)
        self._update_drop_area()
