from unittest.mock import MagicMock

from django.test import SimpleTestCase

from infrastructure.users.models import User
from presentation.api.common.permission import IsCompany


class IsCompanyPermissionTests(SimpleTestCase):
    def setUp(self):
        self.permission = IsCompany()
        self.view = MagicMock()
        
        
        
    def check_permission(self,role=None,authenticated=True):
        request = MagicMock()
        request.user.is_authenticated = authenticated
        request.user.role = role
        
        return self.permission.has_permission(request,self.view)
        

    def test_allows_company(self):
        self.assertTrue(
            self.check_permission(User.Role.COMPANY)
            )


    def test_denies_jobseeker(self):
        self.assertFalse(
            self.check_permission(User.Role.JOB_SEEKER)
        )

    def test_denies_anonymous_user(self):
        self.assertFalse(
            self.check_permission(authenticated=False)
        )



    def test_allow_owner(self):
        request = MagicMock()
        request.user = MagicMock()
        
        company = MagicMock()
        company.user = request.user
        
        self.assertTrue(self.check_permission.has_object_permission(
            request,self.view,company
        ))
        
    def test_denies_non_owner(self):
        
        
        request = MagicMock()
        
        request.user = MagicMock()
        
        company = MagicMock()
        company.user = MagicMock()
        
        self.assertFalse(
            self.check_permission.has_object_permission(
                request,self.view,company
            )
        )

# PYTHONPATH=.. python manage.py test tests.unit.permissions.test_company_permission