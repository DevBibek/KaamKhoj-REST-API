class GetMyJobs:
    def __init__(self,job_repository):
        self.job_repository = job_repository
        
    def execute(self,user):
        company = user.company
        
        return self.job_repository.get_by_company(company)