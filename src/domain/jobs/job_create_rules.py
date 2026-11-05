

class Createjob:
    def validate(user,company):
        
        if user.role != user.Role.COMPANY:
            raise PermissionError('only company user can create job.')
        
        if company is None:
            raise PermissionError("Company profile is required  befor create job")
                
                
        
        if company.verification_status != "VERIFIED":
            raise PermissionError("Company must be verified before posting jobs")
        
        

