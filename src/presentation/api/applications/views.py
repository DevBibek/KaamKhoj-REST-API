from rest_framework import serializers, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.applications.apply_for_job import ApplyForJob
from infrastructure.applications.repository import ApplicationRepository
from infrastructure.users.repository.jobseeker_repository import JobSeekerRepository
from presentation.api.applications.serializers import (
    ApplicationListSerializer,
    ApplicationSerializer,
)
from presentation.api.common.permission import ISApplication, IsCompany
from presentation.api.common.responses import HandleResponseMixin


class ApplayForJobAPI(APIView, HandleResponseMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ISApplication]
    
    def post(self,request):
        serializer = ApplicationSerializer(data = request.data)
        if not serializer.is_valid():
            return self.error_handle(
                msg="Invalid data provide",
                error= serializer.errors,
                code= status.HTTP_404_NOT_FOUND
            )
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
            
            
    
        
from application.applications.get_my_applications import GetMyApplication
from application.applications.update_application_status import UpdataApplication


class GetMyApplicationAPI(viewsets.ReadOnlyModelViewSet):  
    serializer_class = ApplicationListSerializer  
    permission_classes =[ISApplication]
    def get_queryset(self):
        repository = ApplicationRepository()
        use_case = GetMyApplication(repository)
        try:
            return use_case.execute(user = self.request.user)
        
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
        
from application.applications.get_job_application import GetJobApplication
from infrastructure.jobs.repositories import JobRepository
from presentation.api.common.pagination import CustomPagination
from presentation.api.user.serializers.company_serializers import (
    CompanyApplicationSerializer,
)


class CompanyJobApplicationListAPI(APIView):
    permission_clesses = [IsCompany]
    authentication_classes = [JWTAuthentication]
    pagination_cleass = CustomPagination
    def get(self,request,job_id):
        job_repository = JobRepository()
        application_repository = ApplicationRepository()
        
        use_case = GetJobApplication(
            application_repository= application_repository,
            job_repository= job_repository
        )
        
        paginator = self.pagination_cleass()
        try:
            applications = use_case.execute(user= request.user,
                job_id=job_id
            )
            page = paginator.paginate_queryset(applications,request,view=self)
        
        
        except ValueError as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"message":str(e)},status=status.HTTP_403_FORBIDDEN)
        
        
        serializer = CompanyApplicationSerializer(page,many= True)
        
        return paginator.get_paginated_response(serializer.data)
    
        

# from application.applications.update_application_status import UpdataApplication

from .serializers import UpdateApplicationStatusSerializers


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
            raise serializers.ValidationError(str(e))
            
            
        except PermissionError as e:
            raise PermissionDenied(str(e))
        
        
        return Response({
            "message":"Application status update sucessfully",
            "application_id": application.id,
            "application_status":application.status,
        })