def test_create_and_get_slots(test_client):
   # Login as admin
   login = test_client.post("/auth/login", data={"email": "admin@test.com", "password": "admin123"})
   token = login.json()["access_token"]
   headers = {"Authorization": f"Bearer {token}"}
   # Create slot
   slot_data = {
       "location": "B1",
       "slot_number": "P01",
       "floor": 1
   }
   res = test_client.post("/slots/create", json=slot_data, headers=headers)
   assert res.status_code == 200
   assert res.json()["slot_number"] == "P01"
   # Get slots
   res = test_client.get("/slots", headers=headers)
   assert res.status_code == 200
   assert isinstance(res.json(), list)