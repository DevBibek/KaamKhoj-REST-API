from datetime import timedelta

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.users.models import User


class RefreshTokenTest(APITestCase):
    REFRESH_TOKEN_URL = "/api/v1/refresh/token/"
    LOGIN_URL = "/api/v1/auth/login/"
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
        
        
    def test_refresh_token(self):
        response = self.client.post(
            self.LOGIN_URL,
            self.login_data,
            format="json",
            )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        refresh_token = response.cookies["refresh_token"].value
        
        
        
        response = self.client.post(
            self.REFRESH_TOKEN_URL,
            {"refresh_token":refresh_token},
            format="json")
        
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn("access",response.data["Tokens"])
        self.assertTrue(response.data["Tokens"]["access"])
        
        
    def test_refresh_token_required(self):
        refreshs_token = {}
        
        response = self.client.post(
            self.REFRESH_TOKEN_URL,
            {"refresh_token":refreshs_token},
            format="json")
        
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
        
        
    def test_invalid_refresh_token(self):
        invalid_token = "this_is_an_invalid_token"
        response  = self.client.post(
            self.REFRESH_TOKEN_URL,{
                "refresh_token":invalid_token,
                },
            format="json",
            )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        

    def test_expired_refresh_token(self):
        token = RefreshToken.for_user(user=self.user)
        token.set_exp(lifetime=timedelta(seconds=1))
        
        
        response = self.client.post(
            self.REFRESH_TOKEN_URL,
            {"refresh_token":str(token)},
            format="json",
            )
                
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
                
#PYTHONPATH=.. python manage.py test tests.api.auth.test_refresh_token