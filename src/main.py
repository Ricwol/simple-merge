"""
Entry point for launching the Simple Merge application.

Initializes the GUI environment, builds the UI and App
instances, and starts the main event loop.
"""

from tkinterdnd2 import TkinterDnD

from pdfmerger import PDFMerger
from app import App
from ui import UI


def main() -> None:
    """Start the GUI application."""
    root = TkinterDnD.Tk()
    App(UI(root), PDFMerger())
    root.mainloop()


if __name__ == "__main__":
    main()
