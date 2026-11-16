import logging

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.users.create_company import CompanyProfileUseCase
from infrastructure.users.models import Company
from infrastructure.users.repository.company_repository import (
    CompanyRepository,
)
from presentation.api.common.permission import IsCompany
from presentation.api.common.responses import HandleResponseMixin
from presentation.api.user.serializers.company_serializers import (
    CompanyReadSerializer,
    CompanySerializers,
    CompanyUpdateSerializer,
    UpdateVerificatioSerializer,
)

logger = logging.getLogger("kaamkhoj")


class CompanyProfileViewSet(viewsets.ViewSet,HandleResponseMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    def get_use_case(self):
        return CompanyProfileUseCase(CompanyRepository())

    
    def list(self,request):
        try:
            company = self.get_use_case().list(
            user=request.user
            )
    
        except ValueError as e:
            raise NotFound(str(e))
        serializer = CompanyReadSerializer(company)
        
        return self.success_handle(
            msg="Company retrieved successfully",
            data=serializer.data,
            code = status.HTTP_200_OK
        )
        
    @extend_schema(
        request=CompanySerializers,
        summary="Company Profile ",
        description="Create company profile",
    )
    def create(self, request):
        serializer =CompanySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.get_use_case().create(
                user=request.user,
                data = serializer.validated_data
            )
            return self.success_handle(
                msg="Company profile created successfully",
                data=serializer.data,
                code=status.HTTP_201_CREATED
                
            )
        except PermissionError as error:
            raise PermissionDenied(str(error))
        except ValueError as error:
            raise serializers.ValidationError(str(error))
        except Exception:
            logger.exception("failed to create company profile")
            return self.internal_server_error(
                code= status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    @extend_schema(
        request=CompanyUpdateSerializer,
        summary="Company Profile",
        description="Update company profile"
        
    )
    def update(self,request):
        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
                raise NotFound(
                "Company profile not found. Please create your profile first."
                )
        serializer = CompanyUpdateSerializer(
            company,
            data=request.data,
            partial= True
            )
        
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data.copy()
        user_data = validated_data.pop("user",{})
        company_data = validated_data
        try:
            update_company = self.get_use_case().update(
                user=self.request.user,
                user_data=user_data,
                company_data=company_data
            )
            response_serializer = CompanyUpdateSerializer(update_company)
            return self.success_handle(
                msg= "Company profile update sucessfully",
                data = response_serializer.data,
                code = status.HTTP_200_OK
            )
            
        
        except ValueError as error:
            raise serializers.ValidationError(str(error))
        
        except PermissionError as error:
            raise PermissionDenied(str(error))
        
        except Exception:
            logger.exception("failed to update company profile")
            return self.internal_server_error(
                code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

        

    def destroy(self,request):
        try:
            self.get_use_case().delete(
                user=request.user
            )
            return self.delete_handle(
                msg="Company profile delete sucessfully",
                code=status.HTTP_200_OK
            )
        except ValueError as e:
            raise NotFound(str(e))
        
        except PermissionError as error:
            raise PermissionDenied(str(error))
        except Exception:
            logger.exception("failed to delete company profile ")
            return self.internal_server_error(
                code= status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
        
    


from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from application.users.update_verifacation_status import UpdateVerifiedStatus


class UpdateVerificationStatusView(APIView):
    
    permission_classes= [IsAuthenticated,IsAdminUser]
    
    def patch(self,request,id):
        serializer = UpdateVerificatioSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        
        
        company_repo = CompanyRepository()
        use_case = UpdateVerifiedStatus(company_repo=company_repo)
        
        try:
            company = use_case.execute(
                user=request.user,
                company_id=id,
                new_status=request.data.get("verification_status")
            )
        
        except PermissionError as e:
            raise PermissionDenied(detail=str(e))
        
        except ValueError as e:
            raise ValidationError(detail=str(e))
        
        except Company.DoesNotExist:
            raise NotFound("Company not found ")
        
        return Response({
            "message":"Company verification status updated suessfully",
            "company_id":id,
            "company_verification_status":company.verification_status
            
        })
        
    