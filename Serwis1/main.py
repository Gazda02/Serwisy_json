"""
Plik główny serwisu nr.1
Wymaga działania serwisów nr.2 oraz nr.3
"""

from serwis1 import Service1
from flask import Flask, jsonify

app = Flask(__name__)
service1 = Service1()


@app.get('/generate/json/<int:size>')
def generate_jsons(size: int):
    """
    Przesyła podaną ilość losowych jsonów o określonych kluczach

    Parameters
    ----------
    size : int
        Ilość jsonów

    Returns
    -------
    Response
        wygenerowane jsony, status
    """
    return jsonify(service1.generate_jsons(size)), 200


@app.get('/report')
def make_report():
    """
    Przesyła raport zużycia procesora i pamięci w czasie w formie jsona

    Returns
    -------
    Response
        raport w formie jsona, status
    """
    response = service1.make_report()

    if response:
        return jsonify(response), 200
    else:
        return not_found()


@app.errorhandler(404)
def not_found():
    return 'Not found', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
