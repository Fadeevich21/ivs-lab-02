from libs.service_db import ServiceDB
from abc import ABC, abstractmethod
from typing import List


class Query(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_rows(self, service: ServiceDB, time_start: str = "00:00:00", time_end: str = "23:59:59"):
        pass

    @abstractmethod
    def get_columns(self, columns: List[str]):
        pass

    @abstractmethod
    def get_all_columns(self) -> List[str]:
        pass

    @staticmethod
    def units_of_measurement(self) -> List[str]:
        pass


class QueryTrackerData(Query):

    def name(self) -> str:
        return 'Выборка данных'

    def get_rows(self, service: ServiceDB, columns: List[str], time_start: str = "\'00:00:00\'", time_end: str = "\'23:59:59\'"):
        fields = []
        all_columns = self.get_all_columns()
        all_fields = ['device_id', 'date', 'time',
            """(
                    SELECT c.degrees || '°' || c.minutes || ''''
                    FROM latitudes la
                    JOIN coordinates c on la.coordinate_id = c.coordinate_id
                    WHERE la.latitude_id = td.latitude_id
                )""",
            'n_s',
            """(
                    SELECT c.degrees || '°' || c.minutes || ''''
                    FROM longitudes lo
                    JOIN coordinates c on lo.coordinate_id = c.coordinate_id
                    WHERE lo.longitude_id = td.longitude_id
                )""",
            'e_w', 'speed', 'course', 'odometer', 'io_status', 'fix_mode', 'glonass_sat_no', 'gps_sat_no']

        for i in range(len(all_columns)):
            if all_columns[i] in columns:
                fields.append(all_fields[i])

        joins = None
        if 'широта' in columns or 'долгота' in columns:
            joins = []
            if 'широта' in columns:
                joins.append(('latitudes', 'la', 'la.latitude_id = td.latitude_id'))
            if 'долгота' in columns:
                joins.append(('longitudes', 'lo', 'lo.longitude_id = td.longitude_id')
)
        if 'время' not in all_columns:
            return service.select \
            (
                fields=fields,
                tables=[('tracker_data', 'td')],
                joins=joins            
            )
        else:
            time_start = f"'{time_start}'"
            time_end = f"'{time_end}'"
            return service.select \
            (
                fields=fields,
                tables=[('tracker_data', 'td')],
                joins=joins,
                where=[f"time >= {time_start}", f"time <= {time_end}"]            
            )

    def get_columns(self):
        return

    def get_all_columns(self) -> List[str]:
        return ['ID устройства', 'дата', 'время', 'широта', 'север/юг', 'долгота', 'запад/восток', 'скорость', 'направление', 'одометр', 'I/O статус', 'fix-mode', 'glonass_sat_no', 'gps_sat_no']

    def units_of_measurement(self) -> List[str]:
        return ['', '', 'ч', 'град', '', 'град', '', 'км/ч', 'град', 'метры', '', '', 'шт', 'шт']
