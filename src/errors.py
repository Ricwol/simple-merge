class PDFMergerError(Exception):
    """Base error for PDF merger operations."""


class NoFilesError(PDFMergerError):
    """Raised when an operation requires files but none are present."""


class InvalidFileError(PDFMergerError):
    """Raised when a provided file is invalid or not a PDF."""
