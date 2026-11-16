from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc,context):
    response = exception_handler(exc, context)
    
    if response is None:
        return None
        
        
    if response.status_code == 429:
        
        retry_after =getattr(exc,"wait",None)
        return Response(
            {
                "success":False,
                "message":"Too many requests. please try again latter" ,
                "retry after":retry_after,
            },
            status=response.status_code,
            headers=response.headers,
        )
    
    return response