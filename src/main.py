from tkinterdnd2 import TkinterDnD

from pdfmerger import PDFMerger
from app import App
from ui import UIManager


def main() -> None:
    root = TkinterDnD.Tk()
    App(UIManager(root), PDFMerger())
    root.mainloop()


if __name__ == "__main__":
    main()
