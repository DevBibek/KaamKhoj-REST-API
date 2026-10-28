from domain.applications.apply_job_rules import ApplyJobRules


class ApplyForJob:
    def __init__(
        self,
        application_repo,
        job_repo,
        jobseeker_repo
        ):
        self.application_repo = application_repo
        self.job_repo = job_repo
        self.jobseeker_repo =jobseeker_repo
        
        
    def execute(self,user,**data,):
        job =data.get("job")
        
        jobseeker = self.jobseeker_repo.get_by_user(user)
        
        alreday_applied = self.application_repo.has_alreday_applied(jobseeker,job)
        
        #apply business rules
        ApplyJobRules.validate(
            user=user,
            jobseeker=jobseeker,
            alreday_applied=alreday_applied,
            job=job,
        )
        
        return self.application_repo.create(
            jobseeker=jobseeker,
            **data)
        
    