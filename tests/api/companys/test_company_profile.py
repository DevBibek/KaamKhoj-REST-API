from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.users.models import Company, User


class CompanyProfileTest(APITestCase):
    COMPANY_PROFILE_URL = "/api/v1/company/profile/me/"
    def setUp(self):
    
        
        
        self.new_company_user = User.objects.create_user(
            username="testapi",
            first_name ="test",
            last_name = "profile",
            email="testprofile@gmail.com",
            password="testpassword123",
            role = "COMPANY"
            )

        self.company_a_user = User.objects.create_user(
            username="company_a",
            first_name ="company",
            last_name = "a_test",
            email="a@gmail.com",
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
        
        
        self.company_b_user = User.objects.create_user(
            username="company_b",
            first_name ="company_b",
            last_name = "b",
            email="b@gmail.com",
            password="testcompany",
            role = "COMPANY"
            )
        
        self.company_b = Company.objects.create(
            user= self.company_b_user,
            company_name ="Company B",
            description = "ths is company b description",
            location = "Pokhara",
            phone ="9823342323",
            )
                
        
        self.jobseeker_user = User.objects.create_user(
            username="jobseeker",
            first_name ="test",
            last_name = "profile",
            email="jobseekerprofile@gmail.com",
            password="testpassword123",
            role = "JOB_SEEKER"
            )
        
        self.company_data ={
            "company_name":"Test company",
            "description":"we are testing comapy api",
            "location":"nepal",
            "phone":"9838493949",
        }
        
    def authenticate_user(self,user):
        return self.client.force_authenticate(user=user)
    
    
    def test_unauthenticated_user_cannot_retrieve_profile(self):
        response = self.client.get(self.COMPANY_PROFILE_URL)
        
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        
        
    def test_unauthenticated_user_cannot_create_profile(self):
        response = self.client.post(
        self.COMPANY_PROFILE_URL,
        self.company_data,
        format="json"
        )

        self.assertEqual(
        response.status_code,
        status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(Company.objects.count(), 2)
        
    def test_unauthenticated_user_cannot_update_profile(self):
        response = self.client.patch(
            self.COMPANY_PROFILE_URL,
            {"company_name":"Unthenticate Company"},
            format='json',
        )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_unauthenticated_user_cannot_delete_profile(self):
        response = self.client.delete(
            self.COMPANY_PROFILE_URL
        )
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_without_profile_company_cannot_retrieve(self):
        self.authenticate_user(user=self.new_company_user)
        response = self.client.get(self.COMPANY_PROFILE_URL)
                
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        
    def test_without_profile_company_cannot_update(self):
        self.authenticate_user(self.new_company_user)
        response = self.client.patch(
            self.COMPANY_PROFILE_URL,
            {"company_name":"update company"},
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        
    def test_without_profile_jobseeker_cannot_delete(self):
        self.authenticate_user(self.new_company_user)
        response = self.client.delete(self.COMPANY_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    
    def test_company_can_retrieve_own_profile(self):
        self.authenticate_user(self.company_a_user)
        response=self.client.get(
        self.COMPANY_PROFILE_URL,
        ) 
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(self.company_a_user.email,"a@gmail.com")
        self.assertEqual(self.company_a.company_name,"Company A")
    
    
        
    def test_company_can_create_profile(self):
        self.authenticate_user(user=self.new_company_user)
        response = self.client.post(
            self.COMPANY_PROFILE_URL,
            self.company_data,
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["company_name"],"Test company")
        self.assertEqual(Company.objects.count(),3)
        
        response=self.client.get(
            self.COMPANY_PROFILE_URL,
            ) 
        created_profile = Company.objects.get(user=self.new_company_user)
        self.assertEqual(
            created_profile.company_name,"Test company"
        )
        
    
        
    def test_company_owner_only_update_own_prfile(self):
        self.authenticate_user(user=self.company_b_user)
        response = self.client.patch(
            self.COMPANY_PROFILE_URL,
            {"user":{"email":"update@gmail.com"},
            "company_name":"update company B",},
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
        self.company_a.refresh_from_db()
        self.company_b_user.refresh_from_db()
        self.company_b.refresh_from_db()
        
        self.assertEqual(
            self.company_a.company_name,
            "Company A"
            )
        self.assertEqual(
            self.company_b.user.email,
            "update@gmail.com"
        )
        self.assertEqual(
            self.company_b.company_name,
            "update company B")
        
        
        
    def test_company_owner_only_delete_own_prfile(self):
        
        self.authenticate_user(user=self.company_a_user)
        response = self.client.delete(self.COMPANY_PROFILE_URL)
        
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        self.assertFalse(Company.objects.filter(user=self.company_a_user).exists())
        self.assertTrue(Company.objects.filter(user=self.company_b_user).exists())
        
        
        
    def test_company_cannot_create_dublicate_profile(self):
        self.authenticate_user(self.company_a_user)
        response = self.client.post(
            self.COMPANY_PROFILE_URL,
            self.company_data,
            format="json",
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(),2)
        
        
    def test_company_cannot_create_dublicate_phone(self):
        self.authenticate_user(self.new_company_user)
        new_data ={
            **self.company_data,
            "phone":"9823342323",
        }
        response = self.client.post(
            self.COMPANY_PROFILE_URL,
            new_data,
            formant = 'json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(),2)
        
        
    def test_jobseeker_cannot_retrieve_company_profile(self):
        
        self.authenticate_user(user=self.jobseeker_user)
        response = self.client.get(self.COMPANY_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    
    
    def test_jobseeker_cannot_create_company_profile(self):
        self.authenticate_user(user=self.jobseeker_user)
        
        response = self.client.post(
            self.COMPANY_PROFILE_URL,
            self.company_data,
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertEqual(Company.objects.count(),2)
        
        
        
    def test_jobseeker_cannot_update_company_profile(self):
        self.authenticate_user(user=self.jobseeker_user)
        
    
        response = self.client.patch(
            self.COMPANY_PROFILE_URL,
            {"company_name":"company update by jobseekr"},
            format= 'json',
        )
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.company_a.refresh_from_db()
        self.company_b.refresh_from_db()
        
        self.assertEqual(self.company_a.company_name,"Company A")
        self.assertEqual(self.company_b.company_name,"Company B")
        
        
        
    def test_jobseeker_cannot_delete_company_profile(self):
        self.authenticate_user(user=self.jobseeker_user)
                
        response = self.client.delete(self.COMPANY_PROFILE_URL)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertTrue(Company.objects.filter(user=self.company_a_user).exists())
        self.assertTrue(Company.objects.filter(user=self.company_b_user).exists())
        
        
#PYTHONPATH=.. python manage.py test tests.api.companys.test_company_profile