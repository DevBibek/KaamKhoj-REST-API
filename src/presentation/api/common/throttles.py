from rest_framework.throttling import SimpleRateThrottle


class RoleBasedUserThrottle(SimpleRateThrottle):
    role= None
    
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        
        if getattr(request.user,"role",None) != self.role:
            return None
        
        return self.cache_format % {
            "scope":self.scope,
            "ident":request.user.pk,
        }
        
    
    
class JobSeekerThrottle(RoleBasedUserThrottle):
    scope="job_seeker"
    role = "JOB_SEEKER"
    

class CompanyThrottle(RoleBasedUserThrottle):
    scope = "company"
    role = "COMPANY"