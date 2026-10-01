from domain.jobs.entities import Job


class CreateJobService:
    def __init__(self, repository):
        self.repository = repository
        
    def execute(self,data,user):
        if user.role != user.Role.COMPANY:
            raise ValueError("only job company create and acccess job")
        

        
        job = Job(
            title = data["title"],
            description = data["description"],
            salary = data["salary"],
            location = data["location"],
            company= user.company
        )
        return self.repository.create(job)
        
        
        
        