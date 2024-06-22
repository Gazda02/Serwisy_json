>>> Polecenie

Trzy serwisy.

1. Serwis który zwraca pod adresem ‘/generate/json/{size}’ listę jsonow o wskazanym rozmiarze
oraz o strukturze poniżej z losowymi wartościami.
np.
{ _type: "Position", _id: 65483214, key: null, name: "Oksywska", fullName: "Oksywska,
Poland", iata_airport_code: null, type: "location", country: "Poland", geo_position:
{ latitude: 51.0855422, longitude: 16.9987442 }, location_id: 756423, inEurope: true,
countryCode: "PL", coreCountry: true, distance: null }

2. Serwis który pobiera dane z pierwszego i konwertuje go do csv. Pierwszy endpoint który
zawsze zwraca pobrane dane w formacie ‘type, _id, name, type, latitude, longitude’. Drugi
endpoint który zwraca pobrane dane w danej strukturze csv czyli podajemy w zapytaniu ‘ id,
latitude, longitude’ i oczekujemy że zwróci taki wynik ‘ 65483214, 51.0855422, 16.9987442 ’.
Trzeci endpoint który na wejściu oczekuje definicji prostych operacji matematycznych w formie
listy np ‘ latitude*longitude,sqrt(location_id)’ i w wyniku zwróci ‘ 3.0052538 , 869.7258188 ’

3. Serwis który wykonuje zapytania na drugim i wyświetla proste raporty dotyczące wydajności.
Raport powinien zawierać informacje takie jak użycie procesora,pamięci w czasie dla każdego z
poprzednich serwisów oraz czas zapytań http pomiędzy serwisami 3->2->1.
Raport na 1k,10k,100k wygenerowanych jsonow.

>>> Technologie

Python 3.10.5;
Flask 3.0.3;
Flask-CSV 1.2.1;
Requests 2.32.2;
psutil 5.9.8;

Docker 26.1.4;
Docker Compose 2.27.1;


