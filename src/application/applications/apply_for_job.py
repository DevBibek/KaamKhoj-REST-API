from domain.applications.applications import Application
from infrastructure.users.models import JobSeeker, User


class ApplyForJob:
    def __init__(self,repository):
        self.repository = repository
        
    
    def execute(self,data,user):
        if not user.is_active:
            raise ValueError("User must be an active to apply job!")
        
        if user.role!= User.Role.JOB_SEEKER:
            raise PermissionError({"details":"Only jobseeker can applay job "})
        
        jobseeker_user = JobSeeker.objects.filter(user = user)
        if not jobseeker_user:
            raise ValueError({"details":"Before applay job you must create jobseeker profile"})
        
        elif self.repository.exists_by_user(user):
            raise PermissionError({"details":"You have already applied this job!"})
        
        application = Application(
            job=data.get("job"),
            cover_letter= data.get("cover_letter"),
            status= data.get("status","pending"),
            jobseeker = user.jobseeker
        )
        
        return self.repository.save(application)
        
    