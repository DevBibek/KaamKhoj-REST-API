from rest_framework_simplejwt.tokens import RefreshToken


class TokenBlacklistService:
    def blacklist_token(self,refresh_token):
        token = RefreshToken(refresh_token)
        return token.blacklist()