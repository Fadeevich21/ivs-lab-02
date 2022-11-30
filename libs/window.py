from abc import ABC, abstractmethod
import tkinter as tk
from libs.menu import Menu
import libs.query as query 


class Window(ABC):

    def __add_queries(self):
        self.menu.add_query(query.QueryTrackerData())

    @abstractmethod
    def __init__(self, tab: tk.Frame) -> None:
        self.tab = tab
        self.menu = Menu()
        self.__add_queries()

    @abstractmethod
    def handle(self) -> None:
        pass