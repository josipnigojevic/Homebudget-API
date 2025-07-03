def test_list_default_categories(client, auth_header):
    res = client.get("/categories", headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 6

def test_create_invalid_name(client, auth_header):
    res = client.post("/categories", json={"name": ""}, headers=auth_header)
    assert res.status_code == 400

def test_delete_nonexistent_category(client, auth_header):
    res = client.delete("/categories/999", headers=auth_header)
    assert res.status_code == 404
