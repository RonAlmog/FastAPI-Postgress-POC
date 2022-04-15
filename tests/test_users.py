from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    # print(res.json())
    assert res.json().get('message') == 'Hello Worldz'
    assert res.status_code == 200


def test_create_user():
    res = client.post("/users/", json={})
