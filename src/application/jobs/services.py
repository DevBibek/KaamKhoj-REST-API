from domain.jobs.job_create_rules import JobManageRules


class ManageCompanyJobs:
    def __init__(
        self,
        job_repo,
        company_repo):
        
        self.job_repo = job_repo
        self.company_repo = company_repo
        
        
    def get_jobs(self,user):
        company = self.company_repo.get_by_user(user)
        if company is None:
            raise ValueError("Company not found.")
        
        return self.job_repo.list_by_company(company)
        

    def create(self,user,data):
        company = self.company_repo.get_by_user(user)
        
        #apply busines rules.
        JobManageRules.validate_create(
        user = user,
        company=company
        )
        return self.job_repo.create(company,**data)
    
    def get_by_id(self,user,pk):
        job = self.job_repo.get_by_id(pk=pk)
        
        JobManageRules.validate_owner(
            user=user,
            job=job,
            )
        return job
        
    def update(self,pk,user,data):
        job = self.job_repo.get_by_id(pk)
        
        JobManageRules.validate_owner(
            user=user,
            job=job,
            )
        return self.job_repo.update(user,job,**data)
        
            
    def delete(self,user,pk):
        job = self.job_repo.get_by_id(pk=pk)
        JobManageRules.validate_owner(
            user=user,
            job=job
        )
        return self.job_repo.delete(job)