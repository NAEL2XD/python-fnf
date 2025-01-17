import traceback
from tkinter import messagebox

try:
    import source.Main
except SystemExit:
    exit()
except:
    messagebox.showerror(f"Python FNF Error Handler.", f"{traceback.format_exc()}\n\nPlease report it to https://github.com/NAEL2XD/python-fnf (make sure you copy the window popup by pressing CTRL+C and pasting the issue in GitHub)")