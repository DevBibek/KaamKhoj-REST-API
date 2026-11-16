import logging

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed,
    ExpiredTokenError,
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.tokens import RefreshToken

from application.auth.login_user import LoginUser
from application.auth.register_user import RegisterUserUseCase
from infrastructure.auth.jwt_service import JWTService
from infrastructure.auth.password_service import PasswordService
from infrastructure.users.models import User
from infrastructure.users.repository.user_repository import UserRepository
from presentation.api.common.responses import HandleResponseMixin

from .serializer import LoginSerializer, RegisterSerializer

logger = logging.getLogger("kaamkhoj")


class UserRegisterationAPIView(APIView,HandleResponseMixin):
    throttle_scope = "register"
    def get(self,request):
        user = User.objects.all()
        serializer = RegisterSerializer(user,many= True)
        return self.success_handle(
            msg="User data retrived successfully",
            data = serializer.data,
            code= status.HTTP_200_OK
        )
    @extend_schema(
        request=RegisterSerializer,
        responses={201, RegisterSerializer},
        summary="Register User",
        description="Create a new user account."
    )
    
    def post(self,request): 
        serializer = RegisterSerializer(data = request.data)
        if not serializer.is_valid():
            return self.error_handle(
                msg= "invalid input data provied",
                error= serializer.errors,
                code=status.HTTP_400_BAD_REQUEST
                )
                
        try:
                user_repo = UserRepository()
                use_case = RegisterUserUseCase(user_repo)
                user = use_case.execute(serializer.validated_data)
                response_serializer = RegisterSerializer(user)
                return self.success_handle(
                    msg="User registered successfully",
                    data= response_serializer.data,
                    code= status.HTTP_201_CREATED,
                )
    
        except Exception:
                logger.exception("Failed to register user")
                return self.internal_server_error(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from presentation.api.common.permission import IsOwner

from .serializer import UserProfileUpdateSerializer


class MyUserDetailsAPIView(APIView,HandleResponseMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get(self,request,pk):
        user_repo = UserRepository()
        use_case = RegisterUserUseCase(user_repo=user_repo)
        try:
            user = use_case.get_user_by_id(
                pk=pk,
                user = request.user
            )
            serializer = RegisterSerializer(user)
            
            return self.success_handle(
                msg="User retrived successfully",
                data=serializer.data,
                code= status.HTTP_200_OK
                )
        except NotFound as e:
            return self.not_found(
                msg=str(e),
                code= status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            raise serializers.ValidationError(detail=str(e))
        
        
        
        except Exception:
            logger.exception("Failed to retrive User data")
            return self.internal_server_error(
            code= status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        

    
    def patch(self,request,pk):
        try:
            serializer = UserProfileUpdateSerializer(
                request.user,
                data = request.data,
                partial= True) #PATCH can update only somefields 
            
            if serializer.is_valid():
                user_repo = UserRepository()
                use_case = RegisterUserUseCase(user_repo=user_repo)
                try:
                    use_case.update_user(
                    pk=pk,
                    user= request.user,
                    data= serializer.validated_data
                    )
                    return self.success_handle(
                        msg="User data updated successfully",
                        data=serializer.data,
                        code = status.HTTP_200_OK
                    )
                except ValueError as e:
                    raise serializers.ValidationError(detail=str(e))
                
                except serializers.ValidationError as e:
                    return self.error_handle(
                        msg= "Validation failed",
                        error= str(e),
                        code= status.HTTP_400_BAD_REQUEST
                    )
                    
                except NotFound as e:
                    return self.not_found(
                    msg= str(e),
                    code= status.HTTP_404_NOT_FOUND
                    )
                    
            return self.error_handle(
                msg="Validation failed",
                error= serializer.errors,
                code = status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
                return self.not_found(
                msg=f"User with id {pk} dosnt exist!!",
                code= status.HTTP_404_NOT_FOUND
                    )
        except Exception:
                logger.exception("Failed to update user data")
                return self.internal_server_error(
                code= status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            
    
    def delete(self,request,pk):
        user_repo = UserRepository()
        use_case = RegisterUserUseCase(user_repo=user_repo)
        try:
            use_case.delete_user(
            pk=pk,
            user=request.user
            )
            return self.success_handle(
                msg="User delete sucessfully",
                data= None,
                code= status.HTTP_200_OK
            )
        
        except  NotFound as e:
            return self.not_found(
                msg=str(e),
                code= status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
                return self.not_found(
                msg=f"User with id {pk} dosnt exist!!",
                code= status.HTTP_404_NOT_FOUND
                )
        except Exception:
            logger.exception("Failed to delete User data")
            return self.internal_server_error(
            code= status.HTTP_500_INTERNAL_SERVER_ERROR
                    )     
            
            
            
            
            
class LoginJWT(APIView):
    
    
    @staticmethod
    def get_tokens_for_user(user):
        if not user.is_active:
            raise AuthenticationFailed("User is not activate")
        
        refresh = RefreshToken.for_user(user)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token),
        }
    
    def post(self,request):
        try:
            serializer = LoginSerializer(data= request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]
                user = authenticate(request,email = email,password = password)
                if user is not None:
                    tokens = self.get_tokens_for_user(user)
                    response = Response({
                        "message":"User login successfully",
                        "access_token":tokens["access"]
                    })
                    response.set_cookie(
                        key = "refresh_token",
                        value = tokens["refresh"],
                        httponly= True, #prevents js from accessing the refresh token(xss protection)
                        secure = True, ##cookie only sent over https(For productionb always set True)
                        samesite="lax",
                        max_age=60*60*24*7
                    )
                    return response
                return Response({"message":"Invalid email or password !!"},status= status.HTTP_401_UNAUTHORIZED)
            return Response({"message":"Invalid creadentials",
                            "error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                
        
        except Exception:
            logger.exception("Failed to login")
            return Response({"message":"interanl server error"},
            status= status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
            
class LoginAPIView(APIView):
    throttle_scope = "login"
    @extend_schema(
        request=LoginSerializer,
        summary="User Login",
        description="Authenticate user using email and password.",
    )
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        repository = UserRepository()
        
        password_service = PasswordService()
        jwt_service = JWTService()
        
        login_user = LoginUser(
            user_repository=repository,
            password_service= password_service,
            jwt_service= jwt_service
        )
        try:
            result = login_user.execute(
                email=data["email"],
                password=data["password"]
            )
        
        except ValueError as error:
            return Response({
                "detail":str(error)
            },status=status.HTTP_401_UNAUTHORIZED)
        
        user =result["user"]
        tokens = result["tokens"]
        response = Response({
            "message":"User login successful",
            "Access_tokens":tokens["access"],
            "user":{
                "user":user.id,
                "username":user.username,
                "email":user.email,
                "role":user.role
            },
        },status=status.HTTP_200_OK)
            
        response.set_cookie(
            key="refresh_token",
            value= tokens["refresh"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60*60*24*7
        )
        return response

from application.auth.refresh_access_token import RefreshAccessToken


class RefreshTokenAPI(APIView):
    
    throttle_scope = "refresh"
    
    @extend_schema(
        request=None,
        summary="Refresh Access Token",
        description="Generate new access token using the refresh token store in the cookie"
    )
    def post(self,request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({
                "detail":"Refresh token not found"
            },status=status.HTTP_401_UNAUTHORIZED)
            
        jwt_service = JWTService()
        refresh_access_token = RefreshAccessToken(jwt_service=jwt_service)
        try:
            tokens = refresh_access_token.execute(
            refresh_token=refresh_token
            
            )
        
        except ValueError as error:
            return Response({
                "detail": str(error)
            },status=status.HTTP_401_UNAUTHORIZED)
            
        return Response({
            "message":"New access tokens generated successfully",
            "Tokens":tokens
        },status=status.HTTP_200_OK)
        
        
from application.auth.logout import LogoutUser
from infrastructure.auth.token_blacklist import TokenBlacklistService


class LogoutJWTAPI(APIView):
    @extend_schema(
        request=None,
        summary="User Logout",
        description="Logout useing refresh token store in the cookie"
    )
    def post(self,request):
        
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({
                "message":"Refresh token not found in cookies"
                },status=status.HTTP_401_UNAUTHORIZED)
            
        token_blacklist = TokenBlacklistService()
        logut_user = LogoutUser(blacklist_token=token_blacklist)
        
        try:
            logut_user.execute(refresh_token= refresh_token)
        
        except (TokenError,InvalidToken) as e:
            return Response({"message":"Invalid or Expired token",
                    "error": str(e)},status=status.HTTP_401_UNAUTHORIZED)
            
        response =Response({
            "message":"User logged out successfully",
        },status=status.HTTP_200_OK)
        
        response.delete_cookie("refresh_token")
        return response