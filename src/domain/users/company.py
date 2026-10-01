from infrastructure.users.models import Company as CompanyModels


class Company:
    def __init__(
        self,
        user,
        company_name,
        description,
        location,
        website,
        phone,
        ):
        
        self.user = user
        self.company_name = company_name
        self.description = description
        self.location = location
        self.website = website
        self.phone = phone
    
    def validate_phone(self,value):
        if value  == CompanyModels.objects.filter(phone=value).exists():
            return ValueError("Phone numbr is existe")
        return value

