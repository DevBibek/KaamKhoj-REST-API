from django.test import TestCase
from rest_framework import status

from infrastructure.jobs.models import Job
from infrastructure.jobs.repositories import JobRepository
from infrastructure.users.models import Company, User


class JobRepositryTest(TestCase):
    
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
                title=f"Backend Developer{i}",
                description = "test job query performance.",
                salary = 40000.00,
                location = "kathmandu",
                is_active = True,
            )
            
    def test_job_repositry(self):
        repo = JobRepository()
        with self.assertNumQueries(1):
            jobs = repo.get_public_jobs()
            
            for job in jobs:
                print(job.company.company_name)
            self.assertEqual(len(jobs),5)
            self.assertEqual(
                jobs[0].company.company_name,
                "Test Company"
            )


# PYTHONPATH=.. python manage.py test tests.performance.test_job_repository