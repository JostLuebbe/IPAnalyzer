import logging as lg
import tkinter as tk
import traceback

from py_files import logging_setup as ls
from py_files.tkinter_classes import IPAnalyzerGUI


def main():
    root = tk.Tk()
    IPAnalyzerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    ls.logging_setup_main()
    try:
        main()
    except:
        lg.error(traceback.format_exc())
