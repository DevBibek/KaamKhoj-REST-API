from rest_framework import serializers

from infrastructure.users.models import Company


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
            "verification_status",
            "created_at",
            "updated_at"
        )
        read_only_fields = (
            "verification_status",
            "created_at",
            "updated_at",
        )
    
from infrastructure.applications.models import Application


class CompanyApplicationSerializer(serializers.ModelSerializer):
    job_seeker = serializers.CharField(source = "jobseeker.user.username")
    job_title = serializers.CharField(source = "job.title")
    
    class Meta:
        model = Application
        fields = (
            "id",
            'job_seeker',
            "job_title",
            "cover_letter",
            "status",
            "created_at",
        )
        
        
class UpdateVerificatioSerializer(serializers.ModelSerializer):
    verification_status =  serializers.ChoiceField(
        choices=[
            "PENDING",
            "VERIFIED",
            "REJECTED",
        ]
    )
    class Meta:
        model = Company
        fields = ("verification_status")