
from .models import Application


class ApplicationRepository:
    #check user profile
    
    #check already apply user
    def has_alreday_applied(self,jobseeker,job):
        return Application.objects.filter(
            jobseeker=jobseeker,
            job=job).exists()
    
    def get_my_application(self,user):
        return Application.objects.filter(jobseeker = user.jobseeker)
    
    
    def get_by_job(self,job):
        
        return Application.objects.select_related("job","job__company","job__company__user").filter(job = job)
    
    def get_by_id(self,application_id):
        return Application.objects.select_related("job","job__company","job__company__user").filter(id = application_id).first()
    
    
    def create(self,jobseeker,**data):
        return Application.objects.create(jobseeker=jobseeker ,**data)
    
    
    
    def save(self,application):
        application.save(
            update_fields=["status"]
        )
        return application
