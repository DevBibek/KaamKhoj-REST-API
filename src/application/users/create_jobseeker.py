from domain.users.jobseeker_rules import JobSeekerRules
class CreateJobSeeker:
    def __init__(self,jobseeker_repo):
        
        self.jobseeker_repo= jobseeker_repo
        self.jobseeker = None
        
    def load_jobseeker(self,user):
        if self.jobseeker is None:
            self.jobseeker = self.jobseeker_repo.get_by_user(user)
        return self.jobseeker
    
    
    def list(self,user):
        jobseeker = self.jobseeker_repo.get_by_user(user)
        if not jobseeker:
            raise ValueError("Jobseeker profile not found. Please create your profile first.")
        
        return jobseeker
        
    def create(self,user,data):
        jobseeker = self.load_jobseeker(user)
    
        phone_number = data.get("phone_number")
        
        number_exists = self.jobseeker_repo.exists_by_phone_number(phone_number)
        #apply business rules
        JobSeekerRules.validate_create(
            user=user,
            jobseeker_exists= (jobseeker is not None),
            number_exists=number_exists
            )
        
        return self.jobseeker_repo.create(
            user=user,
            **data
            )
    
    def update(self,user,user_data,jobseeker_data):
        jobseeker = self.load_jobseeker(user)
        JobSeekerRules.validate_owner(
            user,
            jobseeker
        )
        return self.jobseeker_repo.update(jobseeker,user_data,jobseeker_data)
        
    
    
    def delete(self,user):
        jobseeker = self.load_jobseeker(user)
        JobSeekerRules.validate_delete(
            user,
            jobseeker
        )
        
        return self.jobseeker_repo.delete(jobseeker)