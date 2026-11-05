from rest_framework import status
from rest_framework.test import APITestCase

from infrastructure.jobs.models import Job
from infrastructure.users.models import Company, User


class PublicJobsPaginationTests(APITestCase):
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
        for i in range(100):
            Job.objects.create(
                company= self.company,
                title=f"Backend Developer {i}",
                description = "test job query performance.",
                salary = 40000.00,
                location = "kathmandu",
                is_active = True,
            )
            
            
    def test_default_page_returns_20_jobs(self):
        response = self.client.get(
            self.PUBLIC_JOBS_URL
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(
            response.data["pagination"]["total_items"],100
            )
        
        self.assertEqual(
            len(response.data["data"]),20
            )
        
        
        
    def test_pagination_total_items(self):
        response = self.client.get(
            self.PUBLIC_JOBS_URL
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["pagination"]["total_items"],100)
        
        
    def test_second_page_returns_20_jobs(self):
        response = self.client.get(
        f"{self.PUBLIC_JOBS_URL}?page=2"
        )
        
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["pagination"]["total_items"],100)
        self.assertEqual(len(response.data["data"]),20)
        self.assertNotEqual(len(response.data["data"]),30)
    
    
    
    def test_custom_page_size_returns_requested_number_of_jobs(self):
        response = self.client.get(
            f"{self.PUBLIC_JOBS_URL}?page=1&page_size=15"
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        
        self.assertEqual(
            len(response.data["data"]),
            15
            )
        
        
    def test_invalid_page_returns_404(self):
        response = self.client.get(
            f"{self.PUBLIC_JOBS_URL}?page=1999"
            )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        
    def test_page_size_is_limited_to_50(self):
        response = self.client.get(
            f"{self.PUBLIC_JOBS_URL}?page=1&page_size=70"
            )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(
            len(response.data["data"]),50
            )
        
    def test_first_page_has_next_but_not_previous_links(self):
        response = self.client.get(
            f"{self.PUBLIC_JOBS_URL}"
            )
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsNotNone(response.data['pagination']["next"])
        self.assertIsNone(response.data["pagination"]["previous"])
        
        
    def test_second_page_has_previous_and_next_links(self):
        response = self.client.get(
            f"{self.PUBLIC_JOBS_URL}?page=2"
            )
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        self.assertIsNotNone(response.data["pagination"]["previous"])
        self.assertIsNotNone(response.data["pagination"]["next"])
        
        
    def test_last_page_has_previous_but_no_next_link(self):
        response = self.client.get(f"{self.PUBLIC_JOBS_URL}?page=5")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["pagination"]["next"])
        self.assertIsNotNone(response.data["pagination"]["previous"])
        
        
    def test_empty_job_list_returns_200(self):
        Job.objects.update(is_active=False)
        
        response = self.client.get(f"{self.PUBLIC_JOBS_URL}")
        
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["pagination"]["total_items"],0)
        self.assertEqual(response.data["data"],[])
        self.assertIsNone(response.data["pagination"]["next"])
        self.assertIsNone(response.data["pagination"]["previous"])
        
        
        
        
        
        
# PYTHONPATH=.. python manage.py test tests.api.jobs.test_public_job_pagination


        """
Phase 1 — Unit testing

Test business logic independently.
- CompanyRules
- JobRules
- ApplicationRules
- Use cases
Next phase



Phase 2 — Repository integration testing

Test database operations.
- Create and retrieve company
- Create and retrieve jobs
- Filter verified companies
- Retrieve applications
- Duplicate application prevention



Phase 3 — API integration testing

Check that the complete API flow works.
- Authentication
- Request validation
- Response format
- Error handling
- User roles and permissions
We will review existing tests and fill gaps rather than repeat them.



Phase 4 — Performance testing

We already tested public job query optimization. Next:
- Company job list
- Application list
- Company applicants list
- Job detail with company information
- Query count as records increase
- Response-time and load testing



Phase 5 — Final testing and quality
- Run the complete test suite.
- Check test coverage.
- Fix flaky tests.
- Check edge cases.
- Prepare test documentation for GitHub.
        """