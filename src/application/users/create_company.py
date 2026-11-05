from rest_framework.exceptions import NotFound

from domain.users.company_rules import CompanyRules


class CompanyProfileUseCase:

    def __init__(self, company_repo):
        self.company_repo = company_repo
        self.company= None
    
    def load_company(self,user):
        if self.company is None:
            self.company = self.company_repo.get_by_user(user)
            
        return self.company
        
    def list(self,user):
        company = self.company_repo.get_by_company(user)
        if not company:
            raise NotFound("Company profile not found. Please create your profile first.")
        
        return company

    def create(self, user,data):
        company = self.load_company(user=user)
    
        CompanyRules.validate_create(
            user,
            profile_exists = (company is not None),
            phone_exists=self.company_repo.exists_by_phone(data["phone"])
        )
        return self.company_repo.create(user, **data)

    def update(self, user,user_data,company_data):
        company = self.load_company(user)
        
        CompanyRules.validate_owner(
            user, 
            company,
            
            )
        return self.company_repo.update(company,user_data,company_data)

    def delete(self, user):
        company = self.load_company(user)
        CompanyRules.validate_delete(user, company)
        self.company_repo.delete(company)






