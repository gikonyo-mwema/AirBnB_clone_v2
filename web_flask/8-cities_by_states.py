#!/usr/bin/python3
"""
This module starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    """
    This function retrieves all states and their cities from storage
    and renders them in a HTML page
    """
    states = sorted(storage.all("State").values(),
                    key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
    This function removes the current SQLAlchem Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
