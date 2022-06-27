import enum
from flask import Flask, abort, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from dataclasses import dataclass
import json

app = Flask(__name__)
cors = CORS(app)


database = 'db.json'

@dataclass
class Node:
    title: str
    avg_time: str
    count: int
    percent: float

@dataclass
class Pathway:
    title: str
    avg_time: str
    nodes: list

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/<title>/")
def api(title):
    if title not in database:
        abort(404)
    pathway = Pathway(title, "3 years", [Node("Software Engineer", "5 months", 10, 50.0), Node("Sr. Software Engineer", "3 years", 4, 100)])
    return render_template('pathway.html', pathway=pathway)

@app.route('/post', methods=["POST"])
@cross_origin()
def save():
    content_type = request.headers.get('Content-Type')
    print(content_type)
    if (content_type == 'application/json'):
        data = json.loads(request.get_data())
        write(data)
        return jsonify({"success": "true"})
    else:
        return jsonify({"error": "Content-Type not supported!"})

@app.route('/details', methods=["POST"])
@cross_origin()
def overwrite():
    content_type = request.headers.get('Content-Type')
    print(content_type)
    if (content_type == 'application/json'):
        data = json.loads(request.get_data())
        write(data, overwrite=True)
        return jsonify({"success": "true"})
    else:
        return jsonify({"error": "Content-Type not supported!"})

def write(data, overwrite=False):
    f = open(database)
    db = json.load(f)
    exists = False
    for index, item in enumerate(db):
        if item['path'] == data['path']:
            if overwrite:
                print(f"path `{item['path']}` exists, overwriting.")
                db[index] = data
            else:
                print(f"path `{item['path']}` exists")
            exists = True
            break
    if not exists:
        print(f'writing `{data["path"]}` to db.')
        db.append(data)
    with open(database, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)