from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.applications.models import Application
from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, JobSeeker, User


class ApplyJobTest(APITestCase):
    APPLY_JOB_URL = "/api/v1/apply/job/"
    
    def setUp(self):
        
        self.new_jobseeker_user= User.objects.create_user(
            username="jobsekerq",
            first_name ="jobseeker",
            last_name = "profile",
            email="testprofile@gmail.com",
            password="testpassword123",
            role = "JOB_SEEKER"
            )

        self.jobseeker_a_user = User.objects.create_user(
            username="jobseekr_a",
            first_name ="jobseekr",
            last_name = "a_test",
            email="a@gmail.com",
            password="testjobseeker",
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
        
        self.company_a = Company.objects.create(
                    user= self.company_user,
                    company_name ="Company A",
                    description = "this is the company a descripation ",
                    location = "kathmandu",
                    phone ="9823342003",
                )
        
        
        self.active_job = Job.objects.create(
                company=self.company_a,
                title="Django Developer",
                description="Backend developer job",
                salary="40000.00",
                location="Kathmandu",
                is_active=True,
            )
        
        
        self.inactive_job = Job.objects.create(
                company=self.company_a,
                title="Django Developer",
                description="Backend developer job",
                salary="40000.00",
                location="Kathmandu",
                is_active=False,
            )
        
        
        
        self.application_data ={
            "job": self.active_job.id,
            "cover_letter":"i am interst in this postiorn"
        }
        
    def authenticate_user(self,user):
        self.client.force_authenticate(user)
        
    def test_unauthenticated_user_cannot_apply(self):
        response = self.client.post(
            self.APPLY_JOB_URL,
            self.application_data,
            format='json',
            )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Application.objects.count(),0)
        
        
    def test_jobseeker_can_apply_to_active_job(self):
        self.authenticate_user(self.jobseeker_a_user)
        response = self.client.post(
        self.APPLY_JOB_URL,
            self.application_data,
            format='json',
        )

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(),1)
    
    def test_inactive_job_cannot_apply(self):
        self.authenticate_user(self.jobseeker_a_user)
        
        response = self.client.post(
            self.APPLY_JOB_URL,
            {
                "job":self.inactive_job.id,
                "cover_letter":"i am interst in this postiorn"
            },
            format='json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(),0)
        
    def test_company_cannot_apply_to_job(self):
        self.authenticate_user(self.company_user)
        response = self.client.post(
            self.APPLY_JOB_URL,
            self.application_data,
            format="json"
        )
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
    def test_cannot_apply_twice_to_same_job(self):
        self.authenticate_user(self.jobseeker_a_user)
        first_response = self.client.post(
            self.APPLY_JOB_URL,
            self.application_data,
            format="json",
        )
        
        self.assertEqual(first_response.status_code,status.HTTP_201_CREATED)        
        
        second_response = self.client.post(
            self.APPLY_JOB_URL,
            self.application_data,
            format="json",
        )
        
        self.assertEqual(second_response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(),1)
        
        
        
    def test_invalid_job_id_cannot_apply(self):
        self.authenticate_user(self.jobseeker_a_user)
        response = self.client.post(
            self.APPLY_JOB_URL,
            {
                "job":9999,
                "cover_letter":"i want to apply this job",
            },
            format= "json",
        )
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(),0)
        
        
    def test_cover_letter_required(self):
        self.authenticate_user(self.jobseeker_a_user)
        response = self.client.post(
            self.APPLY_JOB_URL,
            {"job":self.active_job.id},
            format = 'json',
        )
        
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(),0)


    def test_application_is_saved_with_correct_relationships(self):
        self.authenticate_user(self.jobseeker_a_user)
        response = self.client.post(
            self.APPLY_JOB_URL,
            self.application_data,
            format='json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(),1)
        
        
        application = Application.objects.get(
            job=self.active_job,
            jobseeker = self.jobseeker_a
        )
        
        self.assertEqual(application.job,self.active_job)
        self.assertEqual(application.jobseeker,self.jobseeker_a)
    
    def test_jobseeker_profile_required(self):
        self.authenticate_user(self.new_jobseeker_user)
        
        response = self.client.post(
            self.APPLY_JOB_URL,
            self.application_data,
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(),0)
    
#PYTHONPATH=.. python manage.py test tests.api.applications.test_apply_job