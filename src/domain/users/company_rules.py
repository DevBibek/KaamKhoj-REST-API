

class CompanyRules:
    @staticmethod
    def validate(user,company_exists):
        
        if user.role != user.Role.COMPANY:
            raise PermissionError("Only COMPANY user can create company profile")
        
        if company_exists:
            raise PermissionError("You  alreday have a COMPANY profile ")

        