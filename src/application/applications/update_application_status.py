
class UpdataApplication:
    def __init__(self,application_repository):
        self.application_repository= application_repository
    
    def execute(self,application_id,company_user,new_status):
        application = self.application_repository.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")
    
        
        if application.job.company.user != company_user:
            raise PermissionError("You can not update this application")
        
        
        allowed_status = {
            "PENDING":["REVIEWING"],
            "REVIEWING":["ACCEPETED","REJECTED"],
            "ACCEPETED":[],
            "REJECTED":[],

        }
        current_status = application.status
        
        if new_status not in allowed_status[current_status]:
            raise ValueError(f"You can not change status from"
                            f"{current_status} to {new_status}")
            
        application.status = new_status
        application.save(update_fields = ["status"])
        
        return application
            
    
        