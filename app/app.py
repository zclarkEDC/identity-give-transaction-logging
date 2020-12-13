"""Basic Transaction Logging Python Chalice API"""
import os
import boto3
from chalice import Chalice, Response
from boto3.dynamodb.conditions import Key

app = Chalice(app_name="transaction-logging")
_DYNAMODB = boto3.resource("dynamodb")
_TABLE = None


def get_table():
    """ Return the Transaction Logging Table """
    global _TABLE  # Assignment to global variable will need 'global' keyword

    # Only initialize the Table once for the entire application to limit
    # object duplication and function resource utilization.
    if _TABLE is None:
        _TABLE = _DYNAMODB.Table(os.environ["TRANSACTION_LOG_TABLE"])

    return _TABLE


@app.route("/", methods=["GET"])
def index():
    """ Return all items in the table"""
    response = get_table().scan()
    data = response.get("Items", None)

    return {"data": data}


@app.route("/item/{request_id}", methods=["GET"])
def item_get(request_id):
    """ Returns a specific item based on request_id """
    query_response = get_table().query(KeyConditionExpression=Key("id").eq(request_id))
    data = query_response.get("Items", None)

    return {"data": data}


@app.route("/item", methods=["POST"])
def item_set():
    """ Creates an item based on the request body """
    data = app.current_request.json_body
    try:
        get_table().put_item(Item={"id": data["id"], "text": data["text"]})
        return Response(
            body={"message": "Created new transaction log", "id": data["id"]},
            status_code=201,
            headers=None,
        )
    except KeyError:
        return Response(
            body={"message": "Invalid request body"}, status_code=400, headers=None
        )


@app.route("/hello/{name}")
def hello_name(name):
    """ Test function for hello endpoint """
    # '/hello/james' -> {"hello": "james"}
    return {"hello": name}
