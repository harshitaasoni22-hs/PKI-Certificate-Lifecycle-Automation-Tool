import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200

def test_issue(client):
    r = client.post("/api/v1/issue",
        json={"common_name": "test.example.com"})
    assert r.status_code == 201
    data = r.get_json()
    assert "serial" in data

def test_status(client):
    client.post("/api/v1/issue",
        json={"common_name": "status.test.com"})
    r = client.get("/api/v1/status/status.test.com")
    assert r.status_code == 200
    data = r.get_json()
    assert data is not None
    assert data["status"] == "VALID"

def test_revoke(client):
    client.post("/api/v1/issue",
        json={"common_name": "revoke.test.com"})
    r = client.post("/api/v1/revoke",
        json={"common_name": "revoke.test.com"})
    assert r.get_json()["revoked"] == True

def test_renew(client):
    client.post("/api/v1/issue",
        json={"common_name": "renew.test.com"})
    r = client.post("/api/v1/renew",
        json={"common_name": "renew.test.com"})
    assert r.status_code == 200