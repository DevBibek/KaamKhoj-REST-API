from rest_framework import serializers

from infrastructure.users.models import JobSeeker


class JobSeekerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source = "user.email",read_only = True)
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
            })
    
    
    skills = serializers.CharField(
        required = True,
        error_messages = {
            "required":"Skills is required",
            "blank":"skills cannot be blank"
        })
    education = serializers.CharField(
        required = True,
        max_length = 100,
        error_messages = {
            "required":"education is required",
            "blank":"education cannot be blank",
            "max_length":"education cannot be exceed 100 characters"
        })
    
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
    
    
    