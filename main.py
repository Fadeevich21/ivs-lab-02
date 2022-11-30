from libs.gui import Gui
import tkinter as tk 
from tkinter import ttk

if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    app = Gui(root)
    app.pack()
    root.title('Tracker prepare')
    root.geometry('1000x600')
    root.resizable(width=False, height=False)

    root.mainloop()
