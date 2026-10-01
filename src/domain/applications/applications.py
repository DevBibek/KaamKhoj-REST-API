from infrastructure.users.models import User


class Application:
    def __init__(
        self,
        jobseeker,
        job,
        cover_letter,
        status,
        ):
        self.job = job
        self.cover_letter = cover_letter
        self.status = status
        self.jobseeker = jobseeker
        

