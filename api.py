import flask
from flask import request, jsonify
import requests
import json
import sqlite3
from dataService import dict_factory, create_candidates

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dispatcher_url = 'http://10.2.14.53:5004'


@app.route('/advance', methods=['POST'])
def advance():
    body = request.get_json("metadata")
    print(f"Received advance request body {body}")
    create_candidates()
    return "", 202

    query = bytes.fromhex(body["payload"][2:]).decode()
    print(query)
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory

    try:
        with conn:
            cur = conn.cursor()
            result = cur.execute(query)
        if query.strip()[:6].upper() == "SELECT":
            result = json.dumps(result.fetchall())
        else:
            result = "success"
    except Exception as e:
        result = "EXCEPTION: " + e.__str__()
        print("NOTICE EXCEPTION" + e.__str__())

    print(result)
    add_notice(result)
    finish()
    return "abc", 202


@app.route('/inspect', methods=['GET'])
def inspect(payload):
    print('abcde')
    print(f"Received inspect request payload {payload}")
    return {"reports": [{"payload": payload}]}, 200


def to_hex(value):
    return "0x" + value.encode().hex()


def add_notice(message):
    message = to_hex(message)
    print("Adding notice")
    response = requests.post(dispatcher_url + "/notice", json={"payload": message})
    print(f"Received notice status {response.status_code} body {response.json()}")
    return True


def finish():
    print("Finishing")
    response = requests.post(dispatcher_url + "/finish", json={"status": "accept"})
    print(f"Received finish status {response.status_code}")
    return True


app.run(port=5003)
