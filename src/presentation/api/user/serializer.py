
from rest_framework import serializers

from infrastructure.users.models import Company, JobSeeker, User


class UserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required = True,
        error_messages = {
            "required":"User email is required",
            "blank":"email cannot be blank",
            "invalid":"Enter a valaid email address"
        }),
    role = User._meta.get_field("role").choices
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role"
            )
        

class JobSeekerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.name", read_only=True)
    
    full_name = serializers.CharField(
        required= True,
        max_length = 50,
        error_messages = {
            "required":"Full name is required",
            "max_length":"Full name cannot exceed 50 characters ",
            "blank":"Full name cannot be blank",
            
            
        })
    phone_number = serializers.RegexField(
        regex=r"^(?:\+977)?(?:96|97|98)\d{8}$",

        error_messages={
            "required": "Phone number is required.",
            "blank": "Phone number cannot be blank.",
            "invalid": "Enter a valid Nepali phone number.",
        },
    )
    
    
    address = serializers.CharField(
        required= True,
        max_length = 100,
        error_messages = {
            "required":"address is required",
            "blank":"address cannot be blank",
            "max_length":"address cannot exceed 100 characters",
            }),
    
    
    skills = serializers.CharField(
        required = True,
        error_messages = {
            "required":"Skills is required",
            "blank":"skills cannot be blank"
        }),
    education = serializers.CharField(
        required = True,
        max_length = 100,
        error_messages = {
            "required":"education is required",
            "blank":"education cannot be blank",
            "max_length":"education cannot be exceed 100 characters"
        }),
    
    experience = serializers.IntegerField(
        required = True,
        min_value= 0,
        error_messages = {
            "required":"experience is required",
            "blank":"experience cannot be blank",
            "min_value":"experience cannnot be negative"
            
        })
    
    class Meta:
        model = JobSeeker
        fields = (
            "id",
            "username",
            "email",
            "full_name",
            "phone_number",
            "address",
            "skills",
            "education",
            "experience",
            "resume",
            "created_at",
            "updated_at"
            
        )
        
    read_only_fields = (
        "user",
        "created_at",
        "updated_at",
    )
    
    
    


class CompanySerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(
        required = True,
        max_length= 100,
        error_messages = {
            "required":"Company name is required",
            "blank":"company name cannot be blank",
            "max_length":"company name cannot exceed 100 characters"
        }
    )
    description = serializers.CharField(
        required = True, 
        min_length = 20,
        max_length = 200,
        error_messages = {
            "required": "descritption is required",
            "blank":" description cannot be blank",
            "min_length":" description must be at least 20 characters",
            "max_length": "description cannot exceed 200 characters "
                    })
    
    location = serializers.CharField(
        required = True,
        max_length = 100,
        error_messages = {
            "required":"location is required",
            "blank":"location cannot be blank",
            "max_length":"location cannot exceed 100 characters"
    }
    )

    phone = serializers.RegexField(
        regex=r"^(?:\+977)?(?:96|97|98)\d{8}$",

    error_messages={
        "required": "Phone number is required.",
        "blank": "Phone number cannot be blank.",
        "invalid": "Enter a valid Nepali phone number.",
    },
    )
    class Meta:
        model = Company
        fields =(
            "id",
            "company_name",
            "description",
            "location",
            "website",
            "phone",
            "created_at",
            "updated_at"
        )
    
    read_only_fields = (
            "created_at",
            "updated_at",
        )
    
from infrastructure.applications.models import Application


class CompanyApplicationSerializer(serializers.ModelSerializer):
    job_seeker = serializers.CharField(source = "jobseeker.user.username")
    job_title = serializers.CharField(source = "job.title")
    
    class Meta:
        model = Application
        fields = [
            "id",
            'job_seeker',
            "job_title",
            "cover_letter",
            "status",
            "created_at",
        ]