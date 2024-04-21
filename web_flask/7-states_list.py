#!/usr/bin/python3
"""
Module starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    This function renders a HTML page with a list of all State
    objects present in DBStorage sorted by name (A->Z)
    """
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def handle_teardown(exc):
    """
    This function removes the current SQLAlchemy session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
