from rest_framework import serializers

from infrastructure.applications.models import Application
from infrastructure.users.models import Company, User


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
            


class CompanyUserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length = 150,
        required = False
        )
    first_name = serializers.CharField(
        max_length = 100,
        required = False
    )
    last_name = serializers.CharField(
        max_length = 100,
        required = False
    )
    email = serializers.EmailField(required = False)
    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "Provied as least on user field to update"
            )
        return attrs




class CompanyReadSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = (
            "id",
            "user", 
            "company_name",
            "description",
            "location",
            "website",
            "phone",
            "verification_status",
            "created_at",
            "updated_at"
        )
    
    def get_user(self,obj):
        return {
            "username": obj.user.username,
            "first_name":obj.user.first_name,
            "last_name":obj.user.last_name,
            "email":obj.user.email,
        }
    def get_company_name(self,obj):
        return obj.company_name.upper()
    

class CompanyUpdateSerializer(serializers.ModelSerializer):
    user = CompanyUserUpdateSerializer(required=False)
    class Meta:
        model = Company
        fields = (
            "user",
            "company_name",
            "description",
            "location",
            "website",
            "phone",
        )
    def validate(self, attrs):
        user_data = attrs.get("user",{})
        company = self.instance
        
        if "username" in user_data:
            username_exists = User.objects.filter(
                username =user_data["username"]
            ).exclude(id=company.user_id).exists()
            if username_exists:
                raise serializers.ValidationError({
                    "user": {"username": "This username  is already registered."}
                })
        
        if "email" in user_data:
            username_exists = User.objects.filter(
                email__iexact =user_data["email"]# __iexact :case-insensitive exact matching
            ).exclude(id=company.user_id).exists()
            if username_exists:
                raise serializers.ValidationError({
                    "user": {"username": "This username  is already registered."}
                })
                
                
        return attrs
        
            
class CompanyApplicationSerializer(serializers.ModelSerializer):
    job_seeker = serializers.CharField(source = "jobseeker.full_name")
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
        fields = ["verification_status"]