from unittest.mock import MagicMock

from django.test import SimpleTestCase

from infrastructure.users.models import User
from presentation.api.common.permission import IsJobSeeker


class IsJobSeekerTests(SimpleTestCase):
    def setUp(self):
        self.permission = IsJobSeeker()
        self.view = MagicMock()
        
    def check_permission(self,role=None,authenticated=True):
        request = MagicMock()
        request.user.is_authenticated = authenticated
        request.user.role = role
        return self.permission.has_permission(request,self.view)
    
    
    def test_allow_jobseeker(self):
        self.assertTrue(
            self.check_permission(role = User.Role.JOB_SEEKER)
        )
        
    def test_denies_company(self):
        self.assertFalse(
            self.check_permission(role=User.Role.COMPANY)
        )
        
    
    def test_denies_anonymous_user(self):
        self.assertFalse(
            self.check_permission(authenticated=False)
        )
        
    def test_allows_owner(self):
        request = MagicMock()
        request.user = MagicMock()
        jobseeker = MagicMock()
        jobseeker.user = request.user
        
        self.assertTrue(
            self.permission.has_object_permission(request,self.view,jobseeker)
        )
        
        
    def test_deines_non_owner(self):
        request = MagicMock()
        request.user = MagicMock()
        jobseeker = MagicMock
        jobseeker.user = MagicMock()
        
        self.assertFalse(
            self.permission.has_object_permission(request,self.view,jobseeker)
        )
        

# PYTHONPATH=.. python manage.py test tests.unit.permissions.test_jobseeker_permission