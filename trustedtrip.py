import flask
from flask import request
import requests
import json
from lib import picket

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dispatcher_url = 'http://10.2.14.53:5004'


def isInTheTollZone(gps_data):
    latitude = float(gps_data[2][:2]) + float(gps_data[2][2:]) / 60
    longitude = float(gps_data[4][:2]) + float(gps_data[4][2:]) / 60
    print("Latitude: " + str(latitude))
    print("Longitude: " + str(longitude))

    f = open('Airport_Runway_Protection_Zone_and_Inner_Safety_Zone.geojson')
    data = json.load(f)

    for zone in data['features']:
        if zone['properties']['ZONE_TYPE'] != "Runway Protection Zone":
            continue

        if checkPointInZone(zone['geometry']['coordinates'], latitude, longitude):
            print("Return true")
            return True

    print("Return false")
    return False


def checkPointInZone(gps_data, latitude, longitude):
    print(gps_data[0][0])
    if type(gps_data[0][0]) in (float, int):
        if len(gps_data) < 3:
            print("length is less than 3")
            return False

        fence = create_fence(gps_data)
        if fence.check_point((latitude, longitude)):
            return True

        return False

    for inner_zone in gps_data:
        is_in_zone = checkPointInZone(inner_zone, latitude, longitude)
        if is_in_zone:
            return True

    return False


def create_fence(coordinates):
    fence = picket.Fence()

    for each_pair in coordinates:
        fence.add_point((each_pair[0], each_pair[1]))

    return fence


def to_hex(value):
    return "0x" + value.encode().hex()


def add_notice(message):
    message = to_hex(message)
    print("Adding notice")
    response = requests.post(dispatcher_url + "/notice", json={"payload": message})
    print(f"Received notice status {response.status_code} body {response.json()}")
    return True


def add_voucher(address, message):
    message = to_hex(message)
    print("Adding voucher")
    response = requests.post(dispatcher_url + "/voucher", json={"payload": message, "address": address})
    print(f"Received voucher status {response.status_code}")
    return True


def finish():
    print("Finishing")
    response = requests.post(dispatcher_url + "/finish", json={"status": "accept"})
    print(f"Received finish status {response.status_code}")
    return True


@app.route('/advance', methods=['POST'])
def advance():
    body = request.get_json("metadata")
    print(f"Received advance request body {body}")

    data = bytes.fromhex(body["payload"][2:])
    data = data.decode().split(",")
    print(data)

    is_toll_zone = isInTheTollZone(data)
    # is_toll_zone = True

    if is_toll_zone:
        result = "You are in the toll zone. You need to pay the fee!!!"
        address = body["metadata"]["msg_sender"]
        add_voucher(address, result)
    else:
        result = "You are good"
        add_notice(result)

    print("result in hex")
    print(result)
    finish()
    return "", 202


@app.route('/inspect', methods=['GET'])
def inspect(payload):
    print('abcde')
    print(f"Received inspect request payload {payload}")
    return {"reports": [{"payload": payload}]}, 200


app.run(port=5003)
