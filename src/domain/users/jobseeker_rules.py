class JobSeekerRules:
    
    @staticmethod
    def validate(user,jobseeker_exists,number_exists):
        if user.role != user.Role.JOB_SEEKER:
            raise PermissionError("Only JOBSEEKER user can create jobseeker profile")
        
        if jobseeker_exists:
            raise PermissionError("You already have a JOB_SEEKER profile")
        
        if number_exists:
            raise ValueError("This number is alreday registered")