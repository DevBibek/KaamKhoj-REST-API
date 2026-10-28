class GetPublicJobs:
    def __init__(self,job_repo):
        self.job_repo = job_repo
    
    def execute(
        self,
        search=None,
        location=None,
        min_salary=None,
        max_salary=None,
        ordering=None,
                ):
        
        return self.job_repo.get_public_jobs(
            search=search,
            location=location,
            min_salary=min_salary,
            max_salary=max_salary,
            ordering=ordering
        )