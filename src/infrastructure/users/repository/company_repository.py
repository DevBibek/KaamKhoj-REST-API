from django.db import transaction

from infrastructure.users.models import Company


class CompanyRepository:

    def get_by_company(self, user):
        return Company.objects.filter(user=user).select_related("user").first()

    def get_by_user(self, user):
        try:
            return Company.objects.get(user=user)
        except Company.DoesNotExist:
            return None
    
    def get_by_id(self,company_id):
        return Company.objects.filter(id=company_id).first()
        
    def exists_by_phone(self, phone,):
        return Company.objects.filter(phone=phone).exists()

        

    def create(self, user, **data):
        return Company.objects.create(user=user, **data)

    def update(self, company,user_data,company_data):
        with transaction.atomic():
            user = company.user
            
            for field ,value in user_data.items():
                setattr(user,field,value)
            
            if user_data:
                user.save()
            
            for field, value in company_data.items():
                setattr(company, field, value)
                
            if company_data:
                company.save()
                
                
        return company
    
    def save(self,company):
            company.save(
                update_fields=["verification_status"]
            )
            return company
    

    def delete(self, company):
        company.delete()