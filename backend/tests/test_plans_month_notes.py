def test_plan_crud(client):
    created = client.post(
        "/api/plans",
        json={
            "date": "2026-06-30",
            "time": "09:00",
            "content": "Build SQLite plan API",
            "priority": "high",
            "estimatedMinutes": 90,
        },
    )
    assert created.status_code == 200
    plan = created.json()
    assert plan["content"] == "Build SQLite plan API"
    assert plan["done"] is False
    assert plan["priority"] == "high"

    listed = client.get("/api/plans", params={"date": "2026-06-30"})
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [plan["id"]]

    updated = client.patch(
        f"/api/plans/{plan['id']}",
        json={"done": True, "completion": "CRUD verified"},
    )
    assert updated.status_code == 200
    assert updated.json()["done"] is True
    assert updated.json()["result"] == "CRUD verified"

    deleted = client.delete(f"/api/plans/{plan['id']}")
    assert deleted.status_code == 204
    assert client.get("/api/plans", params={"date": "2026-06-30"}).json() == []


def test_month_note_upsert(client):
    empty = client.get("/api/month-notes", params={"year": 2026, "month": 6})
    assert empty.status_code == 200
    assert empty.json()["content"] == ""

    saved = client.put(
        "/api/month-notes",
        json={"year": 2026, "month": 6, "content": "June focus: backend data layer"},
    )
    assert saved.status_code == 200
    assert saved.json()["content"] == "June focus: backend data layer"

    loaded = client.get("/api/month-notes", params={"year": 2026, "month": 6})
    assert loaded.json()["content"] == "June focus: backend data layer"
