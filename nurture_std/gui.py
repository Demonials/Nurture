import tkinter as tk

class GUIAPI:
    def window(self, title="Nurture", width=600, height=400):
        win = tk.Toplevel()
        win.title(title)
        win.geometry(f"{width}x{height}")
        return win

API = GUIAPI()
