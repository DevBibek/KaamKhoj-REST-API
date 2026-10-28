from infrastructure.users.models import User


class UserRepository:
    def get_by_id(self,pk):
        return User.objects.filter(pk=pk).first()
    
    def get_by_id_and_user(self,pk,user):
        try:
            return User.objects.get(pk=pk,id=user.id)
        except User.DoesNotExist:
            return None
        
        
    def get_by_email(self, email):
        
        return User.objects.filter(
            email=email
        ).first()
        
    def update_profile(self,user,**data):
        
        for field ,value in data.items():
            setattr(user,field,value)
        
        return user.save()
    
    def create(self,data):
        return User.objects.create_user(**data)  
    
    
    def delete_user(self,user):
        return user.delete()   