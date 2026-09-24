def test_checkin(client):
    response = client.post("/checkin",
                           json={"city": "London", "intensity": -1},
                           headers={"X-Device-ID": "test-checkin-123"})
    assert response.status_code == 200
    assert "thermo_offset" in response.json()