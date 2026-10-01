class RefreshAccessToken:
    def __init__(self,jwt_service):
        self.jwt_service = jwt_service

    def execute(self,refresh_token):        
        access_token = self.jwt_service.refresh_token(refresh_token)
        
        return {
            "access": access_token}
        
        
            