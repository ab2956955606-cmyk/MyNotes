def test_ai_settings_are_saved_without_exposing_key(client):
    saved = client.put(
        "/api/ai/settings",
        json={
            "provider": "deepseek",
            "baseUrl": "https://api.deepseek.com",
            "model": "deepseek-chat",
            "apiKey": "sk-test-local",
            "temperature": 0.2,
            "timeoutSeconds": 30,
        },
    )
    assert saved.status_code == 200
    body = saved.json()
    assert body["provider"] == "deepseek"
    assert body["hasApiKey"] is True
    assert "apiKey" not in body

    loaded = client.get("/api/ai/settings")
    assert loaded.status_code == 200
    assert loaded.json()["hasApiKey"] is True
    assert "apiKey" not in loaded.json()


def test_ai_settings_test_uses_mock_without_key(client):
    saved = client.put(
        "/api/ai/settings",
        json={
            "provider": "mock",
            "baseUrl": "https://api.deepseek.com",
            "model": "deepseek-chat",
            "apiKey": "",
            "temperature": 0.3,
            "timeoutSeconds": 20,
        },
    )
    assert saved.status_code == 200

    tested = client.post("/api/ai/test", json={"prompt": "ping"})
    assert tested.status_code == 200
    body = tested.json()
    assert body["ok"] is True
    assert body["mode"] == "mock"
