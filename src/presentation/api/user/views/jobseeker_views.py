import logging

from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.users.create_jobseeker import CreateJobSeeker
from infrastructure.cache.jobseeker_profile_cache import (
    invalidate_jobseeker_profile_cache,
)
from infrastructure.users.models import JobSeeker
from infrastructure.users.repository.jobseeker_repository import JobSeekerRepository
from presentation.api.common.permission import IsJobSeeker
from presentation.api.common.responses import HandleResponseMixin
from presentation.api.user.serializers.jobseeker_serializers import (
    JobseekerReadSerializer,
    JobSeekerSerializer,
    JobseekerUpdateSerializer,
)

logger = logging.getLogger("kaamkhoj")

class JobseekerProfileView(viewsets.ViewSet,HandleResponseMixin):  
    authentication_classes = [JWTAuthentication]
    permission_classes =[ IsJobSeeker ] 
    def get_use_case(self):
        return CreateJobSeeker(JobSeekerRepository())
    
    CACHE_TIMEOUT = 300
    
    def list(self,request):
        cache_key = f"jobseeker_profile:v1:user:{request.user}"
        cache_data = cache.get(cache_key)
        
        if cache_data is not None:
            response = self.success_handle(
                msg="Jobseeker profie retrieved successfully",
                data = cache_data,
                code=status.HTTP_200_OK
            )
            cache_data= None
            
            response["x-Cache"]="HIT"
            
            return response
            
        
        try:
            jobseeker = self.get_use_case().list(
                user=request.user
            )
            
        except ValueError as error:
            raise NotFound(detail=str(error))
        
        serializer = JobseekerReadSerializer(jobseeker)
        profile_data = serializer.data
        
        try:
            cache.set(
                cache_key,
                profile_data,
                timeout= self.CACHE_TIMEOUT
            )
        
        except Exception:
            logger.warning(
                "Jobseeker profiel SET to failed",
                exc_info=True
            )
        
        
        response = self.success_handle(
            msg="Jobseeker profile retrieved successfully",
            data=profile_data,
            code = status.HTTP_200_OK
        )
        response["x-Cache"]="MISS"
        
        return response
    
        
    @extend_schema(
        request=JobSeekerSerializer,
        summary="JobSeeker Profile",
        description="Create a new jobseeker profile",
    )
    def create(self,request):
        serializer = JobSeekerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            jobseeker = self.get_use_case().create(
                user = request.user,
                data = serializer.validated_data,
            )
            response_serializer = JobSeekerSerializer(jobseeker)
            
            #invalidate cached profie after creating a company profile
            invalidate_jobseeker_profile_cache(request.user)
            
            return self.success_handle(
                msg="Jobseeker profile created successfully",
                data = response_serializer.data,
                code=status.HTTP_201_CREATED
            )

        except ValueError as error:
            raise serializers.ValidationError(str(error))
        
        except PermissionError as error:
            raise PermissionDenied(detail=str(error))
        except Exception:
            logger.exception("Failed to create jobseeker profile")
            return self.internal_server_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @extend_schema(
        request=JobseekerUpdateSerializer,
        summary="Update JobSeeker Profile",
        description="Update jobseeker's profiles"
    )
    def update(self,request):
        try:
            jobseeker = JobSeeker.objects.get(user=request.user)
            
        except JobSeeker.DoesNotExist:
                raise NotFound(
                "Jobseeker profile not found. Please create your profile first."
                )
                
                
        serializer = JobseekerUpdateSerializer(
            jobseeker,
            data=request.data,
            partial= True,
            )
        serializer.is_valid(raise_exception=True)
        
        validate_data = serializer.validated_data.copy()
        user_data = validate_data.pop("user",{})
        jobseeker_data = validate_data
        
        try:
            jobseeker = self.get_use_case().update(
                user=request.user,
                user_data=user_data,
                jobseeker_data=jobseeker_data,
            )
            response_serializer = JobseekerUpdateSerializer(jobseeker)
            
            #Invalidate cached profile to the next GET returns updated data
            invalidate_jobseeker_profile_cache(request.user)
            
            
            return self.success_handle(
                msg="Jobseeker profile updated successfully",
                data = response_serializer.data,
                code = status.HTTP_200_OK
            )
            
        except ValueError as error:
            raise NotFound(detail=str(error))
        
        except PermissionError as error:
            raise PermissionDenied(detail=str(error))
        except Exception:
            logger.exception("Failed to create jobseeker profile")
            return self.internal_server_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
            
    def destroy(self,request):
        try:
            self.get_use_case().delete(
                user=request.user
            )
            
            #Remove cached profile after deleteing the company profile
            invalidate_jobseeker_profile_cache(request.user)
            return self.delete_handle(
            msg="Jobseeker profile deleted successfully",
            code=status.HTTP_200_OK,
        )
        
        except ValueError as error:
            raise NotFound(detail=str(error))
        except PermissionError as error:
            raise PermissionDenied(detail=str(error))
        except Exception:
            logger.exception("Failed to delete jobseeker profile")
            return self.internal_server_error(status.HTTP_500_INTERNAL_SERVER_ERROR)