class JobSeekerRules:
    
    @staticmethod
    def validate_create(user,jobseeker_exists,number_exists):
        if user.role != user.Role.JOB_SEEKER:
            raise PermissionError("Only jobseeker user can create jobseeker profile")
        
        if jobseeker_exists:
            raise ValueError("You already have a jobseeker profile")
        
        if number_exists:
            raise ValueError("This number is alreday registered")
        

    @staticmethod
    def validate_owner(user,jobseeker):
        if user.role != user.Role.JOB_SEEKER:
            raise PermissionError("Only jobseeker user can create jobseeker profile")
    
        if not jobseeker:
            raise ValueError("Jobseeker profile not found. Plese create your profile first.")
        
        
        if jobseeker.user_id != user.id:
            raise PermissionError("You cannot manage another jobseeker's profile")
        
    @staticmethod
    def validate_delete(user,jobseeker):
        if not jobseeker:
            raise ValueError("Jobseeker profile not found. Plese create your profile first.")
        
        
        admin_user = user.is_superuser
        owner_user = (
            user.role == user.Role.JOB_SEEKER and 
            jobseeker.user_id == user.id
            )
        
        if not(admin_user or owner_user):
            raise PermissionError("You cannot delete this  jobseeker's profile")
            
        