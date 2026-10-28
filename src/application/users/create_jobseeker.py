from domain.users.jobseeker_rules import JobSeekerRules
class CreateJobSeeker:
    def __init__(self,jobseeker_repo):
        
        self.jobseeker_repo= jobseeker_repo
        
    def gets_jobseeker(self,user):
        return self.jobseeker_repo.list_by_user(user)
        
    def create(self,user,**data):
        
        jobseeker_exists = self.jobseeker_repo.exists_by_user(user)
        phone_number = data.get("phone_number")
        
        number_exists = self.jobseeker_repo.exists_by_phone_number(phone_number)
        #apply business rules
        JobSeekerRules.validate(
            user=user,
            jobseeker_exists= jobseeker_exists,
            number_exists=number_exists )
        
        
        return self.jobseeker_repo.create(
            user=user,
            **data
            )