from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework.permissions import IsAuthenticated

from .views import CompanyAPI, JobseekerAPI

router = DefaultRouter()

router.register("jobseeker-api",JobseekerAPI,basename="jobseekerapi"),
router.register("companay-api",CompanyAPI,basename="company"),

urlpatterns= [
    path("",include(router.urls))
]



