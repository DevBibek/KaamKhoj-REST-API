from .models import Job as JobModel


class JobRepository:
    def get_by_company(self,company):
            return JobModel.objects.select_related("company","company").filter(company = company).order_by("created_at")
    
    def get_by_id(self,job_id):
        try:
            return JobModel.objects.select_related("company","company__user").get(id = job_id)
        
        except JobModel.DoesNotExist:
            return None
        
        
    def create(self,job):
        print("++++++++++++ Job Repositry running ====================")
        return JobModel.objects.create(
            title = job.title,
            description = job.description,
            salary = job.salary,
            location = job.location,
            company= job.company
            )
        