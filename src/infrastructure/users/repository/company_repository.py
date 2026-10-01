from infrastructure.users.models import Company


class CompanyRepository:
    def exists_by_user(self,user):
        return  Company.objects.filter(user=user).exists()
    
    
    def save(self,company):
        print("+++++++++ Run Repository +++++++++++++")
        return Company.objects.create(
            user = company.user,
            company_name = company.company_name,
            description = company.description,
            location = company.location,
            website = company.website,
            phone = company.phone,
        )