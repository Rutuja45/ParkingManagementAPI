def test_booking_flow(test_client):
    # Login

    login = test_client.post("/auth/login", data={"email": "admin@test.com", "password": "admin123"})

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Get slot ID

    slot_id = test_client.get("/slots", headers=headers).json()[0]["id"]

    # Book the slot

    booking = {

        "slot_id": slot_id,

        "start_time": "2025-05-01T10:00:00",

        "end_time": "2025-05-01T11:00:00"

    }

    res = test_client.post("/book", json=booking, headers=headers)

    assert res.status_code == 200

    assert res.json()["slot_id"] == slot_id

    # View bookings

    res = test_client.get("/bookings", headers=headers)

    assert res.status_code == 200

    assert isinstance(res.json(), list)
