"""
Plik główny serwisu nr.2
Wymaga działania serwisów nr.1 oraz nr.3
"""

import flask_csv
from flask import Flask, jsonify, request
from serwis2 import Service2

app = Flask(__name__)
service2 = Service2()


@app.get('/basic')
def basic():
    """
    Przesyła plik csv w formacie ‘type, _id, name, type, latitude, longitude’

    Returns
    -------
    Response
        plik csv (gdy nie wystąpi błąd), status
    """
    to_csv, keys = service2.basic()
    if not to_csv:
        return '', 400
    else:
        return flask_csv.send_csv(to_csv, 'basic.csv', keys, encoding='utf-8'), 200


@app.get('/new/<int:size>')
def new_request(size: int):
    """
    Pobiera z serwisu nr.1 liste jsonów

    Parameters
    ----------
    size : int
        długość listy

    Returns
    -------
    Response
        status
    """
    if service2.new_request(size):
        return '', 200
    else:
        return '', 400


@app.get('/select/<string:heads>')
def select_column(heads: str):
    """
    Przesyła plik csv w wybranym formacie

    Parameters
    ----------
    heads : str
        wybrane elementy rozdzielone przecinakmi ","

    Returns
    -------
    Response
        plik csv (gdy nie wystąpi błąd), status
    """
    to_csv, keys = service2.selected(heads)

    if not to_csv:
        return '', 400
    else:
        return flask_csv.send_csv(to_csv, 'selected.csv', keys, encoding='utf-8'), 200


@app.post('/math')
def calculate():
    """
    Przesyła plik csv z kolumnami odpowiadającymi wybranym działaniom matematycznym

    Returns
    -------
    Response
        plik csv (gdy nie wystąpi błąd), status
    """
    expresions: list = request.json.get('expresions')

    to_csv, keys = service2.calculate(expresions)

    if not to_csv:
        return '', 400
    else:
        return flask_csv.send_csv(to_csv, 'calculated.csv', keys, encoding='utf-8'), 200


@app.get('/report')
def return_report():
    """
    Przesyła raport zużycia procesora i pamięci w czasie w formie jsona

    Returns
    -------
    Response
        raport w formie jsona, status
    """
    response = service2.make_report()

    if response:
        return jsonify(response), 200
    else:
        return not_found()


@app.get('/bridge')
def bridge_rep():
    """
    Endpoint służący do przekazania raportu z serwisu nr.1 do serwisu nr.3

    Returns
    -------
    Response
        raport w formie jsona, status
    """
    response = service2.bridge()

    if response:
        return jsonify(response), 200
    else:
        return '', 400


@app.errorhandler(404)
def not_found():
    return 'Not found', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
