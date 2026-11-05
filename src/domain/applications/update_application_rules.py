from rest_framework.exceptions import NotFound

from infrastructure.users.models import User


class UpdateApplicationRules:
    @staticmethod
    def validate(user,company_user,application,new_status):
        
        if user.role != User.Role.COMPANY:
            raise PermissionError("Only company user can change there owen status")
        
        if application is None:
            raise NotFound("Application not found.")
        
        if application.job.company.user!= company_user:
            raise PermissionError("You cant not update other job application.")
        
        
            
        current_status= application.status
        
        
        allowed_status = {
                    "PENDING":["REVIEWING"],
                    "REVIEWING":["ACCEPTED","REJECTED"],
                    "ACCEPTED":[],
                    "REJECTED":[],
                    }
                
        if new_status not in allowed_status[current_status]:
            raise ValueError(f"You can not change status from {current_status} to {new_status}")