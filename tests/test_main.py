from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_root():
    r = client.get("/")
    assert r.status_code == 200


def test_create_item():
    r = client.post("/items", json={"title": "Buy milk"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False
    assert "id" in data


def test_list_items():
    r = client.get("/items")
    assert r.status_code == 200
    assert "items" in r.json()


def test_toggle_item():
    r = client.post("/items", json={"title": "Toggle me"})
    item_id = r.json()["id"]
    r2 = client.put(f"/items/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["done"] is True


def test_delete_item():
    r = client.post("/items", json={"title": "Delete me"})
    item_id = r.json()["id"]
    r2 = client.delete(f"/items/{item_id}")
    assert r2.status_code == 200


def test_not_found():
    r = client.put("/items/99999")
    assert r.status_code == 404