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


        self.merge_button = tk.Button(
            root,
            text="Merge PDFs",
            command=self.merge_pdfs,
            height=2,
            width=20
        )
        self.merge_button.pack(pady=20)

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
