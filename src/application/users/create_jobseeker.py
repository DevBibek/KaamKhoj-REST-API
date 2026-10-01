from domain.users.jobseeker import JobSeeker
from infrastructure.users.models import User

class CreateJobSeeker:
    def __init__(self,repository):
        
        print("***************APPLICARION CREATE*************")
        self.repository = repository
        
    def execute(self,data,user,phone_number):
        if user.role != User.Role.JOB_SEEKER:
            raise ValueError({"detail":"Only jobseeker can create jobseeker profile"})
        
        if self.repository.exists_by_user(user):
            raise ValueError({"detail":"You have alreday jobseeker profile "})
        
        elif self.repository.exists_by_phone_number(phone_number):
            raise ValueError({"detail":"This phone number is alreday registered"})
    
        
        jobseeker = JobSeeker(
            user= user,
            full_name= data["full_name"],
            phone_number=data["phone_number"],
            address=data["address"],
            skills= data["skills"],
            education=data["education"],
            experience= data["experience"],
            resume=data.get("resume",None),
            
        )
        return self.repository.save(jobseeker)