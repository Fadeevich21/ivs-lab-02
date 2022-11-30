from libs.window import Window
import tkinter as tk
from tkinter import ttk

from libs.query import QueryTrackerData

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


class WindowPlot(Window):

    def __init_x_plots(self) -> None:
        tk.Label(self.tab, text='x:').place(x=680, y=350)
        self.x_plots = ['время', 'широта']
        self.x_plot = ttk.Combobox(self.tab, state="readonly", values=self.x_plots)
        self.x_plot.bind('<<ComboboxSelected>>', self.set_y_plot)
        self.x_plot.current(0)
        self.x_plot.place(x=700, y=350)
        
    def __init_y_plots(self) -> None:
        tk.Label(self.tab, text='y:').place(x=680, y=400)
        self.y_plots = [['скорость', 'направление', 'одометр', 'I/O статус', 'fix-mode', 'glonass_sat_no', 'gps_sat_no'], ['долгота']]
        self.y_plot: ttk.Combobox = None
        self.y_plot = ttk.Combobox(self.tab, state="readonly", values=self.y_plots[0])
        self.y_plot.current(0)
        self.y_plot.place(x=700, y=400)
        
    def __init_plots(self) -> None:
        self.__init_x_plots()
        self.__init_y_plots()


    def __init_start_time(self) -> None:
        tk.Label(self.tab, text='start time:').place(x=680, y=230)
        self.start_time = tk.Entry(self.tab)
        self.start_time.insert(0, '00:00:00')
        self.start_time.place(x=760, y=230, width=65)

    def __init_end_time(self) -> None:
        tk.Label(self.tab, text='end time:').place(x=680, y=270)
        self.end_time = tk.Entry(self.tab)
        self.end_time.insert(0, '23:59:59')
        self.end_time.place(x=760, y=270, width=65)

    def __init_range_times(self) -> None:
        self.__init_start_time()
        self.__init_end_time()

    def __show_plot_btn(self) -> None:
        plot_btn = tk.Button(self.tab, text='plot', command=self.handle)
        plot_btn.place(x=725, y=480, width=100)


    def __init__(self, tab: tk.Frame) -> None:
        super().__init__(tab)

        self.fig = Figure(dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab)
        self.__show_plot_btn()

        self.__init_plots()
        self.__init_range_times()


    def set_y_plot(self, event):
        values = self.y_plots[self.x_plots.index(self.x_plot.get())]
        self.y_plot['values'] = values
        self.y_plot.current(0)

    def get_coords_path(self):
        columns = ['широта', 'долгота']
        records, _ = self.menu.handle(columns)
        x, y = zip(*records)
        x = [float(el.replace('°', '')[:-1]) for el in x]
        y = [float(el.replace('°', '')[:-1]) for el in y]
        
        return [x, y]

    def get_coords_time_attr(self):
        times = [self.start_time.get(), self.end_time.get()]
        columns = [self.x_plot.get(), self.y_plot.get()]
        records, _ = self.menu.handle(columns, times[0], times[1])
        x, y = zip(*records)
        x = [(float(el[:2]) + float(el[3:5]) / 100) for el in x]
        
        return [x, y]

    def __remove_canvas(self) -> None:
        if self.canvas is not None:
            for item in self.canvas.get_tk_widget().find_all():
               self.canvas.get_tk_widget().delete(item)
            self.canvas = None

    def __show_canvas(self) -> None:
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=15, y=20, width=650, height=500)

    def __plot(self) -> None:

        def convert_to_grad(x, pos):
            minutes = x % 100
            grad = int(x // 100) + minutes / 60
            return f"{grad:.{2}f}°"

        self.plot = self.fig.add_subplot(111)
        self.plot.locator_params(axis='x', nbins=8)

        x, y = None, None
        x_column = self.x_plot.get()
        if x_column == 'широта':
            x, y = self.get_coords_path()
            self.plot.xaxis.set_major_formatter(FuncFormatter(convert_to_grad))
            self.plot.yaxis.set_major_formatter(FuncFormatter(convert_to_grad))
            self.plot.plot(x, y, 'o')
        else:
            x, y = self.get_coords_time_attr()
            self.plot.plot(x, y)

    def __set_labels(self) -> None:
        columns = [self.x_plot.get(), self.y_plot.get()]
        query = QueryTrackerData()
        all_columns = query.get_all_columns()
        indexes = [all_columns.index(columns[i]) for i in range(len(columns))]
        units = [query.units_of_measurement()[index] for index in indexes]
        self.plot.set_xlabel(f'{columns[0]} ({units[0]})')
        self.plot.set_ylabel(f'{columns[1]} ({units[1]})')


    def handle(self) -> None:
        self.fig.clear()
        self.__remove_canvas()
        
        self.__plot()
        self.__set_labels()

        self.__show_canvas()