from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, User


class ManageJobAPITest(APITestCase):
    CREATE_JOB_URL = "/api/v1/create/jobs/"
    JOB_DETAIL_URL ="/api/v1/create/jobs/{}/"
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
        
        self.second_job = Job.objects.create(
            company=self.company_b,
            title="JAVA Developer",
            description="Java developer job",
            salary="80000.00",
            location="Lalitpur",
            is_active=True,
            )

        self.job_data= {
            "title": "Django Developer",
            "description": "Backend developer job",
            "salary": "40000.00",
            "location": "Kathmandu",
            }
        
    def authenticate_user(self,user):
        self.client.force_authenticate(user=user)
        
    def test_unthenticate_company_cannot_create_job(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format = 'json',
        )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Job.objects.count(),2)
        
        
        
    def test_company_can_create_job(self):
        self.client.force_authenticate(user=self.company_a_user)
        
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
        self.assertEqual(Job.objects.count(),3)
        
        
        
    def test_jobseeker_cannot_create_job(self):
        
        self.client.force_authenticate(user=self.jobseeker)
        
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format="json",
        )
        
        self.assertEqual(response.status_code ,status.HTTP_403_FORBIDDEN)
        self.assertEqual(Job.objects.count(),2)
        
        
        
        #unverify company
    def test_unverify_company_cannot_create_job(self):
        self.company_a.verification_status = Company.VerificationStatus.PENDING
        self.company_a.save(update_fields=["verification_status"])
        self.client.force_authenticate(user=self.company_a_user)
        
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertEqual(Job.objects.count(),2)
    
    
    def test_company_profile_is_require_for_create_job(self):
        
        self.client.force_authenticate(user=self.nonprofile)
        response = self.client.post(
            self.CREATE_JOB_URL,
            self.job_data,
            format="json",
            )
        
        self.assertEqual( response.status_code ,status.HTTP_400_BAD_REQUEST)
        
    
    
    def test_company_can_retrive_only_own_job(self):
    
        self.client.force_authenticate(user=self.company_a_user)
        
        response = self.client.get(
            self.CREATE_JOB_URL
            )
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
    def test_company_can_get_job_by_id(self):
        self.authenticate_user(self.company_a_user)
        url =self.JOB_DETAIL_URL.format(self.first_job.id)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"],"Django Developer")
        self.assertEqual(response.data["data"]["company"],"Company A")
        
    
    def test_company_can_update_own_job(self):
        self.authenticate_user(self.company_b_user)
        url = self.JOB_DETAIL_URL.format(self.second_job.id)
        response = self.client.put(
            url,
            {
            "title":"Social media mrketing",
            "salary":20000
            },
            format= 'json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"],"Social media mrketing")
        
    def test_company_cannot_update_other_job(self):
        self.authenticate_user(user=self.company_a_user)
        
        url = self.JOB_DETAIL_URL.format(self.second_job.id)
        response = self.client.put(
            url,
            {
            "title":"Social media mrketing",
            "salary":20000
            },
            format= 'json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.second_job.refresh_from_db()
        self.assertEqual(self.second_job.title,"JAVA Developer")
        
        
        
        
        
    def test_company_can_delete_own_job(self):
        self.authenticate_user(user=self.company_a_user)
        url = self.JOB_DETAIL_URL.format(self.first_job.id)
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Job.objects.filter(id=self.first_job.id).exists())
    
    
    def test_company_cannot_delete_other_job(self):
        self.authenticate_user(user=self.company_b_user)
        url = self.JOB_DETAIL_URL.format(self.first_job.id)
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertTrue(Job.objects.filter(id=self.first_job.id).exists())
    
    
    def test_job_seeker_cannot_retrieve_job(self):
        self.client.force_authenticate(user=self.jobseeker)
        response = self.client.get(
            self.CREATE_JOB_URL
            )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
            
    def test_job_seeker_cannot_delete_job(self):
        self.client.force_authenticate(user=self.jobseeker)
        url = self.JOB_DETAIL_URL.format(self.first_job.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertTrue(Job.objects.filter(id=self.first_job.id).exists())
    
        
    def test_invalid_job_id_rejected(self):
        self.client.force_authenticate(user=self.company_a_user)
        url = self.JOB_DETAIL_URL.format(99999)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
        
#  PYTHONPATH=.. python manage.py test tests.api.jobs.test_manage_job
