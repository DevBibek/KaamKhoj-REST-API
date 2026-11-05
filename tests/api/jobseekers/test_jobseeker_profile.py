from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.users.models import JobSeeker, User


class JobSeekerProfileTest(APITestCase):
    
    JOBSEEKR_PROFILE_URL = "/api/v1/jobseeker/profile/me/"
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
        
        self.jobseeker_a = JobSeeker.objects.create(
            user= self.jobseeker_a_user,
            full_name ="jobseeker A",
            phone_number ="9823342003",
            address = "kathmandu",
            skills = "Accountent",
            education ="BBA",
            experience = 2
        )
        
        
        self.jobseeker_b_user= User.objects.create_user(
            username="jobseeker_b",
            first_name ="jobseeker_b",
            last_name = "b",
            email="b@gmail.com",
            password="testjobseekr",
            role = "JOB_SEEKER"
            )
                
        self.jobseeker_b =JobSeeker.objects.create(
            user= self.jobseeker_b_user,
            full_name ="Jobseeker B",
            phone_number ="9823342236",
            address = "Pokhara",
            skills = "Bckend Developer",
            education ="BCA",
            experience = 4
            )
                
        
        self.company_user= User.objects.create_user(
                    username="companyuser",
                    first_name ="test",
                    last_name = "profile",
                    email="company@gmail.com",
                    password="testpassword123",
                    role = "COMPANY"
                    )
        
        
        self.jobseeker_data ={
            "full_name": "joy jowbe",
            "phone_number": "9873273743",
            "address": "Lalitpur",
            "skills": "Ex est Nam in aut ut elit est",
            "education": "BIT",
            "experience": 4,
        }
        
    
    def authenticate_user(self,user):
        return self.client.force_authenticate(user=user)
    
    
    def test_unauthenticated_user_cannot_retrieve_profile(self):
        response = self.client.get(self.JOBSEEKR_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
        
    def test_unauthenticated_user_cannot_create_profile(self):
            response = self.client.post(
            self.JOBSEEKR_PROFILE_URL,
            self.jobseeker_data,
            format="json"
            )
    
            self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
            
            self.assertEqual(JobSeeker.objects.count(), 2)
            
            
            
    def test_unauthenticated_user_cannot_update_profile(self):
        response = self.client.patch(
            self.JOBSEEKR_PROFILE_URL,
            {"full_name":"unauthented jobseeker"},
            format="json",
            )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.jobseeker_a_user.refresh_from_db()
        self.jobseeker_b_user.refresh_from_db()
                        
        self.assertEqual(self.jobseeker_b.full_name,"Jobseeker B")
        self.assertEqual(self.jobseeker_a.full_name,"jobseeker A")
        
        
    def test_unauthenticated_user_cannot_delete_profile(self):
        response = self.client.delete(self.JOBSEEKR_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        self.assertTrue(JobSeeker.objects.filter(user=self.jobseeker_a_user).exists())
        self.assertTrue(JobSeeker.objects.filter(user=self.jobseeker_b_user).exists())


    def test_without_profile_jobseeker_cannot_retrieve(self):
        self.authenticate_user(self.new_jobseeker_user)
        
        response = self.client.get(self.JOBSEEKR_PROFILE_URL)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND )
        
        
    def test_without_profile_jobseeker_cannot_update(self):
        self.authenticate_user(self.new_jobseeker_user)
        response = self.client.patch(
            self.JOBSEEKR_PROFILE_URL,
            {"full_name":"update jobseeker"},
            format='json',
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        
    def test_without_profile_jobseeker_cannot_delete(self):
        self.authenticate_user(self.new_jobseeker_user)
        response = self.client.delete(
            self.JOBSEEKR_PROFILE_URL
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        
    def test_jobseeker_can_retrieve_profile(self):
        self.authenticate_user(self.jobseeker_a_user)
        response = self.client.get(self.JOBSEEKR_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["full_name"],"jobseeker A")
        
        
        
    
    def test_jobseeker_user_can_create_profile(self):
        self.authenticate_user(user=self.new_jobseeker_user)
        response = self.client.post(
            self.JOBSEEKR_PROFILE_URL,
            self.jobseeker_data,
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["full_name"],"joy jowbe")
        self.assertEqual(JobSeeker.objects.count(),3)
        created_profile=  JobSeeker.objects.get(user=self.new_jobseeker_user)
        self.assertEqual(
            created_profile.full_name,
            "joy jowbe"
        )
        
        
    def test_jobseeker_user_can_update_only_own_profile(self):
        self.authenticate_user(user=self.jobseeker_b_user)
        response = self.client.patch(
            self.JOBSEEKR_PROFILE_URL,
            {"user":{
                "email":"update@gmail.com"},
            "full_name":"update jobseeker",
            },
            format="json"
        )
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.jobseeker_b_user.refresh_from_db()
        self.jobseeker_a.refresh_from_db()
        self.jobseeker_b.refresh_from_db()
        
        self.assertEqual(self.jobseeker_b.user.email,"update@gmail.com")
        self.assertEqual(self.jobseeker_b.full_name,"update jobseeker")
        self.assertEqual(self.jobseeker_a.full_name,"jobseeker A")
        
        
    def test_jobseeker_only_delete_own_profile(self):
        self.authenticate_user(user=self.jobseeker_a_user
        )
        response = self.client.delete(self.JOBSEEKR_PROFILE_URL)
        
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.assertFalse(JobSeeker.objects.filter(user = self.jobseeker_a_user).exists())
        self.assertTrue(JobSeeker.objects.filter(user=self.jobseeker_b_user).exists())
        
        
    def test_jobseeker_cannot_create_duplicate_profile(self):
        self.authenticate_user(self.jobseeker_b_user)
        response = self.client.post(
            self.JOBSEEKR_PROFILE_URL,
            self.jobseeker_data,
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(JobSeeker.objects.count(),2)
    
    def test_jobseeker_cannot_create_dublicate_phone(self):
        self.authenticate_user(self.new_jobseeker_user)
        new_data ={
            **self.jobseeker_data,
            "phone_number":"9823342003",
        }
        response = self.client.post(
            self.JOBSEEKR_PROFILE_URL,
            new_data,
            formant = 'json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(JobSeeker.objects.count(),2)
    def test_company_user_cannot_retrieve_jobseeker_profile(self):
        self.authenticate_user(self.company_user)
        response = self.client.get(self.JOBSEEKR_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
            
    
    def test_company_user_cannot_create_jobseeker_profile(self):
        self.authenticate_user(self.company_user)
        response = self.client.post(
            self.JOBSEEKR_PROFILE_URL,
            self.jobseeker_data,
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertEqual(JobSeeker.objects.count(),2)
        
    def test_company_cannot_update_jobseeker_profile(self):
        self.authenticate_user(self.company_user)
        response = self.client.patch(
            self.JOBSEEKR_PROFILE_URL,
            {"user":{
                "email":"update@gmail.com"},
                "full_name":"update jobseeker",
                },
            format="json"
            
            )
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        self.jobseeker_a.refresh_from_db()
        self.jobseeker_b.refresh_from_db()
                
        self.assertEqual(self.jobseeker_b.user.email,"b@gmail.com")
        self.assertEqual(self.jobseeker_b.full_name,"Jobseeker B")
        self.assertEqual(self.jobseeker_a.full_name,"jobseeker A")
        
    def test_company_cannot_delete_jobseeker_profile(self):
        self.authenticate_user(self.company_user)
        response = self.client.delete(self.JOBSEEKR_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.jobseeker_a_user.refresh_from_db()
        self.jobseeker_b_user.refresh_from_db()
        
        self.assertTrue(JobSeeker.objects.filter(user=self.jobseeker_a_user).exists())
        self.assertTrue(JobSeeker.objects.filter(user=self.jobseeker_b_user).exists())



# PYTHONPATH=.. python manage.py test tests.api.jobseekers.test_jobseeker_profile