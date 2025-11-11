from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from typing import Literal

from pypdf import PdfWriter
from tkinterdnd2 import TkinterDnD, DND_FILES


WINDOW_SIZE = "600x400"
BUTTON_WIDTH = 12
ARROW_BUTTON_WITDH = 1
MERGE_BUTTON_FONT = ("Helvetica", 14, "bold")


class SimpleMerge:

    title = "Simple Merge"

    def __init__(self, root: TkinterDnD.Tk) -> None:
        self.root = root
        self.root.title(self.title)
        self.root.geometry(WINDOW_SIZE)

        self.pdf_files: list[str] = []
        self.drag_index: int = 0

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
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_area.bind("<ButtonPress-1>", self.on_press)
        self.drop_area.bind("<B1-Motion>", self.on_drag)
        self.drop_area.bind("<Delete>", self.on_delete)

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
            command=self.move_up,
            width=ARROW_BUTTON_WITDH,
            height=1
        )
        self.move_up_button.pack(pady=(40, 5))

        self.move_down_button = tk.Button(
            arrow_frame,
            text="↓",
            command=self.move_down,
            width=ARROW_BUTTON_WITDH,
            height=1
        )
        self.move_down_button.pack(pady=(5, 40))

    def _setup_action_buttons(self, parent: tk.Frame) -> None:
        self.add_files_button = tk.Button(
            parent,
            text="Add File(s)",
            command=self.add_files,
            width=BUTTON_WIDTH
        )
        self.add_files_button.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

        # Define Remove File(s) and Clear buttons
        self.remove_file_button = tk.Button(
            parent,
            text="Remove File(s)",
            command=self.remove_file,
            width=BUTTON_WIDTH
        )
        self.remove_file_button.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

        self.clear_list_button = tk.Button(
            parent,
            text="Clear All",
            command=self.clear_list,
            width=BUTTON_WIDTH
        )
        self.clear_list_button.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    def _setup_merge_button(self, parent: tk.Frame) -> None:        
        self.merge_button = tk.Button(
            parent,
            text="Merge",
            command=self.merge_pdfs,
            bg="green",
            fg="white",
            font=MERGE_BUTTON_FONT,
            width=20,
            height=2
        )
        self.merge_button.pack(side=tk.BOTTOM, pady=20)

    def on_drop(self, event: tk.Event) -> None:
        files = self.root.tk.splitlist(event.data)
        self._add_files(files)

    def on_press(self, event: tk.Event) -> None:
        self.drag_index = self.drop_area.nearest(event.y)

    def on_drag(self, event: tk.Event) -> None:
        new_index = self.drop_area.nearest(event.y)
        if new_index == self.drag_index:
            return
        
        item = self.drop_area.get(self.drag_index)
        self.drop_area.delete(self.drag_index)
        self.drop_area.insert(new_index, item)

        self.pdf_files.insert(new_index, self.pdf_files.pop(self.drag_index))

        self.drag_index = new_index

    def on_delete(self, _: tk.Event) -> None:
        selected_indices = self.drop_area.curselection()
        if not selected_indices:
            return
        
        for index in sorted(selected_indices, reverse=True):
            self.drop_area.delete(index)
            self.pdf_files.pop(index)

    def move_up(self) -> None:
        selected_indices = self.drop_area.curselection()
        if not selected_indices or selected_indices[0] == 0:
            return
        
        index = selected_indices[0]
        self._swap_pdfs(index, index - 1)

    def move_down(self) -> None:
        selected_indices = self.drop_area.curselection()
        if not selected_indices or selected_indices[0] == len(self.pdf_files) - 1:
            return
        
        index = selected_indices[0]
        self._swap_pdfs(index, index + 1)

    def _swap_pdfs(self, index1: int, index2: int) -> None:
        item1 = self.drop_area.get(index1)
        item2 = self.drop_area.get(index2)

        self.drop_area.delete(index1)
        self.drop_area.insert(index1, item2)
        self.drop_area.delete(index2)
        self.drop_area.insert(index2, item1)

        self.pdf_files[index1], self.pdf_files[index2] = self.pdf_files[index2], self.pdf_files[index1]

        self.drop_area.select_clear(0, tk.END)
        self.drop_area.select_set(index2)

    def add_files(self) -> None:
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        self._add_files(files)
    
    def _add_files(self, files: tuple[str, ...] | Literal[""]) -> None:
        duplicates: list[str] = []

        for file in files:
            file_path = Path(file)
            if file in self.pdf_files:
                duplicates.append(file_path.name)
            elif file_path.suffix.lower() == ".pdf":
                self.pdf_files.append(file)
                self.drop_area.insert(tk.END, file_path.name)
        
        if duplicates:
            messagebox.showinfo(
                title="Duplicate Files",
                message=(
                    "The following files are already in the list and were skipped:\n"
                    + "\n".join(duplicates)
                )
            )

    def remove_file(self) -> None:
        selected_indices = self.drop_area.curselection()
        if not selected_indices:
            return
        
        for index in sorted(selected_indices, reverse=True):
            self.drop_area.delete(index)
            self.pdf_files.pop(index)

    def clear_list(self) -> None:
        self.drop_area.delete(0, tk.END)
        self.pdf_files.clear()

    def merge_pdfs(self) -> None:
        if not self.pdf_files:
            messagebox.showerror(title="Error", message="No PDFs selected!")
            return
        
        if len(self.pdf_files) == 1:
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
        
        self.merge_button.config(state=tk.DISABLED)

        with PdfWriter() as merger:
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_filename)
        
        num_pdfs = len(self.pdf_files)
        for i in range(num_pdfs - 1, -1, -1):
            self.remove_pdf_animated(i)

        self.merge_button.after(
            ms=300 * num_pdfs,
            func=lambda: self._finish_merge(output_filename)
        )

    def remove_pdf_animated(self, index: int) -> None:
        self.drop_area.after(
            ms=300,
            func=lambda: self._remove_pdf(index)
        )

    def _remove_pdf(self, index: int) -> None:
        self.drop_area.delete(index)
        self.pdf_files.pop(index)

    def _finish_merge(self, output_filename: str) -> None:
        self.merge_button.config(state=tk.NORMAL)
        messagebox.showinfo(
            title="Success",
            message=f"PDFs merged to {output_filename}"
        )
