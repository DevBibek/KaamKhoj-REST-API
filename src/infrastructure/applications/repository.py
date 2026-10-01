from .models import Application


class ApplicationRepository:
    def exists_by_user(self,user):
        return Application.objects.filter(jobseeker=user.jobseeker).exists()
    
    def get_my_application(self,user):
        return Application.objects.filter(jobseeker = user.jobseeker)
    
    
    def get_by_job(slelf,job):
        
        return Application.objects.select_related("job","job__company","job__company__user").filter(job = job)
    
    def get_by_id(self,application_id):
        return Application.objects.select_related("job","job__company","job__company__user").get(id = application_id)
    
    def save(self,application):
        return Application.objects.create(
            job = application.job,
            cover_letter = application.cover_letter,
            status = application.status,
            jobseeker = application.jobseeker
        )