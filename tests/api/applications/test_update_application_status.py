from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.applications.models import Application
from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, User,JobSeeker


class UpdateApplicationStatusTest(APITestCase):
    UPDATE_APPLICATION_STATUS_URL ="/api/v1/update/status/{}/"
    def setUp(self):
        
        self.company_a_user =  User.objects.create_user(
            username="company_a",
            first_name ="company",
            last_name = "a_test",
            email="a@gmail.com",
            password="testcompany",
            role = "COMPANY"
            
        )
        
        self.company_b_user = User.objects.create_user(
            username="company_b",
            first_name ="company_b",
            last_name = "b",
            email="b@gmail.com",
            password="testcompany",
            role = "COMPANY"
            )
        
        
        self.company_a = Company.objects.create(
            user= self.company_a_user,
            company_name ="Company A",
            description = "this is the company a descripation ",
            location = "kathmandu",
            phone ="9823342003",
        )
        
        
        self.company_b = Company.objects.create(
            user= self.company_b_user,
            company_name ="Company B",
            description = "ths is company b description",
            location = "Pokhara",
            phone ="9823342323",
            )
        
        
        self.first_job = Job.objects.create(
            company=self.company_a,
            title="Django Developer",
            description="Backend developer job",
            salary="40000.00",
            location="Kathmandu",
            is_active=True,
            )
        
        self.second_job = Job.objects.create(
            company=self.company_b,
            title="JAVA Developer",
            description="Java developer job",
            salary="80000.00",
            location="Lalitpur",
            is_active=True,
            )
        
        self.jobseeker_b_user= User.objects.create_user(
            username="jobseeker",
            first_name ="jobseeker_b",
            last_name = "b",
            email="jobseeker@gmail.com",
            password="testjobseekr",
            role = "JOB_SEEKER"
            )
        
        
        self.jobseeker_b =JobSeeker.objects.create(
            user= self.jobseeker_b_user,
            full_name ="Jobseeker B",
            phone_number ="9823342236",
            address = "pokhara",
            skills = "Bckend Developer",
            education ="BCA",
            experience = 4
            )
        
        self.first_application = Application.objects.create(
            jobseeker= self.jobseeker_b,
            job=self.first_job,
            cover_letter ="i want to apply this job"
        )
        
        
        self.second_application = Application.objects.create(
            jobseeker= self.jobseeker_b,
            job=self.second_job,
            cover_letter ="i want to apply this job"
        )
        
    def authenticate_user(self,user):
        self.client.force_authenticate(user=user)
        
    def test_unathenticate_company_cannot_update_application_status(self):
        url = self.UPDATE_APPLICATION_STATUS_URL.format(self.first_application.id)
        response = self.client.patch(
            url,
            {"status":"ACCEPTED"},
            format='json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_company_can_update_own_job_application_status(self):
        self.authenticate_user(self.company_a_user)
        url = self.UPDATE_APPLICATION_STATUS_URL.format(self.first_application.id)
        response = self.client.patch(
            url,
            {"status":"REVIEWING"},
            format='json',
            )
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        self.first_application.refresh_from_db()
        self.assertEqual(self.first_application.status,"REVIEWING")
        
    def test_company_cannot_update_other_job_application(self):
        self.authenticate_user(self.company_b_user)
        url = self.UPDATE_APPLICATION_STATUS_URL.format(self.first_application.id)
        response = self.client.patch(
                url,
                {"status":"REVIEWING"},
                format='json',
                )
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        self.assertEqual(self.first_application.status,"PENDING")
        
        
    def test_nonexists_application_id_returns404(self):
        self.authenticate_user(self.company_a_user)
        url = self.UPDATE_APPLICATION_STATUS_URL.format(9999)
        response = self.client.patch(
                url,
                {"status":"REVIEWING"},
                format='json'
                )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_status_fields_is_required(self):
        self.authenticate_user(self.company_a_user)
        url = self.UPDATE_APPLICATION_STATUS_URL.format(self.first_application.id)
        response = self.client.patch(
            url,
            {},
            format='json'
            )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_only_validated_status_allowed(self):
        self.authenticate_user(self.company_b_user)

        validated_status = [
        ("PENDING", "REVIEWING"),
        ("REVIEWING", "ACCEPTED"),
        ("REVIEWING", "REJECTED"),
        ]

        for current_status, new_status in validated_status:

            self.second_application.status = current_status
            self.second_application.save()

            url = self.UPDATE_APPLICATION_STATUS_URL.format(
                self.second_application.id
            )

            response = self.client.patch(
                url,
                {"status": new_status},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
            )

        
            self.second_application.refresh_from_db()

            self.assertEqual(
                self.second_application.status,
                new_status,
            )
        
    
    def test_invalid_status_rejected(self):
        self.authenticate_user(self.company_a_user)
        url = self.UPDATE_APPLICATION_STATUS_URL.format(self.first_application.id)
        
        invalid_transitions = [
            ("PENDING","ACCEPTED"),
            ("PENDING","REJECTED"),
            ("ACCEPTED","REVIEWING"),
            ("REJECTED","ACCEPTED"),
            ]
        
        for current_status , new_status in invalid_transitions:
            self.first_application.status = current_status
            self.first_application.save()
            
            response = self.client.patch(
                url,
                {"status":new_status},
                format='json'
                )
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST)
        
            self.first_application.refresh_from_db()
            self.assertEqual(
                self.first_application.status,
                current_status)
            
        
        
    def test_invalid_status_value_rejected(self):
        self.authenticate_user(self.company_a_user)

        url = self.UPDATE_APPLICATION_STATUS_URL.format(
            self.first_application.id
        )

        response = self.client.patch(
            url,
            {"status": "HIRED"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        
    
    
    def test_jobseeker_cannot_update_application_status(self):
        self.authenticate_user(self.jobseeker_b_user)
        url = self.UPDATE_APPLICATION_STATUS_URL.format(self.first_application.id)
        response = self.client.patch(
            url,
            {"status":"REVIEWING"},
            format='json',
            )
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
    
        
# PYTHONPATH=.. python manage.py test tests.api.applications.test_update_application_status