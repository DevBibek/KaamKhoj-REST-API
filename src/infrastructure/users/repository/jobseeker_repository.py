from infrastructure.users.models import JobSeeker
from django.db import transaction

class JobSeekerRepository:
    
    def exists_by_user(self,user):
            return JobSeeker.objects.filter(user=user).exists()
    
    def get_by_user(self,user):
        return JobSeeker.objects.filter(user=user).select_related("user").first()
    
    def exists_by_phone_number(self,phone_number):
        return JobSeeker.objects.filter(phone_number= phone_number).exists()
    
    def create(self,user,**data):
        return JobSeeker.objects.create(user= user,**data)
    
    
    def update(self,jobseeker,user_data,jobseeker_data):
        with transaction.atomic():
            user = jobseeker.user
            
            for field ,value in user_data.items():
                setattr(user,field,value)
                
                if user_data:
                    user.save()
                    
                    
            for field ,value in jobseeker_data.items():
                setattr(jobseeker,field,value)
                if jobseeker_data:
                    jobseeker.save()
            
        return jobseeker
    
    def delete(self,jobseeker):
        return jobseeker.delete()