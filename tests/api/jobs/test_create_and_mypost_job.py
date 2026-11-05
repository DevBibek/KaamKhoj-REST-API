from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, User


class CreateJobsAPITest(APITestCase):
    CREATE_JOB_URL = "/api/v1/create/job/"
    MY_JOBS_URL = "/api/v1/company/my/posts/"
    def setUp(self):
        
        self.user= User.objects.create_user(
            username ="testingapi",
            email="testing@gmail.com",
            password="testpassword123",
            role = User.Role.COMPANY
        )
        
        self.company = Company.objects.create(
            user=self.user,
            company_name = "Test API Company",
            phone = "9823728123",
            location = "nepal",
            verification_status = Company.VerificationStatus.VERIFIED
            
        )
        
    
        self.job = Job.objects.create(
        company=self.company,
        title="Django Developer",
        description="Backend developer job",
        salary="40000.00",
        location="Kathmandu",
        is_active=True,
    )
    

        self.job_data= {
            "title": "Django Developer",
            "description": "Backend developer job",
            "salary": "40000.00",
            "location": "Kathmandu",
            }
        
    def test_company_can_create_job(self):
        self.client.force_authenticate(user=self.user)
        
        new_job_data = {
            **self.job_data,
            "title": "Frontend Developer",
            "salary": "80000.00",
            }
        response = self.client.post(
            self.CREATE_JOB_URL,
            new_job_data,
            format= "json",
            )
        
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(),2)
        new_job = Job.objects.get(title="Frontend Developer")
        self.assertEqual(new_job.company ,self.company)
        
        
    def test_user_who_are_not_allowed_create_job(self):
        seeker = User.objects.create_user(
            username="seeker",
            email="seeker@gmail.com",
            password="testpassword213",
            role = User.Role.JOB_SEEKER
        )
        self.client.force_authenticate(user=seeker)
        
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format="json",
        )
        
        
        self.assertEqual(response.status_code ,status.HTTP_403_FORBIDDEN)
        
        
        #unverify company
        
        self.company.verification_status = Company.VerificationStatus.PENDING
        self.company.save(update_fields=["verification_status"])
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format="json",
        )
        
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
        # Company user without company profile,
    def test_company_profile_is_require_for_create_job(self):
        nonprofile = User.objects.create_user(
            username="nonprofile",
            email="nonprofile32@gmai.com",
            password="testpassword123",
            role = User.Role.COMPANY
            )
        
        self.client.force_authenticate(user=nonprofile)
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format="json",
            )
        
        self.assertEqual( response.status_code ,status.HTTP_403_FORBIDDEN)
        
        #Unathenticated user 
        
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format = 'json',
        )
        
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Job.objects.count(),1)
        
        
    
    def test_company_can_retrive_only_own_job(self):
        another_user = User.objects.create_user(
            username= "testuser",
            email="testjob@gmail.com",
            password="testpassword123",
            role = User.Role.COMPANY
        )
        
        anoother_company = Company.objects.create(
            user=another_user,
            company_name = "Test Company",
            phone = "9282819203",
            location = "KTM",
            verification_status = Company.VerificationStatus.VERIFIED
        )
        another_job = Job.objects.create(
                company=anoother_company,
                title="Other Company Developer",
                description="A different company's job",
                salary="50000.00",
                location="Pokhara",
                is_active=True,)
                
        #authenticate first company user
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(
            self.MY_JOBS_URL)
    
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        jobs = response.data["data"]
        
        
        
        returned_job_ids = [job["id"] for job in jobs]
        
        self.assertIn(self.job.id, returned_job_ids)
        self.assertNotIn(another_job.id,returned_job_ids)
        
        
    def test_job_seeker_cannot_create_job(self):
        # Authenticated Job Seeker
        seeker = User.objects.create_user(
            username="testseeker",
            email="seeker@gmail.com",
            password="testpassword123",
            role=User.Role.JOB_SEEKER,
        )
    
        self.client.force_authenticate(user=seeker)
        response = self.client.get(
            self.MY_JOBS_URL)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
        
        self.client.force_authenticate(user=None)
        response = self.client.get(
            self.MY_JOBS_URL)
        
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
        
        
#  PYTHONPATH=.. python manage.py test tests.api.jobs.test_create_and_mypost_job