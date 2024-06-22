from string import ascii_lowercase
from random import randint, choice, uniform
from serwis import Service


def random_name(_len: int) -> str:
    """
    Generuje losowego string

    Parameters
    ----------
    _len : int
        długość stringa

    Returns
    -------
    str
    """
    _name = ''.join(choice(ascii_lowercase) for i in range(_len))
    return _name.capitalize()


def rand_jsons(size: int) -> list[dict]:
    """
    Generuje liste słowników o losowych wartościach i określonych kluchach

    Parameters
    ----------
    size : int
        ilość słowników, długość listy

    Returns
    -------
    list[dict]
    """
    jsons = []

    for s in range(size):
        name = random_name(randint(5, 10))
        country = random_name(randint(5, 10))

        jsons.append({
            '_type': 'Position',
            '_id': randint(10000000, 99999999),
            'key': None,
            'name': name,
            'fullName': f'{name}, {country}',
            'iata_airport_code': choice((None, name[:3].upper())),
            'type': 'location',
            'country': country,
            'geo_position': {
                'latitude': uniform(-100, 101),
                'longitude': uniform(-100, 101)
            },
            'location_id': randint(100000, 999999),
            'inEurope': choice((True, False)),
            'countryCode': country[:2],
            'coreCountry': choice((True, False)),
            'distance': choice((None, randint(1, 5000)))
        })

    return jsons


class Service1(Service):
    def __init__(self):
        super().__init__()

        # rozpoczęcie działania wątku zbierającego dane do raportu
        self._report_maker.start()

    def generate_jsons(self, size) -> list[dict]:
        """
        Generuje liste słowników o losowych wartościach i określonych kluchach

        Parameters
        ----------
        size : int
            ilość słowników, długość listy

        Returns
        -------
        list[dict]
        """
        return rand_jsons(size)
