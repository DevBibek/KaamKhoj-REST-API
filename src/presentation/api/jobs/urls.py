from django.urls import include, path
from rest_framework.routers import DefaultRouter

from presentation.api.jobs.views import CompanyJobViewSet,MyPostAPI,PublicJobListView

router = DefaultRouter()

router.register(r'create-job',CompanyJobViewSet,basename="jobpostapi")

urlpatterns = [
    path('',include(router.urls)),
    path("jobs/",PublicJobListView.as_view(),name = "jobs"),
    path("company/my-posts/",MyPostAPI.as_view(),name= "my-posts")
]