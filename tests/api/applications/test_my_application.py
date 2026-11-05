from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.applications.models import Application
from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, JobSeeker, User


class MyApplicationTest(APITestCase):
    MY_APPLICATIONS_URL = "/api/v1/my/application/"
    APPLY_JOB_URL ="/api/v1/apply/job/"
    def setUp(self):
        
        self.jobseeker_a_user = User.objects.create_user(
            username="jobseekr_a",
            first_name ="jobseekr",
            last_name = "a_test",
            email="a@gmail.com",
            password="testjobseeker",
            role = "JOB_SEEKER"
            )
        
        self.jobseeker_b_user= User.objects.create_user(
            username="jobseeker_b",
            first_name ="jobseeker_b",
            last_name = "b",
            email="b@gmail.com",
            password="testjobseekr",
            role = "JOB_SEEKER"
            )
                
                
        self.company_user= User.objects.create_user(
                username="company_test",
                first_name ="test",
                last_name = "profile",
                email="company@gmail.com",
                password="testpassword123",
                role = "COMPANY"
                )
                
                
        self.jobseeker_a = JobSeeker.objects.create(
            user= self.jobseeker_a_user,
            full_name ="jobseeker A",
            phone_number ="9823342003",
            address = "kathmandu",
            skills = "Accountent",
            education ="BBA",
            experience = 2
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
                
        self.company_a = Company.objects.create(
            user= self.company_user,
            company_name ="Company A",
            description = "this is the company a descripation ",
            location = "kathmandu",
            phone ="9823342003",
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
            company=self.company_a,
            title="JAVA Developer",
            description="Java developer job",
            salary="80000.00",
            location="Lalitpur",
            is_active=True,
            )
        
        Application.objects.create(
            jobseeker= self.jobseeker_b,
            job=self.first_job,
            cover_letter ="i want to apply this job"
        )
        
        
    def authenticate_user(self,user):
        self.client.force_authenticate(user)
        
    def test_unauthenticated_user_cannot_retrieve_applications(self):
        response = self.client.get(self.MY_APPLICATIONS_URL)
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_job_seeker_can_retrieve_own_applications(self):
        self.authenticate_user(self.jobseeker_b_user)
        
        response = self.client.get(self.MY_APPLICATIONS_URL)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["job_title"],
            "Django Developer"
            )
        
        
        
    def test_job_seeker_cannot_see_other_users_applications(self):
        self.authenticate_user(self.jobseeker_a_user)
        first_response = self.client.post(
            self.APPLY_JOB_URL,
            {
                "job":self.second_job.id,
            "cover_letter":"i want to this job"
            },
            format='json',
            )
        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(),2)
        
        second_response = self.client.get(self.MY_APPLICATIONS_URL)
        
        self.assertEqual(
            second_response.status_code,
            status.HTTP_200_OK
            )
        job_titles = [
            application["job_title"]
            for application in second_response.data
        ]
        self.assertIn("JAVA Developer",job_titles)
        self.assertNotIn("Django Developer",job_titles)
        
    def test_company_cannot_access_my_applications(self):
        self.authenticate_user(self.company_user)
        response = self.client.get(self.MY_APPLICATIONS_URL)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    
    def test_empty_application_list_returns_200(self):
        self.authenticate_user(self.jobseeker_a_user)
        
        response = self.client.get(self.MY_APPLICATIONS_URL)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,[])

    
        


# PYTHONPATH=.. python manage.py test tests.api.applications.test_my_application
