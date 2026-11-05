from infrastructure.users.models import User


class GetMyApplication:
    def __init__(self,repository):
        self.repository = repository
    
    def execute(self,user):
        if user is None:
            raise ValueError("User not found.")
        
        if user.role != User.Role.JOB_SEEKER:
            raise PermissionError({"detail":"only authenticated jobseekr user can see data"})
        
    
        return self.repository.get_my_application(user)
        
    