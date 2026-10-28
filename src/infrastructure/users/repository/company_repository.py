from infrastructure.users.models import Company


class CompanyRepository:
    
    def list_by_user(self,user):
        return Company.objects.filter(user = user)
    
    def exists_by_user(self,user):
        return  Company.objects.filter(user=user).exists()
    
    
    def get_by_id(self,company_id):
        return Company.objects.filter(id=company_id).first()
    
    def get_by_user(self,user):
        return Company.objects.filter(user=user).first()
    
    
    def create(self,user,**data):
        return Company.objects.create(user=user,**data)
    
    
    
    def save(self,company):
        company.save(
            update_fields=["verification_status"]
        )
        return company