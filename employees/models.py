from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


def validate_not_empty(value):
    """Custom validator to ensure string is not empty or whitespace"""
    if not value or not value.strip():
        raise ValidationError('This field cannot be empty.')


class Employee(models.Model):
    """
    Employee Model
    
    Stores employee information including personal details, 
    department assignment, and role.
    """
    
    # Primary Key - Auto-generated unique identifier
    id = models.AutoField(
        primary_key=True,
        verbose_name='Employee ID',
        help_text='Unique identifier for the employee'
    )
    
    # Required Fields
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        validators=[validate_not_empty],
        verbose_name='Full Name',
        help_text='Employee full name'
    )
    
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        validators=[EmailValidator(message='Enter a valid email address.')],
        verbose_name='Email Address',
        help_text='Employee email address (must be unique)',
        error_messages={
            'unique': 'An employee with this email already exists.',
        }
    )
    
    # Optional Fields
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Department',
        help_text='Employee department (e.g., HR, Engineering, Sales)',
        choices=[
            ('HR', 'Human Resources'),
            ('Engineering', 'Engineering'),
            ('Sales', 'Sales'),
            ('Marketing', 'Marketing'),
            ('Finance', 'Finance'),
            ('Operations', 'Operations'),
        ]
    )
    
    role = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Role',
        help_text='Employee role (e.g., Manager, Developer, Analyst)',
        choices=[
            ('Manager', 'Manager'),
            ('Developer', 'Developer'),
            ('Analyst', 'Analyst'),
            ('Designer', 'Designer'),
            ('Lead', 'Team Lead'),
            ('Intern', 'Intern'),
        ]
    )
    
    # Auto-generated timestamp
    date_joined = models.DateField(
        auto_now_add=True,
        editable=False,
        verbose_name='Date Joined',
        help_text='Date when employee record was created'
    )
    
    class Meta:
        db_table = 'employee'
        ordering = ['-date_joined', 'name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['email'], name='idx_employee_email'),
            models.Index(fields=['department'], name='idx_employee_dept'),
            models.Index(fields=['role'], name='idx_employee_role'),
            models.Index(fields=['-date_joined'], name='idx_employee_date'),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def __repr__(self):
        return f"<Employee: {self.id} - {self.name}>"
    
    def clean(self):
        """Additional model-level validation"""
        super().clean()
        
        # Ensure name is not empty or whitespace
        if self.name and not self.name.strip():
            raise ValidationError({'name': 'Name cannot be empty or whitespace.'})
        
        # Normalize email to lowercase
        if self.email:
            self.email = self.email.lower().strip()
    
    def save(self, *args, **kwargs):
        """Override save to ensure validation"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def department_display(self):
        """Returns the display name for department"""
        return self.get_department_display() if self.department else 'Not Assigned'
    
    @property
    def role_display(self):
        """Returns the display name for role"""
        return self.get_role_display() if self.role else 'Not Assigned'

