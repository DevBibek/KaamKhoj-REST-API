from infrastructure.users.models import User


class GetMyApplication:
    def __init__(self,repository):
        self.repository = repository
    
    def execute(self,user):
        if not user:
            raise ValueError("User must be authenticated")
        
        if user.role != User.Role.JOB_SEEKER:
            raise ValueError({"detail":"only jobseekr user can see owne data"})
        
        
        return self.repository.get_my_application(user)