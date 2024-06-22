import psutil
from datetime import datetime
from time import sleep
from threading import Thread


class Service:
    """Klasa bazowa serwisów"""
    def __init__(self):
        """Ustawienie potrzebnych pól"""
        self._answer_time: dict[int, dict] = {}
        self._cpu_usage: dict[int, float] = {}
        self._memory_usage: dict[int, float] = {}
        self._request_count: int = 0

        # ustawienie działania metody tworzącej raport w oddzielnym wątku
        self._report_maker: Thread = Thread(target=self.__resources_usage)
        self._report_maker.daemon = True

    def make_report(self) -> dict:
        """
        Tworzy słownik z zebranymi danymi zurzycia zasobów sprzętowych

        Returns
        -------
        dict
            raport zużycia, klucze[cpu, memory]
        """
        return dict(
                    cpu=self._cpu_usage,
                    memory=self._memory_usage
                    )

    def _update_ans_time(self, t_start: int, t_end: int, size: int) -> None:
        """
        Dodaje nowy słownik z czasem odpowedzi serwisu

        Parameters
        ----------
        t_start : int
            czas rozpoczęcia
        t_end : int
            czas zakonczenia
        size : int
            rozmiar zapytania

        Returns
        -------
        None
        """
        time_ms = round((t_end - t_start)/10**6, 2)

        self._answer_time.update(
            {self._request_count: {
                'req_size': size,
                'ans_time': f'{time_ms} ms'
            }}
        )

    def __resources_usage(self) -> None:
        c_time: str

        while True:
            c_time = f'{datetime.now():%d.%m.%Y %H:%M:%S}'

            self._cpu_usage.update({c_time: psutil.cpu_percent()})
            self._memory_usage.update({c_time: psutil.virtual_memory().percent})

            sleep(1)
