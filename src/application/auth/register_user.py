from rest_framework.exceptions import NotFound

from domain.auth.user_delete_rules import UserDeleteRules


class RegisterUser:
    def __init__(self,user_repo):
        self.user_repo = user_repo
        
        
    def get_user_by_id(self,pk,user):
        user=self.user_repo.get_by_id_and_user(pk=pk,user=user)  
        if user is None:
            raise NotFound(f"User with id {pk} does not exists")
        return user
    
    def update_user(self,pk,user,data):
        user = self.user_repo.get_by_id_and_user(pk,user)
        if user is None:
            raise NotFound(f"User with id {pk} doesnt exists")
        
        return self.user_repo.update_profile(user,**data)

    
    def execute(self,data):
        return self.user_repo.create(data)
    
    
    def delete_user(self,pk,user):
        if user.is_superuser:
            target_user = self.user_repo.get_by_id(pk)
            
        else:
            target_user = self.user_repo.get_by_id_and_user(pk,user)
            
        if target_user is None:
            raise NotFound(f"User with id {pk} doesnt exists")
        
        UserDeleteRules.validate(
            request_user=user,
            target_user=target_user
        )
        
        return self.user_repo.delete_user(target_user)
                
    
