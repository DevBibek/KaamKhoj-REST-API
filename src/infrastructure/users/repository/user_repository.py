from infrastructure.users.models import User


class UserRepository:

    def get_by_email(self, email):

        return User.objects.filter(
            email=email
        )