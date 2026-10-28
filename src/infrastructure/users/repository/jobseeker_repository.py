from infrastructure.users.models import JobSeeker


class JobSeekerRepository:
    
    def exists_by_user(self,user):
            return JobSeeker.objects.filter(user=user).exists()
    
    def list_by_user(self,user):
        return JobSeeker.objects.filter(user=user)
    
    
    def get_by_user(self,user):
        return JobSeeker.objects.filter(user=user).first()
    
    def exists_by_phone_number(self,phone_number):
        return JobSeeker.objects.filter(phone_number= phone_number).exists()
    
    def create(self,user,**data):
        return JobSeeker.objects.create(user= user,**data)