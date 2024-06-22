import requests
from math import *
from serwis import Service
from time import time_ns
from copy import copy


def split_expresions(expresions: list[str]) -> list[list[str]]:
    """
    Przygotowuje wyrażenia do dalszego przetworzenia

    Parameters
    ----------
    expresions : list[str]
        zadane wyrażenia

    Returns
    -------
    list[list[str]]
        odpowiednio rozdzielone wyrażenia
    """
    marks: list = ['*', '/', '+', '-', '(', ')']
    expresions_parts = []

    for expresion in expresions:
        for mark in marks:
            expresion = expresion.replace(mark, f' {mark} ')

        expresions_parts.append(expresion.split())

    return expresions_parts


class Service2(Service):
    def __init__(self):
        super().__init__()
        self.__url: str = 'http://172.20.0.2:5000'
        self.__jsons: list[dict[str, any]] = []
        self.__csv_like: list[dict[str, any]] = []
        self.__keys: list[str] = []
        self.__rows: int = 0
        self._report_maker.start()

    def new_request(self, size: int) -> bool:
        """
        Pobiera z serwisu nr. 1 nowe jsony

        Parameters
        ----------
        size : int
            ilość jsonów

        Returns
        -------
        bool
            'True' gdy zapytanie przebiegło pomyślnie
        """
        t_start: int = time_ns()
        self._request_count += 1
        response = requests.get(f'{self.__url}/generate/json/{size}')

        if response.status_code != 200:
            self.__rows = 0
            self._update_ans_time(t_start, time_ns(), -1)
            return False

        self.__jsons = response.json()
        self.__keys = list(self.__jsons[0].keys())
        self._update_ans_time(t_start, time_ns(), size)
        self.__rows = size
        self.__json_to_csv()

        return True

    def basic(self) -> tuple[list[dict], list]:
        """
        Wybiera podstawowe wartości z pobranego jsona

        Returns
        -------
        tuple[list[dict], list]
            wybrane wartości, tytuły kolumn
        """
        if not self.__rows:
            return [], []

        basic_heads = ['_type', '_id', 'name', 'type', 'latitude', 'longitude']

        ans = self.__select_csv(basic_heads)

        if 'Error' in ans[0]:
            return [], []

        return ans, basic_heads

    def selected(self, heads: str) -> tuple[list[dict], list]:
        """
        Wybiera wybrane wartości z pobranego jsona

        Returns
        -------
        tuple[list[dict], list]
            wybrane wartości, tytuły kolumn
        """
        if not self.__rows:
            return [], []

        heads_tmp = heads.replace(' ', '')
        selected_heads = heads_tmp.split(',')

        ans = self.__select_csv(selected_heads)

        if 'Error' in ans[0]:
            return [], []

        return ans, selected_heads

    def calculate(self, expresions: list[str]) -> tuple:
        """
        Wykonuje zadane działania matematyczne na wartościach z pobranego jsona

        Returns
        -------
        tuple[list[dict], list]
            wyniki działań, zadane działania
        """
        answer: list[dict] = []

        if not self.__rows:
            return tuple()

        expresions_parts = split_expresions(expresions)

        for index in range(self.__rows):
            answer.append(self.__calc_for_csv(expresions, expresions_parts, index))

        return answer, expresions

    def bridge(self) -> dict:
        """
        Pobiera raport z serwisu nr. 1 i aktualizuje go o czas odpowedzi tego serwisu

        Returns
        -------
        dict
            rozszerzony raport serwisu nr. 1
        """
        response = requests.get(f'{self.__url}/report')

        if response.status_code != 200:
            return {}

        service1_rep = response.json()
        service1_rep['answer_time'] = self._answer_time

        return service1_rep

    def __json_to_csv(self) -> None:
        """
        Przekształaca słownik z formy jsona na csv

        Returns
        -------
        None
        """
        self.__csv_like = []

        for index, json in enumerate(self.__jsons):
            geo_position = json.pop('geo_position')
            self.__csv_like.append(copy(json))
            self.__csv_like[index].update(geo_position)

    def __select_csv(self, heads: list[str]) -> list[dict]:
        to_csv: list[dict] = []

        try:
            for index, row in enumerate(self.__csv_like):
                to_csv.append(dict())

                for head in heads:
                    to_csv[index][head] = row[head]

        except KeyError:
            to_csv = [{'Error': 'Key_Error'}]

        return to_csv

    def __calc_for_csv(self, expresions: list[str], expresions_part: list[list[str]], index: int) -> dict:
        """
        Wykonuje zadane działania matematyczne na wskazanych wartościach z pobranego jsona

        Parameters
        ----------
        expresions : list[str]
            zadane działania mateamtyczne (elementy listy)
        expresions_part : list[list[str]]
            zadane działania mateamtyczne rozdzialone przez funkcje 'split_expresions'
        index : int
            wiersz na którym mają zostać wykonane działania
        Returns
        -------
        dict
            działanie: wynik
        """
        ans: dict = {}
        cooked_expr: str = ''

        for expr_i, parts in enumerate(expresions_part):

            for i, part in enumerate(parts):
                val = part

                if part in self.__keys:
                    val = self.__csv_like[index][part]

                    if part == 'distance' and not val:
                        val = 0

                cooked_expr += str(val)

            try:
                ans[expresions[expr_i]] = eval(''.join(cooked_expr))
            except Exception as exept:
                ans[expresions[expr_i]] = str(exept)

            cooked_expr = ''

        return ans
