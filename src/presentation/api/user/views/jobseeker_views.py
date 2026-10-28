from rest_framework import serializers, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.users.create_jobseeker import CreateJobSeeker
from infrastructure.users.repository.jobseeker_repository import JobSeekerRepository
from presentation.api.common.permission import IsJobSeeker
from presentation.api.user.serializers.jobseeker_serializers import JobSeekerSerializer


class JobseekerProfileView(viewsets.ModelViewSet):    
    serializer_class = JobSeekerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes  = [IsJobSeeker]
    def get_jobseeker(self,):
        jobseeker_repo = JobSeekerRepository()
        return CreateJobSeeker(jobseeker_repo=jobseeker_repo)
    
    def get_queryset(self):
        use_case = self.get_jobseeker()
        return use_case.gets_jobseeker(user=self.request.user)
    
    
    def create(self, request, *args, **kwargs):
        use_case = self.get_jobseeker()
        serializer = self.get_serializer(data = request.data,)
        serializer.is_valid(raise_exception = True)
        data = serializer.validated_data
        
        try:
            jobseeker =  use_case.create(
            user= request.user,
            **data
            )
        except PermissionError as e:
            raise PermissionDenied(detail=str(e))
    
    
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
        response_serializer = self.get_serializer(jobseeker)
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
        