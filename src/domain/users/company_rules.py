class CompanyRules:

    @staticmethod
    def validate_create(user, profile_exists,phone_exists):
        if user.role != user.Role.COMPANY:
            raise PermissionError(
                "Only company users can create a company profile."
            )

        if profile_exists:
            raise ValueError(
                "You already have a company profile."
            )
        if phone_exists:
            raise ValueError("This phone number is already registered.")

    @staticmethod
    def validate_owner(user, company):
        
        if user.role != user.Role.COMPANY:
            raise PermissionError(
                "Only company users can manage a company profile."
                )
        if not company:
            raise ValueError("Company profile not found. Please create your profile first.")
        
        if company.user_id != user.id:
            raise PermissionError(
                "You cannot manage another company's profile."
            )
        
    @staticmethod
    def validate_delete(user,company):
        if company is None:
            raise ValueError(" Company profile not found. Plese create your profile first.")
            
        admin_user = user.is_superuser
        owner_user =(
            user.role == user.Role.COMPANY and
            company.user_id == user.id
            )
        if not(admin_user or owner_user):
            
            raise PermissionError("You cannot delete this  company's profile")
            
            