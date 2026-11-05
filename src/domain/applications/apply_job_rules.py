
class ApplyJobRules:
    @staticmethod
    def validate(user,jobseeker,alreday_applied,job):
        if not user.is_active:
            raise ValueError("User must an active to apply job")
        
        if user.role != user.Role.JOB_SEEKER:
            raise PermissionError("Only Jobseeker  user can apply job")
        
        if jobseeker is None:
            raise ValueError("Befor apply job you must create jobseeker profile.")
        
        if job is None:
            raise ValueError("Not found job.")
                
        if not job.is_active:
            raise ValueError("This job is no Longer active")
        
        if alreday_applied:
            raise ValueError("you have alreday apply this job.")