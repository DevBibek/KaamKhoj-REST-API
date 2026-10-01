from django.urls import include, path
from rest_framework.routers import DefaultRouter

from presentation.api.jobs.views import JobPostApi,MyPostAPI

router = DefaultRouter()

router.register(r'jobpost-api',JobPostApi,basename="jobpostapi")

urlpatterns = [
    path('',include(router.urls)),
    path("company/my-posts/",MyPostAPI.as_view(),name= "my-posts")
]