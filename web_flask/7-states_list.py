#!/usr/bin/python3
"""
Module starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states_list")
def states_list():
    """
    This function renders a HTML page with a list of all State
    objects present in DBStorage sorted by name (A->Z)
    """
    states = sorted(list(storage.all("State").values()),
                    key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def handle_teardown(exc):
    """
    This function removes the current SQLAlchemy session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
