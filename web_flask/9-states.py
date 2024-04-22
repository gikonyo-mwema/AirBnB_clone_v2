#!/usr/bin/python3
"""
This module starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def states():
    """
    This function retrieves all states from storage
    and renders them in an HTML page
    """
    states = sorted(storage.all("State").value(),
                    key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>')
def states_id(id):
    """
    This function retrieves a state by its id from storage
    and renders it in an HTML page
    """
    state = storage.get("State", id)
    if state is None:
        return render_template('404.html'), 404
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def teardown_db(exception):
    """
    This function removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
