import flask
from flask import request
import requests
import json
import actions
from dataService import create_base_tables, list_all_candidates, top_candidates, list_campaign
from votingService import vote, create_new_campaign, get_voted_candidate, change_time_campaign

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dispatcher_url = 'http://10.2.14.53:5004'


@app.route('/advance', methods=['POST'])
def advance():
    body = request.get_json("metadata")
    print(f"Received advance request body {body}")
    create_base_tables()

    payload = bytes.fromhex(body["payload"][2:]).decode()
    print(payload)
    payload = json.loads(payload)

    if payload['action'] == actions.LIST_ALL:
        result = list_all_candidates(payload['campaign_id'])
    elif payload['action'] == actions.TOP_CANDIDATES:
        quantity = payload['quantity'] if 'quantity' in payload.keys() else 10
        result = top_candidates(payload['campaign_id'], quantity)
    elif payload['action'] == actions.VOTED_CANDIDATE:
        result = get_voted_candidate(body['metadata']['address'], payload['campaign_id'])
    elif payload['action'] == actions.VOTE:
        result = vote(body['metadata']['address'], payload['candidate_id'], payload['campaign_id'])
    elif payload['action'] == actions.CREATE_CAMPAIGN:
        result = create_new_campaign(body['metadata']['address'], payload)
    elif payload['action'] == actions.LIST_CAMPAIGN:
        result = list_campaign()
    elif payload['action'] == actions.CHANGE_TIME_CAMPAIGN:
        result = change_time_campaign(
            body['metadata']['address'],
            payload['campaign_id'],
            payload['start_time'],
            payload['end_time']
        )
    else:
        result = {}

    print(result)
    print("Result type: " + type(result).__name__)
    # add_notice(json.dumps(result))
    # finish()
    return "", 202


@app.route('/inspect', methods=['GET'])
def inspect(payload):
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
