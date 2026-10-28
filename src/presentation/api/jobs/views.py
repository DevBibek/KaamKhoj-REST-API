import logging

from rest_framework import serializers, viewsets
from rest_framework.exceptions import PermissionDenied

# from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.jobs.services import ManageCompanyJobs
from infrastructure.jobs.repositories import JobRepository
from infrastructure.users.repository.company_repository import CompanyRepository
from presentation.api.common.permission import IsCompany, IsJob
from presentation.api.common.responses import HandleResponseMixin
from presentation.api.jobs.serializers import JobSerializer

logger = logging.getLogger("kaamkhoj")

class CompanyJobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    
    #Authenteaction / Authorization
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]
    def get_application(self):
        job_repo = JobRepository()
        company_repo = CompanyRepository()
        return ManageCompanyJobs(

            job_repo=job_repo,
            company_repo= company_repo)
    
    def get_queryset(self):
        application = self.get_application()
        
        return application.get_jobs(
            company= self.request.user.company)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        data = serializer.validated_data
        use_case = self.get_application()
        
        try:
            job = use_case.create(
                user=request.user,
                **data)
            
        
        except PermissionError as  e:
            raise PermissionDenied(detail=str(e))
        
        except ValueError as e:
            raise ValueError(detail=str(e))
        
        
        response_serilizer = self.get_serializer(job)
        return Response(
            response_serilizer.data,
            status=status.HTTP_201_CREATED
        )
        
        
        
        
    
    
        
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from application.jobs.get_my_jobs import GetMyJobs


class MyPostAPI(APIView):
    permission_classes = [IsCompany]
    def get(self,request):        
        job_repository = JobRepository()
        company_repo = CompanyRepository()
        use_case = GetMyJobs(
            job_repository= job_repository,
            company_repo=company_repo
        )
        
        jobs = use_case.execute(user = request.user)
        
        serializer = JobSerializer(jobs,many = True)
        
        return Response({
            "message":"My jobs retrieved sucessfully",
            "data": serializer.data
        },status=status.HTTP_200_OK)
    
    
    
#========== Public Job API View  For everyone =======================

from application.jobs.get_public_jobs import GetPublicJobs
from presentation.api.common.pagination import CustomPagination


class PublicJobListView(APIView,HandleResponseMixin):
    pagination_class= CustomPagination
    def get(self,request):
        search = request.query_params.get("search")
        location = request.query_params.get("location")
        min_salary = request.query_params.get("min_salary")
        max_salary = request.query_params.get("max_salary")
        ordering = request.query_params.get("ordering")
        
        job_repo = JobRepository()
        use_case = GetPublicJobs(
            job_repo=job_repo
        )
        
        jobs = use_case.execute(
            search=search,
            location=location,
            min_salary=min_salary,
            max_salary=max_salary,
            ordering = ordering,
        )
        if not jobs.exists():
            return  self.not_found(
                msg="Job not found",
                code= status.HTTP_404_NOT_FOUND
            )
            
            
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(jobs,request,)
        
        serializer = JobSerializer(page,many= True)
        
        return paginator.get_paginated_response(serializer.data)
        
        