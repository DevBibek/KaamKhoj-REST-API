from rest_framework.permissions import SAFE_METHODS, BasePermission

from infrastructure.users.models import User


class IsCompany(BasePermission):
    """
    Allows access only to authenticated COMPANY users.
    """
    
    message = "Access restricted: Only authenticated COMPANY accounts are allowed."
    
    def has_permission(self,request,view):        
        if not request.user.is_authenticated:
            return False
    
        return request.user.role == User.Role.COMPANY
        
    
    def has_object_permission(self,request,view,obj,):
        self.message = "Access denied: You do not have permission to modify or access another company's data."
        
        return obj.user == request.user
        
    
class IsJob(BasePermission):
    
    message = "Access restricted: Anyone can read jobs and Only authenticated COMPANY users can access or modify their own data "
    
    def has_permission(self, request, view):
        self.message = "Access restricted: You do not have permission to modify or access anothor users data"
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
            
        return request.user.role == User.Role.COMPANY
    
    def has_object_permission(self, request, view, obj):
        self.message = "Access denied: You do not have permission to modify or access anothor company data"
        if request.method in SAFE_METHODS:
            return True
        
        return obj.company.user == request.user



class IsJobSeeker(BasePermission):
    """
    Custom permission to only allow authenticated JOB_SEEKER users to access or modify their own data
    """
    
    message = "Access restricted: Only  Authenticated JOB_SEEKER accounts are permitted to perfrom this action "
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        return request.user.role== User.Role.JOB_SEEKER  
        
    def has_object_permission(self, request, view, obj):
        self.message = "Access denied: You do not have permission to modify or access another jobseeker data"

        return obj.user == request.user
    
class IsApplication(BasePermission):
    message = "You do not have to permission to access this application"
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated)
    
    
    def has_object_permission(self, request, view, obj):
        
        is_jobseeker_owner = (
            obj.jobseeker.user_id ==request.user.id
            )
        
        is_company_owner = (
            obj.job.company.user_id == request.user.id
        )
        
        return is_jobseeker_owner or is_company_owner
        
    
    
class IsOwner(BasePermission):
    message = "Access denied: You can only access your own data "
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
        