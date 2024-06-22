"""
Plik główny serwisu nr.3
Wymaga działania serwisów nr.1 oraz nr.2
"""

from flask import Flask, render_template, request, jsonify
from serwis3 import Service3


app = Flask(__name__)
service3 = Service3()


@app.route('/')
def panel():
    """
    Strona główna serwisu nr.3

    Returns
    -------
        strona html
    """
    return render_template('panel.html')


@app.post('/new')
def new_jsons():
    """
    Wysyła zapytanie o wygenerrowanie nowej listy jsnonów

    Returns
    -------
        status code
    """
    if service3.new_jsons(int(request.json.get('size'))):
        return 'Ok', 200
    else:
        return 'Not ok', 400


@app.get('/basic')
def basic():
    """
    Przesyła string z pliku csv w formacie ‘type, _id, name, type, latitude, longitude’

    Returns
    -------
    str
        z pliku csv (gdy nie wystąpi błąd), status
    """
    response = service3.basic()

    if response:
        return response, 200
    else:
        return 'Response error', 400


@app.post('/select')
def select():
    """
    Przesyła string z pliku csv w wybranym formacie

    Returns
    -------
    Response
        z pliku csv (gdy nie wystąpi błąd), status
    """
    json = request.json.get('selected')

    if json:
        response = service3.select(json)
    else:
        return 'EmptySelectError', 401

    if response:
        return response, 200
    else:
        return 'Response error', 400


@app.post('/math')
def math():
    """
    Przesyła string z pliku csv z kolumnami odpowiadającymi wybranym działaniom matematycznym

    Returns
    -------
    Response
        z pliku csv (gdy nie wystąpi błąd), status
    """
    eq: str = request.json.get('text')
    eq = eq.replace(' ', '')

    if eq:
        response = service3.math(eq.split(','))
    else:
        return 'EmptySelectError', 401

    if response:
        return response, 200
    else:
        return 'Response error', 400


@app.get('/report')
def show_reports():
    """
    Strona z raportem serwisó nr.1 oraz nr.2

    Returns
    -------
        strona html
    """
    return render_template('report_site.html')


@app.get('/data')
def get_reports():
    """
    Przesyła jsona z raportami z pozostałych serwisów

    Returns
    -------
    Response
        json, status code
    """
    return jsonify(service3.get_reports()), 200


@app.route('/favicon.ico')
def favicon():
    return '', 200


@app.errorhandler(404)
def not_found():
    return 'Not found', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
