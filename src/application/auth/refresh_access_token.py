from rest_framework_simplejwt.exceptions import ExpiredTokenError, TokenError


class RefreshAccessToken:
    def __init__(self,jwt_service):
        self.jwt_service = jwt_service

    def execute(self,refresh_token):   
        try:     
            access_token = self.jwt_service.refresh_token(refresh_token)
            
            return {
                "access": access_token}
        
        except (ExpiredTokenError,TokenError):
            raise ValueError("Your refresh token has expired. Please log in again. ")
        
        