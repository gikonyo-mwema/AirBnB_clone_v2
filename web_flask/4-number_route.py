#!/usr/bin/python3
"""
Script that starts a Flask web application.
"""


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    Function associated with the '/' route.

    Returns:
        str: 'Hello HBNB!'
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
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
    Function associated with '/c/<text>' route

    Args:
        text (str): The text to display after 'C'

    Returns:
        str: 'C ' followed by the value of the text variable
    """
    return 'C %s' % text.replace('_', ' ')


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Function associated with teh '/python/<text>' route

    Args:
        text (str): The text to display after 'Python '

    Returns:
        str: 'Python ' followed by the value of the text variable
    """
    return 'Python %s' % text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def number_n(n):
    """
    Function associated with the '/number/<n>' route

    Args:
        n (int): The number to display

    Returns:
        str: '<n> is a number'
    """
    return '%d is a number' % n


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
