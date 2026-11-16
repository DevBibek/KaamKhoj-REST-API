from django.urls import path

from .views import (
    LoginAPIView,
    LogoutJWTAPI,
    MyUserDetailsAPIView,
    RefreshTokenAPI,
    UserRegisterationAPIView,
)

urlpatterns =  [
    path("auth/register/",UserRegisterationAPIView.as_view(),name="users-register"),
    path("users/me/<int:pk>/",MyUserDetailsAPIView.as_view(),name="my-user-details"),
    # path("login/",LoginJWT.as_view(),name="login"),
    path("auth/login/",LoginAPIView.as_view(),name="user-login"),
    path("refresh/token/",RefreshTokenAPI.as_view(),name="refresh-token"),
    path("auth/logout/",LogoutJWTAPI.as_view(),name="logout_user")
    
    
]
