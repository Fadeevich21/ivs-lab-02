from libs.window import Window
import tkinter as tk
from tkinter import ttk


class WindowData(Window):

    def __init__(self, tab: tk.Frame) -> None:
        super().__init__(tab)

        self.main_workplace = tk.Frame(self.tab)
        self.main_workplace.place(x=0, y=0, width=1000, height=600)
        
        self.__table: ttk.Treeview = None
        self.__scroll_panel_x: ttk.Scrollbar = None
        self.__scroll_panel_y: ttk.Scrollbar = None

        self.__btn_build = ttk.Button(self.main_workplace, text='Построить', command=self.handle)
        self.__btn_build.place(x=450, y=450)

        columns = self.menu.get_query(0).get_all_columns()
        self.enabled = [tk.BooleanVar() for i in range(len(columns))]

        self.enabled_checkbuttons = [ttk.Checkbutton(self.main_workplace, text=columns[i], variable=self.enabled[i], offvalue=False, onvalue=True) for i in range(len(columns))]
        for i in range(len(self.enabled_checkbuttons)):
            self.enabled_checkbuttons[i].place(x=30 + 130 * (i // 2) , y=495 + 25 * (i % 2))


    def __remove_table_elements(self) -> None:
        if self.__table is not None:
            self.__table.destroy()
        if self.__scroll_panel_x is not None:
            self.__scroll_panel_x.destroy()
        if self.__scroll_panel_y is not None:
            self.__scroll_panel_y.destroy()

    def __get_columns(self) -> list:
        all_columns = self.menu.get_query(0).get_all_columns()
        columns = []
        for i in range(len(all_columns)):
            if self.enabled[i].get():
                columns.append(all_columns[i])

        return columns

    def __set_headers(self, headers: list) -> None:
        self.__table['columns'] = headers
        for header in headers:
            self.__table.heading(header, text=header, anchor='center')
            self.__table.column(header, anchor='center')


    def __insert_records_headers(self, columns: list):
        records, headers = self.menu.handle(columns)
        self.__set_headers(headers)
        for i in range(len(records)):
            record = records[i]
            if i % 2 == 0:
                self.__table.insert('', tk.END, values=record)
            else:
                self.__table.insert('', tk.END, values=record, tags='gray')
            self.__table.tag_configure('gray', background='#D3D3D3')

    def __init_table(self) -> None:
        self.__table = ttk.Treeview(self.main_workplace, show='headings')

        columns = self.__get_columns()
        if len(columns) == 0:
            return

        self.__insert_records_headers(columns)

    def __show_table(self) -> None:
        self.__init_table()
        self.__table.place(x=10, y=10, width=930, height=361)


    def __show_scroll_panel_x(self) -> None:
        self.__scroll_panel_x = ttk.Scrollbar(self.main_workplace, command=self.__table.xview, orient='horizontal')
        self.__table.configure(xscrollcommand=self.__scroll_panel_x.set)
        self.__scroll_panel_x.place(x=10, y=370, width=930)

    def __show_scroll_panel_y(self) -> None:
        self.__scroll_panel_y = ttk.Scrollbar(self.main_workplace, command=self.__table.yview)
        self.__table.configure(yscrollcommand=self.__scroll_panel_y.set)
        self.__scroll_panel_y.place(x=940, y=10, height=360)

    def __show_scroll_panels(self) -> None:
        self.__show_scroll_panel_x()
        self.__show_scroll_panel_y()

    def handle(self) -> None:
        self.__remove_table_elements()
        self.__show_table()
        self.__show_scroll_panels()
