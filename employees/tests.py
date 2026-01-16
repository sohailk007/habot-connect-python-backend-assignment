from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Employee

# Get the custom User model
User = get_user_model()


class EmployeeAPITestCase(APITestCase):
    """Complete test suite for Employee API"""
    
    def setUp(self):
        """Set up test data and authentication"""
        self.client = APIClient()
        
        # Create test user using custom User model
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        
        # Get JWT token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create test employee
        self.employee = Employee.objects.create(
            name='Alice Johnson',
            email='alice@example.com',
            department='Engineering',
            role='Developer'
        )
    
    # ========== CREATE TESTS ==========
    
    def test_create_employee_success(self):
        """Test creating employee with valid data"""
        data = {
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'department': 'HR',
            'role': 'Manager'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Bob Smith')
        self.assertEqual(response.data['email'], 'bob@example.com')
    
    def test_create_employee_duplicate_email(self):
        """Test duplicate email returns 400"""
        data = {
            'name': 'Duplicate User',
            'email': 'alice@example.com',
            'department': 'Sales'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_create_employee_empty_name(self):
        """Test empty name returns 400"""
        data = {
            'name': '',
            'email': 'test@example.com'
        }
        response = self.client.post('/api/employees/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ========== LIST TESTS ==========
    
    def test_list_employees(self):
        """Test listing all employees"""
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_filter_by_department(self):
        """Test filtering by department"""
        response = self.client.get('/api/employees/?department=Engineering')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for emp in response.data['results']:
            self.assertEqual(emp['department'], 'Engineering')
    
    def test_filter_by_role(self):
        """Test filtering by role"""
        response = self.client.get('/api/employees/?role=Developer')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_pagination(self):
        """Test pagination (10 per page)"""
        # Create 12 employees
        for i in range(12):
            Employee.objects.create(
                name=f'Employee {i}',
                email=f'emp{i}@example.com'
            )
        
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
    
    # ========== RETRIEVE TESTS ==========
    
    def test_retrieve_employee(self):
        """Test retrieving single employee"""
        response = self.client.get(f'/api/employees/{self.employee.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Alice Johnson')
    
    def test_retrieve_nonexistent_employee(self):
        """Test 404 for non-existent employee"""
        response = self.client.get('/api/employees/9999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ========== UPDATE TESTS ==========
    
    def test_update_employee(self):
        """Test updating employee"""
        data = {
            'name': 'Alice Updated',
            'email': 'alice@example.com',
            'department': 'Sales',
            'role': 'Manager'
        }
        response = self.client.put(
            f'/api/employees/{self.employee.id}/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Alice Updated')
    
    # ========== DELETE TESTS ==========
    
    def test_delete_employee(self):
        """Test deleting employee"""
        response = self.client.delete(f'/api/employees/{self.employee.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # ========== AUTHENTICATION TESTS ==========
    
    def test_authentication_required(self):
        """Test endpoints require authentication"""
        self.client.credentials()  # Remove token
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)