import logging

from django.core.cache import cache

logger = logging.getLogger("kaamkhoj")

def invalidate_jobseeker_profile_cache(user):
    
    #Delete the user's cached jobseeker profile after a profile change.
    try:
        cache.delete(f"jobseeker_profile:v1:user:{user}")
    
    except Exception:
        logger.warning(
            "Failed to jobseeker profile cache",
            exc_info=True
        )