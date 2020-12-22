import win32clipboard
from tkinter import Tk

def clear_clipboard():
    try:
        data = Tk().clipboard_get()
    except:
        data = None

    Tk().clipboard_clear()

    return data
