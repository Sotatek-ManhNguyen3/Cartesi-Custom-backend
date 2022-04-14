import flask
from flask import request
import requests
import json
from lib import picket

app = flask.Flask(__name__)
app.config["DEBUG"] = True


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

        for inner_zone in zone['geometry']['coordinates']:
            if len(inner_zone) < 3:
                continue

            fence = create_fence(inner_zone)
            if fence.check_point((longitude, latitude)):
                return True

    return False


def create_fence(coordinates):
    fence = picket.Fence()

    for each_pair in coordinates:
        fence.add_point((each_pair[0], each_pair[1]))

    return fence


@app.route('/advance', methods=['POST'])
def advance():
    dispatcher_url = 'http://10.2.14.167:5004'
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
    return "", 202


@app.route('/inspect', methods=['GET'])
def inspect(payload):
    print('abcde')
    print(f"Received inspect request payload {payload}")
    return {"reports": [{"payload": payload}]}, 200


app.run(port=5003)
