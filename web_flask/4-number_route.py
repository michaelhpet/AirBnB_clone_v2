#!/usr/bin/python3
"""Flask web application."""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Respond with Hello HBNB!."""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Respond with HBNB."""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Handle c route."""
    text = text.replace("_", " ")
    return f"C {text}"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """Handle Python route."""
    text = text.replace("_", " ")
    return f"Python {text}"


@app.route("/number/<n>", strict_slashes=False)
def n(n):
    """Handle number route."""
    try:
        n = int(n)
        return f"{n} is a number"
    except ValueError:
        pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
