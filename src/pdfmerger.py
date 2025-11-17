"""
This module contains the core logic for managing and merging PDF files.

It validates file inputs, stores paths in order, manipulates
ordering, and writes the merged output file.
"""

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
        """Return the drag index."""
        return self._drag_index

    @drag_index.setter
    def drag_index(self, new_index: int) -> None:
        """Set the drag index."""
        self._drag_index = new_index

    def _validate_file(self, file: str) -> None:
        """Verify that a file exists and has a .pdf suffix.
        
        Raises:
            InvalidFileError: If the file does not exist or is not a PDF.
        """
        path = Path(file)
        if not path.exists():
            logger.debug("File missing: %s", file)
            raise InvalidFileError(f"File does not exist: {file}")
        if path.suffix.lower() != ".pdf":
            logger.debug("Invalid suffix: %s", file)
            raise InvalidFileError(f"Not a PDF: {file}")

    def add_files(self, files: Sequence[str]) -> None:
        """Add pdf files, skipping invalid and duplicates."""
        for file in files:
            path = Path(file)
            try:
                self._validate_file(file)
            except InvalidFileError:
                logger.warning("Skipping invalid file: %s", file)
                continue
            if file in self._pdf_files:
                logger.debug("Skipping duplicate: %s", file)
                continue

            self._pdf_files.append(file)
            logger.info("Added file: %s", path.name)

    def remove_files(self, indices: Sequence[int]) -> None:
        """Remove files by indices ignoring invalid indices."""
        for index in sorted(indices, reverse=True):
            try:
                removed = self._pdf_files.pop(index)
                logger.info(
                    "Removed file at %s: %s", index, Path(removed).name
                )
            except IndexError:
                logger.debug("Ignore invalid remove index: %d", index)

    def clear_files(self) -> None:
        """Clear all files."""
        count = len(self._pdf_files)
        self._pdf_files.clear()
        logger.info("Cleared %d files", count)

    def swap_files(self, i: int, j: int) -> None:
        """Swap two file positions."""
        try:
            self._pdf_files[i], self._pdf_files[j] = self._pdf_files[j], self._pdf_files[i]
            logger.debug("Swapped indexes %d and %d", i, j)
        except IndexError as exc:
            logger.error("Swap failed indexes %d, %d", i, j)
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
            logger.debug(
                "Moved file from %d to %d", self._drag_index, new_index
            )
            self.drag_index = new_index
        except IndexError as exc:
            self._drag_index = None
            logger.error(
                "Move failed from %d to %d", self._drag_index, new_index
            )
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
                "Merged %d files to %s", len(self._pdf_files), output_filename
            )
        return output_filename
