import win32clipboard

def clear_clipboard():
    win32clipboard.OpenClipboard()

    try:
        data = win32clipboard.GetClipboardData()
    except:
        data = None

    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

    return data

