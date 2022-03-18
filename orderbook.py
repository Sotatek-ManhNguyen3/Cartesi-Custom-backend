import flask
from flask import request
from order_book import OrderBook
import json
import requests
from decimal import Decimal

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/advance', methods=['POST'])
def advance():
    body = request.get_json("metadata")
    print(f"Received advance request body {body}")
    data = bytes.fromhex(body["payload"][2:])
    data = json.loads(data.decode())
    print(data['type'])

    ob = OrderBook()
    data = requests.get("https://api.pro.coinbase.com/products/BTC-USD/book?level=2").json()

    ob.bids = {Decimal(price): size for price, size, _ in data['bids']}
    ob.asks = {Decimal(price): size for price, size, _ in data['asks']}

    # Data is accessible by .index(), which returns a tuple of (price, size) at that level in the book
    price, size = ob.bids.index(0)
    print(f"Best bid price: {price} size: {size}")

    price, size = ob.asks.index(0)
    print(f"Best ask price: {price} size: {size}")

    print(f"The spread is {ob.asks.index(0)[0] - ob.bids.index(0)[0]}\n\n")

    # Data is accessible via iteration
    # Note: bids/asks are iterators

    print("Bids")
    for price in ob.bids:
        if price == 23650:
            print("Matcheddddddd")
            print(f"Price: {price} Size: {ob.bids[price]}")
            break

    # print("\n\nAsks")
    # for price in ob.asks:
    #     print(f"Price: {price} Size: {ob.asks[price]}")
    return "", 202


@app.route('/inspect', methods=['GET'])
def inspect(payload):
    print('abcde')
    print(f"Received inspect request payload {payload}")
    return {"reports": [{"payload": payload}]}, 200


app.run(port=5003)
