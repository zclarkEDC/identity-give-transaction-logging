""" Tests for app.py """
import json
from http import HTTPStatus
from chalice.test import Client
from pytest import fixture
from app import app


@fixture(name="client_fixture")
def test_client():
    """ Test fixture for creating a chalice Client """
    with Client(app) as client:
        yield client


# transaction log tests
def test_create_transaction_log_function_bad_request_empty_body(client_fixture):
    """ Ensure the create transaction log function returns a 400 Bad Request on bad/empty requests """
    # empty request
    response = client_fixture.http.post("/transaction")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_transaction_log_function_bad_request_invalid_uuid(client_fixture):
    """ Ensure the create transaction log function returns a 400 Bad Request for invalid uuid """
    # invalid uuid
    req_invalid = {
        "UUID": "c7b82090-172f-11eb-adc1-",
        "Customer": "Login.gov",
        "Service": "Attribute Validation",
        "CSP": "State SSN Verification",
        "Result": "SSN Match",
        "Cost": ".25",
    }
    response = client_fixture.http.request(
        method="POST",
        path="/transaction",
        headers={"Content-Type": "application/json"},
        body=json.dumps(req_invalid),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_transaction_log_function_bad_request_empty_body(client_fixture):
    """ Ensure the delete transaction log function returns a 400 Bad Request on bad/empty requests """
    # the UUID path variable is empty
    response = client_fixture.http.delete("/transaction//3")
    assert response.status_code == HTTPStatus.BAD_REQUEST
