from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.users.models import User


class UserProfileTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            user = User.objects.create_user(
            username="testcompany",
            email="company@gmail.com",
            password="testpassword123",
            role = User.Role.COMPANY,
        )
        )
        return super().setUp()