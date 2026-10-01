

class LoginUser:
    def __init__(self,user_repository,jwt_service,password_service):
        self.user_repository = user_repository
        self.jwt_service = jwt_service
        self.password_service =password_service
        
        
    def execute(self,email,password):
        user = self.user_repository.get_by_email(email)
        
        if not user:
            raise ValueError("Invalid eamil or password")
        
        authenticated_user = self.password_service.authenticate(
            email = email,
            password = password
        )
        
        if not authenticated_user:
            raise ValueError("Invalid email or password")
        
        
        tokens = self.jwt_service.generate_tokens(
            authenticated_user
            
        )
        return {
            "user":authenticated_user,
            "tokens":tokens
        }