import json
import pathlib
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

from nour_transfers.app import create_app

SCHEMA = json.loads((pathlib.Path(__file__).parents[2] / "contracts/transfer_card.schema.json").read_text())


def test_card_matches_what_the_branch_app_expects(client):
    r = client.post("/v1/transfers", json={"itemCode": "AMOX250", "fromBranch": "heliopolis",
                                           "toBranch": "tanta", "quantity": 5})
    Draft202012Validator(SCHEMA, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(r.json())


def test_response_fields_use_exact_camelCase_names(client):
    response = client.post("/v1/transfers", json={"itemCode": "AMOX250", "fromBranch": "heliopolis",
                                                  "toBranch": "tanta", "quantity": 5})

    assert response.status_code == 201
    assert response.json().keys() == {
        "id",
        "itemCode",
        "fromBranch",
        "toBranch",
        "quantity",
        "priority",
        "status",
        "requestedAt",
    }

def test_requested_at_includes_timezone_z_or_offset(client):
    response = client.post("/v1/transfers", json={"itemCode": "AMOX250", "fromBranch": "heliopolis",
                                                  "toBranch": "tanta", "quantity": 5})

    assert response.status_code == 201
    assert response.json()["requestedAt"].endswith("Z")

    offset_client = TestClient(create_app(
        stock={("source", "ITEM"): 10, ("destination", "ITEM"): 0},
        items={"ITEM": {"chronic": False, "reserve": 0}},
        now=lambda: datetime(2026, 11, 3, 12, 30, tzinfo=timezone(timedelta(hours=3))),
    ))
    offset_response = offset_client.post("/v1/transfers", json={"itemCode": "ITEM", "fromBranch": "source",
                                                                 "toBranch": "destination", "quantity": 1})

    assert offset_response.status_code == 201
    assert offset_response.json()["requestedAt"].endswith("+03:00")