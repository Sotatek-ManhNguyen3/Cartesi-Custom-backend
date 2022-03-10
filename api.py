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


def createTableBook():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    result = cur.execute(sql_query)
    tables = result.fetchall()
    if len(tables) == 0:
        print("Books table does not exist")
        query_create_table = "CREATE TABLE books(id integer NOT NULL, name text NOT NULL, quantity integer NOT NULL);"
        cur.execute(query_create_table)
    else:
        print("Books table exists")


@app.route('/advance', methods=['POST'])
def advance():
    dispatcher_url = 'http://192.168.31.148:5004'
    body = request.get_json("metadata")
    print(f"Received advance request body {body}")
    createTableBook()

    query = bytes.fromhex(body["payload"][2:])
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    query = query.decode()
    print(query)

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
    result = "0x" + result.encode().hex()
    print("result")
    print(result)
    # print("Adding notice")
    # response = requests.post(dispatcher_url + "/notice", json={"payload": result})
    # print(f"Received notice status {response.status_code} body {response.json()}")
    # # print("Adding report")
    # # response = requests.post(dispatcher_url + "/report", json={"payload": result})
    # # print(f"Received report status {response.status_code}")
    # # print("Adding voucher")
    # # address = "0x1111111111111111111111111111111111111111"
    # # response = requests.post(dispatcher_url + "/voucher", json={"payload": result, "address": address})
    # # print(f"Received voucher status {response.status_code}")
    # print("Finishing")
    # response = requests.post(dispatcher_url + "/finish", json={"status": "accept"})
    # print(f"Received finish status {response.status_code}")
    return "abc", 202


@app.route('/inspect', methods=['GET'])
def inspect(payload):
    print('abcde')
    print(f"Received inspect request payload {payload}")
    return {"reports": [{"payload": payload}]}, 200


app.run(port=5003)
