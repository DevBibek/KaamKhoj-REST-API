from infrastructure.users.models import JobSeeker


class JobSeekerRepository:
    def exists_by_user(self,user):
        return JobSeeker.objects.filter(user=user).exists()
    
    def exists_by_phone_number(self,phone_number):
        return JobSeeker.objects.filter(phone_number= phone_number)
    
    def save(self,jobseeker):
        return JobSeeker.objects.create(
            user= jobseeker.user,
            full_name = jobseeker.full_name,
            phone_number = jobseeker.phone_number,
            education = jobseeker.education,
            experience = jobseeker.experience,
            address = jobseeker.address,
            skills = jobseeker.skills,
            resume = jobseeker.resume,
            
        )