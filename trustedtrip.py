import flask
from flask import request, jsonify
import requests
import json
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def isInTheTollZone(gps_data):
    print("Latitude: " + gps_data[2])
    print("Longtitude: " + gps_data[4])
    return random.randint(0, 1) == 1


@app.route('/advance', methods=['POST'])
def advance():
    dispatcher_url = 'http://192.168.31.148:5004'
    body = request.get_json("metadata")
    print(f"Received advance request body {body}")

    data = bytes.fromhex(body["payload"][2:])
    data = data.decode().split(",")
    print(data)

    is_toll_zone = isInTheTollZone(data)

    if is_toll_zone:
        result = "You are in the toll zone. You need to pay the fee!!!"
    else:
        result = "You are good"

    print(result)
    result = "0x" + result.encode().hex()
    print("result in hex")
    print(result)
    print("Adding notice")
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


app.run(port=5003)
