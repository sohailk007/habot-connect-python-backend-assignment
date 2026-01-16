from rest_framework.pagination import PageNumberPagination

class EmployeePagination(PageNumberPagination):
    """
    Custom pagination for employee endpoints
    Default: 10 items per page
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'