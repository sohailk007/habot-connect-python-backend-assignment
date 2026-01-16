from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Employee
from .serializers import (
    EmployeeSerializer,
    EmployeeListSerializer,
    EmployeeCreateSerializer
)
from .pagination import EmployeePagination
import drf_spectacular.utils as spectacular
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiResponse,
    OpenApiExample
)




@extend_schema_view(
    get=extend_schema(
        summary="List all employees",
        description="Retrieve a paginated list of all employees with optional filtering and search",
        parameters=[
            OpenApiParameter(
                name='department',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by department (e.g., HR, Engineering, Sales)',
                required=False,
                enum=['HR', 'Engineering', 'Sales', 'Marketing', 'Finance', 'Operations']
            ),
            OpenApiParameter(
                name='role',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by role (e.g., Manager, Developer, Analyst)',
                required=False,
                enum=['Manager', 'Developer', 'Analyst', 'Designer', 'Lead', 'Intern']
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search by name or email',
                required=False,
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Order results (e.g., name, -date_joined)',
                required=False,
            ),
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Page number',
                required=False,
            ),
            OpenApiParameter(
                name='page_size',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Number of results per page (max 100)',
                required=False,
            ),
        ],
        responses={
            200: EmployeeListSerializer(many=True),
            401: OpenApiResponse(description='Unauthorized - Invalid or missing token'),
        },
        tags=['Employees'],
    ),
    post=extend_schema(
        summary="Create a new employee",
        description="Create a new employee record with the provided information",
        request=EmployeeCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=EmployeeSerializer,
                description='Employee created successfully'
            ),
            400: OpenApiResponse(
                description='Bad Request - Validation error',
                examples=[
                    OpenApiExample(
                        'Duplicate Email',
                        value={
                            'email': ['An employee with this email already exists.']
                        }
                    ),
                    OpenApiExample(
                        'Empty Name',
                        value={
                            'name': ['Name cannot be empty.']
                        }
                    ),
                ]
            ),
            401: OpenApiResponse(description='Unauthorized - Invalid or missing token'),
        },
        examples=[
            OpenApiExample(
                'Create Employee Example',
                value={
                    'name': 'Alice Johnson',
                    'email': 'alice.johnson@company.com',
                    'department': 'Engineering',
                    'role': 'Developer'
                },
                request_only=True,
            ),
        ],
        tags=['Employees'],
    )
)    
class EmployeeListCreateView(generics.ListCreateAPIView):
    
    """
    GET  /api/employees/ - List all employees
    POST /api/employees/ - Create a new employee
    
    Features:
    - Pagination (10 per page)
    - Filtering by department and role
    - Search by name and email
    - Ordering
    """
    
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = EmployeePagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['department', 'role']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'email', 'date_joined']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        """
        Use different serializers for list and create actions
        """
        if self.request.method == 'POST':
            return EmployeeCreateSerializer
        return EmployeeListSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new employee
        Returns 201 Created on success
        Returns 400 Bad Request on validation error
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            employee = serializer.save()
            
            # Return full employee details
            response_serializer = EmployeeSerializer(employee)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        """
        List all employees with pagination and filtering
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



@extend_schema_view(
    get=extend_schema(
        summary="Retrieve an employee",
        description="Get detailed information about a specific employee by ID",
        responses={
            200: EmployeeSerializer,
            404: OpenApiResponse(
                description='Employee not found',
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={'detail': 'Employee not found.'}
                    )
                ]
            ),
            401: OpenApiResponse(description='Unauthorized - Invalid or missing token'),
        },
        tags=['Employees'],
    ),
    put=extend_schema(
        summary="Update an employee (full)",
        description="Completely update an employee's information. All fields must be provided.",
        request=EmployeeSerializer,
        responses={
            200: EmployeeSerializer,
            400: OpenApiResponse(
                description='Bad Request - Validation error',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'email': ['An employee with this email already exists.']
                        }
                    )
                ]
            ),
            404: OpenApiResponse(description='Employee not found'),
            401: OpenApiResponse(description='Unauthorized'),
        },
        examples=[
            OpenApiExample(
                'Update Employee',
                value={
                    'name': 'Alice Johnson',
                    'email': 'alice.j@company.com',
                    'department': 'Sales',
                    'role': 'Manager'
                },
                request_only=True,
            ),
        ],
        tags=['Employees'],
    ),
    patch=extend_schema(
        summary="Update an employee (partial)",
        description="Partially update an employee's information. Only provided fields will be updated.",
        request=EmployeeSerializer,
        responses={
            200: EmployeeSerializer,
            400: OpenApiResponse(description='Bad Request - Validation error'),
            404: OpenApiResponse(description='Employee not found'),
            401: OpenApiResponse(description='Unauthorized'),
        },
        examples=[
            OpenApiExample(
                'Partial Update',
                value={
                    'role': 'Lead'
                },
                request_only=True,
            ),
        ],
        tags=['Employees'],
    ),
    delete=extend_schema(
        summary="Delete an employee",
        description="Permanently delete an employee record",
        responses={
            204: OpenApiResponse(description='Employee deleted successfully'),
            404: OpenApiResponse(
                description='Employee not found',
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={'detail': 'Employee not found.'}
                    )
                ]
            ),
            401: OpenApiResponse(description='Unauthorized'),
        },
        tags=['Employees'],
    )
)   
class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/employees/{id}/ - Retrieve a single employee
    PUT    /api/employees/{id}/ - Update an employee (full update)
    PATCH  /api/employees/{id}/ - Partial update an employee
    DELETE /api/employees/{id}/ - Delete an employee
    """
    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single employee by ID
        Returns 404 if not found
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, *args, **kwargs):
        """
        Update an employee (PUT - full update)
        Returns 400 on validation error
        Returns 404 if employee not found
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=partial
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update an employee (PATCH)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete an employee
        Returns 204 No Content on success
        Returns 404 if employee not found
        """
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND
            )


    


