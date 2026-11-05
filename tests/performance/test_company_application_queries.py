from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.applications.models import Application
from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, JobSeeker, User


class CompanyApplicationTest(APITestCase):
    COMPANY_APPLICATION_URL = "/api/v1/job/{}/applications/"
    def setUp(self):
        
        self.company_user= User.objects.create_user(
                username="company_test",
                first_name ="test",
                last_name = "profile",
                email="company@gmail.com",
                password="testpassword123",
                role = "COMPANY"
                )
        
        self.company_a = Company.objects.create(
            user= self.company_user,
            company_name ="Company A",
            description = "this is the company a descripation ",
            location = "kathmandu",
            phone ="9823342003",
            )
        for i in range(25):
            user= User.objects.create_user(
                username=f"jobseeker_{i}",
                first_name ="jobseeker_b",
                last_name = "b",
                email=f"b{i}@gmail.com",
                password="testjobseekr",
                role = "JOB_SEEKER"
                )
            
            self.jobseeker_b =JobSeeker.objects.create(
                user= user,
                full_name =f"Jobseeker {i}",
                phone_number =f"98{10000000 + i}",
                address = "pokhara",
                skills = "Bckend Developer",
                education ="BCA",
                experience = 4
                )
        
        
        self.first_job = Job.objects.create(
            company=self.company_a,
            title="Django Developer",
            description="Backend developer job",
            salary="40000.00",
            location="Kathmandu",
            is_active=True,
            )
        for i in range(25):
            Application.objects.create(
                jobseeker= self.jobseeker_b,
                job=self.first_job,
                cover_letter ="i want to apply this job"
            )
            
    def test_company_application_queries_count(self):
        self.client.force_authenticate(user=self.company_user)
        url= self.COMPANY_APPLICATION_URL.format(self.first_job.id)
        with self.assertNumQueries(3):
            response = self.client.get(url)
            
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(len(response.data["data"]),20)
                

# PYTHONPATH=.. python manage.py test tests.performance.test_company_application_queries