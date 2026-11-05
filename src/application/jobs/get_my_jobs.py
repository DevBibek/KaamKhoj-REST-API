class GetMyJobs:
    def __init__(
        self,
        job_repository,
        company_repo):
        self.job_repository = job_repository
        self.company_repo = company_repo
        
    def execute(self,user):
        company = self.company_repo.get_by_user(user)
        
        if company is None:
            raise ValueError("Company profile not found ")
        
        return self.job_repository.list_by_company(company)