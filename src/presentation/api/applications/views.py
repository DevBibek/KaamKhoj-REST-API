from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.applications.apply_for_job import ApplyForJob
from infrastructure.applications.repository import ApplicationRepository
from presentation.api.applications.serializers import (
    ApplicationListSerializer,
    ApplicationSerializer,
)
from presentation.api.common.permission import ISApplication, IsCompany
from presentation.api.common.responses import HandleResponseMixin


class ApplayForJobAPI(APIView, HandleResponseMixin):
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        serializer = ApplicationSerializer(data = request.data)
        if not serializer.is_valid():
            return self.error_handle(
                msg="Invalid data provide",
                error= serializer.errors,
                code= status.HTTP_404_NOT_FOUND
            )
        repository = ApplicationRepository()
        use_case =  ApplyForJob(
        repository=repository
        )
        try:
            use_case.execute(
            data=serializer.data,
            user= self.request.user
            )
            return self.success_handle(
                msg="Job Apply successfully",
                data=serializer.validated_data,
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
from presentation.api.user.serializer import CompanyApplicationSerializer

        
class CompanyJobApplicationListAPI(APIView):
    permission_classes = [IsCompany]
    authentication_classes = [JWTAuthentication]
    
    def get(self,request,job_id):
        job_repository = JobRepository()
        application_repository = ApplicationRepository()
        
        use_case = GetJobApplication(
            application_repository= application_repository,
            job_repository= job_repository
        )
        
        try:
            applications = use_case.execute(user= request.user,
                job_id=job_id
            )
        
        except ValueError as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"message":str(e)},status=status.HTTP_403_FORBIDDEN)
        
        
        serializer = CompanyApplicationSerializer(applications,many= True)
        
        return Response({
            "message":"Applications retrieved successfully",
            "total applicatin": applications.count(),
            "applications": serializer.data,
        },status= status.HTTP_200_OK)
        
        
    
        
        
        
        
        
        
        
        


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
                application_id= application_id,
                company_user= request.user,
                new_status= new_status
            )
        except ValueError as e:
            return Response({
                "message":str(e)},status=status.HTTP_400_BAD_REQUEST)
            
        except PermissionError as e:
            return Response({
                "message": str(e)
            },status= status.HTTP_403_FORBIDDEN)
        
        
        return Response({
            "message":"Application status update sucessfully",
            "application_id": request.user.id,
            "application_status":application.status,
        })