from django.urls import include, path
from rest_framework.routers import DefaultRouter

from presentation.api.user.views.company_views import (
    CompanyProfileViewAPI,
    UpdateVerificationStatusView,
)
from presentation.api.user.views.jobseeker_views import JobseekerProfileView

router = DefaultRouter()

router.register("jobseeker-profile",JobseekerProfileView,basename="jobseekerapi"),
router.register("company-profile",CompanyProfileViewAPI,basename="company"),

urlpatterns= [
    path("",include(router.urls)),
    path("update-verification/<int:id>/",UpdateVerificationStatusView.as_view()),
    
    
    ]



