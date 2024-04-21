#!/usr/bin/python3
"""
Module starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    """
    This function renders a HTML page with a list of all State
    objects present in DBStorage sorted by name (A->Z)
    """
    states = storage.all("State").values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=state)


@app.teardown_appcontext
def teardown_db(exception):
    """
    This function removes the current SQLAlchemy session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
