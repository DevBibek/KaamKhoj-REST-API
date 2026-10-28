from domain.users.company_rules import CompanyRules


class CreateCompany:
    def __init__(self, company_repo):
        self.company_repo = company_repo
        
    def gets_company(self,user):
        return self.company_repo.list_by_user(user)

    def create(self,user,**data):
        
        company_exists =  self.company_repo.exists_by_user(user)
        
        #apply business rules
        CompanyRules.validate(
        user=user,
        company_exists=company_exists
        )
        
        return self.company_repo.create(user= user,**data)
        
    
        
        