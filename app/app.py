"""Basic Transaction Logging Python Chalice API"""
import os
import boto3
import time
from chalice import Chalice, Response, BadRequestError
from boto3.dynamodb.conditions import Key
from datetime import datetime
from uuid import UUID

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
    print(data)

    return {"data": data}


@app.route("/transaction/{request_id}", methods=["GET"])
def item_get(request_id):
    """ Returns all itmes with the specified UUID """
    if request_id is None or request_id == "":
        raise BadRequestError("Empty request, requires UUID of tranasaction")

    query_response = get_table().query(
        KeyConditionExpression=Key("UUID").eq(request_id)
    )
    data = query_response.get("Items", None)

    return {"data": data}


@app.route("/transaction", methods=["POST"])
def item_set():
    """ Creates an item based on the request body """
    data = app.current_request.json_body
    print(data)

    if data is None:
        raise BadRequestError("Empty request body, requires UUID")

    if "UUID" not in data:
        raise BadRequestError("Invalid request body, missing UUID.")

    # Validate that the UUID fits the UUID v4 model
    try:
        UUID(data.get("UUID"))
    except ValueError as invalid_uuid:
        raise BadRequestError("Invalid UUID.") from invalid_uuid

    # Create a timestamp of when the transaction was completed (the time the call is made to transaction-logging), this will be used as the Sort Key.
    data["Timestamp"] = int(time.time())
    get_table().put_item(Item=data)

    return Response(
        body={
            "message": "Created new transaction log",
            "UUID": data["UUID"],
            "Timestamp": data["Timestamp"],
        },
        status_code=201,
        headers=None,
    )


@app.route("/hello/{name}")
def hello_name(name):
    """ Test function for hello endpoint """
    # '/hello/james' -> {"hello": "james"} update
    return {"hello": name}


@app.route("/transaction/{request_id}/{time_stamp}", methods=["DELETE"])
def item_delete(request_id, time_stamp):
    """ Deletes a specific item based on request_id """
    if request_id is None or request_id == "":
        raise BadRequestError("Invalid UUID, UUID cannot be empty")
    if time_stamp is None or time_stamp == "":
        raise BadRequestError("Invalid Timestamp, Timestamp cannot be empty")

    # Delete item from DB, return the item that was deleted as 'Attributes'
    response_from_db = get_table().delete_item(
        Key={"UUID": request_id, "Timestamp": int(time_stamp)}, ReturnValues="ALL_OLD"
    )
    if "Attributes" not in response_from_db:
        raise BadRequestError("Item does not exist in table")
    return {"message": "Successfully deleted transaction log"}
