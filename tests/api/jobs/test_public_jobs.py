from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, User


class PublicJobsAPITests(APITestCase):
    
    def setUp(self):
        #create company accouount 
        user = User.objects.create_user(
            username="testcompany",
            email="company@gmail.com",
            password="testpassword123",
            role = User.Role.COMPANY,
        )
        
        #create verified company
        self.company = Company.objects.create(
            user=user,
            company_name = "Test Company",
            phone ="982312832",
            verification_status = Company.VerificationStatus.VERIFIED,
        )
        
        #create active jobs
        
        Job.objects.create(
            company=self.company,
            title = "Backend Developer",
            description ="Test Backend developer job",
            salary = "50000.00",
            location = "kathmandu",
            is_active = True,
        )
    
    
    
    def test_public_jobs_returens_200(self):
        response = self.client.get("/api/v1/jobs/")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertTrue(response.data["success"])
        self.assertEqual(
            response.data["pagination"]["total_items"],1
            )
        
        self.assertEqual(response.data["data"][0]["title"],"Backend Developer")
        
        
    def test_public_jobs_filters(self):
        #inactive job
        Job.objects.create(
            company=self.company,
            title = "Inactive Developer Job",
            description = "This job should not be public jobs",
            salary = "12000.00",
            location = "kathamndu",
            is_active = False,
        )
        user = User.objects.create_user(
            username = "pendingcompany",
            email = "pending@example.com",
            password = "testpassword123",
            role = User.Role.COMPANY
        )

        # create unverified company
        
        pending_company = Company.objects.create(
            user=user,
            company_name="Pending Company",
            phone="9812345679",
            verification_status=Company.VerificationStatus.PENDING,
            )
        
        #pending company job
        Job.objects.create(
        company=pending_company,
        title="Pending Company Job",
        description="This job should not be public",
        salary="45000.00",
        location="Pokhara",
        is_active=True,
        )
        response = self.client.get("/api/v1/jobs/")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["pagination"]["total_items"],1
        )
        titles = [job["title"] for job in response.data["data"]]
        
        self.assertEqual(
            titles,["Backend Developer"]
        )
        
        

    
    def test_public_jobs_search_and_location_ordering(self):
        Job.objects.create(
            company=self.company,
            title = "Python Developer",
            description = "Python Backed job",
            salary = "40000.00",
            location = "kathmandu",
            is_active = True
        )
        
        response = self.client.get("/api/v1/jobs/?search=Developer&location=kathmandu&ordering=salary_low")
        
        titles = [job["title"]for job in response.data["data"]]
        
        
        self.assertEqual(response.status_code ,200)
        self.assertEqual(response.data["pagination"]["total_items"],2)

        self.assertEqual(
            titles,["Python Developer","Backend Developer"],
        )

#PYTHONPATH=.. python manage.py test tests.api.jobs.test_public_jobs