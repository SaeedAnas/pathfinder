from flask import Flask, abort, render_template, jsonify, request
from db import fetch_cache, add_to_csv
import util

app = Flask(__name__)
pathways = fetch_cache()
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

    position = position.replace('_', ' ')
    current = pathways.get(position)

    if current is None:
        abort(404)

    prediction = next(current)
    current = pathways.pathways[current]

    data = {"current": current.serialize(), "prediction": prediction}

    return jsonify(data)

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()

    id = data['id']
    position = data['position']
    start = data['start']
    end = data['end']

    if None in (id , position, start, end):
        abort(400)

    if type(id) is int:
        id = str(id)
    else:
        id = id if id.isdigit() else None

    start = start if util.is_date(start) else None
    end = end if util.is_date(end) or end == "" else None

    if None in (id , position, start, end):
        abort(400)
    
    entry = [id, position, start, end]

    add_to_csv(','.join(entry))

    return jsonify({"status": "success"})
