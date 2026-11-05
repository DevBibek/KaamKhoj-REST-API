from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt import token_blacklist

from infrastructure.users.models import User


class AuthLogoutTest(APITestCase):
    LOGIN_URL = "/api/v1/auth/login/"
    REFRESH_TOKEN_URL = "/api/v1/refresh/token/"
    LOGOUT_URL = "/api/v1/auth/logout/"
    
    def setUp(self):
        self.user = User.objects.create_user(
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
        
    def test_user_can_logout(self):
        login_response = self.client.post(
            self.LOGIN_URL,
            self.login_data,
            format="json",
        )
        
        self.assertEqual(login_response.status_code ,status.HTTP_200_OK)
        
        refresh_token = login_response.cookies["refresh_token"].value
        
        #logout user
        logout_response = self.client.post(
            self.LOGOUT_URL,{
                "refresh_token":refresh_token
            },
            format="json",
        )
        
        self.assertEqual(logout_response.status_code,status.HTTP_200_OK)
        self.assertIn("refresh_token", logout_response.cookies)
        self.assertEqual(
            logout_response.cookies["refresh_token"]["max-age"],
            0,
        )
        
        
        # old refresh token must not work after logout
        response= self.client.post(
            self.REFRESH_TOKEN_URL,
            {"refresh_token":refresh_token},
            format = "json",
        )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
        
        
    def test_logout_requires_refresh_token(self):
        response = self.client.post(
            self.LOGOUT_URL,
            {},
            format="json",
            )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    
    def test_logout_reject_invalid_refresh_tokens(self):
        refresh_token = "invalind_refresh_token"
        response = self.client.post(
            self.LOGOUT_URL,
            {"refresh_token":refresh_token},
            format="json",
            )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
#PYTHONPATH=.. python manage.py test tests.api.auth.test_logout