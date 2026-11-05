from unittest.mock import MagicMock

from django.test import SimpleTestCase

from domain.applications.update_application_rules import UpdateApplicationRules
from infrastructure.users.models import User


class UpdateApplicationRulesTests(SimpleTestCase):
    def setUp(self):
        self.user = MagicMock()
        self.user.role = User.Role.COMPANY
        self.user.Role = User.Role

    def create_application(self, current_status):
        application = MagicMock()
        application.status = current_status
        application.job.company.user = self.user
        return application
    
    
    def test_validate_status_allowe(self):  
        
        validated_status = [
            
            ("PENDING", "REVIEWING"),
            ("REVIEWING", "ACCEPTED"),
            ("REVIEWING", "REJECTED"),
            ]
        
        for current_status ,new_status in validated_status:
            with self.subTest(
                current_status=current_status,
                new_status=new_status
                ):
                application = self.create_application(current_status=current_status)
                result = UpdateApplicationRules.validate(
                        user=self.user,
                        company_user=self.user,
                        application=application,
                        new_status=new_status
                    )
                    
                self.assertIsNone(result)
        
        
    def test_invalid_status_rejected(self):
        invalid_transitions = [
            ("PENDING","ACCEPTED"),
            ("PENDING","REJECTED"),
            ("ACCEPTED","REVIEWING"),
            ("REJECTED","ACCEPTED"),
            ]
        for current_status ,new_status in invalid_transitions:
            
            application = self.create_application(current_status=current_status)
            with self.assertRaises(ValueError):
                UpdateApplicationRules.validate(
                    user=self.user,
                    company_user=self.user,
                    application=application,
                    new_status=new_status,
                )
        
            
            
            
    # PYTHONPATH=.. python manage.py test tests.unit.applications.test_update_application_rules
