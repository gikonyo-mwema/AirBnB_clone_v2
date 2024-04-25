#!/usr/bin/python3
"""
This module starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    This function retrieves all states, cities, amenities and
    places from storage
    and renders them in an HTML page
    """
    states = storage.all("State").values()
    cities = storage.all("City").values()
    amenities = storage.all("Amenity").values()
    places = storage.all("Place").values()
    # Sort the objects
    states.sort(key=lambda state: state.name)
    cities.sort(key=lambda city: city.name)
    amenities.sort(key=lambda amenity: amenity.name)
    places.sort(key=lambda place: place.name)
    return render_template('100-hbnb.html', states=states, cities=cities,
                           amenities=amenities, places=places)


@app.teardown_appcontext
def teardown_db(exception):
    """
    This function removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
