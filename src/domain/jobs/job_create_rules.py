from infrastructure.users.models import User

class JobManageRules:
    @staticmethod
    def validate_create(user,company):
        if user.role != User.Role.COMPANY:
            raise PermissionError('Only company user can create job.')
        
        if company is None:
            raise ValueError("Company profile is required  befor create job")
        
        if company.verification_status != "VERIFIED":
            raise PermissionError("Company must be verified before posting jobs")
        
    @staticmethod
    def validate_owner(user,job):
        if user.role != User.Role.COMPANY:
            raise PermissionError("Only authenticated user can update own job")
        
        if job is None:
            raise ValueError("Job not found.")
        
        if job.company.user.id != user.id :
            raise PermissionError("You do not permission to access other job.")