from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI Calculator is running"}

def test_add_endpoint():
    response = client.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_subtract_endpoint():
    response = client.get("/subtract?a=5&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 2

def test_multiply_endpoint():
    response = client.get("/multiply?a=4&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 12

def test_divide_endpoint():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_divide_by_zero_endpoint():
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero"