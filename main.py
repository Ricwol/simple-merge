from tkinterdnd2 import TkinterDnD

from src.pdfmerger import PDFMerger
from src.simplemerge import SimpleMerge
from src.ui import UIManager


def main() -> None:
    root = TkinterDnD.Tk()
    SimpleMerge(UIManager(root), PDFMerger())
    root.mainloop()


if __name__ == "__main__":
    main()
