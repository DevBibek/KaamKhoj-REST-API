from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ApplayForJobAPI,
    GetMyApplicationAPI,
    CompanyJobApplicationListAPI,
    UpdateApplicationStatusAPI,
)

router = DefaultRouter()

router.register("get-myapplication",GetMyApplicationAPI,basename="myapplication")



urlpatterns = [
    path('',include(router.urls)),
    path("apply-job/",ApplayForJobAPI.as_view(), name="apply-job"),
    path("update-status/<int:application_id>/",UpdateApplicationStatusAPI.as_view(),name="update-status"),
    path("job/<int:job_id>/applications/",CompanyJobApplicationListAPI.as_view(),name="job-application"),
]