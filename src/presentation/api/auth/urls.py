from django.urls import path

from .views import (
    LoginAPIView,
    LoginJWT,
    RefreshTokenAPI,
    UserDeatilesApi,
    UserListCreateAPi,
    LogoutJWTAPI
)

urlpatterns =  [
    path("register-api/",UserListCreateAPi.as_view(),name="register-api"),
    path("register-api/<int:pk>/",UserDeatilesApi.as_view(),name="register-api"),
    # path("login/",LoginJWT.as_view(),name="login"),
    path("login/",LoginAPIView.as_view(),name="login"),
    path("refresh-token/",RefreshTokenAPI.as_view(),name="refresh token"),
    path("logout/",LogoutJWTAPI.as_view(),name="logout_user")
    
    
]
