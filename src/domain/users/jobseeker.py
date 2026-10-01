class JobSeeker:
    def __init__(
        self,
        user,
        full_name,
        phone_number,
        address,
        skills,
        education,
        experience,
        resume,
        ):
        
        
        print("**************DOMAIN RUNING**********")
        
        if experience<0:
            raise ValueError("Experience cannot be negative.")
        
        
        self.user = user
        self.full_name = full_name
        self.phone_number = phone_number
        self.address = address
        self.skills = skills
        self.education = education
        self.experience = experience
        self.resume = resume
        
    def update_experience(self,experience):
            if experience<0:
                raise ValueError("experience cannot be negative")
            self.experience = experience
            
    