import pytest

def test_register_validation(client):
    res = client.post("/auth/register", json={})
    assert res.status_code == 400
    assert "errors" in res.get_json()

def test_login_missing_credentials(client):
    res = client.post("/auth/login", json={})
    assert res.status_code == 400

def test_protected_without_token(client):
    res = client.get("/categories")
    assert res.status_code == 401
