from rest_framework import serializers, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.users.create_company import CreateCompany
from infrastructure.users.repository.company_repository import CompanyRepository
from presentation.api.common.permission import IsCompany
from presentation.api.user.serializers.company_serializers import (
    CompanySerializers,
    UpdateVerificatioSerializer,
)


class CompanyProfileViewAPI(viewsets.ModelViewSet):
    erializer_class = CompanySerializers
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]
    
    def get_company(self):
        company_repo = CompanyRepository()
        return CreateCompany(company_repo=company_repo)
    
    def get_queryset(self):
        use_case = self.get_company()
        
        return use_case.gets_company(user=self.request.user) 
    
    
    def create(self, request, *args, **kwargs):
        use_case = self.get_company()
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception = True)
        data = serializer.validated_data

        try:
            company = use_case.create(
                user = self.request.user,
                **data
                )
        except PermissionError as e:
            raise PermissionDenied(str(e))
        

        except ValueError as e:
            raise serializers.ValidationError(str(e))
        response_serializer = self.get_serializer(company)
        
        
        return Response(
        response_serializer.data,
        status=status.HTTP_201_CREATED
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
            raise serializers.ValidationError(detail=str(e))
        
        
        
        return Response({
            "message":"Company verification status updated suessfully",
            "company_id":id,
            "company_verification_status":company.verification_status
            
        })
        