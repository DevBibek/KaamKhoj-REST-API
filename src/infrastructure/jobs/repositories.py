from django.db.models import Q

from .models import Job as JobModel


class JobRepository:
    #Public API :return active jobs from verified companys
    def get_public_jobs(
        self,
        search=None,
        location =  None,
        min_salary = None,
        max_salary = None,
        ordering=None,
        
    ):
        #filter jobs
        queryset = JobModel.objects.filter(
            is_active= True,
            company__verification_status = "VERIFIED"
            ).select_related("company") 
            

        if search and search.strip():
        # for remove space and slace'/'
            clean_search = search.strip().rstrip('/')
            queryset= queryset.filter(
                Q(title__icontains = clean_search)
                |Q(description__icontains= clean_search)
            )
            
        if location :
            queryset = queryset.filter(
                Q(location__icontains = location)
            )
            
        if  min_salary is not None:
            queryset = queryset.filter(
                salary__gte = min_salary
            )
        
        if max_salary is not None:
            queryset = queryset.filter(
                salary__lte = max_salary
            )
    
        # only Allow supported ordering opcation
        
        allowed_ordering = {
        "newset":"-created_at",
        "oldset":"created_at",
        "salary_low":"salary",
        "salary_high":"-salary"
    }
    
        order_by = allowed_ordering.get(
            ordering,
            "-created_at")
        return queryset.order_by(order_by)
            
            
            
            
    def list_by_company(self,company):
            return JobModel.objects.select_related("company").filter(company = company).order_by("-created_at")
        
    
    
    def get_by_id(self,pk):
        try:
            return JobModel.objects.select_related("company","company__user").get(pk =pk)
        except JobModel.DoesNotExist:
            return None
        
    def create(self,company,**data):
        return JobModel.objects.create(
            company = company,**data
            )
                
                
    def update(self,user,job,**data):
        for field ,value in data.items():
            setattr(job,field,value)
            
        job.save()
        
        return job

    
    
    def delete(self,job):
        return job.delete()