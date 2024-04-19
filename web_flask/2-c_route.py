#!/usr/bin/python3
"""
This module starts Flask web application
"""


from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    Function associated with the '/' route

    Returns:
        str: 'Hello HBNB!'
    """
    return 'Hello HBNB!'


@app.route('/hbhb', strict_slashes=False)
def hbnb():
    """
    Function associated with the '/hbnb' route

    Returns:
        str: 'HBNB'
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Function associated with the '/c/<text>' route

    Args:
        text (str): The text to display after 'C'

    Returns:
        str: 'C' followed by the value of the text variable
    """
    return 'C %s' % text.replace('_', ' ')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
