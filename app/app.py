"""Basic Transaction Logging Python Chalice API"""
import json
import boto3
from chalice import Chalice, Response
from boto3.dynamodb.conditions import Key

with open(".chalice/config.json") as config_file:
    CONFIG = json.load(config_file)

if "app_name" not in CONFIG:
    raise KeyError("No 'app_name' configured in app/.chalice/config.json")

APP_NAME = CONFIG.get("app_name")
app = Chalice(app_name=APP_NAME)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("transaction-logs-1")


@app.route("/", methods=["GET"])
def index():
    """recieves get requests, returns all items in the table"""
    response = table.scan()
    data = response.get("Items", None)

    return {"data": data}


@app.route("/item/{request_id}", methods=["GET"])
def item_get(request_id):
    """recieves a get request for a specific item based on id, returns the specified item"""
    query_response = table.query(KeyConditionExpression=Key("id").eq(request_id))
    data = query_response.get("Items", None)

    return {"data": data}


@app.route("/item", methods=["POST"])
def item_set():
    """recieves a post request to create a new item, creates the item or returns error message"""
    data = app.current_request.json_body
    try:
        table.put_item(Item={"id": data["id"], "text": data["text"]})
        return Response(body={"message": "Created new transaction log", "id": data["id"]},
            status_code=201,headers=None)
    except KeyError:
        return Response(body={"message": "Invalid request body"}, status_code=400,headers=None)


@app.route("/hello/{name}")
def hello_name(name):
    """test function for hello endpoint"""
    # '/hello/james' -> {"hello": "james"}
    return {"hello": name}
