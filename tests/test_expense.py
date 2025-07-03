import pytest

@pytest.fixture
def category_id(client, auth_header):
    res = client.get("/categories", headers=auth_header)
    return res.get_json()[0]["id"]

def test_create_expense_missing_fields(client, auth_header):
    res = client.post("/expenses", json={"amount": 10}, headers=auth_header)
    assert res.status_code == 400

def test_delete_nonexistent_expense(client, auth_header):
    res = client.delete("/expenses/999", headers=auth_header)
    assert res.status_code == 404
