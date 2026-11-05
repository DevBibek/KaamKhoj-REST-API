from django.urls import include, path
from rest_framework.routers import DefaultRouter

from presentation.api.user.views.company_views import (
    CompanyProfileViewSet,
    UpdateVerificationStatusView,
)
from presentation.api.user.views.jobseeker_views import JobseekerProfileView

router = DefaultRouter()

# router.register("jobseeker/profile",JobseekerProfileView,basename="jobseekerapi"),
# router.register("company-profile",CompanyProfileViewSet,basename="company"),

urlpatterns= [
    path("",include(router.urls)),
    path(
        'company/profile/me/', 
            CompanyProfileViewSet.as_view({
            'get': 'list',   
            'post': 'create',    
            'put': 'update',     
            'patch': 'update',  
            'delete': 'destroy',
        }),
        name='company-profile'
    ),
    path(
            'jobseeker/profile/me/', 
                JobseekerProfileView.as_view({
                'get': 'list',   
                'post': 'create',    
                'put': 'update',    
                'patch': 'update',   
                'delete': 'destroy', 
                }),
            name='jobseeker-profile',
        ),
    
    
    
    path("admin/companies/<int:id>/verification/",UpdateVerificationStatusView.as_view(),name="update-verification"),
    
    ]



