from domain.jobs.job_create_rules import Createjob


class ManageCompanyJobs:
    def __init__(
        self,
        job_repo,
        company_repo):
        
        self.job_repo = job_repo
        self.company_repo = company_repo
        
        
    def get_jobs(self,company):
        return self.job_repo.list_by_company(company)
        

    def create(self,user,**data):
        company = self.company_repo.get_by_user(user)
        
        #apply busines rules.
        Createjob.validate(
        user = user,
        company=company
        )
        return self.job_repo.create(company,**data)
        
        
        
        