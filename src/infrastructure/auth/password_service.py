from django.contrib.auth import authenticate


class PasswordService:
    def authenticate(self,email,password):
        return authenticate(
            email= email,
            password= password
        )