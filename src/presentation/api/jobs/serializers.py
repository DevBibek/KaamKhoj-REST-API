from rest_framework import serializers

from infrastructure.jobs.models import Job
from presentation.api.user.serializers.company_serializers import CompanySerializers

# class ApplicationSerializer(serializers.Serializer):
#      class Meta:
#             model = Application
#             fields = ["id","status","created_at"]
        
class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(
        read_only = True,
        source = "company.company_name",
    )
    # application = ApplicationSerializer(many=True,read_only= True)
    # total_application = serializers.SerializerMethodField()
    title = serializers.CharField(
        required = True, 
        min_length = 5,
        max_length = 100,
        error_messages = {
            "required": "Job title is required",
            "blank":"Job tittle cannot not be blank",
            "min_length":"Job title must be at least 5 characters",
            "max_length": "Job title cannot exceed 100 characters "
        })
    
    description = serializers.CharField(
        required = True, 
        min_length = 20,
        max_length = 200,
        error_messages = {
                    "required": "Job descritption is required",
                    "blank":"Job description cannot be blank",
                    "min_length":"Job description must be at least 20 characters",
                    "max_length": "Job description cannot exceed 200 characters "
                })
    
    
    location = serializers.CharField(
        required = True, 
        min_length = 2,
        max_length = 100,
        error_messages = {
        "required": "Job location is required",
        "blank":"Job location cannot be blank",
        "min_length":"Job location must be at least 2 characters",
        "max_length": "Job location cannot exceed 100 characters "
        }
    )
    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "company",
            "description",
            "salary",
            "location",
            "is_active",
            "created_at",
            "updated_at"
            )
    
        read_only_fields =(
            "company",
            "is_active",
            "created_at",
            "updated_at",
        )
    
    def validate_salary(self,value):
        if value<=0:
            raise  serializers.ValidationError("Salary must be greater than 0")
        return value

    # def get_total_application(self,obj):
    #     return len(obj.applications.all())