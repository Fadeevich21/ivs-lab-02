from libs.service_db import ServiceDB
from libs.query import Query
from typing import List, Tuple
from tkinter import filedialog


class Menu:

    def __init__(self) -> None:
        def init_tables(file_name: str):
            def get_pre_setting_arr(line: str):
                line = line[:-2]
                arr = line.split(',')
                if '\ufeff&REPORT' in arr:
                    arr.remove('\ufeff&REPORT')
                if '&REPORT' in arr:
                    arr.remove('&REPORT')
                arr = list(filter(None, arr))

                return arr


            with open(file_name) as file:
                i: int = 1
                for line in file:
                    arr = get_pre_setting_arr(line)
                    arr[1] = '.'.join(arr[1][i : i + 2] for i in range(0, len(arr[1]), 2))
                    arr[2] = ':'.join(arr[2][i : i + 2] for i in range(0, len(arr[2]), 2))
                    arr[2] = str((int(arr[2][0:2]) + 3) % 24) + arr[2][2:]
                    if len(arr[2]) != 8:
                        arr[2] = '0' + arr[2]

                    latitude = float(arr[3])
                    longitude = float(arr[5])
                    latitude_coordinate = [int(latitude / 100), round(latitude % 100, 5)]
                    longitude_coordinate = [int(longitude / 100), round(longitude % 100, 5)]
                    arr[3] = str(i)
                    arr[5] = str(i)

                    for j in range(len(arr)):
                        if arr[j].isdigit():
                            arr[j] = int(arr[j])

                    latitude_coordinate.insert(0, i * 2 - 1)
                    longitude_coordinate.insert(0, i * 2)
                    self.__db.insert('coordinates', [latitude_coordinate])
                    self.__db.insert('coordinates', [longitude_coordinate])

                    arr.insert(0, i)
                    self.__db.insert('latitudes', [[i, i * 2 - 1]])
                    self.__db.insert('longitudes', [(i, i * 2)])
                    self.__db.insert('tracker_data', [arr])
                    i += 1
                    if i % 100 == 0:
                        print(f'i = {i}')
                    # break

        self.__db = ServiceDB('database/sql.db')        
        self.__query = {}
        self.__menu = list()

    def get_list_names(self) -> List[str]:
        return list(self.__query.values())

    def add_query(self, query: Query):
        self.__query[len(self.__query)] = query.name()
        self.__menu.append(query)

    def get_choose(self, text_choose: str) -> int:
        for k, v in self.__query.items():
            if v == text_choose:
                return int(k)

    def handle(self, columns: int, time_start: str = '00:00:00', time_end: str = '23:59:59') -> Tuple[List[str], List[str]]:
        choose = 0
        if choose > len(self.__menu):
            raise IndexError(f'Ваш выбор {choose} не допустим')

        get_rows_func = lambda: self.__menu[choose].get_rows(self.__db, columns, time_start, time_end)
        rows = get_rows_func()
        return (rows, columns)

    def get_query(self, choose: int) -> Query:
        return self.__menu[choose]