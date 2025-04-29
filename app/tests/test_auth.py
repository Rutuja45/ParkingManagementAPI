def test_signup_and_login(test_client):
   signup_data = {
       "name": "Test Admin",
       "email": "admin@test.com",
       "password": "admin123",
       "is_admin": True
   }
   response = test_client.post("/auth/signup", json=signup_data)
   assert response.status_code == 200
   login_data = {
       "email": "admin@test.com",
       "password": "admin123"
   }
   response = test_client.post("/auth/login", data=login_data)
   assert response.status_code == 200
   assert "access_token" in response.json()