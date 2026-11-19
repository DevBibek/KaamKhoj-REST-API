import logging

from django.core.cache import cache

logger = logging.getLogger("kaamkhoj")

def invalidate_company_profile_cache(user):
    """
    Delete the user's cached company profile after a profile change.
    """

    try:
        cache.delete(f"company_profile:v1:user:{user}")
        
    except Exception:
        logger.warning(
            "Failed to invalid company profile cache",
            exc_info= True
        )