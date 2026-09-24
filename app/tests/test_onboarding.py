def test_onboarding(client):
    response = client.post("/onboarding",
                           json = {"cold_sensitivity": "мёрзну больше", "climate": "тёплый", "activity": "активно", "rain_sensitivity": "очень важно"},
                           headers={"X-Device-ID": "test-checkin-123"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"




