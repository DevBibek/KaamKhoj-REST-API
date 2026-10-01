from rest_framework import serializers, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.users.create_company import CreateCompany
from application.users.create_jobseeker import CreateJobSeeker
from infrastructure.users.models import Company, JobSeeker
from infrastructure.users.repository.company_repository import CompanyRepository
from infrastructure.users.repository.jobseeker_repository import JobSeekerRepository
from presentation.api.common.permission import IsCompany, IsJobSeeker
from presentation.api.user.serializer import (
    CompanySerializers,
    JobSeekerSerializer,
)


class JobseekerAPI(viewsets.ModelViewSet):    
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes  = IsJobSeeker
    
    def perform_create(self, serializer):
        data = serializer.validated_data

        repository = JobSeekerRepository()

        use_case = CreateJobSeeker(repository)

        try:
            use_case.execute(
            data = data,
            user=self.request.user,
            phone_number = data["phone_number"]
            )
            
            
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
        
    
class CompanyAPI(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializers
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]
        
    
    def perform_create(self, serializer):
        data = serializer.validated_data
        repository = CompanyRepository()
        
        use_case = CreateCompany(repository)
        
        try:
            use_case.execute(
                data = data,
                user = self.request.user
                )

        except ValueError as e:
            raise serializers.ValidationError(str(e))