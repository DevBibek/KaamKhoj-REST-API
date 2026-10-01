class RegisterUser:
    def __init__(self,repository):
        self.repository = repository
        
    def execute(self,data):
        user = self.repository.create(data)
        return user