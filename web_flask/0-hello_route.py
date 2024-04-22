#!/usr/bin/python3
"""
This module starts a Flask web application
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """
    Function associated with the '/' route

    Returns:
        str: 'Hello HBNB!'
    """
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)