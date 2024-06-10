from rest_framework import pagination
from rest_framework.response import Response

class StandartPagination(pagination.PageNumberPagination):
    
    page_size = 5
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100
    last_page_strings = ("last", "end", "final")
    
    def get_paginated_response(self, data):
 
    
        return Response({
            "total_records": self.page.paginator.count,
            "records_count": len(data),
            "pages": self.page.paginator.num_pages,
            "data":data,
            "current_page":self.page.number
        })
    
    