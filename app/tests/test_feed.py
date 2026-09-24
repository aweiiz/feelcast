def test_feed_empty(client):
    response = client.get("/feed?city=TestCity9999")
    assert response.json() == []
    assert response.status_code == 200