#!/usr/bin/python3
"""
This module starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def hbnb_filters():
    """
    This function retrieves all states, cities and amenities from storage
    and renders them in an HTML page
    """
    states = sorted(storage.all("State").values(),
                    key=lambda state: state.name)
    cities = sorted(storage.all("City").value(), key=lambda city: city.name)
    amenities = sorted(storage.all("Amenity").value(),
                       key=lambda amenity: amenity.name)
    return render_template('10-hbnb_filters.html', states=states,
                           cities=cities, amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """
    This function removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
