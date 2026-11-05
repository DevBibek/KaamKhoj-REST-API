from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.applications.models import Application
from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, JobSeeker, User


class CompanyJobApplicationListTest(APITestCase):
    UPDATE_APPLICATIN_STATUS_URL ="/api/v1/job/{}/applications/"
    def setUp(self):
        
        self.company_a_user =  User.objects.create(
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
        
        self.third_job = Job.objects.create(
            company=self.company_b,
            title="Frontend Developer",
            description="Frontend developer job",
            salary="40000.00",
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
        
        Application.objects.create(
            jobseeker= self.jobseeker_b,
            job=self.first_job,
            cover_letter ="i want to apply this job"
        )
        
        
        Application.objects.create(
            jobseeker= self.jobseeker_b,
            job=self.second_job,
            cover_letter ="i want to apply this job"
        )
        
    def authenticate_user(self,user):
        self.client.force_authenticate(user)
        
    def test_unauthenticate_company_cannot_retrieve_own_job_applications(self):
        self.authenticate_user(user=None)
        url = self.UPDATE_APPLICATIN_STATUS_URL.format(self.first_job.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
    def test_company_can_retrieve_applications_for_own_job(self):
        self.authenticate_user(self.company_a_user)
        
        url = self.UPDATE_APPLICATIN_STATUS_URL.format(self.first_job.id)
        response = self.client.get(url)
        
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        job_titels = []
        for application in response.data["data"]:
            job_titels.append(application["job_title"])
        
        self.assertEqual(
            job_titels,
            ["Django Developer"]
        )
    
    def test_company_cannot_retrieve_other_company_job_applications(self):
        self.authenticate_user(self.company_b_user)
        url = self.UPDATE_APPLICATIN_STATUS_URL.format(self.first_job.id)
        
        response = self.client.get(url)
        
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_company_receives_empty_list_when_job_has_no_applications(self):
        self.authenticate_user(self.company_b_user)
        url = self.UPDATE_APPLICATIN_STATUS_URL.format(self.third_job.id)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["data"], [])
        self.assertEqual(response.data["pagination"]["total_items"],0)
        
    def test_nonexistent_job_returns_404(self):
        self.authenticate_user(self.company_a_user)
        url = self.UPDATE_APPLICATIN_STATUS_URL.format(9999)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
            
        
    def test_job_seeker_cannot_access_company_applications(self):
        self.authenticate_user(self.jobseeker_b_user)
        url = self.UPDATE_APPLICATIN_STATUS_URL.format(self.first_job.id)
        
        
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
    
# PYTHONPATH=.. python manage.py test tests.api.applications.test_company_job_application_list
