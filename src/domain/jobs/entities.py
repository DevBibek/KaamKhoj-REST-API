class Job:
    def __init__(
        self,
        title,
        description,
        salary,
        location,
        company,
        ):
        print("+++++++++ Job DOmain running +++++++++++")
        self.title = title
        self.description = description
        self.salary = salary
        self.location = location
        self.company= company
    
    def validate(self):
        if not self.title.strip():
            raise ValueError("job title cannot be empty")
        if self.salary<0:
            raise ValueError(" salary cannot be negative.")
        
        if not self.company_id:
            raise ValueError("Job post must be belong to a valid company")
        
        
        
        
    