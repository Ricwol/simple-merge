from tkinterdnd2 import TkinterDnD

from simplemerge import SimpleMerge


def main() -> None:
    root = TkinterDnD.Tk()
    SimpleMerge(root)
    root.mainloop()


if __name__ == "__main__":
    main()
