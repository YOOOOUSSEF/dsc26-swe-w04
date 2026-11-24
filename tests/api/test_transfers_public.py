def test_request_transfer_returns_a_pending_card(client):
    r = client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                                           "toBranch": "tanta", "quantity": 20})
    assert r.status_code == 201
    assert r.json()["status"] == "pending"

def test_Approving_an_already_approved_transfer_fails(client):
    a = client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                                           "toBranch": "tanta", "quantity": 20})
    b=client.post(f"/v1/transfers/{a.json()['id']}/approve")

    c=client.post(f"/v1/transfers/{a.json()['id']}/approve")
    
    assert b.status_code == 200
    assert b.json()['status']=='approved'
    assert c.status_code==409
    assert c.json()['type']=='/problems/not-pending'

def test_cors_rejects_unapproved_origin(client):
    # ( not allowed origin )
    a= client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                "toBranch": "tanta", "quantity": 20},headers={'Origin':'http://evil.com'})
    assert a.status_code == 201
    assert "access-control-allow-origin" not in a.headers
    assert a.json()['status']=='pending'

    # normal request (Allowed origin)
    b= client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                "toBranch": "tanta", "quantity": 20},headers={'Origin':'https://branch.nour.example'})
    assert b.status_code == 201
    assert b.json()['status']=='pending'
    assert "access-control-allow-origin" in b.headers



def test_inbox_sorted_by_priority(client):
    high_first = client.post("/v1/transfers", json={"itemCode": "AMOX250", "fromBranch": "heliopolis",
                                                    "toBranch": "tanta", "quantity": 1})
    urgent = client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                                                 "toBranch": "tanta", "quantity": 1})
    high_second = client.post("/v1/transfers", json={"itemCode": "AMOX250", "fromBranch": "heliopolis",
                                                      "toBranch": "tanta", "quantity": 1})

    assert high_first.status_code == urgent.status_code == high_second.status_code == 201

    inbox = client.get("/v1/branches/tanta/transfers")
    # check on both id adn priority.
    assert inbox.status_code == 200
    assert [(item["id"], item["priority"]) for item in inbox.json()["items"]] == [
        (urgent.json()["id"], "urgent"),
        (high_first.json()["id"], "high"),
        (high_second.json()["id"], "high"),
    ]

def test_error_response_has_correct_media_type(client):
    response = client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                                                  "toBranch": "tanta", "quantity": 0})

    assert response.status_code == 422
    assert response.headers["content-type"].split(";")[0] == "application/problem+json"

def test_same_branch_transfer_is_rejected(client):
    response = client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                                                  "toBranch": "heliopolis", "quantity": 1})

    assert response.status_code==422
    assert response.json()['type']=='/problems/same-branch'

def test_approval_credits_destination_stock(client):
    transfer = client.post("/v1/transfers", json={"itemCode": "MET500", "fromBranch": "heliopolis",
                                                  "toBranch": "tanta", "quantity": 20})
    assert transfer.status_code == 201

    before_approval = client.get("/v1/branches/tanta/stock/MET500")
    assert before_approval.json()["units"] == 2

    approval = client.post(f"/v1/transfers/{transfer.json()['id']}/approve")
    assert approval.status_code == 200
    assert approval.json()["status"] == "approved"

    after_approval = client.get("/v1/branches/tanta/stock/MET500")
    assert after_approval.json()["units"] == 22