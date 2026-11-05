from unittest.mock import MagicMock

from django.test import SimpleTestCase

from infrastructure.users.models import User
from presentation.api.common.permission import IsJob


class IsJobPermissionTests(SimpleTestCase):

    def setUp(self):
        self.permission = IsJob()
        self.view = MagicMock()

    def check_permission(self, method, role=None, authenticated=True):
        request = MagicMock()
        request.method = method
        request.user.is_authenticated = authenticated
        request.user.role = role

        return self.permission.has_permission(request, self.view)
    
    def check_object_permission(self,method,is_owner = True):
        request = MagicMock()
        request.method = method
        request.user = MagicMock()
        
        
        job = MagicMock()
        
        if is_owner:
            job.company.user = request.user
        
        else:
            job.company.user = MagicMock(name="job_owner")
        
        return self.permission.has_object_permission(request,self.view,job)
        
        
    def test_allows_public_get_job(self):
        self.assertTrue(
            self.check_permission("GET", authenticated=False)
        )

    def test_allows_company_to_create_job(self):
        self.assertTrue(
            self.check_permission("POST", User.Role.COMPANY)
        )
    
    def test_denies_jobseeker_to_create_job(self):
        self.assertFalse(
            self.check_permission("POST", User.Role.JOB_SEEKER)
        )

    def test_denies_anonymous_user_to_create_job(self):
        self.assertFalse(
            self.check_permission("POST", authenticated=False)
        )
    #has_object_permission check out
    
    def test_allow_public_job_get_obj(self):
        self.assertTrue(
            self.check_object_permission("GET",is_owner=False)
        )
    def test_allows_company_to_update_own_job(self):
        self.assertTrue(
            self.check_object_permission("PATCH",is_owner=True)
        )
        
    def test_denies_company_to_update_other_job(self):
        self.assertFalse(
            self.check_object_permission('PATCH',is_owner=False)
        )
    def test_allows_company_to_delete_own_job(self):
        self.assertTrue(
            self.check_object_permission("DELETE",is_owner=True)
        
        )
        
    def test_denies_company_to_delete_other_job(self):
        self.assertFalse(
            self.check_object_permission("DELETE",is_owner=False)
        )
    
# PYTHONPATH=.. python manage.py test tests.unit.permissions.test_job_permission