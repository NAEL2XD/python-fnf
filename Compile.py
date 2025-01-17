from traceback import format_exc as cLog
from tkinter import messagebox
from sys import exit

try:
    import source.Main
except SystemExit:
    exit()
except:
    messagebox.showerror(f"Python FNF Error Handler.", f"{cLog()}\n\nPlease report it to https://github.com/NAEL2XD/python-fnf (make sure you copy the window popup by pressing CTRL+C and pasting the issue in GitHub)")