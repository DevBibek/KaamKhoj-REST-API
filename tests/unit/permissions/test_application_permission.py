from unittest.mock import MagicMock

from django.test import SimpleTestCase

from infrastructure.users.models import User
from presentation.api.common.permission import IsApplication


class IsApplicationPermissionTest(SimpleTestCase):
    def setUp(self):
        self.permission = IsApplication()
        self.view = MagicMock()
        
        
    def check_has_permission(self,authenticated = True):
        request = MagicMock()
        request.user.is_authenticated = authenticated
        
        return self.permission.has_permission(request,self.view)
        
    def check_has_object_permission(self, role=None, is_owner=True):
        request = MagicMock()
        request.user.id = 10

        application = MagicMock()

        if role == User.Role.JOB_SEEKER:
            if is_owner:
                application.jobseeker.user_id = request.user.id
            else:
                application.jobseeker.user_id = 20

        if role == User.Role.COMPANY:
                if is_owner:
                    application.job.company.user_id = request.user.id
                else:
                    application.job.company.user_id = 20

        return self.permission.has_object_permission(
                request, self.view, application
            )
    
    def test_anonymous_user_cannot_access(self):
        self.assertFalse(
            self.check_has_permission(authenticated=False)
        )
        
    def test_jobseeker_can_access_owen_application(self):
        self.assertTrue(
            self.check_has_object_permission(User.Role.JOB_SEEKER,is_owner=True)
        )
        
    
    def test_jobseeker_cannot_access_other_application(self):
        self.assertFalse(
            self.check_has_object_permission(User.Role.JOB_SEEKER,is_owner=False)
        )
    
    
    def test_company_can_access_owen_application(self):
        self.assertTrue(
            self.check_has_object_permission(User.Role.COMPANY,is_owner=True)
        )
        
    
    def test_company_cannot_access_other_application(self):
        self.assertFalse(
            self.check_has_object_permission(User.Role.COMPANY,is_owner=False)
        )
    
    

    
# PYTHONPATH=.. python manage.py test tests.unit.permissions.test_application_permission