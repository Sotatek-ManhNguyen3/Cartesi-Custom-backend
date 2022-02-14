import flask
from flask import request, jsonify
import requests
import sqlite3
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction " \
           "novels.</p> "


@app.route('/advance', methods=['POST'])
def advance():
    dispatcher_url = 'http://10.2.14.167:5004'
    body = request.get_json("metadata")
    print(f"Received advance request body {body}")

    query = bytes.fromhex(body["payload"][2:])
    conn = sqlite3.connect('books')
    conn.row_factory = dict_factory
    query = query.decode()
    print(query)
    with conn:
        cur = conn.cursor()
        result = cur.execute(query)
    if query.strip()[:6].upper() == "SELECT":
        result = json.dumps(result.fetchall())
    else:
        result = "success"

    print("Adding notice")
    result = "0x" + result.encode().hex()
    print(result)
    response = requests.post(dispatcher_url + "/notice", json={"payload": result})
    print(f"Received notice status {response.status_code} body {response.json()}")
    print("Finishing")
    response = requests.post(dispatcher_url + "/finish", json={"status": "accept"})
    print(f"Received finish status {response.status_code}")
    return "abc", 202


@app.route('/inspect', methods=['GET'])
def inspect(payload):
    print('abcde')
    print(f"Received inspect request payload {payload}")
    return {"reports": [{"payload": payload}]}, 200


@app.route('/save-data', methods=['POST'])
def save_data():
    body = request.get_json("metadata")
    query = bytes.fromhex(body["payload"][2:])
    conn = sqlite3.connect('books')
    conn.row_factory = dict_factory
    query = query.decode()
    print(query)
    with conn:
        cur = conn.cursor()
        result = cur.execute(query)
    if query.strip()[:6].upper() == "SELECT":
        # result = jsonify(result.fetchall())
        result = json.dumps(result.fetchall())
    else:
        result = "success"

    result = "0x" + result.encode().hex()
    return result, 202


@app.route('/get-data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('books')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    response = all_books
    return jsonify(response), 202


app.run(port=5003)
