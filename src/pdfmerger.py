from collections.abc import Iterable
from pathlib import Path
from tkinter import messagebox

from pypdf import PdfWriter

from logger import logger

class PDFMerger:

    def __init__(self) -> None:
        self._pdf_files: list[str] = []
        self._drag_index: int | None = None

    def __contains__(self, item: str) -> bool:
        return item in self._pdf_files

    def __len__(self) -> int:
        return len(self._pdf_files)

    def __getitem__(self, item) -> str:
        return self._pdf_files[item]

    @property
    def drag_index(self) -> int | None:
        return self._drag_index

    @drag_index.setter
    def drag_index(self, new_index: int) -> None:
        self._drag_index = new_index

    def add_files(self, files: Iterable[str]) -> None:
        duplicates: list[str] = []

        for file in files:
            file_path = Path(file)

            if file in self._pdf_files:
                duplicates.append(file_path.name)
            elif file_path.suffix.lower() == ".pdf":
                self._pdf_files.append(file)
                logger.info(f"Added file: {file_path.name}")
        
        if duplicates:
            logger.warning(f"Skipped duplicate files: {', '.join(duplicates)}")
            messagebox.showinfo(
                title="Duplicate Files",
                message=(
                    "The following files are already in the list"
                    + " and were skipped:\n"
                    + "\n".join(duplicates)
                )
            )
    
    def remove_files(self, indices: list[int]) -> None:
        for index in sorted(indices, reverse=True):
            self._pdf_files.pop(index)
    
    def clear_files(self) -> None:
        self._pdf_files.clear()

    def swap_files(self, index1: int, index2: int) -> None:
        self._pdf_files[index1], self._pdf_files[index2] = self._pdf_files[index2], self._pdf_files[index1]

    def move_file(self, new_index: int) -> None:
        if self.drag_index is None or new_index == self.drag_index:
            return
        
        file = self._pdf_files.pop(self.drag_index)
        self._pdf_files.insert(new_index, file)
        self.drag_index = new_index

    def merge_pdfs(self, output_filename: str) -> None:
        with PdfWriter() as merger:
            for pdf in self._pdf_files:
                merger.append(pdf)
            merger.write(output_filename)
            logger.info(f"Merged PDFs to {output_filename}")
    