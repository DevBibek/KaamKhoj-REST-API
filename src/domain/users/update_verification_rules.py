class UpdateVerificationRules:
    @staticmethod
    def validate(user,company,new_status):
        if not user.is_staff:
            raise PermissionError("Only admin users can update company verification status.")
        
        if company is None:
            raise ValueError("Company not found")
        
        current_status = company.verification_status
        
        allowed_status = {
            "PENDING":["VERIFIED","REJECTED"],
            "VERIFIED":[],
            "REJECTED":[],
        }
        
        if new_status not in allowed_status[current_status]:
            raise ValueError(f"You can not change status from {current_status} to {new_status}")