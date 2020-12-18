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
