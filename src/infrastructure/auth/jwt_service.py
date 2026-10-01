from rest_framework_simplejwt.tokens import RefreshToken


class JWTService:
    def generate_tokens(self,user):
        refresh = RefreshToken.for_user(user)
        return{
            "refresh":str(refresh),
            "access":str(refresh.access_token)
            }
    
    def refresh_token(self,refresh_token):
        refresh= RefreshToken(refresh_token)
        return str(refresh.access_token)