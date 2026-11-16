from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.applications.apply_for_job import ApplyForJob
from application.applications.get_job_application import GetJobApplication
from application.applications.get_my_applications import GetMyApplication
from application.applications.update_application_status import UpdataApplication
from infrastructure.applications.models import Application
from infrastructure.applications.repository import ApplicationRepository
from infrastructure.jobs.repositories import JobRepository
from infrastructure.users.repository.jobseeker_repository import JobSeekerRepository
from presentation.api.applications.serializers import (
    ApplicationListSerializer,
    ApplicationSerializer,
)
from presentation.api.common.pagination import CustomPagination
from presentation.api.common.permission import IsApplication, IsCompany
from presentation.api.common.responses import HandleResponseMixin
from presentation.api.user.serializers.company_serializers import (
    CompanyApplicationSerializer,
)

from .serializers import UpdateApplicationStatusSerializers


class ApplyForJobAPI(APIView, HandleResponseMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsApplication]
    throttle_scope = "apply_job"
    @extend_schema(
        request=ApplicationSerializer,
        summary="Apply Jobs",
        description="Apply any jobs"
    )
    def post(self,request):
        serializer = ApplicationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        application_repo = ApplicationRepository()
        
        job_repo = JobRepository()
        
        jobseeker_repo = JobSeekerRepository()
        
        
        use_case =  ApplyForJob(
        application_repo=application_repo,
        job_repo = job_repo,
        jobseeker_repo = jobseeker_repo,
        )
        
        data = serializer.validated_data
        try:
            use_case.execute(
            user= self.request.user,
            **data
            )
            return self.success_handle(
                msg="Job Apply successfully",
                data=serializer.data,
                code= status.HTTP_201_CREATED
            )
            
        
        except ValueError as e:
            return self.error_handle(
                msg="Operation failed",
                error= str(e),
                code= status.HTTP_400_BAD_REQUEST
            
            )
        
        except PermissionError as e:
            return self.error_handle(
                msg="Permission denied",
                error= str(e),
                code=status.HTTP_403_FORBIDDEN
            )
            
            
    

class GetMyApplicationAPI(viewsets.ReadOnlyModelViewSet):  
    serializer_class = ApplicationListSerializer  
    permission_classes =[IsApplication]
    def get_queryset(self):
        repository = ApplicationRepository()
        use_case = GetMyApplication(repository)
        try:
            return use_case.execute(user = self.request.user)
        
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
        except PermissionError as e:
            raise PermissionDenied(detail=str(e))
        
        



class CompanyJobApplicationListAPI(APIView):
    permission_classes= [IsAuthenticated,IsCompany]
    authentication_classes = [JWTAuthentication]
    pagination_class= CustomPagination
    def get(self,request,job_id):
        job_repository = JobRepository()
        application_repository = ApplicationRepository()
        
        use_case = GetJobApplication(
            application_repository= application_repository,
            job_repository= job_repository
        )
        
        paginator = self.pagination_class()
        paginator.message ="Application retrieved successfully"
        try:
            applications = use_case.execute(user= request.user,
                job_id=job_id
            )
            page = paginator.paginate_queryset(applications,request,view=self)
        
        
        except ValueError as e:
            raise NotFound(detail=str(e))
        
        except PermissionError as e:
            raise PermissionDenied(detail=str(e))
        
        
        serializer = CompanyApplicationSerializer(page,many= True)
        
        return paginator.get_paginated_response(serializer.data)
    
        

class UpdateApplicationStatusAPI(APIView):
    permission_classes = [IsCompany]
    authentication_classes = [JWTAuthentication]
    
    def patch(self,request,application_id):
        serializer =UpdateApplicationStatusSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data["status"]
        
        repository = ApplicationRepository()
        use_case = UpdataApplication(application_repository = repository)
        
        try :
            application = use_case.execute(
                user=request.user,
                application_id= application_id,
                company_user= request.user,
                new_status= new_status
            )
            
        except ValueError as e:
            raise ValidationError(detail=str(e))
            
        except PermissionError as e:
            raise PermissionDenied(str(e))
        
        except Application.DoesNotExist:
            raise NotFound("Application not found.")
        
        return Response({
            "message":"Application status update sucessfully",
            "application_id": application.id,
            "application_status":application.status,
        })