# Employee Management REST API

A complete Django REST API for managing employee records with CRUD operations, JWT authentication, filtering, pagination, and comprehensive testing.

## 🚀 Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete employees
- ✅ **JWT Authentication** - Token-based security
- ✅ **Filtering** - By department and role
- ✅ **Pagination** - 10 employees per page
- ✅ **Search** - By name and email
- ✅ **Validation** - Email uniqueness, name validation
- ✅ **Swagger UI** - Interactive API documentation
- ✅ **Comprehensive Tests** - 12 test cases covering all endpoints

## 📋 Requirements

```txt
Django>=6.0
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.3.0
django-filter>=23.2
drf-spectacular>=0.27.0
```

## ⚙️ Installation

```bash
# Clone repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## 📊 Employee Model

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Auto | Unique identifier |
| `name` | String | Yes | Employee name |
| `email` | Email | Yes | Unique email address |
| `department` | String | No | HR, Engineering, Sales, etc. |
| `role` | String | No | Manager, Developer, Analyst, etc. |
| `date_joined` | Date | Auto | Record creation date |

## 🔐 Authentication

### Get JWT Token
```bash
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Token in Requests
```bash
Authorization: Bearer <access_token>
```

## 🌐 API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/api/token/` | Get JWT token | 200, 401 |
| POST | `/api/employees/` | Create employee | 201, 400 |
| GET | `/api/employees/` | List employees | 200, 401 |
| GET | `/api/employees/{id}/` | Get employee | 200, 404 |
| PUT | `/api/employees/{id}/` | Update employee | 200, 400, 404 |
| PATCH | `/api/employees/{id}/` | Partial update | 200, 400, 404 |
| DELETE | `/api/employees/{id}/` | Delete employee | 204, 404 |

## 📝 Usage Examples

### Create Employee
```bash
POST /api/employees/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@company.com",
  "department": "Engineering",
  "role": "Developer"
}
```

### List Employees
```bash
GET /api/employees/
Authorization: Bearer <token>
```

### Filter by Department
```bash
GET /api/employees/?department=Engineering
Authorization: Bearer <token>
```

### Filter by Role
```bash
GET /api/employees/?role=Manager
Authorization: Bearer <token>
```

### Search by Name/Email
```bash
GET /api/employees/?search=john
Authorization: Bearer <token>
```

### Pagination
```bash
GET /api/employees/?page=2
Authorization: Bearer <token>
```

### Get Single Employee
```bash
GET /api/employees/1/
Authorization: Bearer <token>
```

### Update Employee
```bash
PUT /api/employees/1/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Updated",
  "email": "john@company.com",
  "department": "Sales",
  "role": "Manager"
}
```

### Delete Employee
```bash
DELETE /api/employees/1/
Authorization: Bearer <token>
```

## 📚 API Documentation

### Swagger UI (Interactive)
```
http://localhost:8000/api/docs/
```

### ReDoc (Documentation)
```
http://localhost:8000/api/redoc/
```

### OpenAPI Schema (JSON)
```
http://localhost:8000/api/schema/
```

## 🧪 Testing

### Run All Tests
```bash
python manage.py test employees
```

### Expected Output
```
Found 12 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............
----------------------------------------------------------------------
Ran 12 tests in 2.345s

OK
```

### Test Coverage
- ✅ Create employee (valid & duplicate email)
- ✅ List employees (filtering & pagination)
- ✅ Retrieve employee (success & 404)
- ✅ Update employee (full & partial)
- ✅ Delete employee (success & 404)
- ✅ Authentication requirement

## 🔍 HTTP Status Codes

| Code | Status | Usage |
|------|--------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid token |
| 404 | Not Found | Resource not found |

## 🛠️ Project Structure

```
backend/
├── employees/
│   ├── models.py          # Employee model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   ├── tests.py           # Test cases
│   └── admin.py           # Django admin
├── company_api/
│   ├── settings.py        # Project settings
│   └── urls.py            # Main URL config
├── manage.py
└── requirements.txt
```

## 🎯 Key Features Implemented

### Validation
- Email must be unique
- Email format validation
- Name cannot be empty
- Department/Role choices validation

### Error Handling
- Proper HTTP status codes
- Descriptive error messages
- Validation error details

### Security
- JWT token authentication
- Token expiration (1 hour access, 1 day refresh)
- All endpoints protected
- Password hashing

### Performance
- Database indexing on frequently queried fields
- Pagination for large datasets
- Optimized queries

## 📱 Postman Testing

1. **Get Token**: POST `/api/token/` with credentials
2. **Set Authorization**: Add Bearer token in Authorization header
3. **Test Endpoints**: Use the token for all requests

**Postman Collection**: Available in project documentation

## 🚦 Quick Start Commands

```bash
# Setup
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver

# Run tests
python manage.py test

# Access API
http://localhost:8000/api/employees/

# Access Swagger
http://localhost:8000/api/docs/
```

## 📄 License

This project is part of HabotConnect hiring assignment.

## 👤 Author

**Position**: Python Backend Developer  
**Company**: HabotConnect  
**Date**: January 2025

---

**Note**: This API follows RESTful principles and includes comprehensive error handling, validation, authentication, and testing as per project requirements.
