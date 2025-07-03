import pytest

def auth_header(client):
    client.post('/auth/register', json={'username':'s1','password':'pw3','starting_budget':0})
    token = client.post('/auth/login', json={'username':'s1','password':'pw3'}).get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_stats_no_expenses(client, auth_header):
    res = client.get("/expenses/stats?period=last_month", headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_spent"] == 0
    assert data["total_earned"] == 0
    assert data["net_flow"] == 0


