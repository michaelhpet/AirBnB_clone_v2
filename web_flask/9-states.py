#!/usr/bin/python3
"""Flask web application."""
from flask import Flask
from flask import render_template
from models import storage


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


@app.route("/number/<int:n>", strict_slashes=False)
def n(n):
    """Handle number route."""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Render number page."""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """Render number odd or even template."""
    return render_template("6-number_odd_or_even.html", n=n)


@app.route("/states", strict_slashes=False)
def states():
    """Render states."""
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Render a single state."""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
