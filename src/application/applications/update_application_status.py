from domain.applications.update_application_rules import UpdateApplicationRules


class UpdataApplication:
    def __init__(self,application_repository):
        self.application_repository= application_repository
    
    def execute(self,user,application_id,company_user,new_status):
        application = self.application_repository.get_by_id(application_id)
        
        UpdateApplicationRules.validate(
            user=user,
            company_user=company_user,
            application=application,
            new_status=new_status,
            )
        

        application.status = new_status
        return self.application_repository.save(application)