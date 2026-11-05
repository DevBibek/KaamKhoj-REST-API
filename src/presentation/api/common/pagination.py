from rest_framework.pagination import (
    CursorPagination,
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 50
    
    message = "Data retrieved successfuly"
    def get_paginated_response(self, data):
        return Response({
            "success": True,
            "message": self.message,
            "pagination": {
                "total_items": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "data": data,
        })
    

class CustomLimitPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param="limit"
    offset_query_param="offset"
    max_limit = 50 
    
class CustomCursorPagination(CursorPagination):
    page_size = 20
    cursor_query_param = "cursor"
    ordering = "-id"