import tkinter as tk
from tkinter import ttk

from libs.window_data import WindowData
from libs.window_plot import WindowPlot
from libs.window_skyplot import WindowSkyplot


class Gui(tk.Frame):

    def __init_window_data(self) -> None:
        self.tab_data = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_data, text='Данные')
        WindowData(self.tab_data)

    def __init_window_plot(self) -> None:
        self.tab_plot = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_plot, text='Графики')
        WindowPlot(self.tab_plot)

    def __init_window_skyplot(self) -> None:
        self.tab_skyplot = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_skyplot, text='Скайпвоть')
        WindowSkyplot(self.tab_skyplot)

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.tab_control = ttk.Notebook(root)
        self.__init_window_data()
        self.__init_window_plot()
        self.__init_window_skyplot()
        self.tab_control.place(x=10, y=10, width=970, height=580)
