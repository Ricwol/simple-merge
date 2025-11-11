from ast import Delete
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from pypdf import PdfWriter
from tkinterdnd2 import TkinterDnD, DND_FILES


class SimpleMerge:

    def __init__(self, root: TkinterDnD.Tk) -> None:
        self.root = root
        self.root.title("Simple Merge")
        self.pdf_files: list[str] = []
        self.drag_index: int = 0

        self.drop_area: tk.Listbox = tk.Listbox(
            root,
            selectmode=tk.EXTENDED,
            height=10,
            width=50
        )
        self.drop_area.pack(pady=20)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

        self.drop_area.bind("<ButtonPress-1>", self.on_press)
        self.drop_area.bind("<B1-Motion>", self.on_drag)

        self.drop_area.bind("<Delete>", self.on_delete)

        self.merge_button = tk.Button(
            root,
            text="Merge PDFs",
            command=self.merge_pdfs,
            height=2,
            width=20
        )
        self.merge_button.pack(pady=20)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.move_up_button = tk.Button(
            button_frame,
            text="↑",
            command=self.move_up,
            width=10
        )
        self.move_up_button.pack(side=tk.RIGHT, padx=5)

        self.move_down_button = tk.Button(
            button_frame,
            text="↓",
            command=self.move_down,
            width=10
        )
        self.move_down_button.pack(side=tk.RIGHT, padx=5)

        self.remove_file_button = tk.Button(
            button_frame,
            text="Remove File(s)",
            command=self.remove_file,
            width=10
        )
        self.remove_file_button.pack(side=tk.RIGHT, padx=5)

        self.clear_list_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_list,
            width=10
        )
        self.clear_list_button.pack(side=tk.RIGHT, padx=5)

    def on_drop(self, event: tk.Event) -> None:
        files: list[str] = self.root.tk.splitlist(event.data)
        for file in files:
            file_path = Path(file)
            if file_path.suffix.lower() == ".pdf":
                self.pdf_files.append(file)
                self.drop_area.insert(tk.END, file_path.name)

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
