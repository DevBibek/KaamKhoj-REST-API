from infrastructure.jobs.models import Job

class GetJobApplication:
    def __init__(
        self,
        application_repository,
        job_repository
        ):
        
        self.application_repository = application_repository
        self.job_repository = job_repository
        
        
        
    def execute(self,user,job_id,):
        
        #find the requesed job
        job = self.job_repository.get_by_id(job_id)
        
        # if job dosesnt exits
        if not job:
            raise ValueError(f"{job_id} Job not found !")
        
        
        # Check that logged-in user owns this jobs.
        if job.company.user != user:
            raise PermissionError("You do not have permission to view these application.")
            
        
        # get all applciations for job
        applications = self.application_repository.get_by_job(job)
        
        
        return applications
        
    