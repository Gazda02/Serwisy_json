import requests
import csv
from time import time_ns
from serwis import Service
from copy import deepcopy


def fix_equations(equations: list[str]) -> list[str]:
    """
    Naprawia wyrażenia po metodzie 'split', łączy rozdzielone wyrażenia w których wystąpił przecinek ",".
    Np. ['pow(a', 'b)'] -> ['pow(a, b)']

    Parameters
    ----------
    equations : list[str]
        zadane wyrażenia

    Returns
    -------
    list[str]
        naprawione wyrażenia
    """
    for expresion in equations:
        if '(' in expresion and ')' not in expresion:
            next_i = equations.index(expresion) + 1

            if '(' not in equations[next_i] and ')' in equations[next_i]:
                expresion += f' , {equations.pop(next_i)}'
                equations[next_i - 1] = expresion

            else:
                return []

        elif '(' not in expresion and ')' in expresion:
            return []

    return equations


class Service3(Service):
    def __init__(self):
        super().__init__()
        self.__url = 'http://172.20.0.3:5000'
        self.__reports: dict = {}
        self.__sum_of_jsons: int = 0
        self.__json_size: int = 0
        self.__flag_1k: bool = True
        self.__flag_10k: bool = True
        self.__flag_100k: bool = True

    def new_jsons(self, size: int) -> bool:
        """
        Wysyła zapytanie o nowe jsony, mierzy czas odpowedzi

        Parameters
        ----------
        size : int
            ilośc jsonów

        Returns
        -------
        bool
            'True' jeśi zkonczone powodzeniem
        """
        t_start = time_ns()
        self._request_count += 1

        response = requests.get(f'{self.__url}/new/{size}')

        if response.status_code != 200:
            self.__json_size = 0
            self._update_ans_time(t_start, time_ns(), -1)
            return False

        self.__sum_of_jsons += size
        self.__json_size = size
        self._update_ans_time(t_start, time_ns(), self.__json_size)
        self.__update_report()

        return True

    def basic(self) -> str:
        """
        Wysyła zapytanie o csv w podstawowej formie, mierzy czas odpowedzi

        Returns
        -------
        str
            string w formacie csv
        """
        if not self.__json_size:
            return ''

        t_start = time_ns()
        self._request_count += 1

        response = requests.get(f'{self.__url}/basic')

        if response.status_code != 200:
            self._update_ans_time(t_start, time_ns(), -1)
            return ''

        self._update_ans_time(t_start, time_ns(), self.__json_size)

        response_decoded = response.content.decode('utf-8')
        csv_readed = csv.reader(response_decoded.splitlines(), dialect=csv.excel_tab)
        rows = list(map(lambda row: row[0], csv_readed))
        csv_like_str = '<br>'.join(rows)

        return csv_like_str

    def select(self, selected: list) -> str:
        """
        Wysyła zapytanie o wybrane kolumny z pliku csv, mierzy czas odpowedzi

        Parameters
        ----------
        selected : list
            nagłówki wybranych kolumn

        Returns
        -------
        str
            string w formacie csv
        """
        if not self.__json_size:
            return ''

        selected_endpoint = ','.join(selected)

        t_start = time_ns()
        self._request_count += 1

        response = requests.get(f'{self.__url}/select/{selected_endpoint}')

        if response.status_code != 200:
            self._update_ans_time(t_start, time_ns(), -1)
            return ''

        self._update_ans_time(t_start, time_ns(), self.__json_size)

        response_decoded = response.content.decode('utf-8')
        csv_readed = csv.reader(response_decoded.splitlines(), dialect=csv.excel_tab)
        rows = list(map(lambda row: row[0], csv_readed))
        csv_like_str = '<br>'.join(rows)

        return csv_like_str

    def math(self, eq: list) -> str:
        """
        Wysyła zapytanie z wprowadzonymi wyrażeniami matematycznymi na wartościch pliku csv, mierzy czas odpowedzi

        Parameters
        ----------
        eq : list

        Returns
        -------
        str
            string w formacie csv
        """
        if not self.__json_size:
            return ''

        t_start = time_ns()
        self._request_count += 1

        response = requests.post(f'{self.__url}/math', json=dict(expresions=fix_equations(eq)))

        if response.status_code != 200:
            self._update_ans_time(t_start, time_ns(), -1)
            return ''

        self._update_ans_time(t_start, time_ns(), self.__json_size)

        response_decoded = response.content.decode('utf-8')
        csv_readed = csv.reader(response_decoded.splitlines(), dialect=csv.excel_tab)
        rows = list(map(lambda row: row[0], csv_readed))
        csv_like_str = '<br>'.join(rows)

        return csv_like_str

    def get_reports(self) -> dict:
        """Przesyła raport"""
        return self.__reports

    def __collect_reports(self) -> None:
        """
        Wysyła zapytania do serwisu nr. 2 o raporty, aktualizuje o czas odpowedzi serwisu nr. 2, nie mierzy czasu

        Returns
        -------
        None
        """
        response_s1 = requests.get(f'{self.__url}/bridge')

        if response_s1.status_code != 200:
            return

        report_s1 = response_s1.json()

        response_s2 = requests.get(f'{self.__url}/report')

        if response_s2.status_code != 200:
            return

        report_s2 = response_s2.json()
        report_s2['answer_time'] = deepcopy(self._answer_time)

        self.__reports = dict(
            service1=report_s1,
            service2=report_s2
        )

    def __update_report(self) -> None:
        """
        Funkcja typu guard, blokuje możliwość pobierania raportów przy każdym pobraniu nowych jsonów.
        Raporty możliwe na 1k, 10k oraz 100k jsonów.

        Returns
        -------
        None
        """
        if self.__sum_of_jsons < 1000:
            return

        if self.__flag_1k and int(self.__sum_of_jsons/1000) >= 1:
            self.__collect_reports()
            self.__flag_1k = False

        if self.__flag_10k and int(self.__sum_of_jsons/10000) >= 1:
            self.__collect_reports()
            self.__flag_10k = False

        if self.__flag_100k and int(self.__sum_of_jsons/100000) >= 1:
            self.__collect_reports()
            self.__flag_100k = False
