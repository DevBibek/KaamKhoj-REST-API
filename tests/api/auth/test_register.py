from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.users.models import User


class RegisterAPITest(APITestCase):
    REGISTER_URL = "/api/v1/auth/register/"
    def setUp(self):
        User.objects.create_user(
            username = "testiuser",
            first_name ="test",
            last_name = "api",
            email="testuser@gmail.com",
            password="testpassword123",
            role= "COMPANY"
        )
        
        self.user_data = {  
            "username": "testing12",
            "first_name":"test",
            "last_name":"api",
            "email":"test@gmail.com",
            "password":"testing123",
            "role": "JOB_SEEKER",
        }
    
    
    
    def test_user_can_register_and_dublicte_emal_and_username_rejected(self):
        response = self.client.post(
            self.REGISTER_URL,
            self.user_data,
            format = "json"
        )

        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        
        #dublicte data chcek
        dublicate_data = {
            **self.user_data,
            "username": "testing12",
            "email":"test@gmail.com",
        }
        response = self.client.post(
            self.REGISTER_URL,
            dublicate_data,
            format="json",
            )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),2)
        
        
    def test_fields_are_required_and_invalid_email_not_exacpte(self):
        
        required_fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
        ]
        for field in required_fields:
            with self.subTest(field=field):
                data = self.user_data.copy()
                data.pop(field)
                
                response = self.client.post(
                    self.REGISTER_URL,
                    data,
                    format="json",
                )
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
        
        #Invalic emal check 
        invalid_data = {
            **self.user_data,
            "email":"Testingexample.com"
        }
        respone = self.client.post(
            self.REGISTER_URL,
            invalid_data,
            format="json"
        )
        self.assertEqual(respone.status_code ,status.HTTP_400_BAD_REQUEST)
        
        self.assertEqual(User.objects.count(),1)
        
        
        
#PYTHONPATH=.. python manage.py test tests.api.auth.test_register