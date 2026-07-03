from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/1", json={"name": "Laptop", "price": 1000})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item created"
    assert data["item"]["name"] == "Laptop"
    assert data["item"]["price"] == 1000

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1000

def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_duplicate_item():
    response = client.post("/items/1", json={"name": "Laptop", "price": 1000})
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}