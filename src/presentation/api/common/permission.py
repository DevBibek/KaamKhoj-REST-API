from rest_framework.permissions import SAFE_METHODS, BasePermission

from infrastructure.users.models import User


class IsCompany(BasePermission):
    """
    Custom permission to only allow authenticated company users to access or modify their own data.
    """
    
    message = "Access restricted: Only authenticated COMPANY accounts are permitted to perform this action."
    
    def has_permission(self,request,view):        
        return(request.user.is_authenticated and 
            request.user.role == User.Role.COMPANY)
        
    
    def has_object_permission(self,request,view,obj,):
        self.message = "Access denied: You do not have permission to modify or access another company's data."
        
        return obj.user == request.user
        
    
class IsJob(BasePermission):
    
    message = "Access restricted: Anyone can read jobs and Only authenticated COMPANY users can access or modify their own data "
    
    def has_permission(self, request, view):
        self.message = "Access restricted: You do not have permission to modify or access anothor users data"
        if request.method in SAFE_METHODS:
            return True
        
        return (request.user.is_authenticated and
                request.user.role == User.Role.COMPANY)
    
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
        return(request.user.is_authenticated and
            request.user.role== User.Role.JOB_SEEKER  
            )
        
    def has_object_permission(self, request, view, obj):
        self.message = "Access denied: You do not have permission to modify or access another jobseeker data"

        return obj.user == request.user
    
class ISApplication(BasePermission):
    message = "Access denied:Only authenticated jobseeker applay job"
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated)
    
    
    def has_object_permission(self, request, view, obj):
        self.message = "Access denied: You do not have permission to modify or access another Jobseeker data"
        return obj.jobseeker.user == request.user