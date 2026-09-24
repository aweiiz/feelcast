def test_whoami(client):
    response = client.get("/whoami", headers={"X-Device-ID": "test-device-123"})
    assert response.status_code == 200
    assert response.json()["device_id"] == "test-device-123"
    assert "user_id" in response.json()

