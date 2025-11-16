from collections.abc import Iterator, Sequence
from pathlib import Path

from pypdf import PdfWriter

from errors import (
    InvalidFileError,
    NoFilesError,
    PDFMergerError
)
from logger import logger

class PDFMerger:
    """Manage ordered PDF file paths and write merged output."""

    def __init__(self) -> None:
        self._pdf_files: list[str] = []
        self._drag_index: int | None = None

    def __contains__(self, item: str) -> bool:
        return item in self._pdf_files

    def __len__(self) -> int:
        return len(self._pdf_files)

    def __iter__(self) -> Iterator[str]:
        return iter(self._pdf_files)

    @property
    def drag_index(self) -> int | None:
        return self._drag_index

    @drag_index.setter
    def drag_index(self, new_index: int) -> None:
        self._drag_index = new_index

    def _validate_file(self, file: str) -> None:
        path = Path(file)
        if not path.exists():
            logger.debug(f"File missing: {file}")
            raise InvalidFileError(f"File does not exist: {file}")
        if path.suffix.lower() != ".pdf":
            logger.debug(f"Invalid suffix: {file}")
            raise InvalidFileError(f"Not a PDF: {file}")

    def add_files(self, files: Sequence[str]) -> list[str]:
        """Add pdf files, skipping invalid and duplicates."""
        for file in files:
            path = Path(file)
            try:
                self._validate_file(file)
            except InvalidFileError:
                logger.warning(f"Skipping invalid file: {file}")
                continue
            if file in self._pdf_files:
                logger.debug(f"Skipping duplicate: {file}")
                continue

            self._pdf_files.append(file)
            logger.info(f"Added file: {path.name}")
        return self._pdf_files.copy()
    
    def remove_files(self, indices: Sequence[int]) -> None:
        """Remove files by indices ignoring invalid indices."""
        for index in sorted(indices, reverse=True):
            try:
                removed = self._pdf_files.pop(index)
                logger.info(f"Removed file at {index}: {Path(removed).name}")
            except IndexError:
                logger.debug(f"Ignore invalid remove index: {index}")
    
    def clear_files(self) -> None:
        """Clear all files."""
        count = len(self._pdf_files)
        self._pdf_files.clear()
        logger.info(f"Cleared {count} files")

    def swap_files(self, i: int, j: int) -> None:
        """Swap two file positions."""
        try:
            self._pdf_files[i], self._pdf_files[j] = self._pdf_files[j], self._pdf_files[i]
            logger.debug(f"Swapped indexes {i} and {j}")
        except IndexError as exc:
            logger.error(f"Swap failed indexes {i}, {j}")
            raise PDFMergerError("Index out of range for swap") from exc

    def move_file(self, new_index: int) -> None:
        """Move file from `drag_index` to `new_index`."""
        if self.drag_index is None:
            logger.debug("move_file called with no drag_index")
            return

        if new_index == self.drag_index:
            return

        try:
            file = self._pdf_files.pop(self.drag_index)
            self._pdf_files.insert(new_index, file)
            logger.debug(f"Moved file from {self._drag_index} to {new_index}")
            self.drag_index = new_index
        except IndexError as exc:
            self._drag_index = None
            logger.error(f"Move failed from {self._drag_index} to {new_index}")
            raise PDFMergerError("Index out of range for move") from exc

    def merge_pdfs(self, output_filename: str) -> str:
        """Write merged PDF to `output_filename` and return its path."""
        if not self._pdf_files:
            logger.error("merge_pdfs called with no files")
            raise NoFilesError("No PDF files to merge")

        with PdfWriter() as merger:
            for pdf in self._pdf_files:
                merger.append(pdf)
            merger.write(output_filename)
            logger.info(
                f"Merged {len(self._pdf_files)} files to {output_filename}"
            )
        return output_filename
