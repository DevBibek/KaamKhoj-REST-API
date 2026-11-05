from unittest.mock import MagicMock

from django.test import SimpleTestCase

from domain.users.update_verification_rules import UpdateVerificationRules


class UpdateVerificationRulesTests(SimpleTestCase):
    def setUp(self):
        self.admin = MagicMock()
        self.admin.is_staff = True
        
    def make_company(self,current_status):
        company = MagicMock()
        company.verification_status = current_status
        return company
        
        
    def test_allows_valid_verification_transitions(self):
        valid_transitions =[
            ("PENDING","VERIFIED"),
            ("PENDING","REJECTED"),
            ]
        
        for current_status,new_status in valid_transitions:
            with self.subTest(
                current_status=current_status,
                new_status=new_status
                ):
                company = self.create_company(current_status=current_status)
                result = UpdateVerificationRules.validate(
                    user=self.admin,
                    company=company,
                    new_status=new_status
                )
                
                self.assertIsNone(result)
            
            
    def test_rejects_invalid_status_transitions(self):
        invalid_transitions = [
            ("VERIFIED","PENDING"),
            ("REJECTED","PENDING"),
            ("VERIFIED","REJECTED")
        ]
        for current_status,new_status in invalid_transitions:
            with self.subTest(
                current_status=current_status,
                new_status=new_status 
                ):
                company = self.create_company(current_status=current_status)
                with self.assertRaises(ValueError):
                    UpdateVerificationRules.validate(
                    user=self.admin,
                    company=company,
                    new_status=new_status,
                )
                
    
    def test_non_staff_user_cannot_update_status(self):
        user = MagicMock()
        user.is_staff = False
        
        company = self.create_company("PENDING")
        with self.assertRaises(PermissionError):
            UpdateVerificationRules.validate(
                user=user,
                company=company,
                new_status= "VERIFIED",
            )
                
            
# PYTHONPATH=.. python manage.py test tests.unit.companys.test_update_company_verification_rules