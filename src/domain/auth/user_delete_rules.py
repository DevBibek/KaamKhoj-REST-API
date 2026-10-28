class UserDeleteRules:
    @staticmethod
    def validate(request_user ,target_user):
        is_owner = request_user.id == target_user.id
        is_admin = request_user.is_superuser
        
        if not (is_owner or is_admin):
            raise PermissionError("You do not have permission to delete this user")