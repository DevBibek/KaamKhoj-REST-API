from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, User


class ManageJobAPITest(APITestCase):
    MY_POST_JOB_URL="/api/v1/company/my/posts/"
    
    def setUp(self):
        self.jobseeker = User.objects.create_user(
            username="seeker",
            email="seeker@gmail.com",
            password="testpassword213",
            role = User.Role.JOB_SEEKER
        )
        self.nonprofile = User.objects.create_user(
            username="nonprofile",
            email="nonprofile32@gmai.com",
            password="testpassword123",
            role = User.Role.COMPANY
            )
        
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
            role = "COMPANY",
            
            )
        
        
        self.company_a = Company.objects.create(
            user= self.company_a_user,
            company_name ="Company A",
            description = "this is the company a descripation ",
            location = "kathmandu",
            phone ="9823342003",
            verification_status = Company.VerificationStatus.VERIFIED
        )
    
        
        self.company_b = Company.objects.create(
            user= self.company_b_user,
            company_name ="Company B",
            description = "ths is company b description",
            location = "Pokhara",
            phone ="9823342323",
            verification_status = Company.VerificationStatus.VERIFIED,
            
            )
        
        
        self.first_job = Job.objects.create(
            company=self.company_a,
            title="Django Developer",
            description="Backend developer job",
            salary="40000.00",
            location="Kathmandu",
            is_active=True,
            )
        for i in range(5):
            self.second_job = Job.objects.create(
                company=self.company_b,
                title=f"Developer{i}",
                description="Java developer job",
                salary="80000.00",
                location="Lalitpur",
                is_active=True,
                )
            
            
    def authenticate_user(self,user):
        self.client.force_authenticate(user=user)
        
    def test_unauthenticate_user_cannot_retrieve_job(self):
        self.authenticate_user(user=None)
        response = self.client.get(self.MY_POST_JOB_URL)
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
    def test_company_can_retrive_own_job(self):
        self.authenticate_user(user=self.company_b_user)
        
        response = self.client.get(self.MY_POST_JOB_URL)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["data"][4]["title"],"Developer0")
        self.assertNotEqual(response.data["data"][4]["title"],"Django Developer")
        
        
    def test_company_emty_jobs_returens_200(self):
        self.authenticate_user(user=self.company_b_user)
        
        Job.objects.filter(company = self.company_b).delete()
        
        response = self.client.get(self.MY_POST_JOB_URL)
    
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["data"],[])
        
    
    def test_jobseeker_cannot_retrieve_job(self):
        self.authenticate_user(user=self.jobseeker)
        
        response = self.client.get(self.MY_POST_JOB_URL)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
# PYTHONPATH=.. python manage.py test tests.api.jobs.test_my_post_job