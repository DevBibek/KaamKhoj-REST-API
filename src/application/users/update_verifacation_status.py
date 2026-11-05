from domain.users.update_verification_rules import UpdateVerificationRules


class UpdateVerifiedStatus:
    def __init__(
        self,
        company_repo
    ):
        self.company_repo = company_repo
        
        
        
    def execute(self,user,company_id,new_status):
        company = self.company_repo.get_by_id(company_id)
        
        UpdateVerificationRules.validate(
            user=user,
            company=company,
            new_status=new_status,
        )
        company.verification_status = new_status
        
        return self.company_repo.save(company)
