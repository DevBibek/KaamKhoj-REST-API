import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.jobs.services import CreateJobService
from infrastructure.jobs.models import Job

# from domain.jobs.entities import Job
from infrastructure.jobs.repositories import JobRepository
from presentation.api.common.permission import IsCompany, IsJob
from presentation.api.common.responses import HandleResponseMixin
from presentation.api.jobs.serializers import JobPostSerializer

from .filters import JobFilters

logger = logging.getLogger("kaamkhoj")

class JobPostApi(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobPostSerializer
    
    #Filtering
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter]
    filter_class = JobFilters
    
    #Searching
    search_fields = ["title","company__company_name","description"]
    
    #ordering 
    ordering_fields = ["created_at","salary","title"]
    
    ordering = ["-created_at"]
    
    #Authenteaction / Authorization
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsJob,IsCompany]
    
    def perform_create(self, serializer):
        data = serializer.validated_data
        
        repository = JobRepository()
        
        use_case = CreateJobService(repository)
        
        
        try:
            use_case.execute(
                data= data,
                user=self.request.user
            )

        except ValueError as e:
            raise serializers.ValidationError(str(e))


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from application.jobs.get_my_jobs import GetMyJobs
from infrastructure.users.models import User


class MyPostAPI(APIView):
    def get(self,request):
        self.permission_classes = [IsCompany]
        if request.user.role != User.Role.COMPANY:
            return Response({"message":"Only Company can access my posts."},status=status.HTTP_403_FORBIDDEN
            )
        
        job_repository = JobRepository()
        use_case = GetMyJobs(
            job_repository= job_repository
        )
        
        jobs = use_case.execute(user = request.user)
        
        serializer = JobPostSerializer(jobs,many = True)
        
        return Response({
            "message":"My jobs retrieved sucessfully",
            "data": serializer.data
        },status=status.HTTP_200_OK)