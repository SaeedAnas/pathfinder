from crypt import methods
from flask import Flask, abort, render_template, jsonify, request
from db import fetch_pathways

app = Flask(__name__)
pathways = fetch_pathways()
suggestions = pathways.get_positions()

def next(position, count=2):

    prediction = []

    for _ in range(count):
        n = pathways.predict(position)

        if n is None:
            break

        prediction.append(n.serialize())
        position = n.position

    return prediction

@app.route("/")
def index():
    return render_template('index.html', suggestions=suggestions)

@app.route("/api/<path:position>/")
def api(position):
    current = pathways.get(position)

    if current is None:
        abort(404)

    prediction = next(current)
    current = pathways.pathways[current]

    data = {"current": current.serialize(), "prediction": prediction}

    return jsonify(data)