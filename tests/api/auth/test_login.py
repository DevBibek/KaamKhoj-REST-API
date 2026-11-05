from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.users.models import User


class LoginAPITest(APITestCase):
    LOGIN_URL = "/api/v1/auth/login/"
    def setUp(self):
        User.objects.create_user(
            username = "testiuser",
            first_name ="test",
            last_name = "api",
            email="testuser@gmail.com",
            password="testpassword123",
            role= "COMPANY"
            )
        
        self.login_data = {
            "email":"testuser@gmail.com",
            "password":"testpassword123",
        }
    
    def test_user_can_login(self):
        response = self.client.post(
            self.LOGIN_URL,
            self.login_data,
            format = "json"
        )
    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        self.assertEqual(response.data["user"]["email"],"testuser@gmail.com")
        self.assertIn("Access_tokens",response.data)
        self.assertTrue(response.data["Access_tokens"])
        self.assertIn("refresh_token",response.cookies)
        self.assertTrue(response.cookies["refresh_token"].value)
        
        
        
        
    def test_login_fails_with_wrong_password(self):
        data ={
            **self.login_data,
            "password":"worongpassword",
        }
        
        response = self.client.post(
            self.LOGIN_URL,
            data,
            format= "json",
            )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_login_fails_with_invalid_emal(self):
        invalid_data = {
            **self.login_data,
            "email":"invalidemal.com"
        }
        response = self.client.post(
            self.LOGIN_URL,
            invalid_data,
            format= 'json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_and_unknown_emal(self):
        #unknown emal 
        invalid_data = {
            **self.login_data,
            "email":"unknown@gmail.com"
            }
        response = self.client.post(
            self.LOGIN_URL,
            invalid_data,
            format= 'json',
                )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_required_fields(self):
        required_fields = ["email","password"]
        for field in required_fields:
            with self.subTest(field=field):
                data = self.login_data.copy()
                data.pop(field)
                
                response = self.client.post(
                    self.LOGIN_URL,
                    data,
                    format="json"
                    )
            
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        

#PYTHONPATH=.. python manage.py test tests.api.auth.test_login
