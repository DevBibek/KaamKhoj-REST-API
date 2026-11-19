import logging

from django.core.cache import cache

logger = logging.getLogger("kaamkhoj")

def invalidate_jobs_cache():
    try:
        cache.delete_pattern("public_jobs:v1:*")
    
    except Exception:
        logger.warning(
            "Failed to invalidate jobs cache",
            exc_info= True,
        )