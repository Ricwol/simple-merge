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

        self.drop_area: tk.Listbox = tk.Listbox(
            root,
            selectmode=tk.EXTENDED,
            height=10,
            width=50
        )
        self.drop_area.pack(pady=20)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

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

    def merge_pdfs(self) -> None:
        if not self.pdf_files:
            messagebox.showerror("Error", "No PDFs selected!")
            return
        if len(self.pdf_files) == 1:
            messagebox.showerror("Error", "Can't merge only one PDF file!")
            return

        output_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save merged PDF as..."
        )
        if not output_filename:
            return
        
        with PdfWriter() as merger:
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_filename)
        
        messagebox.showinfo("Success", f"PDFs merged to {output_filename}")
