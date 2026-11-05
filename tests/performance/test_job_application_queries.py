from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.applications.models import Application
from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, JobSeeker, User


class JobApplicationTest(APITestCase):
    JOB_SEEKER_APPLICATION_URL ="/api/v1/my/application/"
    def setUp(self):
        
        self.jobseeker_user = User.objects.create_user(
            username="jobseekr_a",
            first_name ="jobseekr",
            last_name = "a_test",
            email="a@gmail.com",
            password="testjobseeker",
            role = "JOB_SEEKER"
        )
        
        self.jobseeker = JobSeeker.objects.create(
            user= self.jobseeker_user,
            full_name ="jobseeker A",
            phone_number ="9823342003",
            address = "kathmandu",
            skills = "Accountent",
            education ="BBA",
            experience = 2
        )
        
        company_user= User.objects.create_user(
                username="company_test",
                first_name ="test",
                last_name = "profile",
                email="company@gmail.com",
                password="testpassword123",
                role = "COMPANY"
                )
        
        self.company = Company.objects.create(
            user= company_user,
            company_name ="Company A",
            description = "this is the company a descripation ",
            location = "kathmandu",
            phone ="9823342003",
            )
        for i in range(10):
            job = Job.objects.create(
                company=self.company,
                title=f"Django Developer{i}",
                description="Backend developer job",
                salary="40000.00",
                location="Kathmandu",
                is_active=True,
                )

            Application.objects.create(
                    jobseeker= self.jobseeker,
                    job=job,
                    cover_letter ="i want to apply this job"
                )
            
    def test_jobseeker_application_queries_count(self):
        self.client.force_authenticate(user=self.jobseeker_user)
        with self.assertNumQueries(1):
            response = self.client.get(self.JOB_SEEKER_APPLICATION_URL)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),10)
        
# PYTHONPATH=.. python manage.py test tests.performance.test_job_application_queries