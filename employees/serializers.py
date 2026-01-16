from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Main serializer for Employee model
    Handles all CRUD operations with complete validation
    """
    
    # Read-only fields
    id = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateField(read_only=True, format="%Y-%m-%d")
    
    # Optional: Display names for choices
    department_display = serializers.CharField(
        source='get_department_display',
        read_only=True
    )
    role_display = serializers.CharField(
        source='get_role_display',
        read_only=True
    )
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'email',
            'department',
            'department_display',
            'role',
            'role_display',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def validate_name(self, value):
        """
        Validate that name is not empty or whitespace
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Name cannot be empty or contain only whitespace."
            )
        return value.strip()
    
    def validate_email(self, value):
        """
        Validate email format and uniqueness
        """
        if not value:
            raise serializers.ValidationError("Email is required.")
        
        # Normalize email to lowercase
        value = value.lower().strip()
        
        # Check uniqueness (exclude current instance during update)
        instance_id = self.instance.id if self.instance else None
        if Employee.objects.filter(email=value).exclude(id=instance_id).exists():
            raise serializers.ValidationError(
                "An employee with this email already exists."
            )
        
        return value
    
    def validate_department(self, value):
        """
        Validate department is a valid choice
        """
        if value and value not in dict(Employee._meta.get_field('department').choices):
            raise serializers.ValidationError(
                f"Invalid department. Choose from: HR, Engineering, Sales, Marketing, Finance, Operations."
            )
        return value
    
    def validate_role(self, value):
        """
        Validate role is a valid choice
        """
        if value and value not in dict(Employee._meta.get_field('role').choices):
            raise serializers.ValidationError(
                f"Invalid role. Choose from: Manager, Developer, Analyst, Designer, Lead, Intern."
            )
        return value
    
    def validate(self, attrs):
        """
        Cross-field validation
        """
        # Add any cross-field validation logic here
        return attrs
    
    def create(self, validated_data):
        """
        Create and return a new Employee instance
        """
        return Employee.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing Employee instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.department = validated_data.get('department', instance.department)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class EmployeeListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for list views
    Optimized for performance with fewer fields
    """
    
    department_name = serializers.CharField(
        source='department_display',
        read_only=True
    )
    role_name = serializers.CharField(
        source='role_display',
        read_only=True
    )
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'email',
            'department',
            'department_name',
            'role',
            'role_name',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for employee creation
    Can include additional fields or validation specific to creation
    """
    
    class Meta:
        model = Employee
        fields = ['name', 'email', 'department', 'role']
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        
        value = value.lower().strip()
        
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An employee with this email already exists."
            )
        
        return value

