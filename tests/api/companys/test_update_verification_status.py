from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.users.models import Company, JobSeeker, User


class UpdateVerificationStatusTest(APITestCase):
    UPDATE_COMPANY_VERIFICATION_URL ="/api/v1/admin/companies/{}/verification/"
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="adminpassword",
        )
        
        self.company_user = User.objects.create_user(
            username="companyuser",
            email="company@gmail.com",
            password="companypassword",
            role="COMPANY",
        )
        
        self.jobseeker_user =User.objects.create_user(
            username="jobseekeruser",
            email="jobseekr@gmail.com",
            password="jobseekerpassword",
            role = "JOB_SEEKER",
        )
        
        
        self.company_a_user = User.objects.create_user(
            username="company_a",
            first_name ="company",
            last_name = "a_test",
            email="a@gmail.com",
            password="testcompany",
            role = "COMPANY"
        )
        
        self.company_a = Company.objects.create(
            user= self.company_a_user,
            company_name ="Company A",
            description = "This is the company a descripation ",
            location = "kathmandu",
            phone ="9823342003",
        )
    
    def authenticate_user(self,user):
        self.client.force_authenticate(user=user)
        
        
    def test_unauthenticated_user_cannot_update_verification(self):
        url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
        response = self.client.patch(
            url,
            {
                "verification_status":"VERIFIED"
            },
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
            
    def test_admin_can_update_verification_status(self):
        self.authenticate_user(user=self.admin_user)
        
        url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
        
        response = self.client.patch(
            url,
            {"verification_status":"VERIFIED"},
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(
            response.data["company_verification_status"],
            "VERIFIED",
            )
        self.company_a.refresh_from_db()
        self.assertEqual(self.company_a.verification_status,"VERIFIED")
        
        
    def test_admin_can_set_valid_status_transitions(self):
        self.authenticate_user(user=self.admin_user)
        validated_status = [
            ("PENDING","VERIFIED"),
            ("PENDING","REJECTED"),
        ]
        for current_status,new_status in validated_status:
            self.company_a.verification_status = current_status
            self.company_a.save()
            url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
            
            response = self.client.patch(
                url,
                {"verification_status":new_status},
                format="json",
                )
            
            self.company_a.refresh_from_db()
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(self.company_a.verification_status,new_status)

    def test_invalid_status_transitions_are_rejected(self):
        self.authenticate_user(user=self.admin_user)
        
        invalid_status = [
            ("VERIFIED","PENDING"),
            ("REJECTED","PENDING"),
            ("VERIFIED","REJECTED"),
            ("VERIFIED","VERIFIED")
        ]
        
        for curent_status,new_status in invalid_status:
            self.company_a.verification_status = curent_status
            self.company_a.save()
            url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
            
            response = self.client.patch(
                url,
                {
                "verification_status":new_status
                },
                format="json",
            )
            
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.company_a.refresh_from_db()
            self.assertEqual(self.company_a.verification_status,curent_status)

    def test_invalid_verification_status_value_is_rejected(self):
        self.authenticate_user(user=self.admin_user)
        url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
        response = self.client.patch(
                url,
                {
                "verification_status":"invalid status"
                },
                format="json",
            )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        
    def test_nonexistent_company_returns_404(self):
        self.authenticate_user(user=self.admin_user)
        url = self.UPDATE_COMPANY_VERIFICATION_URL.format(9999)
            
        response = self.client.patch(
                url,
                {
                "verification_status":"VERIFIED"
                },
                format="json",
            )

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        

    def test_verification_status_is_required(self):
        self.authenticate_user(user=self.admin_user)
        
        url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
        
        response = self.client.patch(
            url,
            { },
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        

    def test_company_user_cannot_update_status(self):
        self.authenticate_user(user=self.company_user)
        url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
        
        response = self.client.patch(
                url,
                {
                "verification_status":"VERIFIED"
                },
                format="json",
            )
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
    def test_jobseeker_cannot_update_verification_status(self):
        self.authenticate_user(user=self.jobseeker_user)
        url = self.UPDATE_COMPANY_VERIFICATION_URL.format(self.company_a.id)
        
        response = self.client.patch(
                url,
                {
                "verification_status":"VERIFIED"
                },
                format="json",
            )
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
# PYTHONPATH=.. python manage.py test tests.api.companys.test_update_verification_status
