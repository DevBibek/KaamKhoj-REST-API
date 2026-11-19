import hashlib
import logging
from urllib.parse import urlencode

from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

# from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.jobs.services import ManageCompanyJobs
from infrastructure.cache.job_cache import invalidate_jobs_cache
from infrastructure.jobs.repositories import JobRepository
from infrastructure.users.repository.company_repository import CompanyRepository
from presentation.api.common.permission import IsCompany, IsJob
from presentation.api.common.responses import HandleResponseMixin
from presentation.api.jobs.serializers import JobSerializer

logger = logging.getLogger("kaamkhoj")



class CompanyCreateJobAPI(viewsets.ViewSet,HandleResponseMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsJob,IsAuthenticated]
    
    def get_use_case(self):
        job_repo = JobRepository()
        company_repo = CompanyRepository()
            
        return ManageCompanyJobs(
        job_repo=job_repo,
        company_repo=company_repo
        )
            
    def list(self,request):
        try:
            job = self.get_use_case().get_jobs(
                user=request.user
            )
            
            serializer = JobSerializer(job,many=True)
            return self.success_handle(
                msg="Company Job retrived successfully",
                data = serializer.data,
                code=status.HTTP_200_OK
            )
        except ValueError as e:
            raise NotFound(detail=str(e))
        
        
    # Document the required request fields and job creation behavior in Swagger.
    @extend_schema(
        request=JobSerializer,
        summary="Create Jobs",
        description=(
        "Create a job under the authenticated company."
        "Only authorized companies can create jobs.")

    )
    def create(self,request):
        serializer = JobSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.get_use_case().create(
                user=request.user,
                data=serializer.validated_data
                )
            
            # Remove stale public job listings after a successful job creation.
            invalidate_jobs_cache()
            
            return self.success_handle(
                msg="Job created successfully",
                data=serializer.data,
                code = status.HTTP_201_CREATED
            )
        except ValueError as error:
            raise serializers.ValidationError(detail=str(error))
        
        except PermissionError as error:
            raise PermissionDenied(detail=str(error))
        
        except Exception:
            logger.exception("Failed to create job.")
            return self.internal_server_error(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def retrieve(self,request,pk):
        try:
            job =self.get_use_case().get_by_id(
                user=request.user,
                pk=pk
            )
            
            serializer = JobSerializer(job)
            return self.success_handle(
                msg="Job retrieve successfully",
                data = serializer.data,
                code = status.HTTP_200_OK
            )
            
        except ValueError as error:
            raise NotFound(detail=str(error))
        
        except PermissionError as error:
            raise PermissionDenied(detail=str(error))
        
        except Exception:
            logger.exception("Filed to retrive  job.")
            return self.internal_server_error(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    # Document the required request fields and job creation behavior in Swagger.
    @extend_schema(
        responses=JobSerializer,
        summary="Update Job",
        description="Update jobs under the authenticated and own company"
    )
    def update(self,request,pk):
        serializer = JobSerializer(data =request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            updated_job = self.get_use_case().update(
                pk=pk,
                user= request.user,
                data=serializer.validated_data
            )
            
            # Remove stale public job listings after a successful job update.
            invalidate_jobs_cache()
            
            response_serializer = JobSerializer(updated_job)
                    
            return self.success_handle(
                msg="Job updated successfully",
                data = response_serializer.data,
                code = status.HTTP_200_OK
            )
        
        except ValueError as error:
            raise NotFound(detail=str(error))
        
        except PermissionError as error:
            raise PermissionDenied(detail=str(error))
        
        except Exception:
            logger.exception("Filed to update job.")
            return self.internal_server_error(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self,request,pk):
        try:
            self.get_use_case().delete(
                user=request.user,
                pk=pk
                )
            
            # Remove stale public job listings after a successful job delete.
            invalidate_jobs_cache()
            
            return self.delete_handle(
                msg="Job delete successfully",
                code = status.HTTP_204_NO_CONTENT
            )
        except ValueError as error:
            raise NotFound(detail=str(error))
        
        except PermissionError as error:
            raise PermissionDenied(detail=str(error))
        
        except Exception:
            logger.exception("Filed to delete job")
            return self.internal_server_error(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
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
    throttle_scope = "public_job"
    pagination_class= CustomPagination
    CACHE_TIMEOUT = 90
    def get(self,request):
        # Create unique cache key
        
        query_params = sorted(request.query_params.lists())
        query_string = urlencode(query_params,doseq=True)
        request_path = f"{request.path}?{query_string}"
        
        hashed_path = hashlib.sha256(
            request_path.encode()
        ).hexdigest()
        
        cache_key = f"public_jobs:v1:{hashed_path}"
        
        #check redis cache
        
        try:
            cache_data = cache.get(cache_key)
        except Exception:
            logger.warning(
                "Redis cache GET failed",
                exc_info= True
            )
            cache_data = None
            
            
        # cache HIT
        if cache_data is not None:
            response = Response(cache_data)
            response["X-Cache"] ="HIT"
            return response
        
        # Cache MISS - Get form database
        
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
            
        # Apply pagination
        paginator = self.pagination_class()
        
        paginator.message = "Jobs retrieved successfully."
        page = paginator.paginate_queryset(jobs,request,)
        
        #Serializer data
        serializer = JobSerializer(
            page,
            many= True
            )
        
        response = paginator.get_paginated_response(serializer.data)
        
        
        #Save response in redis
        
        try:
            cache.set(
                cache_key,
                response.data,
                timeout=self.CACHE_TIMEOUT
            )
        
        except Exception:
            logger.warning(
                "Redis cache SET failed"    ,
                exc_info= True
            )
        response["X-Cache"] = "MISS"
        
        return response
        
        