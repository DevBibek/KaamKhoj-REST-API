from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, User


class PublicJobQueryTest(APITestCase):
    PUBLIC_JOBS_URL = "/api/v1/jobs/"
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="company",
            email="company@gmail.com",
            password="test123",
            role="COMPANY"
        )

        self.company = Company.objects.create(
            user=self.user,
            company_name="Test Company",
            phone="9823342003",
            verification_status="VERIFIED"
        )
        for i in range(5):
            Job.objects.create(
                company= self.company,
                title=f"Backend Developer {i}",
                description = "test job query performance.",
                salary = 40000.00,
                location = "kathmandu",
                is_active = True,
            )
            
    
    def test_public_query_count(self):
        with CaptureQueriesContext(connection) as queries:
            respone = self.client.get(self.PUBLIC_JOBS_URL)

            
        self.assertEqual(
            respone.status_code,
            status.HTTP_200_OK
            )
        for query in queries:
            print(f"queries ========== {query["sql"]}")
        print(f"Total databse queries run ==  {len(queries)}")
    
    # PYTHONPATH=.. python manage.py test tests.performance.test_job_queries